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

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
