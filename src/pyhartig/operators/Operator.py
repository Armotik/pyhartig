from abc import ABC, abstractmethod
from typing import List, Any, TYPE_CHECKING, Dict
from pyhartig.algebra.Tuple import MappingTuple

if TYPE_CHECKING:
    from pyhartig.operators.ExtendOperator import ExtendOperator


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

    @abstractmethod
    def explain(self, indent: int = 0, prefix: str = "") -> str:
        """
        Generate a human-readable explanation of the operator tree.

        :param indent: Current indentation level
        :param prefix: Prefix for tree structure (e.g., "├─", "└─")
        :return: String representation of the operator tree
        """
        pass

    @abstractmethod
    def explain_json(self) -> Dict[str, Any]:
        """
        Generate a JSON-serializable explanation of the operator tree.

        :return: Dictionary representing the operator tree structure
        """
        pass

    def extend(self, var_name: str, expression: Any) -> 'ExtendOperator':
        """
        Fluent interface helper to chain ExtendOperators.

        :usage:
            op.extend("new_col", Constant("val")).extend(...)

        :param var_name: Name of the variable to extend
        :param expression: Expression to compute the new value
        :return: ExtendOperator instance
        """
        from pyhartig.operators.ExtendOperator import ExtendOperator

        return ExtendOperator(
            parent_operator=self,
            new_attribute=var_name,
            expression=expression
        )

