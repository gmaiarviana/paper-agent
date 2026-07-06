"""Testes da auto-regulação básica (W-PROTO-FILA-3.1)."""

from tools.workflow_platform.job_queue.load import (
    LOAD_STATE_COLORS,
    QUEUE_APPROACHING_THRESHOLD,
    QUEUE_TARGET_LIMIT,
    QueueLoadState,
    compute_load_state,
)


def test_zero_items_is_ok():
    assert compute_load_state(0) == QueueLoadState.OK


def test_below_approaching_is_ok():
    assert compute_load_state(14) == QueueLoadState.OK


def test_at_approaching_threshold_is_approaching():
    assert compute_load_state(15) == QueueLoadState.APPROACHING
    assert compute_load_state(QUEUE_APPROACHING_THRESHOLD) == QueueLoadState.APPROACHING


def test_just_below_target_is_approaching():
    assert compute_load_state(19) == QueueLoadState.APPROACHING


def test_at_target_is_over_limit():
    assert compute_load_state(20) == QueueLoadState.OVER_LIMIT
    assert compute_load_state(QUEUE_TARGET_LIMIT) == QueueLoadState.OVER_LIMIT


def test_far_above_target_is_over_limit():
    assert compute_load_state(50) == QueueLoadState.OVER_LIMIT


def test_load_state_colors_covers_all_three_states():
    assert set(LOAD_STATE_COLORS.keys()) == set(QueueLoadState)
    for color in LOAD_STATE_COLORS.values():
        assert color.startswith("#")
        assert len(color) == 7
