"""
Test Suite for Union Operator

This module provides comprehensive unit tests for the UnionOperator,
which merges the results of multiple operators into a single relation.
Tests validate merging behavior, tuple preservation, and empty result handling.
"""

import pytest
from pyhartig.operators.UnionOperator import UnionOperator
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.functions.builtins import to_iri
from pyhartig.algebra.Terms import IRI


class TestUnionOperator:
    """Test suite for the Union operator."""

    @pytest.fixture
    def debug_logger(self):
        """
        Fixture providing a debug logging function.
        
        Returns:
            callable: Function for structured debug output
        """
        def log(section, message):
            print(f"\n{'=' * 80}")
            print(f"[DEBUG] {section}")
            print(f"{'-' * 80}")
            print(message)
            print(f"{'=' * 80}\n")
        return log

    @pytest.fixture
    def dataset_a(self):
        """
        Fixture providing first dataset.
        
        Returns:
            dict: JSON structure with team A information
        """
        return {
            "team": [
                {"id": 1, "name": "Alice", "department": "Engineering"},
                {"id": 2, "name": "Bob", "department": "Engineering"}
            ]
        }

    @pytest.fixture
    def dataset_b(self):
        """
        Fixture providing second dataset.
        
        Returns:
            dict: JSON structure with team B information
        """
        return {
            "team": [
                {"id": 3, "name": "Charlie", "department": "Marketing"},
                {"id": 4, "name": "Diana", "department": "Marketing"}
            ]
        }

    @pytest.fixture
    def dataset_c(self):
        """
        Fixture providing third dataset.
        
        Returns:
            dict: JSON structure with team C information
        """
        return {
            "team": [
                {"id": 5, "name": "Eve", "department": "Sales"},
                {"id": 6, "name": "Frank", "department": "Sales"}
            ]
        }

    def test_union_two_sources(self, dataset_a, dataset_b, debug_logger):
        """
        Test basic union of two source operators.
        
        Validates that Union correctly merges results from two
        independent data sources.
        """
        debug_logger("Test: Union of Two Sources",
                     "Objective: Merge two independent datasets")

        # Create two source operators
        source_a = JsonSourceOperator(
            source_data=dataset_a,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "dept": "$.department"
            }
        )

        source_b = JsonSourceOperator(
            source_data=dataset_b,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "dept": "$.department"
            }
        )

        debug_logger("Pipeline Configuration",
                     f"Source A: 2 persons from Engineering\n"
                     f"Source B: 2 persons from Marketing\n"
                     f"Union(A, B) expected: 4 tuples")

        # Create union operator
        union_op = UnionOperator(operators=[source_a, source_b])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        # Validations
        assert len(result) == 4, "Union should produce 4 tuples"
        
        # Verify all names are present
        names = [tuple["person_name"] for tuple in result]
        assert "Alice" in names
        assert "Bob" in names
        assert "Charlie" in names
        assert "Diana" in names

        # Verify departments
        engineering_count = sum(1 for t in result if t["dept"] == "Engineering")
        marketing_count = sum(1 for t in result if t["dept"] == "Marketing")
        assert engineering_count == 2
        assert marketing_count == 2

        debug_logger("Validation",
                     "✓ Union of two sources successful\n"
                     "✓ All tuples preserved\n"
                     "✓ Correct department distribution")

    def test_union_three_sources(self, dataset_a, dataset_b, dataset_c, debug_logger):
        """
        Test union of three source operators.
        
        Validates that Union can merge multiple (>2) data sources.
        """
        debug_logger("Test: Union of Three Sources",
                     "Objective: Merge three independent datasets")

        source_a = JsonSourceOperator(
            source_data=dataset_a,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "dept": "$.department"
            }
        )

        source_b = JsonSourceOperator(
            source_data=dataset_b,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "dept": "$.department"
            }
        )

        source_c = JsonSourceOperator(
            source_data=dataset_c,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "dept": "$.department"
            }
        )

        debug_logger("Pipeline Configuration",
                     f"Source A: 2 persons (Engineering)\n"
                     f"Source B: 2 persons (Marketing)\n"
                     f"Source C: 2 persons (Sales)\n"
                     f"Union(A, B, C) expected: 6 tuples")

        union_op = UnionOperator(operators=[source_a, source_b, source_c])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Departments present: {set(t['dept'] for t in result)}")

        assert len(result) == 6, "Union should produce 6 tuples"
        
        departments = set(t["dept"] for t in result)
        assert "Engineering" in departments
        assert "Marketing" in departments
        assert "Sales" in departments

        debug_logger("Validation",
                     "✓ Union of three sources successful\n"
                     "✓ All 6 tuples preserved\n"
                     "✓ Three departments represented")

    def test_union_with_extended_sources(self, dataset_a, dataset_b, debug_logger):
        """
        Test union of extended source operators.
        
        Validates that Union works correctly when sources have
        computed attributes via Extend operator.
        """
        debug_logger("Test: Union with Extended Sources",
                     "Objective: Merge sources with computed RDF attributes")

        # Create and extend first source
        source_a = JsonSourceOperator(
            source_data=dataset_a,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        extend_a = ExtendOperator(
            parent_operator=source_a,
            new_attribute="subject",
            expression=FunctionCall(
                function=to_iri,
                arguments=[
                    Reference("person_id"),
                    Constant("http://example.org/person/")
                ]
            )
        )

        # Create and extend second source
        source_b = JsonSourceOperator(
            source_data=dataset_b,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        extend_b = ExtendOperator(
            parent_operator=source_b,
            new_attribute="subject",
            expression=FunctionCall(
                function=to_iri,
                arguments=[
                    Reference("person_id"),
                    Constant("http://example.org/person/")
                ]
            )
        )

        debug_logger("Pipeline Configuration",
                     f"Source A -> Extend(subject=IRI)\n"
                     f"Source B -> Extend(subject=IRI)\n"
                     f"Union of extended sources")

        union_op = UnionOperator(operators=[extend_a, extend_b])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Sample subjects:\n" + 
                     "\n".join(f"  - {t['subject']}" for t in result[:2]))

        assert len(result) == 4
        
        # Verify all tuples have computed IRI subjects
        for tuple in result:
            assert "subject" in tuple
            assert isinstance(tuple["subject"], IRI)
            assert tuple["subject"].value.startswith("http://example.org/person/")

        debug_logger("Validation",
                     "✓ Union with extended sources successful\n"
                     "✓ All computed attributes preserved\n"
                     "✓ IRI subjects correctly generated")

    def test_union_with_empty_source(self, dataset_a, debug_logger):
        """
        Test union where one source produces no tuples.
        
        Validates that Union handles empty results gracefully.
        """
        debug_logger("Test: Union with Empty Source",
                     "Objective: Handle union with one empty source")

        source_a = JsonSourceOperator(
            source_data=dataset_a,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        # Source with non-matching iterator (empty result)
        source_empty = JsonSourceOperator(
            source_data={"other": []},
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        debug_logger("Pipeline Configuration",
                     f"Source A: 2 tuples\n"
                     f"Source Empty: 0 tuples\n"
                     f"Union should return only Source A results")

        union_op = UnionOperator(operators=[source_a, source_empty])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}")

        assert len(result) == 2
        assert result[0]["person_name"] == "Alice"
        assert result[1]["person_name"] == "Bob"

        debug_logger("Validation",
                     "✓ Union with empty source successful\n"
                     "✓ Non-empty results preserved")

    def test_union_all_empty_sources(self, debug_logger):
        """
        Test union where all sources are empty.
        
        Validates that Union returns empty result when all sources are empty.
        """
        debug_logger("Test: Union of All Empty Sources",
                     "Objective: Handle union where all sources are empty")

        source_1 = JsonSourceOperator(
            source_data={"team": []},
            iterator_query="$.team[*]",
            attribute_mappings={"id": "$.id"}
        )

        source_2 = JsonSourceOperator(
            source_data={"team": []},
            iterator_query="$.team[*]",
            attribute_mappings={"id": "$.id"}
        )

        union_op = UnionOperator(operators=[source_1, source_2])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}")

        assert len(result) == 0

        debug_logger("Validation",
                     "✓ Union of empty sources returns empty result")

    def test_union_preserves_tuple_order(self, dataset_a, dataset_b, debug_logger):
        """
        Test that union preserves the order of tuples from sources.
        
        Validates that tuples from first operator appear before
        tuples from second operator.
        """
        debug_logger("Test: Union Preserves Tuple Order",
                     "Objective: Verify tuple ordering in union result")

        source_a = JsonSourceOperator(
            source_data=dataset_a,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        source_b = JsonSourceOperator(
            source_data=dataset_b,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        union_op = UnionOperator(operators=[source_a, source_b])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Order: " + ", ".join(t["person_name"] for t in result))

        # First two should be from dataset_a
        assert result[0]["person_name"] == "Alice"
        assert result[1]["person_name"] == "Bob"
        
        # Next two should be from dataset_b
        assert result[2]["person_name"] == "Charlie"
        assert result[3]["person_name"] == "Diana"

        debug_logger("Validation",
                     "✓ Tuple order preserved\n"
                     "✓ Source A tuples before Source B tuples")

    def test_union_with_different_attributes(self, debug_logger):
        """
        Test union of sources with different attribute schemas.
        
        Validates behavior when sources produce tuples with
        different attribute sets.
        """
        debug_logger("Test: Union with Different Attributes",
                     "Objective: Handle sources with different schemas")

        data_with_age = {
            "persons": [
                {"id": 1, "name": "Alice", "age": 30}
            ]
        }

        data_with_role = {
            "persons": [
                {"id": 2, "name": "Bob", "role": "Developer"}
            ]
        }

        source_1 = JsonSourceOperator(
            source_data=data_with_age,
            iterator_query="$.persons[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "age": "$.age"
            }
        )

        source_2 = JsonSourceOperator(
            source_data=data_with_role,
            iterator_query="$.persons[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name",
                "role": "$.role"
            }
        )

        debug_logger("Pipeline Configuration",
                     f"Source 1 schema: [person_id, person_name, age]\n"
                     f"Source 2 schema: [person_id, person_name, role]\n"
                     f"Union merges different schemas")

        union_op = UnionOperator(operators=[source_1, source_2])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuple 1 keys: {list(result[0].keys())}\n"
                     f"Tuple 2 keys: {list(result[1].keys())}")

        assert len(result) == 2
        
        # First tuple has age
        assert "age" in result[0]
        assert result[0]["age"] == 30
        
        # Second tuple has role
        assert "role" in result[1]
        assert result[1]["role"] == "Developer"

        debug_logger("Validation",
                     "✓ Union with different schemas successful\n"
                     "✓ Each tuple maintains its original attributes")

    def test_union_duplicate_tuples(self, debug_logger):
        """
        Test union behavior with duplicate tuples.
        
        Validates that Union does NOT eliminate duplicates
        (bag semantics, not set semantics).
        """
        debug_logger("Test: Union with Duplicate Tuples",
                     "Objective: Verify bag semantics (duplicates preserved)")

        same_data = {
            "team": [
                {"id": 1, "name": "Alice"}
            ]
        }

        source_1 = JsonSourceOperator(
            source_data=same_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        source_2 = JsonSourceOperator(
            source_data=same_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        union_op = UnionOperator(operators=[source_1, source_2])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Expected: 2 (duplicates preserved)")

        # Union should preserve duplicates (bag semantics)
        assert len(result) == 2
        assert result[0]["person_name"] == "Alice"
        assert result[1]["person_name"] == "Alice"

        debug_logger("Validation",
                     "✓ Union preserves duplicates\n"
                     "✓ Bag semantics confirmed")

    def test_union_single_operator(self, dataset_a, debug_logger):
        """
        Test union with a single operator.
        
        Validates edge case where Union contains only one operator.
        """
        debug_logger("Test: Union with Single Operator",
                     "Objective: Handle union with only one source")

        source_a = JsonSourceOperator(
            source_data=dataset_a,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        union_op = UnionOperator(operators=[source_a])
        result = union_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}")

        assert len(result) == 2
        assert result[0]["person_name"] == "Alice"
        assert result[1]["person_name"] == "Bob"

        debug_logger("Validation",
                     "✓ Union with single operator works\n"
                     "✓ Results passed through unchanged")

