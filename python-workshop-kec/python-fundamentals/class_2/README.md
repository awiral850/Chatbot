# Python Class 2: Libraries, venv, pip, Imports, Structure, Config

## 1. What are Libraries?
A library is a collection of code (modules) you can use in your own programs. Python has a huge standard library and many third-party libraries (install with pip).

- **Standard Library**: Comes with Python (e.g., `math`, `os`, `json`)
- **Third-party**: You install (e.g., `requests`, `numpy`)

**Why use libraries?**
- Save time, avoid rewriting code
- Solve common problems quickly

---

## 2. Why Virtual Environments (`venv`)?
Different projects may need different versions of the same library. Installing everything globally can cause conflicts.

**Example:**
- Project A needs `requests==2.25.0`
- Project B needs `requests==2.31.0`
- If you install both globally, one project will break!

**Solution:** Use a virtual environment for each project. Each venv has its own set of libraries and versions.

### How to create and activate a venv
```bash
python3 -m venv .venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

---

## 3. pip: Python's Package Manager
`pip` lets you install, remove, and manage libraries inside your venv.

```bash
pip install requests
pip uninstall requests
pip freeze > requirements.txt
pip install -r requirements.txt
```

---

## 4. Imports in Python
Imports let you use code from other files or libraries.

### Types of imports
- Standard library: `import math`
- Third-party: `import requests`
- Local: `from utils.helper import greet`

### How import paths work
- The starting point is always the file you run (e.g., `main.py`).
- Imports are relative to the project root (where you run the script).

---

## 5. Folder Structure & Import Examples

This structure helps you understand imports and the effect of `__init__.py`:

```
greet()
load_data()
tool_func()
project_demo/
    main.py
    utils/
        __init__.py
        helper.py
    data/
        __init__.py
        loader.py
```

- `main.py` imports from `utils.helper` and `data.loader`.
- `data/__init__.py` runs code when you import from `data` (see below for a real-world example).

### How `__init__.py` Makes a Package Cohesive
You can use `__init__.py` to set up package-wide variables, configuration, or code that should run when the package is imported.

Suppose you want to log when the data package is loaded, or set up a shared resource:

**data/__init__.py**
```python
print("[data] Data package initialized!")
DATA_SOURCE = "data.csv"
```

**data/loader.py**
```python
from data import DATA_SOURCE

def load_data():
    print(f"Loading data from {DATA_SOURCE}")
```

**utils/helper.py**
```python
def greet():
    print("Hello from helper!")
```

**main.py**
```python
from utils.helper import greet
from data.loader import load_data

greet()
load_data()
```

When you run `main.py`, you'll see:
```
[data] Data package initialized!
Hello from helper!
Loading data from data.csv
```

This shows how `__init__.py` can be used for package setup, and how imports work between folders.
```

---

## 6. Configuration: Why Not Hardcode?
Hardcoding secrets or settings in your code is risky:
- You might accidentally share passwords if you upload code to GitHub.
- Changing settings (like API keys) means editing code, which is error-prone.

**Better:** Use `.env` or `.json` files for configuration.

### .env Example
```
API_KEY=your_api_key_here
DEBUG=True
```
Load with `python-dotenv`:
```python
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")
DEBUG = os.getenv("DEBUG")
```

### config.json Example
```json
{
    "api_key": "your_api_key_here",
    "debug": true
}
```
Load in Python:
```python
import json
with open("config.json") as f:
    config = json.load(f)
print(config["api_key"])
```

---

## Summary
- Use libraries to save time and effort.
- Use venv to avoid dependency conflicts.
- Use pip to manage libraries.
- Understand how imports work and how folder structure affects them.
- Never hardcode secrets/configs; use `.env` or `.json` files instead.
