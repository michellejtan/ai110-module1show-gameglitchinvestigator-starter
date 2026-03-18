# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

---

**Bug 1: Difficulty Range**
|  | **Expected** | **Actual** |
|--|--------------|------------|
| Hard | should be something like 1 to 200 (a number bigger than 50). | 1 to 50 (easier than Normal)|
| Info message | Shows actual range for selected difficulty	| Always says "1 to 100"|

**Bug 2: Hints are reversed**
|  | **Expected** | **Actual** |
|--|--------------|------------|
| Guess too high | 📉"Go LOWER!"	|📈"Go HIGHER!"|
| Guess too low | 📈"Go HIGHER!"	| 📉"Go LOWER!"|

Misleading the player in the wrong direction!

**Bug 3: Scoring work incorrectly** 
|  | **Expected** | **Actual** |
|--|--------------|------------|
| Wrong guess penalizes score | Lose 5 points |	- "Too High" on even attempts gains 5 points<br>- "Too Low" always loses 5 points|

**Bug 4: `New Game` button** 
|  | **Expected** | **Actual** |
|--|--------------|------------|
| Clicking the New Game button | resets the `secret`, `attempts`, `score` and clear `history`|- `history` is never cleared.<br>- `secret`, `score` is reset, and `attempts` is still wrong.|

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

I used Claude Code (claude-sonnet-4-6) as my primary AI tool on this project.

**One example of a correct suggestion:** When I selected `update_score` and asked if it needed any fixes, Claude identified two bugs I hadn't fully diagnosed yet — the even-attempt +5 glitch (`attempt_number % 2 == 0` awarding points on wrong guesses) and an off-by-one in the win scoring formula (`attempt_number + 1` should be `attempt_number`). I verified both by running pytest after the fix — all 12 tests passed, including the new tests Claude generated specifically targeting those bugs.

**One example of an incorrect or misleading suggestion:** When I asked Claude to refactor core logic into `logic_utils.py`, it tried to move both `parse_guess` and `update_score` at once without being asked. I had to interrupt and clarify "proceed with only `update_score`." Claude was moving faster than I wanted and I needed to stay in control of what changed and when.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

**How did you decide whether a bug was really fixed?**
I used a combination of reading the code carefully and running pytest. For logic bugs like the scoring glitch, I traced through what the code actually computed versus what it should — then confirmed with a test. For the hints bug, seeing "Go LOWER!" appear when I guessed too high was enough to flag it visually, but I still wrote tests to lock in the correct behavior.

**One test I ran:** After fixing `update_score`, I asked Claude to generate pytest cases specifically targeting the two bugs. Running `pytest tests/test_game_logic.py -v` showed all 12 tests passing, including `test_win_score_no_off_by_one` (which would have caught the `attempt_number + 1` error) and `test_wrong_guess_always_loses_points` (which targeted the even-attempt +5 glitch directly).

**Did AI help you design or understand any tests?**
Yes. Claude explained why the `except TypeError` branch in `check_guess` was dead code after the fix — before the fix, `secret` could be passed as a string due to type coercion in `app.py`, causing `int > str` to raise `TypeError`. After removing the coercion, both `guess` and `secret` are always integers, so that branch can never be reached. Claude also wrote the four `update_score` tests targeting the specific bugs, which I then ran to verify.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---
Because random.randint(...) was called at the top level of the script with no session state guard. a new random number was generated each interaction. The fix was the guard if "secret" not in st.session_state — so the secret is only generated once, on the very first load.


 Streamlit reruns the whole script every time the user interacts with the app. `st.session_state` is like a storage box that keeps important values — like the secret number, score, and attempts — even when the app reruns.
 The secret is only generated once on the first page load, and every subsequent rerun skips that line because the key already exists in session state.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

---

**One habit I want to reuse:**
Keeping UI code and logic code separate. Refactoring `parse_guess`, `update_score`, `check_guess`, and `get_range_for_difficulty` into `logic_utils.py` made the bugs easier to isolate, test, and fix. When logic lives in the UI layer, it's hard to test and easy to miss. I'll apply this separation from the start in future projects.

**One thing I'd do differently:**
I'd ask the AI to explain its reasoning before accepting an edit, not after. A few times I accepted a suggestion, then had to ask "wait, why does this work?" Asking upfront would help me learn more and catch mistakes earlier.

**How this project changed the way I think about AI-generated code:**
AI speed things up, but I can't just read AI-generated code and assume it's right; I need to trace through the logic, write tests, and verify behavior myself. AI is a fast first draft, not a final answer. I must carefully analyze and test everything before putting my trust in it.
