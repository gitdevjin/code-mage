# Formatter and Linter

To set up automated Ruff linting and formatting with VS Code, Follow the instructions:

### 1. Python Extension for VS Code (if not already installed):

The Python extension for VS Code is needed to enable Python-specific features, such as linting and formatting integration. Open VS Code, go to the Extensions view (Ctrl+Shift+X or Cmd+Shift+X on macOS),search for "Python" by Microsoft and install it if you haven’t already.

### 2. Ruff VS Code Extension:

Install the Ruff extension in VS Code to enable real-time linting and formatting.
In the Extensions view, search for "Ruff," and install the extension.

## Manually Running Ruff Formatter and Linter

### Run the `Ruff formatter` with the following command in the root directory

```bash
poetry run ruff format .
```

### Run the `Ruff Linter` with the following command in the root directory

```bash
poetry run ruff check .
```

# Testing

For testing, we use `pytest`.

### install `pytest` if not installed yet.
```bash
poetry add --dev pytest
```

### Running `pytest`
This command will run files named `test_*.py` or `*_test.py`
```bash
poetry run pytest
```


For more detailed test result, you can use `-v` option
```bash
poetry run pytest -v
```

for more detailed test information
```bash
poetry run pytest -vv
```

### Writing TestCode
You should name your test class and method as follows:

#### Class name starts with `Test`

#### Method name starts with `test_`

```python
class TestMyFeature: # class name
    def test_feature_functionality: # method name
```