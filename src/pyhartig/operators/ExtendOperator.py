from typing import List
from pyhartig.operators.Operator import Operator
from pyhartig.algebra.Tuple import MappingTuple
from pyhartig.expressions.Expression import Expression


class ExtendOperator(Operator):
    """
    Implements the Extend operator.
    Extends a mapping relation with a new attribute derived from an expression phi.
    """

    def __init__(self, parent_operator: Operator, new_attribute: str, expression: Expression):
        """
        Initializes the Extend operator.
        :param parent_operator: The operator that provides the input relation (r)
        :param new_attribute: The name of the new attribute to add (a)
        :param expression: The expression to evaluate (phi)
        :return: None
        """
        super().__init__()
        self.parent_operator = parent_operator
        self.new_attribute = new_attribute
        self.expression = expression

    def execute(self) -> List[MappingTuple]:
        """
        Executes the Extend logic.
        r' = { t U {a -> eval(phi, t)} | t in r }
        :return: A list of extended MappingTuples.
        """

        # Get input tuples from parent
        parent_rows = self.parent_operator.execute()

        new_rows = []
        for row in parent_rows:
            # Create a new tuple (copy) to avoid side effects on the parent data
            new_row = MappingTuple(row)

            # Calculate the new value using the Expression system
            computed_value = self.expression.evaluate(row)

            # Assign the new value to the new attribute
            new_row[self.new_attribute] = computed_value

            new_rows.append(new_row)

        return new_rows
