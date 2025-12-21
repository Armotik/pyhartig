# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-21

### Added

#### Project Operator (Opérateur de Projection)
- **New Operator**: Added `ProjectOperator` for restricting mapping relations to specified attributes
  - Based on Definition 11 of relational algebra for mapping relations
  - Formal notation: `Project^P(r) : (A, I) -> (P, I')`
  - Input: Mapping relation `r = (A, I)` and non-empty subset `P ⊆ A`
  - Output: New mapping relation `(P, I')` where `I' = { t[P] | t ∈ I }`
  - For each tuple `t`, creates `t[P]` with `dom(t[P]) = P` and `t[P](a) = t(a)` for all `a ∈ P`

- **Strict Mode (Default)**:
  - Raises `KeyError` when projecting attributes not present in tuple
  - Enforces constraint `P ⊆ A` from classical relational algebra
  - Safer behavior: detects bugs early
  - Heterogeneous schemas handled via `Union` + multiple `Project` operations

- **ProjectOperator Features**:
  - `execute()`: Projects tuples to retain only specified attributes (strict mode)
  - `explain()`: Human-readable ASCII tree visualization
  - `explain_json()`: Machine-readable JSON format for API/tools

- **Use Case**: Useful for retaining only attributes needed in subsequent mapping steps

#### EquiJoin Operator (Opérateur d'Équi-jointure)
- **New Operator**: Implemented `EquiJoinOperator` for combining two mapping relations based on join conditions
  - Based on Definition 12 of relational algebra for mapping relations
  - Formal notation: `EqJoin^J(r₁, r₂) : Operator × Operator → Operator`
  - Input: Two mapping relations `r₁ = (A₁, I₁)` and `r₂ = (A₂, I₂)`
  - Join Conditions: Set `J ⊆ A₁ × A₂` defining attribute pairs for equality testing
  - Precondition: `A₁ ∩ A₂ = ∅` (attribute sets must be disjoint)
  - Output: New mapping relation `(A, I)` where:
    - `A = A₁ ∪ A₂` (union of all attributes)
    - `I = { t₁ ∪ t₂ | t₁ ∈ I₁, t₂ ∈ I₂, ∀(a₁, a₂) ∈ J : t₁(a₁) = t₂(a₂) }`

- **Join Condition Semantics**:
  - Supports multiple join conditions (compound keys)
  - Tuple pairs are merged only when ALL conditions are satisfied
  - Correctly handles `None` values in join attributes

- **EquiJoinOperator Features**:
  - `execute()`: Performs nested loop equi-join with condition checking
  - `explain()`: Human-readable ASCII tree visualization showing join conditions
  - `explain_json()`: Machine-readable JSON format for API/tools

- **Validation**:
  - Raises `ValueError` if attribute sets are not disjoint (A₁ ∩ A₂ ≠ ∅)
  - Raises `ValueError` if join attribute lists have different lengths

- **Use Case**: Particularly relevant for referencing object maps (referencing object maps) in RML translation, where joins are needed to combine data from multiple sources

### Testing

- Added comprehensive test suite for `ProjectOperator` (`test_12_project_operator.py`)
  - Basic projection tests (single, multiple, all attributes)
  - Strict mode validation (missing attribute raises `KeyError`)
  - Empty result handling
  - Operator composition (Project + Extend, Project + Union)
  - Chained projections
  - Explain functionality tests
  - Edge cases (IRI values, duplicate tuples, tuple order)
  - Integration tests (RDF generation, heterogeneous schema handling)
  - 20 new tests

- Added comprehensive test suite for `EquiJoinOperator` (`test_13_equijoin_operator.py`)
  - Basic equijoin tests (single condition, multiple conditions)
  - No-match scenarios (empty result)
  - Cartesian product-like behavior (many-to-many matches)
  - Precondition validation (disjoint attributes, equal-length attribute lists)
  - Empty relation handling (left/right empty)
  - Operator composition (EquiJoin + Extend, EquiJoin + Project)
  - Chained equijoins (three-way joins)
  - Explain functionality tests (text and JSON formats)
  - RML referencing object map use case simulation
  - Edge cases (null values, value preservation)
  - 17 new tests

### TODO
- Update documentation to include `ProjectOperator` and `EquiJoinOperator`
- Add examples in README and user guides
- Confirm tests
- Add existing tests from :
  - https://rml.io/test-cases/ 
  - https://github.com/anuzzolese/pyrml
  - https://github.com/RMLio/rmlmapper-java
  - https://github.com/morph-kgc/morph-kgc

## [0.1.15] - 2025-12-9

### Added

#### Explain Functionality
- **Pipeline Visualization**: Added `explain()` method to all operators for human-readable pipeline visualization
  - ASCII tree format with proper indentation
  - Shows operator hierarchy and parameters
  - Displays expression details inline
  - Example output:
    ```
    Union(
      operators: 2
      ├─ [0]:
        Extend(
          attribute: subject
          expression: to_iri(Ref(person_id), Const('http://example.org/'))
          parent:
            └─ Source(
                 iterator: $.team[*]
                 mappings: ['person_id', 'person_name']
               )
        )
      └─ [1]:
        Source(...)
    )
    ```

- **JSON Explanation API**: Added `explain_json()` method to all operators for programmatic access
  - Machine-readable JSON format
  - Complete operator tree structure
  - Expression details with type information
  - Suitable for visualization tools and API endpoints
  - Example output:
    ```json
    {
      "type": "Extend",
      "parameters": {
        "new_attribute": "subject",
        "expression": {
          "type": "FunctionCall",
          "function": "to_iri",
          "arguments": [...]
        }
      },
      "parent": {...}
    }
    ```

- **MappingParser Integration**: Added helper methods for pipeline explanation
  - `MappingParser.explain()` - Get text explanation of RML-generated pipeline
  - `MappingParser.explain_json()` - Get JSON explanation
  - `MappingParser.save_explanation(path, format)` - Save explanation to file

### Changed

- **Operator Base Class**: Updated `Operator` abstract class with new abstract methods
  - Added `explain(indent: int, prefix: str) -> str` abstract method
  - Added `explain_json() -> Dict[str, Any]` abstract method
  - All concrete operators now implement these methods

- **SourceOperator**: Enhanced with explanation capabilities
  - Implements `explain()` for text format
  - Implements `explain_json()` for JSON format
  - Shows iterator query and attribute mappings

- **JsonSourceOperator**: Enhanced with JSON-specific explanation details
  - Adds `source_type: "JSON"` to JSON output
  - Shows JSONPath-specific parameters

- **ExtendOperator**: Enhanced with expression visualization
  - Recursive expression explanation
  - Shows parent operator hierarchy
  - Detailed RDF term representation in JSON (IRI, Literal, BlankNode)

- **UnionOperator**: Enhanced with multi-child visualization
  - Shows operator count
  - Lists all child operators with proper tree formatting
  - JSON format includes all children in array

### Testing

- Added comprehensive test suite for `explain()` functionality
  - Tests for all operator types
  - Tests for expression formatting
  - Tests for nested operator trees
  - Tests for Union with multiple children

- Added comprehensive test suite for `explain_json()` functionality
  - Validates JSON structure for all operators
  - Tests expression serialization
  - Tests RDF term representation (IRI, Literal, BlankNode)
  - Tests nested pipelines
  - Validates JSON serializability (no serialization errors)
  - 12 new tests with 100% pass rate

- Updated GitHub/GitLab use case test
  - Added validation for proper IRI generation
  - Validates that subjects are IRI type, not Literal
  - Ensures N-Triples output is valid RDF

### Documentation

- Added "Pipeline Visualization" section to README
  - Documents `explain()` and `explain_json()` usage
  - Provides examples for both formats
  - Shows integration with MappingParser

- Updated test suite documentation
  - Added test category for explain functionality
  - Updated test count (95 → 107 tests)

## [0.1.14] - 2025-12-09
### Changed
- **Project structure in `README.md`**.

## [0.1.13] - 2025-12-09

### Fixed
- **RML Term Type Defaults**: Fixed `MappingParser._create_ext_expr()` to correctly apply R2RML default term types:
  - Subject Maps now default to `rr:IRI` (was incorrectly defaulting to Literal)
  - Predicate Maps now default to `rr:IRI` (was incorrectly defaulting to Literal)
  - Object Maps continue to default to `rr:Literal` (correct)
- This fix ensures generated RDF subjects and predicates are proper IRIs, not literals, making the output conformant with RDF standards

### Technical Details
- Modified `_create_ext_expr()` to accept `default_term_type` parameter
- Updated method calls in `parse()` to specify appropriate defaults based on map type