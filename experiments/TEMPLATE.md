# NNN — short name

## Before shipping (commit this part first)

- **Date shipped (UTC):** YYYY-MM-DD
- **Who:** Zeke / Claude
- **Question:** what do we want to know?
- **Change:** exactly what ships, one change.
- **Hypothesis:** what we expect, with a number and the source it shows up in.
  e.g. "daily visitors from `entry:mcp` rise from ~75 to at least 90."

## During the window

- Bug fixes shipped while this ran (date, what), or "none".

## After 7 days

- **Data:** `data/NNN.json` (`./compare.py START --save NNN`)
- **Result:** what happened, in numbers.
- **Verdict:** right / wrong / can't tell (say why).
