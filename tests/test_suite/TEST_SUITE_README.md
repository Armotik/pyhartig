# PyHartig Comprehensive Test Suite

## Overview

This test suite provides comprehensive validation of the PyHartig. The tests are organized into eight categories, each focusing on specific aspects of the system's functionality.

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

**Key Features**:
- Tests operator interoperability
- Validates complex pipeline construction
- Ensures data flow integrity

### 4. Complete Pipeline Tests (`test_04_complete_pipelines.py`)

**Objective**: End-to-end transformation scenarios.

**Test Coverage**:
- RDF triple generation pipeline
- Person profile generation
- Hierarchical data processing
- Error-resilient pipelines

**Key Features**:
- Realistic use case demonstrations
- Full transformation workflows
- Production-like scenarios

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

# Complete pipelines
pytest tests/test_suite/test_04_complete_pipelines.py -v -s

# Real data integration
pytest tests/test_suite/test_08_real_data_integration.py -v -s
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

- **Total Test Files**: 8
- **Test Categories**: Source, Extend, Composition, Pipelines, Functions, Expressions, Libraries, Integration
- **Coverage Areas**: Operators, Expressions, Functions, Libraries, Real Data
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

**Last Updated**: 2025-11-25
**Test Suite Version**: 1.0.0

