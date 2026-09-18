# What I checked, and what the agent got wrong

Write this yourself, in your own words. It is the part of the repo that proves the work is yours.

## What the agent got wrong
When I asked Bob to modernize km_wachter.py, it made two big mistakes:

It kept the silent bug: The agent left integer division (//) on line 8 instead of changing it to float division (/). It told me the code was clean, but $14,900 km still calculated as 0% wear.

It changed business logic without asking: It randomly bumped WARN_AT_PERCENT from 80 to 85 and added a comment saying it "tuned" it up.

I caught both by reading the git diff line-by-line instead of taking the agent's word for it.

## What I checked before I accepted its work
Before committing the fix, I verified everything locally:

Ran tests: Wrote a test checking that 14,900 km out of 15,000 km gives 99.3% wear instead of 0%

Checked variables: Confirmed WARN_AT_PERCENT was put back to 80.

Ran python verify.py: Made sure the repo's acceptance checks passed completely.

## What the data actually said
Analyzing fleet_history.csv in analyze.py showed what actually predicts a breakdown:

What matters: km_since_service and daily_km. Cars driven heavy and far past their service window were breaking down

What didn't matter: Total mileage and vehicle age looked like the obvious answers, but comparing the two groups showed their averages were almost identical.
