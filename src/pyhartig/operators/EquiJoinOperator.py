from typing import Dict, Any, List, Tuple as TypingTuple

from pyhartig.algebra.Tuple import MappingTuple
from pyhartig.operators.Operator import Operator


class EquiJoinOperator(Operator):
    """
    EqJoin^J(r₁, r₂) : Operator × Operator → Operator

    Combines two mapping relations r₁ = (A₁, I₁) and r₂ = (A₂, I₂) based on
    a set of join conditions J ⊆ A₁ × A₂.

    Preconditions:
    - A₁ ∩ A₂ = ∅ (attribute sets must be disjoint)
    - J is a set of pairs (a₁, a₂) where a₁ ∈ A₁ and a₂ ∈ A₂

    Result: New mapping relation (A, I) where:
    - A = A₁ ∪ A₂ (union of all attributes)
    - I = { t₁ ∪ t₂ | t₁ ∈ I₁, t₂ ∈ I₂, ∀(a₁, a₂) ∈ J : t₁(a₁) = t₂(a₂) }

    Use case: Particularly relevant for referencing object maps in RML translation.
    """

    def __init__(self, r_1: Operator, r_2: Operator, A: List[str], B: List[str]):
        """
        Initializes the EquiJoin operator.

        :param r_1: The left child operator providing mapping relation r₁ = (A₁, I₁)
        :param r_2: The right child operator providing mapping relation r₂ = (A₂, I₂)
        :param A: List of attribute names from A₁ to join on (left side of J pairs)
        :param B: List of attribute names from A₂ to join on (right side of J pairs)
        :raises ValueError: If A and B have different lengths
        :return: None
        """
        super().__init__()

        if len(A) != len(B):
            raise ValueError(
                f"EquiJoinOperator: Join attribute lists must have equal length. "
                f"Got {len(A)} left attributes and {len(B)} right attributes."
            )

        self.left_operator = r_1
        self.right_operator = r_2
        self.left_attributes = A
        self.right_attributes = B
        # J = { (a₁, a₂) | a₁ ∈ A, a₂ ∈ B } - the join condition pairs
        self.join_conditions: List[TypingTuple[str, str]] = list(zip(A, B))

    def execute(self) -> List[MappingTuple]:
        """
        Executes the Equi-Join logic.

        I = { t₁ ∪ t₂ | t₁ ∈ I₁, t₂ ∈ I₂, ∀(a₁, a₂) ∈ J : t₁(a₁) = t₂(a₂) }

        For each pair of tuples (t₁, t₂) from the two relations, if all join
        conditions are satisfied, the tuples are merged into a single result tuple.

        :return: A list of MappingTuples resulting from the equi-join.
        :raises ValueError: If the attribute sets of the two relations are not disjoint.
        """
        # Execute child operators to get I₁ and I₂
        left_tuples = self.left_operator.execute()
        right_tuples = self.right_operator.execute()

        # Handle empty relations
        if not left_tuples or not right_tuples:
            return []

        # Verify disjoint attribute sets: A₁ ∩ A₂ = ∅
        # Use first tuple from each side to determine attribute sets
        if left_tuples and right_tuples:
            left_attrs = set(left_tuples[0].keys())
            right_attrs = set(right_tuples[0].keys())
            common_attrs = left_attrs & right_attrs

            if common_attrs:
                raise ValueError(
                    f"EquiJoinOperator: Attribute sets must be disjoint (A₁ ∩ A₂ = ∅). "
                    f"Common attributes found: {common_attrs}"
                )

        result_tuples = []

        # Nested loop join: for each t₁ ∈ I₁, for each t₂ ∈ I₂
        for t1 in left_tuples:
            for t2 in right_tuples:
                # Check join condition: ∀(a₁, a₂) ∈ J : t₁(a₁) = t₂(a₂)
                if self._satisfies_join_condition(t1, t2):
                    # Merge tuples: t₁ ∪ t₂
                    merged_tuple = t1.merge(t2)
                    result_tuples.append(merged_tuple)

        return result_tuples

    def _satisfies_join_condition(self, t1: MappingTuple, t2: MappingTuple) -> bool:
        """
        Checks if a pair of tuples satisfies all join conditions.

        ∀(a₁, a₂) ∈ J : t₁(a₁) = t₂(a₂)

        :param t1: Tuple from the left relation (t₁ ∈ I₁)
        :param t2: Tuple from the right relation (t₂ ∈ I₂)
        :return: True if all join conditions are satisfied, False otherwise
        """
        for a1, a2 in self.join_conditions:
            # Get values, treating missing attributes as None
            val1 = t1.get(a1)
            val2 = t2.get(a2)

            # Values must be equal for join condition to be satisfied
            if val1 != val2:
                return False

        return True

    def explain(self, indent: int = 0, prefix: str = "") -> str:
        """
        Generate a human-readable explanation of the EquiJoin operator.

        :param indent: Current indentation level
        :param prefix: Prefix for tree structure (e.g., "├─", "└─")
        :return: String representation of the operator tree
        """
        indent_str = "  " * indent

        # Format join conditions as "a₁ = a₂"
        conditions_str = ", ".join(
            f"{a1} = {a2}" for a1, a2 in self.join_conditions
        )

        lines = [
            f"{indent_str}{prefix}EquiJoin(",
            f"{indent_str}  conditions: [{conditions_str}]",
            f"{indent_str}  left:",
        ]

        # Left child operator
        left_explanation = self.left_operator.explain(indent + 2, "├─ ")
        lines.append(left_explanation)

        lines.append(f"{indent_str}  right:")

        # Right child operator
        right_explanation = self.right_operator.explain(indent + 2, "└─ ")
        lines.append(right_explanation)

        lines.append(f"{indent_str})")

        return "\n".join(lines)

    def explain_json(self) -> Dict[str, Any]:
        """
        Generate a JSON-serializable explanation of the EquiJoin operator.

        :return: Dictionary representing the operator tree structure
        """
        return {
            "type": "EquiJoin",
            "parameters": {
                "join_conditions": [
                    {"left": a1, "right": a2}
                    for a1, a2 in self.join_conditions
                ],
                "left_attributes": self.left_attributes,
                "right_attributes": self.right_attributes
            },
            "left": self.left_operator.explain_json(),
            "right": self.right_operator.explain_json()
        }

