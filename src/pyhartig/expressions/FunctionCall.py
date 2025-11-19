from typing import Any, List, Callable
from pyhartig.expressions.Expression import Expression
from pyhartig.algebra.Tuple import MappingTuple, EPSILON

class FunctionCall(Expression):
    """
    Represents the application of an extension function f to subexpressions. (f(phi1, ..., phin))
    """

    def __init__(self, function: Callable, arguments: List[Expression]):
        """
        Initializes a FunctionCall expression.
        :param function: Python callable representing the function to be applied (e.g., built-in or user-defined).
        :param arguments: List of sub-expressions (Expression) that will provide the arguments
        """
        self.function = function
        self.arguments = arguments

    def evaluate(self, tuple_data: MappingTuple) -> Any:
        """
        Evaluates the function call against the provided tuple data.
        :param tuple_data: The tuple data to evaluate against.
        :return: The result of applying the function to the evaluated arguments, or EPSILON if any argument is EPSILON or an error occurs.
        """
        # Evaluate all arguments
        evaluated_args = [arg.evaluate(tuple_data) for arg in self.arguments]

        # If any argument evaluates to EPSILON, return EPSILON for the whole function call
        if any(arg == EPSILON for arg in evaluated_args):
            return EPSILON

        # Apply the function to the evaluated arguments
        try:
            return self.function(*evaluated_args)
        except Exception as e:
            # In case of any error during function application, return EPSILON
            return EPSILON

    def __repr__(self):
        """
        Returns a string representation of the FunctionCall expression.
        :return: A string representing the FunctionCall expression.
        """
        args_repr = ", ".join(repr(a) for a in self.arguments)
        func_name = getattr(self.function, "__name__", str(self.function))
        return f"{func_name}({args_repr})"