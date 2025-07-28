import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import sys
import argparse
from io import StringIO
from main import main, generate_content

from config import MAX_ITERS 

class TestMain(unittest.TestCase):
    def setUp(self):
        # Set up common test fixtures
        self.max_iters = MAX_ITERS  # Match your actual MAX_ITERS from config
        self.test_prompt = "test prompt"
        self.mock_api_key = "mock-api-key-123"
        self.mock_response_text = "Mock response text"
        
        # Mock environment variables
        self.env_patcher = patch.dict(
            'os.environ', 
            {'GEMINI_API_KEY': self.mock_api_key}
        )
        self.env_patcher.start()
        
        # Capture stdout
        self.held_output = StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.held_output

    def tearDown(self):
        # Clean up after each test
        self.env_patcher.stop()
        sys.stdout = self.original_stdout
        self.held_output.close()

    @patch('main.genai.Client')
    @patch('main.load_dotenv')
    @patch('main.argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse, mock_load, mock_client):
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.prompt = self.test_prompt
        mock_args.verbose = False
        mock_parse.return_value = mock_args
        
        # Setup mock client and response
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.text = self.mock_response_text
        mock_response.function_calls = None
        mock_client_instance.models.generate_content.return_value = mock_response
        
        # Call the function
        result = main()
        
        # Assertions
        mock_load.assert_called_once()
        mock_client.assert_called_once_with(api_key=self.mock_api_key)
        self.assertEqual(result, self.mock_response_text)
        self.assertIn("Final response:", self.held_output.getvalue())

    @patch('main.genai.Client')
    @patch('main.load_dotenv')
    def test_main_missing_api_key(self, mock_load, mock_client):
        # Remove the API key from environment
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(SystemExit):
                main()
            self.assertIn("Error: GEMINI_API_KEY not found", self.held_output.getvalue())

    @patch('main.generate_content')
    @patch('main.genai.Client')
    @patch('main.load_dotenv')
    @patch('main.argparse.ArgumentParser.parse_args')
    def test_main_max_iters_reached(self, mock_parse, mock_load, mock_client, mock_generate):
        # Setup mock arguments
        mock_args = MagicMock()
        mock_args.prompt = self.test_prompt
        mock_args.verbose = False
        mock_parse.return_value = mock_args
        
        # Make generate_content always return None to trigger max iters
        mock_generate.return_value = None
        
        # Call the function - should exit
        with self.assertRaises(SystemExit):
            main()
        self.assertIn(f"Maximum iterations ({self.max_iters}) reached", self.held_output.getvalue())

class TestGenerateContent(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_messages = []
        self.verbose = False
        
        # Common mock response components
        self.mock_part = MagicMock()
        self.mock_part.function_response.response = "mock function response"
        self.mock_content = MagicMock()
        self.mock_content.parts = [self.mock_part]

    @patch('main.types.Content')
    def test_generate_content_simple_response(self, mock_content_type):
        # Setup mock response without function calls
        mock_response = MagicMock()
        mock_response.text = "Simple response"
        mock_response.function_calls = None
        mock_response.candidates = []
        mock_response.usage_metadata = MagicMock()
        mock_response.usage_metadata.prompt_token_count = 10
        mock_response.usage_metadata.candidates_token_count = 20
        
        self.mock_client.models.generate_content.return_value = mock_response
        
        # Call the function
        result = generate_content(self.mock_client, self.mock_messages, self.verbose)
        
        # Assertions
        self.assertEqual(result, "Simple response")
        self.mock_client.models.generate_content.assert_called_once()

    @patch('main.types.Content')
    @patch('main.call_function')
    def test_generate_content_with_function_calls(self, mock_call_function, mock_content_type):
        # Setup mock response with function calls
        mock_response = MagicMock()
        mock_response.text = None
        mock_response.function_calls = [MagicMock()]
        mock_response.candidates = []
        
        # Mock the function call response
        mock_call_result = MagicMock()
        mock_call_result.parts = [MagicMock()]
        mock_call_result.parts[0].function_response = MagicMock()
        mock_call_function.return_value = mock_call_result
        
        self.mock_client.models.generate_content.return_value = mock_response
        
        # Call the function - should return None and append to messages
        result = generate_content(self.mock_client, self.mock_messages, self.verbose)
        
        # Assertions
        self.assertIsNone(result)
        mock_call_function.assert_called_once()
        mock_content_type.assert_called_once()

    @patch('main.call_function')
    def test_generate_content_empty_function_result(self, mock_call_function):
        # Setup mock response with function calls
        mock_response = MagicMock()
        mock_response.function_calls = [MagicMock()]
        
        # Mock empty function call result
        mock_call_result = MagicMock()
        mock_call_result.parts = []
        mock_call_function.return_value = mock_call_result
        
        self.mock_client.models.generate_content.return_value = mock_response
        
        # Should raise exception
        with self.assertRaises(Exception) as context:
            generate_content(self.mock_client, self.mock_messages, self.verbose)
        self.assertIn("empty function call result", str(context.exception))

    @patch('main.types.Content')
    def test_generate_content_verbose_output(self, mock_content_type):
        # Setup mock response with verbose output
        mock_response = MagicMock()
        mock_response.text = "Verbose response"
        mock_response.function_calls = None
        mock_response.candidates = []
        mock_response.usage_metadata = MagicMock()
        mock_response.usage_metadata.prompt_token_count = 10
        mock_response.usage_metadata.candidates_token_count = 20
        
        self.mock_client.models.generate_content.return_value = mock_response
        
        # Capture output
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = generate_content(self.mock_client, self.mock_messages, verbose=True)
            output = fake_out.getvalue()
            
        # Assert verbose output
        self.assertIn("Prompt tokens: 10", output)
        self.assertIn("Response tokens: 20", output)

if __name__ == '__main__':
    unittest.main()