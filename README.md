# digikala-tools

Digikala Tools for LLMs

## Installation

This projects uses [uv](https://docs.astral.sh/uv/), a simple and fast dependency manager for Python projects. First install it following the instructions in [this link](https://docs.astral.sh/uv/getting-started/installation/). I prefer _Standalone installer_:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Update _uv_ as follow:

```bash
uv self update
```

You can create virtual environment as follow:

```bash
uv venv
```

Then if you want to use [usage.ipynb](./usage.ipynb) install all dependencies as follow:

```bash
uv sync
```

And if you just want to use the package use following command to exclude `dev` dependencies:

```bash
uv sync --no-dev
```

## Usage

Currently the only tool availabe is *digikala_search_tool* for [LangChain](https://www.langchain.com/) You can import it as follow:

```python
from digikala_tools.langchain_tools import get_digikala_search_tool
```

The only parameter is `return_direct`, which controls the flow of agent execution. 
Set this parameter to `True` if you want to return the tool result immediately and stop the agent. 
Set it to `False` if you want the agent to use the tool result and continue executing.

```python
digikala_search_tool = get_digikala_search_tool(return_direct=True)
```

Refer to [usage.ipynb](./usage.ipynb) to see the tool in action.