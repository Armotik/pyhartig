import pytest
from pyhartig.algebra.Tuple import MappingTuple, EPSILON
from pyhartig.algebra.Terms import IRI
from pyhartig.expressions.Constant import Constant
from pyhartig.expressions.Reference import Reference
from pyhartig.expressions.FunctionCall import FunctionCall
from pyhartig.functions.builtins import to_iri, concat


@pytest.fixture
def sample_tuple():
    """Sample tuple representing a data row."""
    return MappingTuple({"id": "123", "name": "Alice"})


def test_constant_expression(sample_tuple):
    """A Constant should always return its value."""
    const = Constant("http://example.org/")
    assert const.evaluate(sample_tuple) == "http://example.org/"


def test_reference_expression_success(sample_tuple):
    """A Reference should return the attribute value."""
    ref = Reference("name")
    assert ref.evaluate(sample_tuple) == "Alice"


def test_reference_expression_missing(sample_tuple):
    """A Reference to a missing attribute should return EPSILON."""
    ref = Reference("age")  # Does not exist
    assert ref.evaluate(sample_tuple) == EPSILON


def test_function_call_recursive(sample_tuple):
    """
    Complex recursive test.
    Expression: toIRI(concat("http://example.org/user/", Reference("id")))
    """
    # 1. Build Expression Tree
    # concat("http://example.org/user/", ?id)
    concat_expr = FunctionCall(
        concat,
        [
            Constant("http://example.org/user/"),
            Reference("id")  # Value is "123"
        ]
    )

    # toIRI(...)
    final_expr = FunctionCall(
        to_iri,
        [concat_expr]
    )

    # 2. Evaluate
    result = final_expr.evaluate(sample_tuple)

    # 3. Verify
    assert isinstance(result, IRI)
    assert result.value == "http://example.org/user/123"


def test_function_call_propagation_error(sample_tuple):
    """If a sub-expression fails (Epsilon), the parent must return Epsilon."""
    expr = FunctionCall(
        concat,
        [Constant("Prefix"), Reference("Inexistant")]
    )
    assert expr.evaluate(sample_tuple) == EPSILON