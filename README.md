# AI Agent Project 

## Goal of project

Build an LLM-powered command-line program capable of reading, updating, and running Python code using the Gemini API. Learn how LLMs and agentic coding tools work.

## Learning objectives

Write a toy agentic code editor in Python, similar to Claude Code or Cursor's agent mode. Understand how agents work from scratch by using the free Google Gemini API to create an LLM-powered code agent. You'll use function calling and feedback loops to build an agent that can find and fix bugs in a real project!

## uv - Why not

This projecvt uses "https://github.com/astral-sh/uv"
which is described as a "An extremely fast Python package and project manager, written in Rust"

If not installed, you can infect your system using

```shell
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

or with pip
```shell
$ pip install uv
```

or if you use o/s is Windows
```shell
$ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

to update use
```shell
$ uv self update
```
## Virtual Environment and install Dependencies

First add venv and then install dependencies

```shell
$ uv venv
$ source .venv/bin/activate
$ uv pip install .
```

## Testing

The following are examples of running prompts

```shell
$ uv run main.py "run tests.py" --verbose
$ uv run main.py "get the contents of lorem.txt" --verbose
$ uv run main.py "create a new README.md file with the contents '# calculator'" --verbose
$ uv run main.py "what files are in the root?" --verbose
```

Additional Unit Tests added

```shell
$ python -m unittest test_main.py --verbose
```