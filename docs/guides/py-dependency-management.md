# Python dependency management  

## Package dependencies

### 1. Your shared package needs a library from PyPi or other registry:

- declare this, example

  ```
  # qavex/packages/<my-package>/pyproject.toml

  [project]
  name = "my-package"
  version = "0.1.0"
  dependencies = [
    "pydantic",
    "requests",
  ]
  ```

## Service dependencies

### 2. Your backend service needs <my-package> from above:

- declare this, example:

  ```
  # qavex/backend/<my-service>/pyproject.toml

  [project]
  name = "my-service"
  version = "0.1.0"
  dependencies = [
    "my-package == 0.1.0",
  ]
  ```

# CONFIGURE `UV`

### 3. You are going to ```"import <my-package>"``` somewhere in ```<my-service>```:

- declare ```<my-package>``` dependency, example:  


```
# qavex/pyproject.toml

[project]
name = "qavex-monorepo"
version = "0.1.0"
requires-python = "==3.11.*"
dependencies = [
  "my-package == 0.1.0",
]
```

### 4. Declare from where <my-code> should be taken  

#### 4.1. installation from local folder

- include the following section :


```
# qavex/.pyproject.toml

[tool.uv.sources]
my-service = { workspace = true }
my-package = { workspace = true }
```

#### 4.2. installation from external source

- include  something like this example:

```
# qavex/.pyproject.toml

[tool.uv.sources]
my-package = { git = "https://github.com/<my-package>/<my-package>" }
my-service = { git = "https://github.com/<my-service>/<my-service>" }
```


### 5. Discover workspace members

- include the following section

```
# qavex/pyproject.toml

[tool.uv.workspace]
members = [
  "backend/*"
  "packages/py-packages/*",
]
```

This setting will guide the UV how to make the graph of all deps needed

### 6. Final config file

```
# qavex/pyproject.toml

[project]
name = "qavex-monorepo"
version = "0.1.0"
requires-python = "==3.11.*"
dependencies = [
  "my-package == 0.1.0",
  "my-service == 0.1.0",
]

[tool.uv.sources]
my-service = { workspace = true }
my-package = { workspace = true }

[tool.uv.workspace]
members = [
  "packages/py-packages/*",
  "services/*",
]

exclude = []
```

## Create virtual envyronment

Run within `/qavex` (project's root folder):

```
uv venv
uv sync
```

or

```
uv sync
```

After this:

- uv will make `qavex/.venv`
- uv will make a graph of all deps needed via `[tool.uv.workspace]`
- uv will install everything from `[project.dependencies]` into `qavex/.venv` in an editable mode
- it almost equals to `pip install -e .`
- uv will use code's sources from  [tool.uv.sources] section
- uv will create `qavex/uv.lock` file that will keep in sync all the dependencies

## You are done!!!

## Please note:
- do not forget reconfigure `pyproject.toml` files after any dependencies change
- do not forget to run `uv sync` after any dependencies change to keep `uv.lock` file in sync with project's state
- do not use auto installation via IDE as you probably will get unexpected behavior:
  - deps are installed in .venv
  - deps are included in workspace `qavex/pyproject.toml`
  - imports are working:
    - !!! deps are absent in the main source of truth - `qavex/<my-service>/pyproject.toml`
