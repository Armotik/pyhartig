from typing import List, Dict, Any

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

    def explain(self, indent: int = 0, prefix: str = "") -> str:
        """
        Generate a human-readable explanation of the Union operator.
        :param indent: Current indentation level
        :param prefix: Prefix for tree structure (e.g., "├─", "└─")
        :return: String representation of the operator tree
        """
        indent_str = "  " * indent
        lines = [f"{indent_str}{prefix}Union(", f"{indent_str}  operators: {len(self.operators)}"]

        for i, op in enumerate(self.operators):
            is_last = (i == len(self.operators) - 1)
            child_prefix = "└─ " if is_last else "├─ "
            lines.append(f"{indent_str}  {child_prefix}[{i}]:")
            lines.append(op.explain(indent + 2, ""))

        lines.append(f"{indent_str})")

        return "\n".join(lines)

    def explain_json(self) -> Dict[str, Any]:
        """
        Generate a JSON-serializable explanation of the Union operator.
        :return: Dictionary representing the operator tree structure
        """
        return {
            "type": "Union",
            "parameters": {
                "operator_count": len(self.operators)
            },
            "children": [op.explain_json() for op in self.operators]
        }