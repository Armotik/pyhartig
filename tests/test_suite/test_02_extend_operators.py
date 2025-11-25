"""
Test Suite for Extend Operators

This module provides comprehensive unit tests for the ExtendOperator,
which augments mapping relations with computed attributes derived
from algebraic expressions.
"""

import pytest
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.functions.builtins import to_iri, to_literal, concat
from pyhartig.algebra.Tuple import EPSILON
from pyhartig.algebra.Terms import IRI, Literal


class TestExtendOperator:
    """Test suite for the Extend operator."""

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
    def simple_source_operator(self):
        """
        Fixture providing a simple source operator with test data.
        
        Returns:
            JsonSourceOperator: Configured operator with sample data
        """
        data = {
            "persons": [
                {"id": "1", "name": "Alice", "age": 30},
                {"id": "2", "name": "Bob", "age": 25}
            ]
        }
        return JsonSourceOperator(
            source_data=data,
            iterator_query="$.persons[*]",
            attribute_mappings={
                "id": "$.id",
                "name": "$.name",
                "age": "$.age"
            }
        )

    def test_extend_with_constant(self, simple_source_operator, debug_logger):
        """
        Test extending a relation with a constant value.
        
        Validates that the Extend operator correctly adds a constant
        attribute to all tuples.
        """
        debug_logger("Test: Extend with Constant Expression", 
                     "Objective: Add constant 'type' attribute to all tuples")
        
        # Create extend operator with constant
        extend_op = ExtendOperator(
            parent_operator=simple_source_operator,
            new_attribute="type",
            expression=Constant("Person")
        )
        
        debug_logger("Configuration", 
                     f"Parent operator: JsonSourceOperator\n"
                     f"New attribute: type\n"
                     f"Expression: Constant('Person')")
        
        result = extend_op.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        # Assertions
        assert len(result) == 2
        for tuple in result:
            assert "type" in tuple
            assert tuple["type"] == "Person"
        
        debug_logger("Validation", 
                     "✓ Constant successfully added to all tuples")

    def test_extend_with_reference(self, simple_source_operator, debug_logger):
        """
        Test extending with a reference to an existing attribute.
        
        Validates that references correctly retrieve values from
        source tuples.
        """
        debug_logger("Test: Extend with Reference Expression", 
                     "Objective: Copy 'name' attribute to 'label' attribute")
        
        extend_op = ExtendOperator(
            parent_operator=simple_source_operator,
            new_attribute="label",
            expression=Reference("name")
        )
        
        debug_logger("Configuration", 
                     f"Parent operator: JsonSourceOperator\n"
                     f"New attribute: label\n"
                     f"Expression: Reference('name')")
        
        result = extend_op.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        assert len(result) == 2
        assert result[0]["label"] == result[0]["name"]
        assert result[1]["label"] == result[1]["name"]
        
        debug_logger("Validation", 
                     "✓ Reference correctly copied attribute values")

    def test_extend_with_function_call(self, simple_source_operator, debug_logger):
        """
        Test extending with a function call expression.
        
        Validates that function calls correctly compute new values
        based on existing attributes.
        """
        debug_logger("Test: Extend with Function Call", 
                     "Objective: Generate IRI from 'id' attribute")
        
        # Create function call: to_iri(id, "http://example.org/person/")
        func_call = FunctionCall(
            function=to_iri,
            arguments=[
                Reference("id"),
                Constant("http://example.org/person/")
            ]
        )
        
        extend_op = ExtendOperator(
            parent_operator=simple_source_operator,
            new_attribute="uri",
            expression=func_call
        )
        
        debug_logger("Configuration", 
                     f"Parent operator: JsonSourceOperator\n"
                     f"New attribute: uri\n"
                     f"Expression: to_iri(Reference('id'), Constant('http://example.org/person/'))")
        
        result = extend_op.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        assert len(result) == 2
        assert isinstance(result[0]["uri"], IRI)
        assert result[0]["uri"].value == "http://example.org/person/1"
        assert result[1]["uri"].value == "http://example.org/person/2"
        
        debug_logger("Validation", 
                     f"✓ Function call successfully generated IRIs:\n"
                     f"  - {result[0]['uri']}\n"
                     f"  - {result[1]['uri']}")

    def test_extend_chaining(self, simple_source_operator, debug_logger):
        """
        Test chaining multiple Extend operators.
        
        Validates that multiple extensions can be applied sequentially,
        with later extensions accessing earlier computed attributes.
        """
        debug_logger("Test: Chained Extend Operations", 
                     "Objective: Chain multiple extensions sequentially")
        
        # First extension: add 'type' constant
        extend_op1 = ExtendOperator(
            parent_operator=simple_source_operator,
            new_attribute="type",
            expression=Constant("Person")
        )
        
        # Second extension: concatenate name and type
        concat_expr = FunctionCall(
            function=concat,
            arguments=[
                Reference("name"),
                Constant(" - "),
                Reference("type")
            ]
        )
        
        extend_op2 = ExtendOperator(
            parent_operator=extend_op1,
            new_attribute="full_label",
            expression=concat_expr
        )
        
        debug_logger("Configuration", 
                     f"Extension chain:\n"
                     f"  1. Add 'type' = Constant('Person')\n"
                     f"  2. Add 'full_label' = concat(name, ' - ', type)")
        
        result = extend_op2.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        assert len(result) == 2
        assert "type" in result[0]
        assert "full_label" in result[0]
        
        # Note: concat returns Literal, so we check lexical_form
        assert result[0]["full_label"].lexical_form == "Alice - Person"
        assert result[1]["full_label"].lexical_form == "Bob - Person"
        
        debug_logger("Validation", 
                     f"✓ Chained extensions successful:\n"
                     f"  - {result[0]['full_label']}\n"
                     f"  - {result[1]['full_label']}")

    def test_extend_with_epsilon_handling(self, debug_logger):
        """
        Test Extend operator behavior with undefined values (EPSILON).
        
        Validates that expressions returning EPSILON are properly
        assigned to the new attribute.
        """
        debug_logger("Test: EPSILON Handling in Extend", 
                     "Objective: Validate behavior with undefined references")
        
        # Create source with minimal data
        data = {"items": [{"id": "A"}, {"id": "B"}]}
        source_op = JsonSourceOperator(
            source_data=data,
            iterator_query="$.items[*]",
            attribute_mappings={"id": "$.id"}
        )
        
        # Reference non-existent attribute
        extend_op = ExtendOperator(
            parent_operator=source_op,
            new_attribute="missing_ref",
            expression=Reference("nonexistent")
        )
        
        debug_logger("Configuration", 
                     f"Source data: items with only 'id' attribute\n"
                     f"Expression: Reference('nonexistent')\n"
                     f"Expected: EPSILON for all tuples")
        
        result = extend_op.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        assert len(result) == 2
        assert result[0]["missing_ref"] == EPSILON
        assert result[1]["missing_ref"] == EPSILON
        
        debug_logger("Validation", 
                     "✓ EPSILON correctly assigned for undefined references")

    def test_extend_fluent_interface(self, simple_source_operator, debug_logger):
        """
        Test fluent interface for chaining extensions.
        
        Validates the convenience method for creating extension chains.
        """
        debug_logger("Test: Fluent Interface for Extensions", 
                     "Objective: Use extend() method for chaining")
        
        # Create initial extend operator
        extend_op = ExtendOperator(
            parent_operator=simple_source_operator,
            new_attribute="type",
            expression=Constant("Person")
        )
        
        # Use fluent interface to add another extension
        extended = extend_op.extend(
            var_name="category",
            expression=Constant("Staff")
        )
        
        debug_logger("Configuration", 
                     f"Using fluent interface:\n"
                     f"  extend_op.extend('category', Constant('Staff'))")
        
        result = extended.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        assert len(result) == 2
        assert result[0]["type"] == "Person"
        assert result[0]["category"] == "Staff"
        
        debug_logger("Validation", 
                     "✓ Fluent interface successfully chains extensions")

    def test_extend_with_complex_expression(self, debug_logger):
        """
        Test Extend with nested function calls.
        
        Validates handling of complex expressions with multiple
        levels of function composition.
        """
        debug_logger("Test: Complex Nested Expression", 
                     "Objective: Convert concatenated string to typed literal")
        
        data = {"users": [{"first": "John", "last": "Doe"}]}
        source_op = JsonSourceOperator(
            source_data=data,
            iterator_query="$.users[*]",
            attribute_mappings={"first": "$.first", "last": "$.last"}
        )
        
        # Complex expression: to_literal(concat(first, " ", last), xsd:string)
        concat_expr = FunctionCall(
            function=concat,
            arguments=[
                Reference("first"),
                Constant(" "),
                Reference("last")
            ]
        )
        
        literal_expr = FunctionCall(
            function=to_literal,
            arguments=[
                concat_expr,
                Constant("http://www.w3.org/2001/XMLSchema#string")
            ]
        )
        
        extend_op = ExtendOperator(
            parent_operator=source_op,
            new_attribute="full_name",
            expression=literal_expr
        )
        
        debug_logger("Configuration", 
                     f"Expression: to_literal(concat(first, ' ', last), xsd:string)\n"
                     f"Nested function calls with 2 levels")
        
        result = extend_op.execute()
        
        debug_logger("Execution Result", 
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i+1}. {tuple}" for i, tuple in enumerate(result)))
        
        assert len(result) == 1
        assert isinstance(result[0]["full_name"], Literal)
        assert result[0]["full_name"].lexical_form == "John Doe"
        
        debug_logger("Validation", 
                     f"✓ Complex expression evaluated correctly:\n"
                     f"  Result: {result[0]['full_name']}")

