### Getting Started

1. Install Python : https://www.python.org/downloads/

2. Install Poetry

```console
pipx install poetry
```

Or

```console
curl -sSL https://install.python-poetry.org | python3 -
```

3. Clone the repository
```
git clone https://github.com/gitdevjin/code-mage.git
cd code_mage
```

4. Install Poetry Package
```
poetry install
```

Now you are ready to use the tool!

### Usage


```console
poetry run codemage <source_file>
```

Options
-t, --target : choose your target language (currently python, java, c++, javascript is supported)
-o, --output : enter your output file name without extension

