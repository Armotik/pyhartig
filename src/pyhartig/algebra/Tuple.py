from typing import Dict, Union


class _Epsilon:
    """
    Means ‘Processing error’ or ‘Undefined value’
    """

    def __repr__(self):
        """
        String representation of the Epsilon object
        :return: String "ε"
        """
        return "ε"

    def __eq__(self, other):
        """
        Equality check for Epsilon objects
        :param other: Object to compare with
        :return: True if other is an instance of _Epsilon, False otherwise
        """
        return isinstance(other, _Epsilon)


EPSILON = _Epsilon()  # Singleton instance of Epsilon

# Definition of AlgebraicValue type
# For now, Base Python type + EPSILON
AlgebraicValue = Union[str, int, float, bool, None, _Epsilon]


class MappingTuple(dict):
    """
    Represents a data row (t) in a Mapping Relation.
    Partial function t: A -> T U {ε}

    Inherits from ‘dict’ to maintain compatibility with existing code, but adds semantics.
    """

    def __init__(self, data: Dict[str, AlgebraicValue] = None, **kwargs):
        """
        Initialize the MappingTuple with optional data.
        :param data: Dictionary of attribute-value pairs
        :param kwargs: Additional attribute-value pairs
        """
        if data is None:
            data = {}

        data.update(kwargs)
        super().__init__(data)

    def __setitem__(self, key: str, value: AlgebraicValue):
        """
        Overload to ensure that keys are strings
        :param key: Attribute name
        :param value: Attribute value
        :return: None
        """
        if not isinstance(key, str):
            raise TypeError(f"The attribute (key) of a MappingTuple must be a string, received: {type(key)}")
        super().__setitem__(key, value)

    def __repr__(self):
        """
        String representation of the MappingTuple (for debugging)
        :return: String representation of the underlying dictionary
        """
        items_str = ", ".join(f"{k}={repr(v)}" for k, v in self.items())
        return f"Tuple({items_str})"

    def merge(self, other: 'MappingTuple') -> 'MappingTuple':
        """
        Operation t U t
        Merges two compatible tuples
        :param other: The other MappingTuple to merge with
        :return: A new MappingTuple resulting from the merge
        """
        # Check compatibility
        for key in self:
            if key in other and self[key] != other[key]:
                raise ValueError(
                    f"Tuples are not compatible for merging: conflict on attribute '{key}' : {self[key]} != {other[key]}")

        # Merge tuples
        new_data = self.copy()
        new_data.update(other)
        return MappingTuple(new_data)
