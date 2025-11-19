from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class IRI:
    """
    Represents an Internationalized Resource Identifier (IRI).
    Examples: <http://example.org/resource>, <urn:isbn:0451450523>
    """
    value: str

    def __repr__(self):
        """
        String representation of the IRI
        :return: String representation of the IRI
        """
        return f"<{self.value}>"

@dataclass(frozen=True)
class Literal:
    """
    Represents an RDF Literal
    Examples: "Hello World", "42"^^http://www.w3.org/2001/XMLSchema#integer
    """
    lexical_form: str
    datatype_iri: str = "http://www.w3.org/2001/XMLSchema#string"

    def __repr__(self):
        """
        String representation of the Literal
        :return: String representation of the Literal
        """
        if self.datatype_iri == "http://www.w3.org/2001/XMLSchema#string":
            return f'"{self.lexical_form}"'
        return f'"{self.lexical_form}"^^{self.datatype_iri}'

@dataclass(frozen=True)
class BlankNode:
    """
    Represents an RDF Blank Node
    Examples: _:b0, _:node1
    """
    identifier: str

    def __repr__(self):
        """
        String representation of the Blank Node
        :return: String representation of the Blank Node
        """
        return f"_:{self.identifier}"

RdfTerm = Union[IRI, Literal, BlankNode]