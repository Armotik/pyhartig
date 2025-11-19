from abc import ABC, abstractmethod
from typing import Any
from pyhartig.algebra.Tuple import MappingTuple

class Expression(ABC):
    """
    Represents an algebraic expression phi
    """

    @abstractmethod
    def evaluate(self, mapping: MappingTuple) -> Any:
        """
        Evaluate the expression against a given mapping tuple. (eval(phi, t))
        :param mapping: Mapping tuple to evaluate against
        :return: Result of the evaluation
        """
        pass