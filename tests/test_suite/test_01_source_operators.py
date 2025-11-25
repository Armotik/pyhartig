"""
Test Suite for Source Operators

This module provides comprehensive unit tests for source operators,
specifically focusing on the JsonSourceOperator implementation.
Tests validate iterator and extraction query mechanisms.
"""

import pytest
import json
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator


class TestJsonSourceOperator:
    """Test suite for JSON-based source operators."""

    @pytest.fixture
    def sample_json_data(self):
        """
        Fixture providing sample JSON data for testing.
        
        Returns:
            dict: Sample JSON structure with nested data
        """
        return {
            "project": "SPARQLLM Beta",
            "team": [
                {
                    "id": 1,
                    "name": "Alice",
                    "roles": ["Dev", "Admin"],
                    "skills": ["Python", "RDF"]
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "roles": ["User"],
                    "skills": ["Java"]
                }
            ]
        }

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

    def test_simple_iterator_extraction(self, sample_json_data, debug_logger):
        """
        Test basic iterator functionality with simple extraction queries.
        
        Validates that the source operator correctly iterates through
        JSON arrays and extracts specified attributes.
        """
        debug_logger("Test: Simple Iterator and Extraction",
                     "Objective: Extract team member names and IDs")

        # Define source operator
        operator = JsonSourceOperator(
            source_data=sample_json_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        debug_logger("Configuration",
                     f"Iterator: $.team[*]\n"
                     f"Mappings:\n"
                     f"  - person_id: $.id\n"
                     f"  - person_name: $.name")

        # Execute operator
        result = operator.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        # Assertions
        assert len(result) == 2, "Should extract 2 team members"
        assert result[0]["person_name"] == "Alice"
        assert result[0]["person_id"] == 1
        assert result[1]["person_name"] == "Bob"
        assert result[1]["person_id"] == 2

        debug_logger("Validation", "✓ All assertions passed")

    def test_array_extraction(self, sample_json_data, debug_logger):
        """
        Test extraction of array-valued attributes.
        
        Validates that the operator correctly handles extraction queries
        that return multiple values, generating Cartesian products.
        """
        debug_logger("Test: Array Extraction with Cartesian Product",
                     "Objective: Extract roles and skills arrays")

        operator = JsonSourceOperator(
            source_data=sample_json_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "name": "$.name",
                "role": "$.roles[*]"
            }
        )

        debug_logger("Configuration",
                     f"Iterator: $.team[*]\n"
                     f"Mappings:\n"
                     f"  - name: $.name\n"
                     f"  - role: $.roles[*]")

        result = operator.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        # Alice has 2 roles, Bob has 1 role
        assert len(result) == 3, "Should generate 3 tuples (2 for Alice, 1 for Bob)"

        alice_tuples = [t for t in result if t["name"] == "Alice"]
        bob_tuples = [t for t in result if t["name"] == "Bob"]

        assert len(alice_tuples) == 2
        assert len(bob_tuples) == 1

        alice_roles = {t["role"] for t in alice_tuples}
        assert alice_roles == {"Dev", "Admin"}

        debug_logger("Validation",
                     f"✓ Cartesian product correctly generated\n"
                     f"  - Alice tuples: {len(alice_tuples)}\n"
                     f"  - Bob tuples: {len(bob_tuples)}\n"
                     f"  - Alice roles: {alice_roles}")

    def test_nested_extraction(self, debug_logger):
        """
        Test extraction from nested JSON structures.
        
        Validates operator behavior with deeply nested data.
        """
        nested_data = {
            "organization": {
                "departments": [
                    {
                        "name": "Engineering",
                        "manager": {
                            "name": "Charlie",
                            "level": 5
                        }
                    },
                    {
                        "name": "Sales",
                        "manager": {
                            "name": "Diana",
                            "level": 4
                        }
                    }
                ]
            }
        }

        debug_logger("Test: Nested Extraction",
                     "Objective: Extract manager data from nested structure")

        operator = JsonSourceOperator(
            source_data=nested_data,
            iterator_query="$.organization.departments[*]",
            attribute_mappings={
                "dept": "$.name",
                "mgr_name": "$.manager.name",
                "mgr_level": "$.manager.level"
            }
        )

        debug_logger("Configuration",
                     f"Input data:\n{json.dumps(nested_data, indent=2)}\n\n"
                     f"Iterator: $.organization.departments[*]\n"
                     f"Mappings:\n"
                     f"  - dept: $.name\n"
                     f"  - mgr_name: $.manager.name\n"
                     f"  - mgr_level: $.manager.level")

        result = operator.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        assert len(result) == 2
        assert result[0]["dept"] == "Engineering"
        assert result[0]["mgr_name"] == "Charlie"
        assert result[1]["mgr_level"] == 4

        debug_logger("Validation", "✓ Nested extraction successful")

    def test_empty_result_handling(self, debug_logger):
        """
        Test operator behavior with queries yielding no results.
        
        Validates graceful handling of empty result sets.
        """
        data = {"items": []}

        debug_logger("Test: Empty Result Handling",
                     "Objective: Validate behavior with empty iterators")

        operator = JsonSourceOperator(
            source_data=data,
            iterator_query="$.items[*]",
            attribute_mappings={"value": "$.val"}
        )

        result = operator.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Expected: 0 tuples for empty iterator")

        assert len(result) == 0, "Empty iterator should produce no tuples"

        debug_logger("Validation", "✓ Empty result correctly handled")

    def test_missing_attribute_extraction(self, debug_logger):
        """
        Test extraction query on non-existent attributes.
        
        Validates that missing attributes result in empty value lists,
        not errors.
        """
        data = {
            "records": [
                {"id": 1, "name": "Item1"},
                {"id": 2}  # Missing 'name' attribute
            ]
        }

        debug_logger("Test: Missing Attribute Extraction",
                     "Objective: Handle missing attributes gracefully")

        operator = JsonSourceOperator(
            source_data=data,
            iterator_query="$.records[*]",
            attribute_mappings={
                "record_id": "$.id",
                "record_name": "$.name"
            }
        )

        debug_logger("Configuration",
                     f"Input data:\n{json.dumps(data, indent=2)}\n\n"
                     f"Note: Second record lacks 'name' attribute")

        result = operator.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        # Only the first record with both attributes should generate a tuple
        assert len(result) == 1, "Only complete records should generate tuples"
        assert result[0]["record_name"] == "Item1"

        debug_logger("Validation",
                     "✓ Missing attributes handled correctly\n"
                     "  Cartesian product with empty list yields no tuples")

    def test_cartesian_product_multiple_arrays(self, debug_logger):
        """
        Test Cartesian product with multiple array-valued extractions.
        
        Validates that the operator correctly computes the Cartesian
        product when multiple attributes have multiple values.
        """
        data = {
            "items": [
                {
                    "id": "A",
                    "colors": ["red", "blue"],
                    "sizes": ["S", "M"]
                }
            ]
        }

        debug_logger("Test: Multiple Array Cartesian Product",
                     "Objective: Generate all combinations of colors and sizes")

        operator = JsonSourceOperator(
            source_data=data,
            iterator_query="$.items[*]",
            attribute_mappings={
                "item_id": "$.id",
                "color": "$.colors[*]",
                "size": "$.sizes[*]"
            }
        )

        debug_logger("Configuration",
                     f"Input data:\n{json.dumps(data, indent=2)}\n\n"
                     f"Expected combinations: 2 colors × 2 sizes = 4 tuples")

        result = operator.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        assert len(result) == 4, "Should generate 2×2=4 combinations"

        # Verify all combinations exist
        combinations = {(t["color"], t["size"]) for t in result}
        expected = {("red", "S"), ("red", "M"), ("blue", "S"), ("blue", "M")}
        assert combinations == expected

        debug_logger("Validation",
                     f"✓ All combinations generated correctly:\n"
                     f"  {combinations}")
