# PyHartig Comprehensive Test Suite

## Overview

This test suite provides comprehensive validation of the PyHartig. The tests are organized into eleven categories, each focusing on specific aspects of the system's functionality.

## Test Organization

### 1. Source Operator Tests (`test_01_source_operators.py`)

**Objective**: Validate JSON source operators with iteration and extraction mechanisms.

**Test Coverage**:
- Simple iterator and extraction queries
- Array-valued attribute extraction with Cartesian products
- Nested JSON structure traversal
- Empty result handling
- Missing attribute graceful degradation
- Multi-dimensional Cartesian products

**Key Features**:
- Tests the fundamental `JsonSourceOperator` implementation
- Validates JSONPath query execution
- Ensures correct Cartesian product generation

### 2. Extend Operator Tests (`test_02_extend_operators.py`)

**Objective**: Validate attribute augmentation through algebraic expressions.

**Test Coverage**:
- Extension with constant expressions
- Extension with reference expressions
- Extension with function call expressions
- Operator chaining
- EPSILON handling
- Fluent interface patterns
- Complex nested expressions

**Key Features**:
- Tests the `ExtendOperator` core functionality
- Validates expression evaluation in tuple context
- Ensures proper attribute addition and propagation

### 3. Operator Composition Tests (`test_03_operator_composition.py`)

**Objective**: Validate operator fusion and pipeline construction.

**Test Coverage**:
- Basic Source-Extend fusion
- Multi-stage extension pipelines
- Extend on Cartesian product results
- Dependent computed attributes
- Empty result propagation
- Parallel extension branches
- Union with Extend composition
- Extend after Union
- Union of complex pipelines
- Nested Union composition

**Key Features**:
- Tests operator interoperability
- Validates complex pipeline construction
- Ensures data flow integrity
- **Union operator integration with other operators**

### 4. Complete Pipeline Tests (`test_04_complete_pipelines.py`)

**Objective**: End-to-end transformation scenarios.

**Test Coverage**:
- RDF triple generation pipeline
- Person profile generation
- Hierarchical data processing
- Error-resilient pipelines
- Multi-source Union pipeline
- Union with post-processing
- Complex RDF generation with Union

**Key Features**:
- Realistic use case demonstrations
- Full transformation workflows
- Production-like scenarios
- Multi-source data integration scenarios

### 5. Built-in Function Tests (`test_05_builtin_functions.py`)

**Objective**: Validate RDF term construction and transformation functions.

**Test Coverage**:
- `to_iri()`: String to IRI conversion, base resolution, type handling
- `to_literal()`: Literal construction with datatype specification
- `concat()`: String concatenation with various input types
- Function composition patterns
- EPSILON propagation

**Key Features**:
- Comprehensive function testing
- Edge case validation
- Type conversion verification

### 6. Expression System Tests (`test_06_expression_system.py`)

**Objective**: Validate the algebraic expression evaluation system.

**Test Coverage**:
- Constant expressions
- Reference expressions
- Function call expressions
- Nested function composition
- EPSILON handling in expressions
- Expression string representations

**Key Features**:
- Expression abstraction validation
- Evaluation mechanism testing
- Composition pattern verification

### 7. Library Integration Tests (`test_07_library_integration.py`)

**Objective**: Validate integration with external libraries.

**Test Coverage**:
- JSONPath-ng library queries (basic and complex)
- JSONPath edge cases
- Operator-library integration
- Python JSON library features
- Unicode handling
- RDF term construction patterns
- Library version compatibility

**Key Features**:
- External dependency validation
- Library feature coverage
- Integration point testing

### 8. Real Data Integration Tests (`test_08_real_data_integration.py`)

**Objective**: Validate functionality with actual project data files.

**Test Coverage**:
- Loading `test_data.json`
- Team member extraction
- Cartesian product with real data
- Complete RDF generation pipeline
- Mapping file validation
- Project metadata extraction

**Key Features**:
- Uses actual project data files
- Validates realistic scenarios
- Tests with `data/test_data.json` and `data/mappings/test_mapping.yaml`

### 9. Union Operator Tests (`test_09_union_operator.py`)

**Objective**: Validate the Union operator for merging multiple data sources.

**Test Coverage**:
- Union of two and three sources
- Union with extended sources (Extend before Union)
- Union with empty sources
- Union preserving tuple order
- Union with different attribute schemas
- Union duplicate handling (bag semantics)
- Union single operator edge case

**Key Features**:
- Tests the `UnionOperator` core functionality
- Validates multi-source data merging
- Ensures proper tuple preservation and ordering
- Tests integration with other operators (Source, Extend)
- Validates edge cases (empty sources, single operator, duplicates)

**Additional Integration Tests**:
- Union with Extend composition (in `test_03_operator_composition.py`)
- Extend after Union (in `test_03_operator_composition.py`)
- Union of complex pipelines (in `test_03_operator_composition.py`)
- Nested Union composition (in `test_03_operator_composition.py`)
- Multi-source Union pipeline (in `test_04_complete_pipelines.py`)
- Union with post-processing (in `test_04_complete_pipelines.py`)
- Complex RDF generation with Union (in `test_04_complete_pipelines.py`)

### 10. Explain Tests (`test_10_explain.py`)

**Objective**: Validate human-readable pipeline visualization with the `explain()` method.

**Test Coverage**:
- Simple source operator explanation
- Extend operator with expression visualization
- Union operator with multiple children
- Nested operator hierarchies
- Complex expression trees display

**Key Features**:
- Tests the `explain()` method for all operator types
- Validates tree-like structure generation
- Ensures proper indentation and formatting
- Displays expression details (Constants, References, FunctionCalls)

**Example Output**:
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
  ...
)
```

### 11. Explain JSON Tests (`test_11_explain_json.py`)

**Objective**: Validate JSON-based pipeline representation with the `explain_json()` method.

**Test Coverage**:
- Source operator with all parameters
- Extend with Constant expressions
- Extend with Reference expressions
- Extend with FunctionCall expressions (to_iri, to_literal, concat)
- Extend with IRI constant values
- Nested Extend operators
- Union operator with children array
- Union with extended sources
- Complex nested pipeline structures
- Valid JSON serialization verification

**Key Features**:
- Tests the `explain_json()` method for all operator types
- Validates complete serializable pipeline representation
- Ensures proper JSON structure with type information
- Provides programmatic access to pipeline structure

### 12. Project Operator Tests (`test_12_project_operator.py`)

**Objective**: Validate the Project operator for restricting mapping relations to specified attributes.

Based on Definition 11: `Project^P(r) : (A, I) -> (P, I')` where:
- `r = (A, I)`: Source mapping relation with attributes A and instance I
- `P ⊆ A`: Non-empty subset of attributes to retain
- Result: New mapping relation `(P, I')` where `I' = { t[P] | t ∈ I }`

**Test Coverage**:
- Single attribute projection
- Multiple attribute projection
- Identity projection (P = A)
- Value preservation verification (`t[P](a) = t(a)`)
- **Strict mode validation**: Missing attribute raises `KeyError`
- Multiple missing attributes error reporting
- Empty source handling
- Operator composition (Project + Extend, Project + Union)
- Chained projections
- Explain functionality (`explain()` and `explain_json()`)
- IRI value preservation
- Duplicate tuple handling (bag semantics)
- Tuple order preservation

**Key Features**:
- Tests the `ProjectOperator` core functionality
- Validates strict mode behavior (P ⊆ A enforced)
- Tests integration with other operators (Source, Extend, Union)
- Validates edge cases and error handling
- Integration tests for RDF generation and heterogeneous schema handling

**Strict Mode Rationale**:
- Safer behavior: detects bugs early when projecting non-existent attributes
- Conforms to classical relational algebra where `P ⊆ A` is required
- Heterogeneous schemas can be handled with `Union` + multiple `Project` operations

**Example - Handling Heterogeneous Schemas**:
```python
# Source A has: id, name, dept
source_a = JsonSourceOperator(data_a, "$.items[*]", {"id": "$.id", "name": "$.name", "dept": "$.dept"})

# Source B has: id, name, role (different schema)
source_b = JsonSourceOperator(data_b, "$.items[*]", {"id": "$.id", "name": "$.name", "role": "$.role"})

# Project each to common schema before union
project_a = ProjectOperator(source_a, {"id", "name"})
project_b = ProjectOperator(source_b, {"id", "name"})

# Union now works with homogeneous schemas
union = UnionOperator([project_a, project_b])
```

**Example Output**:
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
  ]
}
```

## Running the Tests

### Run All Tests

```bash
# Retournez à la racine du projet
cd ../..

# Puis exécutez les tests
pytest tests/test_suite/ -v -s

# Ou le script de tests
python tests/test_suite/run_all_tests.py

```

### Run Specific Test Categories

```bash
cd ../..

# Source operators only
pytest tests/test_suite/test_01_source_operators.py -v -s

# Extend operators only
pytest tests/test_suite/test_02_extend_operators.py -v -s

# Union operators only
pytest tests/test_suite/test_09_union_operator.py -v -s

# Explain tests
pytest tests/test_suite/test_10_explain.py -v -s

# Explain JSON tests
pytest tests/test_suite/test_11_explain_json.py -v -s

# Project operators only
pytest tests/test_suite/test_12_project_operator.py -v -s

# Complete pipelines
pytest tests/test_suite/test_04_complete_pipelines.py -v -s

# Real data integration
pytest tests/test_suite/test_08_real_data_integration.py -v -s

# All Union-related tests (across all files)
pytest tests/test_suite/ -k union -v -s

# All explain-related tests
pytest tests/test_suite/ -k explain -v -s
```

### Run with Markers

```bash
cd ../.. 
# Unit tests only
pytest tests/test_suite/ -m unit -v

# Integration tests only
pytest tests/test_suite/ -m integration -v
```

## Debug Output

All tests include comprehensive debug output that provides:

1. **Test Objective**: Clear statement of what is being tested
2. **Configuration Details**: Input data, operator setup, expression definitions
3. **Execution Results**: Detailed output including tuple counts and sample data
4. **Validation Summary**: Confirmation of assertions and key findings

### Example Debug Output

```
================================================================================
[DEBUG] Test: Simple Iterator and Extraction
--------------------------------------------------------------------------------
Objective: Extract team member names and IDs
================================================================================

================================================================================
[DEBUG] Configuration
--------------------------------------------------------------------------------
Iterator: $.team[*]
Mappings:
  - person_id: $.id
  - person_name: $.name
================================================================================

================================================================================
[DEBUG] Execution Result
--------------------------------------------------------------------------------
Number of tuples: 2
Tuples:
  1. Tuple(person_id=1, person_name='Alice')
  2. Tuple(person_id=2, person_name='Bob')
================================================================================

================================================================================
[DEBUG] Validation
--------------------------------------------------------------------------------
✓ All assertions passed
================================================================================
```

## Test Data Files

The test suite uses the following data files:

- **`data/test_data.json`**: Sample JSON data with team structure
- **`data/mappings/test_mapping.yaml`**: Example RML-like mapping configuration
- **`data/mappings/expected_test_output.nt`**: Expected RDF output (N-Triples format)

## Test Statistics

- **Total Test Files**: 11
- **Total Tests**: 108
- **Test Categories**: Source, Extend, Union, Composition, Pipelines, Functions, Expressions, Libraries, Integration, Explain, Explain JSON
- **Coverage Areas**: Operators, Expressions, Functions, Libraries, Real Data, Multi-Source Merging, Pipeline Visualization
- **Debug Traces**: Comprehensive output for all tests

## Requirements

```
pytest>=7.0.0
jsonpath-ng~=1.7.0
```

Optional for YAML mapping validation:
```
PyYAML>=6.0
```

## Continuous Integration

These tests are designed to be:
- **Automated**: Can run in CI/CD pipelines
- **Reproducible**: Consistent results across environments
- **Documented**: Self-documenting through debug output
- **Comprehensive**: Cover all major system components

## Troubleshooting

### Common Issues

**Import Errors**: Ensure the project is installed in development mode:
```bash
pip install -e .
```

**JSONPath Errors**: Verify jsonpath-ng is installed:
```bash
pip install jsonpath-ng~=1.7.0
```

**Debug Output Not Showing**: Use the `-s` flag with pytest:
```bash
pytest tests/test_suite/ -v -s
```

## License

This test suite is part of the PyHartig project and follows the same license.

---

**Last Updated**: 2025-12-09
**Test Suite Version**: 2.1.0

