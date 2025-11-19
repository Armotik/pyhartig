import pytest
from typing import Dict, Any
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator


# --- FIXTURES ---

@pytest.fixture
def sample_json_data() -> Dict[str, Any]:
    """
    Provides sample JSON data for testing.
    :return: Sample JSON data
    """
    return {
        "university": "Nantes Université",
        "students": [
            {
                "id": "s1",
                "name": "Alice",
                "courses": ["Math", "Physics"],
                "badges": ["Gold"]
            },
            {
                "id": "s2",
                "name": "Bob",
                "courses": ["Biology"],
                "badges": []
            }
        ]
    }


# --- TESTS ---

def test_initialization(sample_json_data):
    """Test the initialization of JsonSourceOperator."""
    iterator = "$.students[*]"
    mappings = {"student_name": "name"}

    print("[DEBUG] test_initialization - iterator:", iterator)
    print("[DEBUG] test_initialization - mappings:", mappings)

    operator = JsonSourceOperator(sample_json_data, iterator, mappings)

    print("[DEBUG] test_initialization - operator.source_data:", operator.source_data)

    assert isinstance(operator, JsonSourceOperator)
    assert operator.source_data == sample_json_data


def test_single_value_extraction(sample_json_data):
    """Test Scenario 1: Simple extraction of single values."""
    # Iterator selecting only Bob (index 1)
    iterator = "$.students[1]"
    mappings = {
        "id": "id",
        "course": "courses"
    }

    print("[DEBUG] test_single_value_extraction - iterator:", iterator)
    print("[DEBUG] test_single_value_extraction - mappings:", mappings)

    operator = JsonSourceOperator(sample_json_data, iterator, mappings)
    results = operator.execute()

    print("[DEBUG] test_single_value_extraction - results:", results)

    assert len(results) == 1
    assert results[0] == {"id": "s2", "course": "Biology"}


def test_cartesian_product_flattening(sample_json_data):
    """Test Scenario 2: Extraction resulting in Cartesian Product."""
    # Iterator selecting only Alice (index 0)
    iterator = "$.students[0]"
    mappings = {
        "student_name": "name",
        "course_name": "courses",
        "badge_label": "badges"
    }

    print("[DEBUG] test_cartesian_product_flattening - iterator:", iterator)
    print("[DEBUG] test_cartesian_product_flattening - mappings:", mappings)

    operator = JsonSourceOperator(sample_json_data, iterator, mappings)
    results = operator.execute()

    print("[DEBUG] test_cartesian_product_flattening - results:", results)

    # Assert we have exactly 2 rows generated from 1 object
    assert len(results) == 2

    # Verify the content of the generated tuples
    expected_tuple_1 = {"student_name": "Alice", "course_name": "Math", "badge_label": "Gold"}
    expected_tuple_2 = {"student_name": "Alice", "course_name": "Physics", "badge_label": "Gold"}

    print("[DEBUG] test_cartesian_product_flattening - expected_tuple_1 in results:", expected_tuple_1 in results)
    print("[DEBUG] test_cartesian_product_flattening - expected_tuple_2 in results:", expected_tuple_2 in results)

    assert expected_tuple_1 in results
    assert expected_tuple_2 in results


def test_full_iteration(sample_json_data):
    """Test Scenario 3: Full iteration over all students."""
    iterator = "$.students[*]"
    mappings = {
        "id": "id",
        "course": "courses"
    }

    print("[DEBUG] test_full_iteration - iterator:", iterator)
    print("[DEBUG] test_full_iteration - mappings:", mappings)

    operator = JsonSourceOperator(sample_json_data, iterator, mappings)
    results = operator.execute()

    print("[DEBUG] test_full_iteration - results:", results)

    assert len(results) == 3

    # Check if Bob is present
    bob_entry = {"id": "s2", "course": "Biology"}
    print("[DEBUG] test_full_iteration - bob_entry in results:", bob_entry in results)

    assert bob_entry in results


def test_empty_list_handling(sample_json_data):
    """Test Scenario 4: Extraction resulting in empty lists."""
    iterator = "$.students[1]"  # Bob
    mappings = {
        "name": "name",
        "badge": "badges"  # Empty list []
    }

    print("[DEBUG] test_empty_list_handling - iterator:", iterator)
    print("[DEBUG] test_empty_list_handling - mappings:", mappings)

    operator = JsonSourceOperator(sample_json_data, iterator, mappings)
    results = operator.execute()

    print("[DEBUG] test_empty_list_handling - results:", results)

    # Since 'badges' is empty, product() returns empty.
    assert len(results) == 0


def test_missing_path_handling(sample_json_data):
    """Test Scenario 5: Extraction with non-existent paths."""
    iterator = "$.students[*]"
    mappings = {
        "name": "name",
        "ghost_field": "non_existent_path"  # Returns []
    }

    print("[DEBUG] test_missing_path_handling - iterator:", iterator)
    print("[DEBUG] test_missing_path_handling - mappings:", mappings)

    operator = JsonSourceOperator(sample_json_data, iterator, mappings)
    results = operator.execute()

    print("[DEBUG] test_missing_path_handling - results:", results)

    assert len(results) == 0

