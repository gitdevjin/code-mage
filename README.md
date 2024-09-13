# Description
-------------
**CodeMage** is a tool that translate a source file written in one programming language into another language.
The translation will be done by Large Language Model AI(such as ChatGPT)

# Getting Started
------------------

### 1. Install Python : https://www.python.org/downloads/

### 2. Install Poetry

```console
curl -sSL https://install.python-poetry.org | python3 -
```

Or if you have `pipx` installed on your locall machine, you can use the following commend
How to download [`pipx`](https://github.com/pypa/pipx)
```console
pipx install poetry
```

3. Clone the repository
```console
git clone https://github.com/gitdevjin/code-mage.git
cd code_mage
```

4. Install Poetry Package
```console
poetry install
```

5. Create your API_KEY at [here](https://openrouter.ai/docs/api-keys)
It's free with sign-up. You can easily sign-up with your google account

6. Create `.env` file in the root directory and save the following:
```
OPENROUTER_API_KEY=your open_router_api_key
```



Now you are ready to use the tool!

## Usage

```console
poetry run codemage <source_file>
```

Options

-t, --target : choose your target language (currently python, java, c++, javascript is supported)

-o, --output : enter your output file name without extension

