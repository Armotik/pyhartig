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

Current implementation status covers the foundations required to reproduce **Source**, **Extend**, **Union**, and **Project** operators as defined in the paper:

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
* **Project Operator**:
    * Implementation of the algebraic projection logic ($Project^{P}(r)$).
    * Restricts mapping relations to specified subset of attributes.
    * Strict mode: raises exception if projected attribute not found (enforces $P \subseteq A$).
    * Useful for schema normalization before Union operations.
* **Expression System ($\varphi$)**:
    * Composite pattern implementation for recursive expressions.
    * Supports `Constant`, `Reference` (attributes), and `FunctionCall`.
* **Built-in Functions**:
    * Implementation of Annex B functions: `toIRI`, `toLiteral`, `concat`.
    * Strict error propagation handling (Epsilon).
* **RML Mapping Support**:
    * Includes an RML Parser (`MappingParser`) that translates declarative RML mapping files (Turtle .ttl) into an executable algebraic pipeline
* **Pipeline Visualization**:
    * `explain()` method for human-readable pipeline trees
    * `explain_json()` method for programmatic access to pipeline structure
    * Detailed expression and operator visualization

## 3. Theoretical Foundation

This implementation is formally grounded in the algebraic foundation defined by **Olaf Hartig**. We are implementing the
operators described in his work, which provide a formal semantics for defining data transformation and integration
operators independent of the specific data source.

This implementation is formally grounded in the algebraic foundation defined by Olaf Hartig.

**Reference :** [Hartig, O., & Min Oo, S. (2025). An Algebraic Foundation for Knowledge Graph Construction.](https://arxiv.org/abs/2503.10385).

### 3.1. RML/R2RML Conformance

This implementation follows the **RML** (RDF Mapping Language) and **R2RML** (RDB to RDF Mapping Language) specifications:

- **Default Term Types** (as per R2RML specification):
  - Subject Maps: `rr:IRI` (default)
  - Predicate Maps: `rr:IRI` (default)
  - Object Maps: `rr:Literal` (default)
  
- **Supported Term Map Components**:
  - `rr:constant` - Fixed values
  - `rr:reference` - JSONPath references
  - `rr:template` - String templates with placeholders
  - `rr:termType` - Explicit term type override

#### Example

```turtle
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix ex: <http://example.org/> .

 a rr:TriplesMap;
  rr:subjectMap [
    rr:template "http://example.org/person/{id}";
    # termType defaults to rr:IRI for subject maps
  ];
  
  rr:predicateObjectMap [
    rr:predicateMap [
      rr:constant ex:name;
      # termType defaults to rr:IRI for predicate maps
    ];
    rr:objectMap [
      rr:reference "$.name";
      # termType defaults to rr:Literal for object maps
    ]
  ].
```

**References:**
- [R2RML Specification](https://www.w3.org/TR/r2rml/)
- [RML Specification](https://rml.io/specs/rml/)

## 4. Project Structure

The project is organized to strictly follow the definitions provided in the research paper:

```text
src/pyhartig/
├── data/               # Sample data files for testing
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
├── mapping/            # RML Mapping Parser
│   └── MappingParser.py # Parses RML files into operator pipelines
└── operators/          # Algebraic Operators
    ├── Operator.py     # Abstract base class for all operators
    ├── ExtendOperator.py # Extend operator implementation
    ├── ProjectOperator.py # Project operator implementation
    ├── UnionOperator.py  # Union operator implementation
    ├── SourceOperator.py # Abstract Source operator
    └── sources/        # Source operator implementations
        └── JsonSourceOperator.py # JSON data source operator
tests/                  # Unit tests for all components
├── use_cases/        # Example usage scripts
│   └── github_gitlab/ # Example with GitHub and GitLab data
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
    ├── test_10_explain.py          # Tests for explain() method
    ├── test_11_explain_json.py     # Tests for explain_json() method
    ├── test_12_project_operator.py # Tests for ProjectOperator
    └── TEST_SUITE_README.md  # Comprehensive test suite documentation
LICENSE                 # MIT License
README.md               # Project documentation
CHANGELOG.md            # Project changelog
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
### 6.1. The "Data-Driven" Way (Using RML)

This is the recommended way. You define your mapping in RML (Turtle) and let the engine execute it.

```python
from pyhartig.mapping.MappingParser import MappingParser

# 1. Load your RML mapping file
parser = MappingParser("tests/use_cases/github_gitlab/data/fusion_mapping.ttl")

# 2. Compile it into an algebraic pipeline
pipeline = parser.parse()

# 3. Execute to get the RDF graph (as tuples)
results = pipeline.execute()

for row in results:
    print(f"{row['subject']} {row['predicate']} {row['object']}")
```

### 6.2. The "Algebraic" Way (Manual Python Code)

You can manually construct the operator pipeline for debugging or specific logic.

```python
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.operators.UnionOperator import UnionOperator
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.Constant import Constant
from pyhartig.functions.builtins import to_iri, concat

# 1. Define Source
source_op = JsonSourceOperator(
    source_data={"users": [{"id": 1, "name": "Alice"}]},
    iterator_query="$.users[*]",
    attribute_mappings={"uid": "id", "name": "name"}
)

# 2. Define Transformation (Extend)
# Create IRI: http://ex.org/user/{uid}
iri_expr = FunctionCall(
    to_iri,
    [FunctionCall(concat, [Constant("http://ex.org/user/"), Reference("uid")])]
)

extend_op = ExtendOperator(source_op, "subject", iri_expr)

# 3. Execute
results = extend_op.execute()
``` 

### 6.3. Pipeline Visualization

#### 6.3.1. Human-Readable Format

Get a visual representation of your pipeline structure:

```python
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.Constant import Constant
from pyhartig.functions.builtins import to_iri

# Build a pipeline
data = {"team": [{"id": 1, "name": "Alice"}]}
source = JsonSourceOperator(
    source_data=data,
    iterator_query="$.team[*]",
    attribute_mappings={"person_id": "$.id", "person_name": "$.name"}
)

uri_expr = FunctionCall(to_iri, [Reference("person_id"), Constant("http://example.org/")])
extend = ExtendOperator(source, "subject", uri_expr)

# Explain the pipeline
print(extend.explain())
```

**Output:**
```
Extend(
  attribute: subject
  expression: to_iri(Ref(person_id), Const('http://example.org/'))
  parent:
    └─ Source(
         type: JsonSourceOperator
         iterator: $.team[*]
         mappings: ['person_id', 'person_name']
       )
)
```

#### 6.3.2. JSON Format (Programmatic Access)

Get a machine-readable JSON representation:

```python
import json

# Get JSON explanation
explanation = extend.explain_json()
print(json.dumps(explanation, indent=2))
```

**Output:**
```json
{
  "type": "Extend",
  "parameters": {
    "new_attribute": "subject",
    "expression": {
      "type": "FunctionCall",
      "function": "to_iri",
      "arguments": [
        {
          "type": "Reference",
          "attribute": "person_id"
        },
        {
          "type": "Constant",
          "value_type": "str",
          "value": "http://example.org/"
        }
      ]
    }
  },
  "parent": {
    "type": "Source",
    "operator_class": "JsonSourceOperator",
    "parameters": {
      "iterator": "$.team[*]",
      "attribute_mappings": {
        "person_id": "$.id",
        "person_name": "$.name"
      },
      "source_type": "JSON",
      "jsonpath_iterator": "$.team[*]"
    }
  }
}
```

#### 6.3.3. Explaining RML Mappings

Visualize the pipeline generated from RML mappings:

```python
from pyhartig.mapping.MappingParser import MappingParser

parser = MappingParser("mapping.ttl")

# Text format
print(parser.explain())

# JSON format
import json
print(json.dumps(parser.explain_json(), indent=2))

# Save to file
parser.save_explanation("pipeline.json", format="json")
parser.save_explanation("pipeline.txt", format="text")
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
- Pipeline explanation (text and JSON formats).

### 7.1. Comprehensive Test Suite

The project includes a comprehensive test suite with **128 tests** organized into **12 categories**, all of which pass successfully. Below are representative examples from each category with their results.

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

**Result:** Functions successfully composed with proper type conversions and error propagation.

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

**Result:** Pipeline executed successfully on real data with correct Cartesian product handling.

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



**Result:** Multi-source union with post-processing successful. All 4 persons merged and uniformly transformed with roles preserved.

**Additional Union Test Coverage:**
- Union of two and three sources
- Union with extended sources (Extend before Union)
- Extend after Union (post-processing)
- Union of complex multi-stage pipelines
- Nested Union composition (Union of Unions)
- Union with empty sources and edge cases
- Union preserving tuple order (bag semantics)
- Union with different attribute schemas

#### 7.1.10. Explain Tests

**Example: Pipeline Visualization with explain()**

Tests the human-readable pipeline visualization for debugging and documentation purposes.

**Real-world example from GitHub/GitLab integration use case:**

```text
Union(
  operators: 48
  ├─ [0]:
    Extend(
      attribute: object
      expression: Const(<http://schema.org/Issue>)
      parent:
        └─ Extend(
          attribute: predicate
          expression: Const(<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
          parent:
            └─ Extend(
              attribute: subject
              expression: to_iri(concat(Const('http://gitlab.com/issue/'), Ref(iid)))
              parent:
                └─ Source(
                  iterator: $[*]
                  mappings: ['iid']
                )
            )
        )
    )
  ├─ [1]:
    Extend(
      attribute: object
      expression: Const("GitHub")
      parent:
        └─ Extend(
          attribute: predicate
          expression: Const(<http://example.org/source>)
          parent:
            └─ Extend(
              attribute: subject
              expression: to_iri(concat(Const('http://github.com/issue/'), Ref(number)))
              parent:
                └─ Source(
                  iterator: $[*]
                  mappings: ['number']
                )
            )
        )
    )
  ├─ [2]:
    Extend(
      attribute: object
      expression: to_literal(Ref(body), Const('http://www.w3.org/2001/XMLSchema#string'))
      parent:
        └─ Extend(
          attribute: predicate
          expression: Const(<http://schema.org/description>)
          parent:
            └─ Extend(
              attribute: subject
              expression: to_iri(concat(Const('http://github.com/issue/'), Ref(number)))
              parent:
                └─ Source(
                  iterator: $[*]
                  mappings: ['number', 'body']
                )
            )
        )
    )
  ...
)
```

**Result:** Pipeline visualization successfully generates readable tree-like structures showing:
- Operator hierarchy with proper indentation
- Expression details (Constants, References, FunctionCalls)
- Source mappings and iterators
- Union structure with numbered children

**Additional Explain Test Coverage:**
- Simple source operator explanation
- Extend operator with expression visualization
- Union operator with multiple children (up to 48 operators)
- Nested operator hierarchies
- Complex expression trees with nested function calls

#### 7.1.11. Explain JSON Tests

**Example: Programmatic Pipeline Analysis with explain_json()**

Tests the JSON-based pipeline representation for programmatic access to pipeline structure.

**Real-world example from GitHub/GitLab integration use case:**

```json
{
  "type": "Union",
  "parameters": {
    "operator_count": 36
  },
  "children": [
    {
      "type": "Extend",
      "parameters": {
        "new_attribute": "object",
        "expression": {
          "type": "FunctionCall",
          "function": "to_literal",
          "arguments": [
            {
              "type": "Reference",
              "attribute": "created_at"
            },
            {
              "type": "Constant",
              "value_type": "str",
              "value": "http://www.w3.org/2001/XMLSchema#string"
            }
          ]
        }
      },
      "parent": {
        "type": "Extend",
        "parameters": {
          "new_attribute": "predicate",
          "expression": {
            "type": "Constant",
            "value_type": "IRI",
            "value": "http://schema.org/dateCreated"
          }
        },
        "parent": {
          "type": "Extend",
          "parameters": {
            "new_attribute": "subject",
            "expression": {
              "type": "FunctionCall",
              "function": "to_iri",
              "arguments": [
                {
                  "type": "FunctionCall",
                  "function": "concat",
                  "arguments": [
                    {
                      "type": "Constant",
                      "value_type": "str",
                      "value": "http://github.com/issue/"
                    },
                    {
                      "type": "Reference",
                      "attribute": "number"
                    }
                  ]
                }
              ]
            }
          },
          "parent": {
            "type": "Source",
            "operator_class": "JsonSourceOperator",
            "parameters": {
              "iterator": "$[*]",
              "attribute_mappings": {
                "number": "number",
                "created_at": "created_at"
              },
              "source_type": "JSON",
              "jsonpath_iterator": "$[*]"
            }
          }
        }
      }
    }
  ]
}
```

**Result:** JSON explanation provides complete serializable pipeline representation including:
- Full operator type hierarchy
- Expression trees with function calls and arguments
- Source operator metadata (iterator, mappings, source type)
- Nested parent-child relationships
- Valid JSON for programmatic processing

**Additional Explain JSON Test Coverage:**
- Source operator with all parameters
- Extend with Constant expressions
- Extend with Reference expressions
- Extend with FunctionCall expressions (to_iri, to_literal, concat)
- Extend with IRI constant values
- Nested Extend operators
- Union operator with children array
- Union with extended sources
- Complex nested pipeline structures (up to 36+ operators)
- Valid JSON serialization verification

#### 7.1.12. Project Operator Tests

**Example: Projection to Subset of Attributes**

Tests restricting a mapping relation to a specified subset of attributes based on Definition 11.

```python
# Project^P(r) : (A, I) -> (P, I')
# Input relation r with attributes: {person_id, person_name, dept, salary}
# Projection P = {person_id, person_name}

# Input tuples:
# Tuple(person_id=1, person_name='Alice', dept='Engineering', salary=75000)
# Tuple(person_id=2, person_name='Bob', dept='Marketing', salary=65000)

# Result tuples (only projected attributes):
# Tuple(person_id=1, person_name='Alice')
# Tuple(person_id=2, person_name='Bob')
```

**Result:** Projection successfully restricts tuples to specified attributes P.

**Example: Strict Mode - Missing Attribute Error**

Tests that projecting a non-existent attribute raises a KeyError (strict mode enforces P ⊆ A).

```python
# Attempt to project non-existent attribute
project = ProjectOperator(source, {"person_name", "nonexistent_attr"})
project.execute()

# Raises KeyError:
# "ProjectOperator: Attribute(s) {'nonexistent_attr'} not found in tuple.
#  Available attributes: {'person_id', 'person_name', 'dept', 'salary'}.
#  Projection requires P ⊆ A (all projected attributes must exist in the tuple)."
```

**Result:** Strict mode correctly detects missing attributes and raises informative exception.

**Example: Heterogeneous Schema Handling with Union + Project**

Tests the recommended approach for handling different schemas: project each source to common attributes before union.

```python
# Source A has: {id, name, dept}
# Source B has: {id, name, role}  (different schema)

# Project each to common schema
project_a = ProjectOperator(source_a, {"id", "name"})
project_b = ProjectOperator(source_b, {"id", "name"})

# Union now works with homogeneous schemas
union = UnionOperator([project_a, project_b])

# Result: All tuples have only {id, name} attributes
```

**Result:** Heterogeneous schemas successfully normalized using Project before Union.

**Additional Project Operator Test Coverage:**
- Single attribute projection
- Multiple attribute projection
- Identity projection (P = A)
- Value preservation verification (t\[P](a) = t(a))
- Strict mode validation (KeyError for P ⊄ A)
- Multiple missing attributes error reporting
- Empty source handling (Project^P(∅) = ∅)
- Operator composition (Project + Extend, Project + Union)
- Chained projections (Project(Project(r)))
- Explain functionality (text and JSON)
- IRI value preservation in projection
- Duplicate tuple handling (bag semantics)
- Tuple order preservation
- RDF triple generation with Project
- Integration tests for schema normalization


### 7.2. Test Suite Summary

**Execution Results:**
- **Total Tests:** 128
- **Passed:** 128 (100%)
- **Failed:** 0
- **Execution Time:** ~2.50s

**Coverage:**
- Source operators with JSONPath integration
- Extend operators with expression evaluation
- Union operators for multi-source data merging
- Project operators for attribute restriction (strict mode)
- Operator composition and chaining
- Complete end-to-end pipelines
- Built-in RDF functions (toIRI, toLiteral, concat)
- Expression system (Constant, Reference, FunctionCall)
- External library integration (jsonpath-ng, JSON)
- Real data transformation scenarios
- Pipeline visualization with explain()
- JSON pipeline representation with explain_json()
- Heterogeneous schema handling with Project + Union

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

