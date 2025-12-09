from typing import Any, List, Dict
from jsonpath_ng import parse

from pyhartig.operators.SourceOperator import SourceOperator


class JsonSourceOperator(SourceOperator):

    def _apply_iterator(self, data: Any, query: str) -> List[Any]:
        """
        Apply the iterator query on the data source (function eval(D, q))
        :param data: JSON data source
        :param query: Iterator query
        :return: List of context
        """
        jsonpath_expr = parse(query)
        return [match.value for match in jsonpath_expr.find(data)]

    def _apply_extraction(self, context: Any, query: str) -> List[Any]:
        """
        Apply the extraction query on a context object (function eval'(D, d, q'))
        :param context: Context object
        :param query: Extraction query
        :return: List of extracted values for the attribute
        """
        jsonpath_expr = parse(query)
        matches = jsonpath_expr.find(context)

        # If no matches found, return empty list
        if not matches:
            return []

        # Flatten the results
        results = []
        for match in matches:

            # If the match value is a list, extend the results; otherwise, append the single value
            if isinstance(match.value, list):
                results.extend(match.value)
            else:
                results.append(match.value)
        return results

    def explain_json(self) -> Dict[str, Any]:
        """
        Generate a JSON-serializable explanation of the JsonSource operator
        :return: Dictionary representing the operator tree structure
        """
        base = super().explain_json()
        base["parameters"]["source_type"] = "JSON"
        base["parameters"]["jsonpath_iterator"] = self.iterator_query
        return base
