# Description
**CodeMage** is a tool that translates a source file written in one programming language into another language.
The translation will be done by Large Language Model AI(such as ChatGPT)

## Release 0.1

### Features
    1. Supported Languages: Javascript, Python, C++, Java
    2. Default target Language is Python



# Getting Started

### 1. Install Python : https://www.python.org/downloads/

<br>

### 2. Install Poetry

```console
curl -sSL https://install.python-poetry.org | python3 -
```

**OR** if you have `pipx` installed on your locall machine, you can use the following commend

[How to download `pipx`](https://github.com/pypa/pipx)

```console
pipx install poetry
```

<br>

### 3. Clone the repository
```console
git clone https://github.com/gitdevjin/code-mage.git
cd code_mage
```

<br>

### 4. Install Poetry Package
```console
poetry install
```

<br>

### 5. Create your API_KEY at [here](https://openrouter.ai/docs/api-keys)
It's free with sign-up. You can easily sign-up with your google account

<br>

### 6. Create `.env` file in the root directory and save the following:
```
OPENROUTER_API_KEY=your open_router_api_key
```

Now you are ready to use the tool!

<br>

# Usage

```console
poetry run codemage <source_file>
```

## Examples
You can try the tool with the included example files as followings:

```console
poetry run codemage ./example/test.js -t python -o result
```


```console
poetry run codemage ./example/test.js ./example/sample.js -target c++
```

## Options

-h, --help : display help message and exit

-l, --language : choose your target language (currently python, java, c++, and javascript are supported)

-o, --output : enter your output file name without extension

-m, --model : select LLM API model (currently openrouter, and groq are supported)

-v, --version : Show program's version number and exit

-t, --token-usage : Get information about token usage for the prompt and response


