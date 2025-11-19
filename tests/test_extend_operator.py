import pytest
from typing import List, Any
from pyhartig.algebra.Tuple import MappingTuple
from pyhartig.algebra.Terms import IRI
from pyhartig.operators.Operator import Operator
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.functions.builtins import to_iri, concat


# --- MOCK OPERATOR ---
# Instead of relying on JsonSourceOperator (and filesystem),
# we create a simple Mock operator for pure unit testing.

class MockSourceOperator(Operator):
    def __init__(self, data: List[MappingTuple]):
        self.data = data

    def execute(self) -> List[MappingTuple]:
        print("[DEBUG] MockSourceOperator.execute - data:", self.data)
        return self.data


# --- TESTS ---


def test_extend_simple_constant():
    """Test creating a new attribute with a constant value."""
    # Input: One row with an ID
    input_data = [MappingTuple({"id": "101"})]
    print("[DEBUG] test_extend_simple_constant - input_data:", input_data)
    source = MockSourceOperator(input_data)

    # Operation: Extend with constant "http://base.org/"
    extend_op = ExtendOperator(
        parent_operator=source,
        new_attribute="base_url",
        expression=Constant("http://base.org/")
    )
    print("[DEBUG] test_extend_simple_constant - extend_op:", extend_op)

    results = extend_op.execute()
    print("[DEBUG] test_extend_simple_constant - results:", results)

    assert len(results) == 1
    assert results[0]["id"] == "101"
    assert results[0]["base_url"] == "http://base.org/"


def test_extend_reference_copy():
    """Test creating a new attribute that is just a copy of another."""
    input_data = [MappingTuple({"id": "101", "name": "Alice"})]
    print("[DEBUG] test_extend_reference_copy - input_data:", input_data)
    source = MockSourceOperator(input_data)

    extend_op = ExtendOperator(
        parent_operator=source,
        new_attribute="user_id",
        expression=Reference("id")
    )
    print("[DEBUG] test_extend_reference_copy - extend_op:", extend_op)

    results = extend_op.execute()
    print("[DEBUG] test_extend_reference_copy - results:", results)

    assert results[0]["user_id"] == "101"


def test_extend_complex_expression():
    """Test the real use case: Constructing an IRI from an ID."""
    input_data = [MappingTuple({"id": "123"})]
    print("[DEBUG] test_extend_complex_expression - input_data:", input_data)
    source = MockSourceOperator(input_data)

    # 1. Build the expression tree
    concat_expr = FunctionCall(
        concat,
        [Constant("http://example.org/user/"), Reference("id")]
    )
    print("[DEBUG] test_extend_complex_expression - concat_expr:", concat_expr)

    final_expr = FunctionCall(to_iri, [concat_expr])
    print("[DEBUG] test_extend_complex_expression - final_expr:", final_expr)

    extend_op = ExtendOperator(
        parent_operator=source,
        new_attribute="subject_iri",
        expression=final_expr
    )
    print("[DEBUG] test_extend_complex_expression - extend_op:", extend_op)

    results = extend_op.execute()
    print("[DEBUG] test_extend_complex_expression - results:", results)

    result_row = results[0]
    generated_iri = result_row["subject_iri"]
    print("[DEBUG] test_extend_complex_expression - generated_iri:", generated_iri)

    assert isinstance(generated_iri, IRI)
    assert generated_iri.value == "http://example.org/user/123"


def test_chaining_extends():
    """Test chaining multiple Extend operators."""
    input_data = [MappingTuple({"id": "5"})]
    print("[DEBUG] test_chaining_extends - input_data:", input_data)
    source = MockSourceOperator(input_data)

    op1 = ExtendOperator(source, "prefix", Constant("User_"))
    print("[DEBUG] test_chaining_extends - op1:", op1)

    concat_expr = FunctionCall(concat, [Reference("prefix"), Reference("id")])
    print("[DEBUG] test_chaining_extends - concat_expr:", concat_expr)

    op2 = ExtendOperator(op1, "full_name", concat_expr)
    print("[DEBUG] test_chaining_extends - op2:", op2)

    results = op2.execute()
    print("[DEBUG] test_chaining_extends - results:", results)

    assert results[0]["id"] == "5"
    assert results[0]["prefix"] == "User_"
    assert results[0]["full_name"].lexical_form == "User_5"
