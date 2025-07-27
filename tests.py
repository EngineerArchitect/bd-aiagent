from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file_content import write_file

class TestRunner:
    def __init__(self):
        self.test_cases = {
            'get_files_info': [
                {"args": ("calculator", "."), "desc": "Current directory"},
                {"args": ("calculator", "pkg"), "desc": "Package directory"},
                {"args": ("calculator", "/bin"), "desc": "System directory"},
                {"args": ("calculator", "../"), "desc": "Parent directory"}
            ],
            'get_file_content': [
                {"args": ("calculator", "main.py"), "desc": "Existing file"},
                {"args": ("calculator", "pkg/calculator.py"), "desc": "Nested file"},
                {"args": ("calculator", "/bin/cat"), "desc": "System file"},
                {"args": ("calculator", "pkg/does_not_exist.py"), "desc": "Non-existent file"}
            ],
            'write_file': [
                {"args": ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), "desc": "Simple write"},
                {"args": ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), "desc": "Nested write"},
                {"args": ("calculator", "/tmp/temp.txt", "this should not be allowed"), "desc": "Unauthorized write"}
            ],
            'run_python_file': [
                {"args": ("calculator", "main.py"), "desc": "should print the calculator's usage instructions"},
                {"args": ("calculator", "main.py",  ["3 + 5"]), "desc": "should run the calculator... which gives a kinda nasty rendered result"},
                {"args": ("calculator", "tests.py"), "desc": "should run tests"},
                {"args": ("calculator", "../main.py"), "desc": "Attempt to run non-existent file"},
                {"args": ("calculator", "nonexistent.py"), "desc": "this should return an error"}
            ]
        }

    def run_test(self, func_name, test_func):
        print(f"\n=== Running {func_name} tests ===")
        for i, test_case in enumerate(self.test_cases[func_name], 1):
            try:                
                args = test_case["args"]
                print(f"\nTest {i}: {test_case['desc']}")
                print(f"Function: {func_name}{args}")
                print("-" * 60)
                result = test_func(*args)
                print(result)
                print("-" * 60)
            except Exception as e:
                print(f"Error in test {i}: {test_case['desc']}")
                print(f"Exception: {e}")
                print("-" * 60)

    def run_all_tests(self):
        self.run_test('get_files_info', get_files_info)
        self.run_test('get_file_content', get_file_content)
        self.run_test('write_file', write_file)
        self.run_test('run_python_file', run_python_file)

if __name__ == "__main__":
    runner = TestRunner()
    # Run all tests by default
    # runner.run_all_tests()  
    
    # Alternatively run specific tests:
    runner.run_test('run_python_file', run_python_file)