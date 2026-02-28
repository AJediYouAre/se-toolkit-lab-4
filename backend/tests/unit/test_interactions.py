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