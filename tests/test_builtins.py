import pytest
from pyhartig.algebra.Tuple import EPSILON
from pyhartig.algebra.Terms import IRI, Literal
from pyhartig.functions.builtins import to_iri, to_literal, concat

def test_to_iri_valid():
    """Verifies simple conversion from string to IRI."""
    result = to_iri("http://example.org/Alice")
    assert isinstance(result, IRI)
    assert result.value == "http://example.org/Alice"

def test_to_iri_with_base():
    """Verifies relative resolution with a base"""
    result = to_iri("Alice", base="http://example.org/")
    assert isinstance(result, IRI)
    assert result.value == "http://example.org/Alice"

def test_to_iri_error():
    """Verifies toIRI returns EPSILON if input is invalid."""
    assert to_iri(None) == EPSILON
    assert to_iri(EPSILON) == EPSILON

def test_to_literal():
    """Verifies creation of typed literals."""
    res_int = to_literal(42, "http://www.w3.org/2001/XMLSchema#integer")
    assert isinstance(res_int, Literal)
    assert res_int.lexical_form == "42"
    assert res_int.datatype_iri == "http://www.w3.org/2001/XMLSchema#integer"

def test_concat_success():
    """Verifies concatenation of two strings."""
    res = concat("Hello ", "World")
    assert isinstance(res, Literal)
    assert res.lexical_form == "Hello World"
    assert res.datatype_iri == "http://www.w3.org/2001/XMLSchema#string"

def test_concat_error():
    """Verifies error propagation (Epsilon)."""
    assert concat("Hello", EPSILON) == EPSILON
    assert concat(None, "World") == EPSILON