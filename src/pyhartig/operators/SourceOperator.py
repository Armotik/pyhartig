from abc import ABC, abstractmethod
from typing import Any, Dict, List
from itertools import product

class SourceOperator(ABC):
    """
    Abstract class defining the algebraic logic of the Source operator
    """

    def __init__(self, source_data: Any, iterator_query: str, attribute_mappings: Dict[str, str]):
        """
        Constructor
        :param source_data: Data source
        :param iterator_query: Iterative query that selects a set of context objects from s
        :param attribute_mappings: Mapping that associates an attribute a with an extraction query q'
        """
        self.source_data = source_data
        self.iterator_query = iterator_query
        self.attribute_mappings = attribute_mappings

    @abstractmethod
    def _apply_iterator(self, data: Any, query: str) -> List[Any]:
        """
        Apply the iterator query on the data source (function eval(D, q))
        :param data: Data source
        :param query: Iterator query
        :return: List of context
        """
        pass

    @abstractmethod
    def _apply_extraction(self, context: Any, query: str) -> List[Any]:
        """
        Apply the extraction query on a context object (function eval'(D, d, q'))
        :param context: Context object
        :param query: Extraction query
        :return: List of extracted values for the attribute
        """
        pass

    def execute(self) -> list[Any]:
        """
        Execute the Source operator logic
        :return: List of rows resulting from the Source operator
        """

        result = []

        # Apply the iterator to get context objects
        contexts = self._apply_iterator(self.source_data, self.iterator_query)

        # For each context, apply the extraction queries for each attribute
        for context in contexts:

            extracted_values = {}

            # Extract values for each attribute
            for attr_name, extraction_query in self.attribute_mappings.items():
                values = self._apply_extraction(context, extraction_query)
                extracted_values[attr_name] = values

            keys = list(extracted_values.keys())
            values_lists = list(extracted_values.values())

            # Generate all combinations of extracted values
            for combination in product(*values_lists):
                row = dict(zip(keys, combination))
                result.append(row)

        return result