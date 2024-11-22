<img src="https://vhs.charm.sh/vhs-5IzBzwY5YvLUKiO1Ntq8DX.gif">

# Description

**CodeMage** is a tool that translates a source file written in one programming language into another language.
The translation will be done by Large Language Model AI(such as ChatGPT)



## Features (Release 1.1.2)

    1. Supported Languages: Javascript, Python, C++, Java
    2. Default target Language is Python
    3. Supported LLM model: openrouter, groq
    4. Default LLM model is openrouter(sao10k/l3-euryale-70b)



<br>
<br>

# Getting started

### Prerequisite


1. Python
- You need python 3.12 or later version to use this tool
- Install Python : https://www.python.org/downloads/



<br>
<br>

## Start with `PyPI`

### 1. Download the package using PyPI
```bash
# for window user
pip install code-mage

# for mac user
pip3 install code-mage
```

<br>

### 2. Create your API_KEY at [openrouter](https://openrouter.ai/docs/api-keys) Or [Groq](https://console.groq.com/keys)

It's free with sign-up. You can easily sign-up with your google account

<br>

### 3.a Set-up the API_KEY using `Variable` (option 1)

```bash
export GROQ_API_KEY=YOUR-API-KEY # if you use groq model
export OPENROUTER_API_KEY=YOUR-API-KEY # if you use openrouter model
```

<br>

### 3.b Set-up with `.toml` file (option 2)

With this option, you can also set other tool options more easily

- Start by creating a `.codemage-config.toml` in your home directory.

```bash
vi ~/.codemage-config.toml
```

- Add the following environment settings in the file:

```toml
# the double quotes for string values are necessary.

model="groq" # if you wish to use OPEN ROUTER you can just delete this line
GROQ_API_KEY="<YOUR-GROQ-API-KEY>"
OPENROUTER_API_KEY="<YOUR-OPEN-ROUTER-API-KEY>"
language="java" # you can use any of the supported languages
stream=false # if you wish to get the output streamed, set it `true`
token_usage=false # if you wish to get token_usage info, set it `true`
output="result" # type any name for the output file without the extension
```

<br>

### 4. Run the tool

```bash
codemage <file-you-want-to-convert>

# For example,
codemage test.js
codemage test.js -s
codemage test.js -m openrouter # specify your model, or the default model is "groq"
```

<br>

# Start by cloning the github repo

If you are using the tool by cloning the repo, you need poetry package manager.

### 1. Install Poetry (if not installed yet)

```console
curl -sSL https://install.python-poetry.org | python3 -
```

**OR** if you have `pipx` installed on your local machine, you can use the following commend

```console
pipx install poetry
```

Refer to [How to download pipx](https://github.com/pypa/pipx)

<br>

### 2. Clone the repository

```console
git clone https://github.com/gitdevjin/code-mage.git
cd code_mage
```

<br>

### 3. Install Poetry Dependencies

```console
poetry install
```

<br>

### 4. Create your API_KEY at [openrouter](https://openrouter.ai/docs/api-keys) Or [Groq](https://console.groq.com/keys)

It's free with sign-up. You can easily sign-up with your google account

<br>

### 5-a Create `.env` file in the root directory and save the following:

```
OPENROUTER_API_KEY=your_open_router_api_key
GROQ_API_KEY=your_groq_api_key
```
<br>

### 5-b Using TOML files

You can also use `.toml` file with this method
Refer to [this](#3b-set-up-with-toml-file-option-2)

Now you are ready to use the tool!

<br>

# Usage

- Run the command

```console
poetry run codemage <source_file>
poetry run codemage ./example/test.js
```

## Examples

You can try the tool with the included example files as followings:

```console
poetry run codemage ./example/test.js -l python
```

<br>

You can also use the tool with multiple files:

```console
poetry run codemage ./example/test.js ./example/sample.js -l java
```

<br>

You can select model with `-m, --model <model_name>` option:

```console
poetry run codemage ./example/test.js -m groq -o result -t
```

<br>

You can stream out the result onto `stdout` with `-s, --stream` flag:

```console
poetry run codemage ./example/test.js -s
```

## Options

-h, --help : display help message and exit

-l, --language : choose your target language (currently python, java, c++, and javascript are supported)

-o, --output : enter your output file name without extension

-m, --model : select LLM API model (currently openrouter, and groq are supported)

-v, --version : Show program's version number and exit

-t, --token-usage : Get information about token usage for the prompt and response

-s, --stream : Stream out the output into stdout
