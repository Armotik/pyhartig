"""
Test Suite for Operator Composition

This module validates the integration and composition of multiple
operators, specifically focusing on Source and Extend operator fusion.
Tests demonstrate how operators combine to form complex data pipelines.
"""

import pytest
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.functions.builtins import to_iri, to_literal, concat
from pyhartig.algebra.Terms import IRI, Literal


class TestOperatorComposition:
    """Test suite for operator composition and fusion."""

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
    def team_data(self):
        """
        Fixture providing team structure data.
        
        Returns:
            dict: JSON structure with team information
        """
        return {
            "project": "MCP-SPARQLLM",
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

    def test_source_extend_basic_fusion(self, team_data, debug_logger):
        """
        Test basic fusion of Source and Extend operators.
        
        Validates that Extend correctly processes Source output,
        adding computed attributes to each tuple.
        """
        debug_logger("Test: Basic Source-Extend Fusion",
                     "Objective: Extract team data and add RDF type")

        # Create source operator
        source_op = JsonSourceOperator(
            source_data=team_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "person_id": "$.id",
                "person_name": "$.name"
            }
        )

        # Extend with RDF type
        extend_op = ExtendOperator(
            parent_operator=source_op,
            new_attribute="rdf_type",
            expression=Constant(IRI("http://xmlns.com/foaf/0.1/Person"))
        )

        debug_logger("Pipeline Configuration",
                     f"Stage 1 - Source:\n"
                     f"  Iterator: $.team[*]\n"
                     f"  Mappings: person_id, person_name\n\n"
                     f"Stage 2 - Extend:\n"
                     f"  New attribute: rdf_type\n"
                     f"  Expression: Constant(IRI(foaf:Person))")

        result = extend_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        assert len(result) == 2
        assert all("rdf_type" in tuple for tuple in result)
        assert all(isinstance(tuple["rdf_type"], IRI) for tuple in result)
        assert result[0]["person_name"] == "Alice"
        assert result[1]["person_name"] == "Bob"

        debug_logger("Validation",
                     "✓ Source-Extend fusion successful\n"
                     "✓ All tuples contain computed RDF type")

    def test_source_multiple_extends(self, team_data, debug_logger):
        """
        Test Source operator with multiple sequential Extends.
        
        Validates complex pipelines where multiple computed attributes
        are added sequentially, potentially depending on each other.
        """
        debug_logger("Test: Source with Multiple Sequential Extends",
                     "Objective: Build complex RDF representation")

        # Source operator
        source_op = JsonSourceOperator(
            source_data=team_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "id": "$.id",
                "name": "$.name"
            }
        )

        # First extension: generate subject IRI
        subject_expr = FunctionCall(
            function=to_iri,
            arguments=[
                Reference("id"),
                Constant("http://example.org/person/")
            ]
        )
        extend_subject = ExtendOperator(
            parent_operator=source_op,
            new_attribute="subject",
            expression=subject_expr
        )

        # Second extension: add RDF type
        extend_type = ExtendOperator(
            parent_operator=extend_subject,
            new_attribute="type",
            expression=Constant(IRI("http://xmlns.com/foaf/0.1/Person"))
        )

        # Third extension: convert name to literal
        name_literal_expr = FunctionCall(
            function=to_literal,
            arguments=[
                Reference("name"),
                Constant("http://www.w3.org/2001/XMLSchema#string")
            ]
        )
        extend_name = ExtendOperator(
            parent_operator=extend_type,
            new_attribute="name_literal",
            expression=name_literal_expr
        )

        debug_logger("Pipeline Configuration",
                     f"Stage 1 - Source: Extract id and name\n"
                     f"Stage 2 - Extend: subject = to_iri(id, base)\n"
                     f"Stage 3 - Extend: type = foaf:Person\n"
                     f"Stage 4 - Extend: name_literal = to_literal(name, xsd:string)")

        result = extend_name.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Sample tuple:\n{result[0] if result else 'No results'}")

        assert len(result) == 2

        # Verify first tuple structure
        tuple1 = result[0]
        assert "subject" in tuple1
        assert "type" in tuple1
        assert "name_literal" in tuple1
        assert isinstance(tuple1["subject"], IRI)
        assert isinstance(tuple1["type"], IRI)
        assert isinstance(tuple1["name_literal"], Literal)
        assert tuple1["subject"].value == "http://example.org/person/1"
        assert tuple1["name_literal"].lexical_form == "Alice"

        debug_logger("Validation",
                     f"✓ Multi-stage pipeline successful\n"
                     f"✓ Subject IRI: {tuple1['subject']}\n"
                     f"✓ Type IRI: {tuple1['type']}\n"
                     f"✓ Name literal: {tuple1['name_literal']}")

    def test_source_cartesian_with_extend(self, team_data, debug_logger):
        """
        Test Extend operator on Source with Cartesian product.
        
        Validates that extensions are correctly applied to each tuple
        generated by Cartesian product in the Source operator.
        """
        debug_logger("Test: Extend on Cartesian Product",
                     "Objective: Apply extensions to expanded tuple set")

        # Source with array extraction (generates Cartesian product)
        source_op = JsonSourceOperator(
            source_data=team_data,
            iterator_query="$.team[*]",
            attribute_mappings={
                "name": "$.name",
                "role": "$.roles[*]"
            }
        )

        # Extend with role-based category
        category_expr = FunctionCall(
            function=concat,
            arguments=[
                Constant("Role: "),
                Reference("role")
            ]
        )
        extend_op = ExtendOperator(
            parent_operator=source_op,
            new_attribute="role_label",
            expression=category_expr
        )

        debug_logger("Pipeline Configuration",
                     f"Stage 1 - Source:\n"
                     f"  Generates Cartesian product for roles\n"
                     f"  Alice: 2 roles, Bob: 1 role → 3 tuples\n\n"
                     f"Stage 2 - Extend:\n"
                     f"  role_label = concat('Role: ', role)")

        result = extend_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuples:\n" + "\n".join(f"  {i + 1}. {tuple}" for i, tuple in enumerate(result)))

        # Alice has 2 roles, Bob has 1 role → 3 tuples
        assert len(result) == 3
        assert all("role_label" in tuple for tuple in result)

        alice_tuples = [t for t in result if t["name"] == "Alice"]
        assert len(alice_tuples) == 2
        assert all(t["role_label"].lexical_form.startswith("Role: ") for t in alice_tuples)

        debug_logger("Validation",
                     f"✓ Extend applied to all Cartesian product tuples\n"
                     f"✓ Alice tuples: {len(alice_tuples)}\n"
                     f"✓ Sample role_label: {result[0]['role_label']}")

    def test_complex_fusion_with_dependencies(self, debug_logger):
        """
        Test operator fusion with dependent computed attributes.
        
        Validates that later extensions can reference attributes
        computed by earlier extensions in the pipeline.
        """
        debug_logger("Test: Complex Fusion with Dependencies",
                     "Objective: Computed attributes referencing earlier computations")

        data = {
            "people": [
                {"first_name": "John", "last_name": "Doe", "age": 30}
            ]
        }

        # Source
        source_op = JsonSourceOperator(
            source_data=data,
            iterator_query="$.people[*]",
            attribute_mappings={
                "first": "$.first_name",
                "last": "$.last_name",
                "age": "$.age"
            }
        )

        # Extension 1: Compute full name
        full_name_expr = FunctionCall(
            function=concat,
            arguments=[
                Reference("first"),
                Constant(" "),
                Reference("last")
            ]
        )
        extend_name = ExtendOperator(
            parent_operator=source_op,
            new_attribute="full_name",
            expression=full_name_expr
        )

        # Extension 2: Create label using computed full_name
        label_expr = FunctionCall(
            function=concat,
            arguments=[
                Reference("full_name"),  # References computed attribute!
                Constant(" (age: "),
                Reference("age"),
                Constant(")")
            ]
        )
        extend_label = ExtendOperator(
            parent_operator=extend_name,
            new_attribute="description",
            expression=label_expr
        )

        debug_logger("Pipeline Configuration",
                     f"Stage 1 - Source: Extract first, last, age\n"
                     f"Stage 2 - Extend: full_name = concat(first, ' ', last)\n"
                     f"Stage 3 - Extend: description = concat(full_name, ' (age: ', age, ')')\n"
                     f"Note: Stage 3 references computed attribute from Stage 2")

        result = extend_label.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Tuple: {result[0] if result else 'No results'}")

        assert len(result) == 1
        assert result[0]["full_name"].lexical_form == "John Doe"

        debug_logger("Validation",
                     f"✓ Dependent computations successful\n"
                     f"✓ full_name: {result[0]['full_name']}\n"
                     f"✓ description computed using full_name")

    def test_empty_source_extend_propagation(self, debug_logger):
        """
        Test Extend behavior when Source produces no tuples.
        
        Validates that empty result sets propagate correctly
        through the pipeline.
        """
        debug_logger("Test: Empty Source Propagation",
                     "Objective: Validate empty result set handling")

        data = {"items": []}

        source_op = JsonSourceOperator(
            source_data=data,
            iterator_query="$.items[*]",
            attribute_mappings={"value": "$.val"}
        )

        extend_op = ExtendOperator(
            parent_operator=source_op,
            new_attribute="computed",
            expression=Constant("value")
        )

        debug_logger("Configuration",
                     "Source with empty iterator → Extend should receive no tuples")

        result = extend_op.execute()

        debug_logger("Execution Result",
                     f"Number of tuples: {len(result)}\n"
                     f"Expected: 0 (empty propagates through pipeline)")

        assert len(result) == 0

        debug_logger("Validation",
                     "✓ Empty result set correctly propagated")

    def test_parallel_extend_branches(self, team_data, debug_logger):
        """
        Test multiple independent Extend branches from same Source.
        
        Validates that the same Source can feed multiple independent
        extension pipelines.
        """
        debug_logger("Test: Parallel Extension Branches",
                     "Objective: Multiple independent extensions from one source")

        source_op = JsonSourceOperator(
            source_data=team_data,
            iterator_query="$.team[*]",
            attribute_mappings={"id": "$.id", "name": "$.name"}
        )

        # Branch 1: Add subject IRI
        branch1 = ExtendOperator(
            parent_operator=source_op,
            new_attribute="subject",
            expression=FunctionCall(
                function=to_iri,
                arguments=[Reference("id"), Constant("http://example.org/person/")]
            )
        )

        # Branch 2: Add label literal (independent of branch 1)
        branch2 = ExtendOperator(
            parent_operator=source_op,
            new_attribute="label",
            expression=FunctionCall(
                function=to_literal,
                arguments=[Reference("name"), Constant("http://www.w3.org/2001/XMLSchema#string")]
            )
        )

        debug_logger("Pipeline Configuration",
                     f"Single Source with two independent branches:\n"
                     f"  Branch 1: Add 'subject' IRI\n"
                     f"  Branch 2: Add 'label' literal")

        result1 = branch1.execute()
        result2 = branch2.execute()

        debug_logger("Execution Results",
                     f"Branch 1 tuples: {len(result1)}\n"
                     f"  Sample: {result1[0] if result1 else 'None'}\n\n"
                     f"Branch 2 tuples: {len(result2)}\n"
                     f"  Sample: {result2[0] if result2 else 'None'}")

        assert len(result1) == 2
        assert len(result2) == 2
        assert "subject" in result1[0]
        assert "subject" not in result2[0]
        assert "label" in result2[0]
        assert "label" not in result1[0]

        debug_logger("Validation",
                     "✓ Parallel branches execute independently\n"
                     "✓ Each branch has distinct attributes")
