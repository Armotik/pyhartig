from typing import Any, Union
import urllib.parse

from pyhartig.algebra.Tuple import EPSILON, _Epsilon
from pyhartig.algebra.Terms import IRI, Literal, BlankNode, RdfTerm

# Aliases for input types (native Python or RDF Term)
Value = Union[str, int, float, bool, RdfTerm, None, _Epsilon]


def _to_string(value: Value) -> Union[str, None]:
    """
    Convert a Value to its string representation if possible.
    :param value: Value to convert
    :return: String representation or None if conversion is not possible
    """
    # Check for native string
    if isinstance(value, str):
        return value

    # Check for RDF Literal with xsd:string datatype
    if isinstance(value, Literal) and value.datatype_iri == "http://www.w3.org/2001/XMLSchema#string":
        return value.lexical_form
    return None


def to_iri(value: Value, base: str = None) -> Union[IRI, _Epsilon]:
    """
    Convert a Value to an IRI, resolving against a base if provided.
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


def to_literal(value: Value, datatype: str) -> Union[Literal, _Epsilon]:
    """
    Convert a Value to a Literal with the specified datatype.
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

    return Literal(lex, datatype)


def concat(val1: Value, val2: Value) -> Union[Literal, _Epsilon]:
    """
    Concatenate two Values as strings.
    :param val1: first Value
    :param val2: second Value
    :return: Literal with concatenated string or EPSILON if conversion is not possible
    """
    str1 = _to_string(val1)
    str2 = _to_string(val2)

    # If both can be converted to strings, concatenate them
    if str1 is not None and str2 is not None:
        return Literal(str1 + str2, "http://www.w3.org/2001/XMLSchema#string")

    return EPSILON