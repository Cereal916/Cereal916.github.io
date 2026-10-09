---
title: Scoring in depth
section: Playing
order: 20
description: Exactly how House of Pips adds up a play's points and a hand award, in order: perk bonuses, Midas Touch, Golden Double, The Equalizer, maluses, Pip Shield, Malus Ward and skill bonuses.
---

# Scoring in depth

Most of the time a play scores its open-end total plus a few perk bonuses. When
several perks and maluses meet on one play, the **order** they apply in decides
the result. This page lists that order for scoring plays and for the hand
award.

## Which plays score

A play scores when, after your bone is placed, the open ends add up to a
**positive multiple of five**. Perk bonuses can only add to a play that already
scores; no perk turns a total of 12 into a scoring play. (The
{{supply:pip_eraser}} supply is the exception: it lowers the total before this
check, so it can turn 16 into a scoring 15.)

## Reading the flying counts

The numbers that fly from the table show each scoring end's contribution. An
exposed double counts both halves, so a double-one shows **2**. Bare short
sides of a spinner show no number because they add no points. A blank scoring
end can still show **0**.

Here the outer ends contribute **4 + 1 = 5**. The double-one's long sides are
covered, and its empty short sides add nothing.

{{shot:score-ends}}

Solo and online play show the same adjusted end counts. If
{{supply:pip_eraser}} reduces an exposed double-six's contribution from 12 to
**11**, the flying number is **11**. With **4** at the other end, the base
total is **15**, matching the scoring sequence and Ledger.

{{shot:score-eraser}}

## The order on a scoring play

1. **Open-end total.** The sum of the open ends after your play, including any
   {{supply:pip_eraser}} reduction.
2. **Perk bonuses** are added, each multiplied by the number of copies you
   hold. In order: {{perk:doubles}}, {{perk:blank}}, {{perk:draw}},
   {{perk:chain}}, {{perk:underdog}}, {{perk:lowball}}, {{perk:odd_job}},
   {{perk:even_flow}}, {{perk:first_blood}}, {{perk:five_alive}},
   {{perk:momentum}}, {{perk:jackpot}}, {{perk:royal_flush}},
   {{perk:branch_bank}}, {{perk:insurance}}, {{perk:collector}},
   {{perk:domino_effect}}, {{perk:echo}} and {{perk:long_count}}.
3. **{{perk:midas}}** doubles the sum of the step 2 bonuses, once per copy.
4. **{{perk:golden_double}}** doubles the whole play so far if you played a
   double, once per copy.
5. **{{perk:equalizer}}** doubles the whole play so far if you were 30 or more
   behind, once per copy.
6. **{{perk:cracked}}** takes 5 per copy off a double.
7. **{{perk:jinx}}** wipes out a play whose open ends total exactly 5.
8. **{{perk:tax}}** takes 1 per copy for each bonus line on the play (steps 2
   to 5), but never below the open-end total and never adding points.
9. **{{perk:shield}}** gives back up to 5 per copy of what steps 6 to 8 took.
10. **{{skill:malus_ward}}**, if charged, cancels the first malus that took
    points, and Pip Shield is worked out again.
11. **Skill bonuses**: {{skill:coffin_corner}} adds its points if the play
    still scores.

The order of step 2 only matters for {{perk:echo}}, which repeats the last
bonus line added on your previous bonus-earning play.

:::example A big play, step by step
You hold {{perk:doubles}}, {{perk:even_flow}}, {{perk:midas}},
{{perk:golden_double}} and the {{perk:tax}} malus. You play 3-3 and the open
ends total 15.

- Step 1, open ends: **15**.
- Step 2, Double Trouble +5 and Even Flow +5: **25**.
- Step 3, Midas Touch doubles the 10 bonus points: **35**.
- Step 4, Golden Double doubles the play: **70**.
- Step 8, Perk Tax: four bonus lines (Double Trouble, Even Flow, Midas Touch,
  Golden Double) and one copy, so -4: **66**.

With one {{perk:shield}} as well, the 4 taxed points come back and the play
scores **70**.
:::

## After the play

- **{{perk:stumble}}** forces a boneyard draw at the start of your next turn
  if the play scored.
- **{{perk:time_loop}}**, if armed, gives you another turn if the play scored.
- **{{perk:long_count}}** banks a charge if the play didn't score, or empties
  its bank if the open ends totalled exactly 5.
- **{{perk:domino_effect}}**, {{perk:chain}} and {{perk:momentum}} update
  their streaks.

## The order of a hand award

When a hand ends, the winner scores the loser's remaining pips. Perks held by
the **loser** change the award in this order:

1. Start with the loser's **remaining pips**.
2. **{{perk:immunity}}** makes the award zero and skips steps 3 to 6.
3. **{{perk:fortress}}** caps the award at 10.
4. **{{perk:soft_landing}}** takes off 5 per copy (never below zero).
5. **{{perk:heavy_hand}}** adds 5 per copy.
6. **{{perk:exposed}}** adds 25% per copy, compounding, rounded up.
7. **{{skill:malus_ward}}**, if the loser has it charged, cancels the malus
   applied last.

Then the **winner's** perk applies:

8. **{{perk:close}}** doubles the award per copy, but only when the winner went
   domino.
9. The result is **rounded up to the next multiple of five**.

:::example
You lose holding 18 pips with one {{perk:fortress}} and one
{{perk:heavy_hand}}. Fortress caps the award at 10, Heavy Hand adds 5: 15. If
Rival went domino holding one {{perk:close}}, it doubles to **30**.
:::

## Malus points outside a play

- **{{perk:leak}}** takes 2 points per copy from your match score each time you
  draw. It is not part of any play, so {{perk:shield}} doesn't cover it.
- Your match score never drops below zero.

## Points, XP and Bone Bucks

Every point you score, from plays and hand awards alike, also earns career
XP, and the points you bank in a hand add to that hand's Bone Bucks. See
{{page:career}}.
