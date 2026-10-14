# Experiments

How Agent Lab tests a change. It follows the lab's rule for a finding (ANDROMEDA.md, "What
counts as a finding"): date, who, question, hypothesis written before, data, result, verdict.

## The rules

1. **Write the hypothesis before shipping.** Copy `TEMPLATE.md` to `NNN-short-name.md`, fill
   in the question and hypothesis, commit it, *then* deploy. A hypothesis committed after the
   deploy is not one.
2. **One experiment at a time, 7 days each.** A change meant to attract agents or turn readers
   into doers is an experiment. The next one ships only when this one's 7 days are up.
3. **Bug fixes ship anytime.** Fixing something broken (a wrong status code, a crash) is not an
   experiment. Each one is noted in the running experiment's file under "During the window",
   because it may move the numbers.
4. **Checks between are observe-only.** `notes/observations.md` keeps logging what is new or
   odd. Nothing is judged before day 7.
5. **Compare 7 days to 7 days, split by source.** Run `./compare.py START --save NNN` on day 8,
   where START is the UTC date the change shipped. It writes the query's numbers to
   `data/NNN.json`, kept with the finding so anyone can re-check them.
6. **Write the verdict, right or wrong.** A wrong hypothesis is a finding too.

## What "source" means

Each visitor-day (a distinct `ip_hash` on one UTC day) gets one source, from its first hit of
the day:

- **`via:<tag>`** when that hit carries `?via=` (cut at its first `/`, because agents append
  paths to it: `mcp-registry/mcp/sse` is `via:mcp-registry`);
- otherwise **`entry:<surface>`**, the surface it hit first: `mcp`, `a2a`, `home`, `llms.txt`,
  `openapi`, `robots/sitemap`, `api`, `other`.

About 90% of visitors carry no `via`, which is why the entry surface is needed.

The headline number is **daily visitors**: visitor-days in the window divided by 7.
