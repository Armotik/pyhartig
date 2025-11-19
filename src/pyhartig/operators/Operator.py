from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pyhartig.algebra.Tuple import MappingTuple


class Operator(ABC):
    """
    Abstract base class for all operators in the system.
    """

    @abstractmethod
    def execute(self) -> List[MappingTuple]:
        """
        Execute the operator and return a list of MappingTuple results.
        :return: List of MappingTuple
        """
        pass
