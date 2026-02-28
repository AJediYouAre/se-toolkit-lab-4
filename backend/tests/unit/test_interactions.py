"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Test that filtering by item_id correctly excludes interactions with 
    different learner_id but same item_id."""
    interactions = [
        _make_log(1, 1, 1),  # item_id=1, learner_id=1
        _make_log(2, 2, 1)   # item_id=1, learner_id=2 (the test case)
    ]
    result = _filter_by_item_id(interactions, 1)
    
    assert len(result) == 2
    assert {interaction.id for interaction in result} == {1, 2}
    assert all(interaction.item_id == 1 for interaction in result)

def test_filter_handles_negative_item_id() -> None:
    """Test that filtering works correctly with negative item_id values."""
    interactions = [
        _make_log(1, 1, -1),
        _make_log(2, 2, -1),
        _make_log(3, 3, 1)
    ]
    result = _filter_by_item_id(interactions, -1)
    
    assert len(result) == 2
    assert {interaction.id for interaction in result} == {1, 2}
    assert all(interaction.item_id == -1 for interaction in result)


def test_filter_handles_zero_item_id() -> None:
    """Test that filtering works correctly with zero as item_id."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 0),
        _make_log(3, 3, 1)
    ]
    result = _filter_by_item_id(interactions, 0)
    
    assert len(result) == 2
    assert {interaction.id for interaction in result} == {1, 2}
    assert all(interaction.item_id == 0 for interaction in result)


def test_filter_handles_maximum_integer_values() -> None:
    """Test that filtering works correctly with very large item_id values."""
    large_id = 2**31 - 1  # Max 32-bit integer
    interactions = [
        _make_log(1, 1, large_id),
        _make_log(2, 2, large_id - 1)
    ]
    result = _filter_by_item_id(interactions, large_id)
    
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == large_id


def test_filter_returns_empty_when_no_matching_item_id() -> None:
    """Test that filtering returns empty list when no interactions match the item_id."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 2),
        _make_log(3, 3, 3)
    ]
    result = _filter_by_item_id(interactions, 999)
    
    assert result == []


def test_filter_preserves_interaction_order() -> None:
    """Test that filtering preserves the original order of matching interactions."""
    interactions = [
        _make_log(1, 1, 2),  # Non-matching
        _make_log(2, 2, 1),  # Matching
        _make_log(3, 3, 3),  # Non-matching
        _make_log(4, 4, 1),  # Matching
        _make_log(5, 5, 1)   # Matching
    ]
    result = _filter_by_item_id(interactions, 1)
    
    assert len(result) == 3
    assert [interaction.id for interaction in result] == [2, 4, 5]