from pyhartig.expressions.Constant import Constant
from pyhartig.operators.ExtendOperator import ExtendOperator
from pyhartig.operators.UnionOperator import UnionOperator
from pyhartig.operators.sources.JsonSourceOperator import JsonSourceOperator


def test_simple_source_explain():
    source = JsonSourceOperator(
        source_data={"items": [{"id": 1}]},
        iterator_query="$.items[*]",
        attribute_mappings={"item_id": "$.id"}
    )

    explanation = source.explain()

    assert "Source(" in explanation
    assert "$.items[*]" in explanation
    assert "item_id" in explanation


def test_extend_explain():
    source = JsonSourceOperator(
        source_data={"items": [{"id": 1}]},
        iterator_query="$.items[*]",
        attribute_mappings={"item_id": "$.id"}
    )
    extend = ExtendOperator(source, "new_attr", Constant("value"))

    explanation = extend.explain()

    assert "Extend(" in explanation
    assert "new_attr" in explanation
    assert "Const('value')" in explanation
    assert "Source(" in explanation  # Parent included


def test_union_explain():
    source_a = JsonSourceOperator(
        source_data={"items": [{"id": 1}]},
        iterator_query="$.items[*]",
        attribute_mappings={"item_id": "$.id"}
    )
    source_b = JsonSourceOperator(
        source_data={"items": [{"id": 2}]},
        iterator_query="$.items[*]",
        attribute_mappings={"item_id": "$.id"}
    )
    union = UnionOperator([source_a, source_b])

    explanation = union.explain()

    assert "Union(" in explanation
    assert "operators: 2" in explanation
    assert "[0]:" in explanation
    assert "[1]:" in explanation