from typing import List

from pyhartig.algebra.Tuple import MappingTuple
from pyhartig.operators.Operator import Operator


class UnionOperator(Operator):
    """
    Implements the Union operator.
    Merges the results of multiple operators into a single relation.
    """

    def __init__(self, operators: list[Operator]):
        """
        Initializes the Union operator.
        :param operators: A list of operators whose results will be merged.
        :return: None
        """
        super().__init__()
        self.operators = operators

    def execute(self) -> List[MappingTuple]:
        """
        Executes all child operators and merges their results.
        Union(r1, r2, ..., rn) = new MpaaingRelation (A_1, I_union)
        I_union = I_1 U I_2 U ... U I_n
        :return:
        """
        merged_results = []
        for op in self.operators:
            merged_results.extend(op.execute())
        return merged_results