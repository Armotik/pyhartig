from typing import Union
import urllib.parse

from pyhartig.algebra.Tuple import EPSILON, _Epsilon, AlgebraicValue
from pyhartig.algebra.Terms import IRI, Literal

def _to_string(value: AlgebraicValue) -> Union[str, None]:
    """
    Convert a AlgebraicValue to its string representation if possible.
    :param value: Value to convert
    :return: String representation or None if conversion is not possible
    """
    # Check for primitive types
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)

    # Check for Algebraic Terms
    if isinstance(value, Literal):
        return value.lexical_form
    if isinstance(value, IRI):
        return value.value
    return None


def to_iri(value: AlgebraicValue, base: str = None) -> Union[IRI, _Epsilon]:
    """
    Convert a AlgebraicValue to an IRI, resolving against a base if provided.
    :param value: Value to convert
    :param base: Optional base IRI for resolution
    :return: IRI or EPSILON if conversion is not possible
    """
    # Handle EPSILON and None cases
    if value is None or value == EPSILON:
        return EPSILON

    lex = _to_string(value)

    # If lexical form is None, return EPSILON
    if lex is None:
        return EPSILON

    # Check if lexical form is already an IRI (simplified check)
    if ":" in lex:
        # Presume it's a valid IRI
        return IRI(lex)

    # Resolve against base if provided
    if base:
        resolved = urllib.parse.urljoin(base, lex)
        return IRI(resolved)

    # If no base is provided and lexical form is not a valid IRI, return EPSILON
    return EPSILON


def to_literal(value: AlgebraicValue, datatype: str) -> Union[Literal, _Epsilon]:
    """
    Convert an AlgebraicValue to a Literal with the specified datatype.
    :param value: Value to convert
    :param datatype: Datatype IRI for the Literal
    :return: Literal or EPSILON if conversion is not possible
    """
    # Handle EPSILON and None cases
    if value is None or value == EPSILON:
        return EPSILON

    lex = str(value)
    # Extract lexical form from RDF Terms
    if isinstance(value, Literal):
        lex = value.lexical_form
    # Handle BlankNode case (not convertible to Literal)
    elif isinstance(value, IRI):
        lex = value.value
    elif isinstance(value, (int, float, bool)):
        lex = str(value)

    return Literal(lex, datatype)


def concat(*args: AlgebraicValue) -> Union[Literal, _Epsilon]:
    """
    Concatenate multiple AlgebraicValues into a single string Literal.
    :param args: Values to concatenate
    :return: Literal with concatenated string or EPSILON if conversion is not possible
    """
    result_str = ""
    for val in args:
        s = _to_string(val)
        if s is None:
            # If any argument is invalid/Epsilon, propagate error
            return EPSILON
        result_str += s

    return Literal(result_str, "http://www.w3.org/2001/XMLSchema#string")