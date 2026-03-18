from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_hard_range_larger_than_normal():
    # Bug fix: Hard was returning (1, 50), smaller than Normal's (1, 100).
    # Hard must have a strictly larger upper bound than Normal to actually be harder.
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard upper bound ({hard_high}) must be greater than Normal ({normal_high})"
    )


def test_difficulty_ranges_increase_with_difficulty():
    # Easy < Normal < Hard — each level must have a strictly larger search space.
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high


# FIX: Claude caught that old tests compared a tuple to a string; I accepted the unpacking fix.
def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# FIX: Claude wrote these tests to specifically catch the reversed hints bug I identified.

def test_too_high_hint_says_go_lower():
    # Bug: when guess > secret, message wrongly said "Go HIGHER!" instead of "Go LOWER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'Go LOWER' hint, got: {message}"

def test_too_low_hint_says_go_higher():
    # Bug: when guess < secret, message wrongly said "Go LOWER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'Go HIGHER' hint, got: {message}"

def test_hints_not_swapped():
    # Directly assert the two directions are never mixed up
    _, high_msg = check_guess(99, 1)   # way too high
    _, low_msg = check_guess(1, 99)    # way too low
    assert "LOWER" in high_msg
    assert "HIGHER" in low_msg


# FIX: Tests targeting update_score bugs — even-attempt +5 glitch and win scoring off-by-one.

def test_wrong_guess_always_loses_points():
    # Bug: "Too High" on even attempt_number awarded +5 instead of -5.
    score = update_score(100, "Too High", attempt_number=2)  # even attempt — was the glitchy case
    assert score == 95, f"Expected 95, got {score}"

def test_wrong_guess_odd_attempt_loses_points():
    # Confirm odd attempts were always correct — regression guard.
    score = update_score(100, "Too High", attempt_number=3)
    assert score == 95, f"Expected 95, got {score}"

def test_win_score_no_off_by_one():
    # Bug: points used attempt_number + 1, so a first-try win gave 80 instead of 90.
    score = update_score(0, "Win", attempt_number=1)
    assert score == 90, f"Expected 90 for first-attempt win, got {score}"

def test_win_score_later_attempt():
    # Confirm scoring decreases correctly with attempt number.
    score = update_score(0, "Win", attempt_number=5)
    assert score == 50, f"Expected 50 for attempt 5, got {score}"
