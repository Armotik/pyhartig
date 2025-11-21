# pyhartig

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org/downloads)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A Python implementation of the formal algebra for Knowledge Graph Construction, based on the work of Olaf
> Hartig. [An Algebraic Foundation for Knowledge Graph Construction](https://arxiv.org/abs/2503.10385)

---

## 1. Project Context

This library is a research project developed for the **"Engineering For Research I"** module.

It is part of the **M1 Computer Science, SMART Computing Master's Program** at **Nantes Université**.

The project is hosted by the **LS2N (Laboratoire des Sciences du Numérique de Nantes)**, within the **GDD (Gestion des Données Distribuées) team**.

It serves as the core logical component for the **MCP-SPARQLLM** project, aiming to translate heterogeneous data sources
into RDF Knowledge Graphs via algebraic operators.

## 2. Features

`pyhartig` provides a set of composable Python objects representing the core algebraic operators for querying
heterogeneous data sources.

Current implementation status covers the foundations required to reproduce **Source** and **Extend** operators as defined in the paper:

* **Algebraic Structures**: Strict typing for `MappingTuple`, `IRI`, `Literal`, `BlankNode`, and the special error value `EPSILON` ($\epsilon$).
* **Source Operator**:
    * Generic abstract implementation (`SourceOperator`).
    * Concrete implementation for JSON data (`JsonSourceOperator`) using JSONPath.
    * Supports Cartesian Product flattening for multi-valued attributes.
* **Extend Operator**:
    * Implementation of the algebraic extension logic ($Extend_{\varphi}^{a}(r)$).
    * Allows dynamic creation of new attributes based on complex expressions.
* **Expression System ($\varphi$)**:
    * Composite pattern implementation for recursive expressions.
    * Supports `Constant`, `Reference` (attributes), and `FunctionCall`.
* **Built-in Functions**:
    * Implementation of Annex B functions: `toIRI`, `toLiteral`, `concat`.
    * Strict error propagation handling (Epsilon).

## 3. Theoretical Foundation

This implementation is formally grounded in the algebraic foundation defined by **Olaf Hartig**. We are implementing the
operators described in his work, which provide a formal semantics for defining data transformation and integration
operators (like `Source`, `Join`, `Project`, etc.) independent of the specific data source.

This implementation is formally grounded in the algebraic foundation defined by Olaf Hartig.

**Reference :** [Hartig, O., & Min Oo, S. (2025). An Algebraic Foundation for Knowledge Graph Construction.](https://arxiv.org/abs/2503.10385).

## 4. Project Structure

The project is organized to strictly follow the definitions provided in the research paper:

```text
src/pyhartig/
├── algebra/            # Core algebraic definitions
│   ├── Terms.py        # RDF Terms (IRI, Literal, BlankNode)
│   └── Tuple.py        # MappingTuple and Epsilon
├── expressions/        # Recursive expression system 
│   ├── Expression.py   # Abstract base class
│   ├── Constant.py     # Constant values
│   ├── Reference.py    # Attribute references
│   └── FunctionCall.py # Extension function applications
├── functions/          # Extension functions
│   └── builtins.py     # Implementation of toIRI, concat, etc.
└── operators/          # Algebraic Operators
    ├── Operator.py     # Abstract base class for all operators
    ├── ExtendOperator.py # Extend operator implementation
    ├── SourceOperator.py # Abstract Source operator
    └── sources/        # Source operator implementations
        └── JsonSourceOperator.py # JSON data source operator
tests/                  # Unit tests for all components
├── test_builtins.py    # Tests for built-in functions
├── test_expressions.py # Tests for expression evaluations
└── test_operators.py   # Tests for algebraic operators
LICENSE                 # MIT License
README.md               # Project documentation
pyproject.toml          # Project configuration and dependencies
requirements.txt        # Additional dependencies
```

## 5. Installation

For development, it is highly recommended to install the library in "editable" mode in a virtual environment.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Armotik/pyhartig
   cd pyhartig
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install in editable mode (with test dependencies):**
   ```bash
   pip install -e '.[test]'
   ```
   
## 6. Usage Example
### 6.1. Using the JsonSourceOperator

```python
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator

data = {
    "team": [
        {"id": 1, "name": "Alice", "roles": ["Dev", "Admin"]},
        {"id": 2, "name": "Bob",   "roles": ["User"]}
    ]
}

# 1. Define Iterator (q)
iterator = "$.team[*]"

# 2. Define Mappings (P)
mappings = {
    "user_id": "id",
    "user_role": "roles"
}

# 3. Execute
op = JsonSourceOperator(data, iterator, mappings)
results = op.execute()

# 4. Output (MappingTuples)
# Alice generates 2 tuples due to Cartesian Product (Dev + Admin)
for row in results:
    print(row)
```

### 6.2 Using Expressions

```python
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.functions.builtins import concat, to_iri
from pyhartig.algebra.Tuple import MappingTuple

# Goal: Create an IRI [http://example.org/user/1](http://example.org/user/1) from ID "1"

# Expression: toIRI(concat("[http://example.org/user/](http://example.org/user/)", Reference("id")))
expr = FunctionCall(
    to_iri,
    [
        FunctionCall(
            concat,
            [Constant("[http://example.org/user/](http://example.org/user/)"), Reference("id")]
        )
    ]
)

row = MappingTuple({"id": "1"})
result = expr.evaluate(row)
print(result) # Output: [http://example.org/user/1](http://example.org/user/1)
```

### 6.3 Transforming Data (Extend Operator)

```python
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.functions.builtins import concat, to_iri

# Assume 'source_op' is the operator from Example 5.1

# Define the Expression: toIRI(concat("[http://example.org/user/](http://example.org/user/)", Reference("user_id")))
expr = FunctionCall(
    to_iri,
    [
        FunctionCall(
            concat,
            [Constant("[http://example.org/user/](http://example.org/user/)"), Reference("user_id")]
        )
    ]
)

# Apply Extend Operator
extend_op = ExtendOperator(
    parent_operator=source_op,
    new_attribute="subject",
    expression=expr
)

results = extend_op.execute()

for row in results:
    print(f"User: {row['user_name']} -> URI: {row['subject']}")
```

## 7. Testing

This project uses `pytest` for unit testing. To run the tests, ensure you have installed the test dependencies and execute:

```bash
pytest tests/
```

Tests cover:
- Algebraic logic (Cartesian Product flattening).
- JSONPath extraction.
- Built-in functions correctness and error propagation.
- Recursive expression evaluation.
- Operator chaining (`Source` -> `Extend`).

## 6. Authors

This project is developed by:

* **Anthony MUDET**
* **Léo FERMÉ**
* **Mohamed Lamine MERAH**

### 6.1. Supervision

This project is supervised by:

* **Full Professor Pascal MOLLI**
* **Full Professor Hala SKAF-MOLLI**
* **Associate Professor Gabriela MONTOYA**

## 7. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 8. Acknowledgements

We would like to thank the LS2N and GDD team for their support and resources provided during this project.
We also acknowledge the foundational work of Olaf Hartig, which inspired this implementation.

## 9. Contact

For any questions or contributions, please open an issue or contact the authors directly.

