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

Current implementation status covers the foundations required to reproduce **Source**, **Extend**, and **Union** operators as defined in the paper:

* **Algebraic Structures**: Strict typing for `MappingTuple`, `IRI`, `Literal`, `BlankNode`, and the special error value `EPSILON` ($\epsilon$).
* **Source Operator**:
    * Generic abstract implementation (`SourceOperator`).
    * Concrete implementation for JSON data (`JsonSourceOperator`) using JSONPath.
    * Supports Cartesian Product flattening for multi-valued attributes.
* **Extend Operator**:
    * Implementation of the algebraic extension logic ($Extend_{\varphi}^{a}(r)$).
    * Allows dynamic creation of new attributes based on complex expressions.
* **Union Operator**:
    * Implementation of the algebraic union logic for merging multiple data sources.
    * Preserves tuple order and supports bag semantics (duplicates preserved).
    * Enables multi-source data integration scenarios.
* **Expression System ($\varphi$)**:
    * Composite pattern implementation for recursive expressions.
    * Supports `Constant`, `Reference` (attributes), and `FunctionCall`.
* **Built-in Functions**:
    * Implementation of Annex B functions: `toIRI`, `toLiteral`, `concat`.
    * Strict error propagation handling (Epsilon).

## 3. Theoretical Foundation

This implementation is formally grounded in the algebraic foundation defined by **Olaf Hartig**. We are implementing the
operators described in his work, which provide a formal semantics for defining data transformation and integration
operators independent of the specific data source.

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
    ├── UnionOperator.py  # Union operator implementation
    ├── SourceOperator.py # Abstract Source operator
    └── sources/        # Source operator implementations
        └── JsonSourceOperator.py # JSON data source operator
tests/                  # Unit tests for all components
└── test_suite
    ├── conftest.py      # Pytest configuration
    ├── run_all_tests.py # Script to run all tests
    ├── test_01_source_operator.py  # Tests for SourceOperator
    ├── test_02_extend_operator.py  # Tests for ExtendOperator
    ├── test_03_operator_composition.py # Tests for operator chaining
    ├── test_04_complete_pipelines.py  # End-to-end pipeline tests
    ├── test_05_builtin_functions.py   # Tests for built-in functions
    ├── test_06_expression_system.py    # Tests for expression evaluation
    ├── test_07_library_integration.py  # Tests for external library integration
    ├── test_08_real_data_integration.py  # Tests with real project data
    ├── test_09_union_operator.py  # Tests for UnionOperator
    └── TEST_SUITE_README.md  # Comprehensive test suite documentation
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

# Assume 'source_op' is the operator from Example 6.1

# Define the Expression: toIRI(concat("http://example.org/user/", Reference("user_id")))
expr = FunctionCall(
    to_iri,
    [
        FunctionCall(
            concat,
            [Constant("http://example.org/user/"), Reference("user_id")]
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

### 6.4 Merging Multiple Data Sources (Union Operator)

```python
from pyhartig.operators.UnionOperator import UnionOperator
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator

# Data from different departments
engineering_data = {
    "employees": [
        {"id": "E001", "name": "Alice", "dept": "Engineering"},
        {"id": "E002", "name": "Bob", "dept": "Engineering"}
    ]
}

marketing_data = {
    "employees": [
        {"id": "M001", "name": "Charlie", "dept": "Marketing"},
        {"id": "M002", "name": "Diana", "dept": "Marketing"}
    ]
}

# Create source operators for each department
source_eng = JsonSourceOperator(
    source_data=engineering_data,
    iterator_query="$.employees[*]",
    attribute_mappings={
        "emp_id": "$.id",
        "emp_name": "$.name",
        "department": "$.dept"
    }
)

source_mkt = JsonSourceOperator(
    source_data=marketing_data,
    iterator_query="$.employees[*]",
    attribute_mappings={
        "emp_id": "$.id",
        "emp_name": "$.name",
        "department": "$.dept"
    }
)

# Union the two sources
union_op = UnionOperator(operators=[source_eng, source_mkt])
results = union_op.execute()

# Output: 4 employees (2 from Engineering + 2 from Marketing)
for row in results:
    print(f"{row['emp_name']} - {row['department']}")
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
- Operator chaining (`Source` -> `Extend` -> `Union`).
- Multi-source data merging and integration.

### 7.1. Comprehensive Test Suite

The project includes a comprehensive test suite with **95 tests** organized into **9 categories**, all of which pass successfully. Below are representative examples from each category with their results.

#### 7.1.1. Source Operator Tests

**Example: Array Extraction with Cartesian Product**

Tests the extraction of multi-valued attributes and automatic Cartesian product generation.

```python
# Input data
data = {
    "team": [
        {"name": "Alice", "roles": ["Dev", "Admin"]},
        {"name": "Bob", "roles": ["User"]}
    ]
}

# Configuration
iterator = "$.team[*]"
mappings = {"name": "$.name", "role": "$.roles[*]"}

# Results (3 tuples generated)
# 1. Tuple(name='Alice', role='Dev')
# 2. Tuple(name='Alice', role='Admin')
# 3. Tuple(name='Bob', role='User')
```

**Result:** Cartesian product correctly generated - Alice generates 2 tuples (one per role), Bob generates 1 tuple.

#### 7.1.2. Extend Operator Tests

**Example: Extend with Function Call**

Tests the generation of RDF IRIs from existing attributes.

```python
# Generate IRI from ID attribute
expression = to_iri(Reference('id'), Constant('http://example.org/person/'))
extend_op = ExtendOperator(source_op, 'uri', expression)

# Results
# 1. Tuple(id='1', name='Alice', age=30, uri=<http://example.org/person/1>)
# 2. Tuple(id='2', name='Bob', age=25, uri=<http://example.org/person/2>)
```

**Result:** Function call successfully generated IRIs for all tuples with proper RDF term types.

#### 7.1.3. Operator Composition Tests

**Example: Source with Multiple Sequential Extends**

Tests the chaining of multiple transformation stages.

```python
# Pipeline stages:
# Stage 1: Source - Extract id and name
# Stage 2: Extend - subject = to_iri(id, base)
# Stage 3: Extend - type = foaf:Person
# Stage 4: Extend - name_literal = to_literal(name, xsd:string)

# Result for Alice
# Tuple(
#   id=1, 
#   name='Alice',
#   subject=<http://example.org/person/1>,
#   type=<http://xmlns.com/foaf/0.1/Person>,
#   name_literal="Alice"
# )
```

**Result:** Multi-stage pipeline successful with proper RDF term construction at each stage.

#### 7.1.4. Complete Pipeline Tests

**Example: RDF Triple Generation Pipeline**

Tests end-to-end transformation from JSON to RDF-like structures.

```python
# Input: Team data with roles and skills arrays
# Pipeline: Source → Generate Subject → Add Type → Convert to Literals

# Results (5 tuples total - Cartesian product of roles × skills)
# Alice: 4 tuples (2 roles × 2 skills)
# Bob: 1 tuple (1 role × 1 skill)

# Sample output
# Tuple(
#   member_id=1,
#   member_name='Alice',
#   role='Dev',
#   skill='Python',
#   subject=<http://example.org/person/1>,
#   rdf_type=<http://xmlns.com/foaf/0.1/Person>,
#   name_literal="Alice",
#   role_literal="Dev",
#   skill_literal="Python"
# )
```

**Result:** Pipeline executed successfully with 5 RDF-like tuples properly typed (IRI/Literal).

#### 7.1.5. Built-in Function Tests

**Example: Function Integration**

Tests composition of multiple built-in functions.

```python
# Compose concat and to_iri functions
# Step 1: concat('John', ' Doe') → "John Doe"
# Step 2: to_literal(name, xsd:string) → "John Doe"
# Step 3: to_iri(name_literal, base) → <http://example.org/person/John Doe>

# Final result
# IRI: <http://example.org/person/John Doe>
```

**Result:** ✓ Functions successfully composed with proper type conversions and error propagation.

#### 7.1.6. Expression System Tests

**Example: Complex Nested Expression**

Tests recursive expression evaluation with multiple levels of nesting.

```python
# Expression: to_literal(concat(Ref('name'), Const('_'), Ref('department')), xsd:string)
# Input: Tuple(name='Alice', department='Engineering')

# Inner: concat('Alice', '_', 'Engineering') → "Alice_Engineering"
# Outer: to_literal("Alice_Engineering", xsd:string) → "Alice_Engineering"

# Result: "Alice_Engineering" (typed literal)
```

**Result:** Nested functions evaluated correctly with proper intermediate result handling.

#### 7.1.7. Library Integration Tests

**Example: JSONPath Complex Queries**

Tests integration with the `jsonpath-ng` library for complex data extraction.

```python
# Test recursive descent and nested arrays
# Query 1: $..employees[*].name (recursive)
# Results: ['Alice', 'Bob', 'Charlie']

# Query 2: Nested array skills
# Results: ['Python', 'Java', 'C++', 'Go', 'Recruiting']
```

**Result:** Recursive descent and nested array traversal work correctly with external library.

#### 7.1.8. Real Data Integration Tests

**Example: Complete RDF Generation from Test Data**

Tests the entire system using the actual project data file (`data/test_data.json`).

```python
# Input: MCP-SPARQLLM project data with team members, roles, and skills
# Pipeline: Full 6-stage transformation to RDF structures

# Results: 5 tuples generated
# - Alice: 4 tuples (Dev×Python, Dev×RDF, Admin×Python, Admin×RDF)
# - Bob: 1 tuple (User×Java)

# Sample tuple structure:
# Tuple(
#   member_id=1,
#   member_name='Alice',
#   role='Dev',
#   skill='Python',
#   subject=<http://example.org/person/1>,
#   rdf_type=<http://xmlns.com/foaf/0.1/Person>,
#   name_literal="Alice",
#   role_literal="Dev",
#   skill_literal="Python"
# )
```

**Result:** ✓ Pipeline executed successfully on real data with correct Cartesian product handling.

#### 7.1.9. Union Operator Tests

**Example: Union with Post-Processing**

Tests merging data from different sources and applying uniform transformations to the merged result.

```python
# Input: Authors and Contributors from different data sources
# Pipeline 1: Authors → Extend(role='Author')
# Pipeline 2: Contributors → Extend(role='Contributor')
# Pipeline 3: Union(Pipeline1, Pipeline2)
# Pipeline 4-6: Post-process with URI, full_name, and label generation

# Results: 4 persons (2 authors + 2 contributors)
# Sample output:
# label="Alice Smith (Author)"
# label="Charlie Brown (Contributor)"
```

**Result:** ✓ Multi-source union with post-processing successful. All 4 persons merged and uniformly transformed with roles preserved.

**Additional Union Test Coverage:**
- Union of two and three sources
- Union with extended sources (Extend before Union)
- Extend after Union (post-processing)
- Union of complex multi-stage pipelines
- Nested Union composition (Union of Unions)
- Union with empty sources and edge cases
- Union preserving tuple order (bag semantics)
- Union with different attribute schemas

### 7.2. Test Suite Summary

**Execution Results:**
- **Total Tests:** 95
- **Passed:** 95 (100%)
- **Failed:** 0
- **Execution Time:** ~2.00s

**Coverage:**
- Source operators with JSONPath integration
- Extend operators with expression evaluation
- Union operators for multi-source data merging
- Operator composition and chaining
- Complete end-to-end pipelines
- Built-in RDF functions (toIRI, toLiteral, concat)
- Expression system (Constant, Reference, FunctionCall)
- External library integration (jsonpath-ng, JSON)
- Real data transformation scenarios

## 8. Authors

This project is developed by:

* **Anthony MUDET**
* **Léo FERMÉ**
* **Mohamed Lamine MERAH**

### 8.1. Supervision

This project is supervised by:

* **Full Professor Pascal MOLLI**
* **Full Professor Hala SKAF-MOLLI**
* **Associate Professor Gabriela MONTOYA**

## 9. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 10. Acknowledgements

We would like to thank the LS2N and GDD team for their support and resources provided during this project.
We also acknowledge the foundational work of Olaf Hartig, which inspired this implementation.

## 11. Contact

For any questions or contributions, please open an issue or contact the authors directly.

