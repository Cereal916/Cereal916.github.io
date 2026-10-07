---
title: FAQ and troubleshooting
section: Help
order: 20
description: Answers to common House of Pips questions: passing, drawing, why a perk didn't trigger, odd scores, locked menus, saves and online issues.
---

# FAQ and troubleshooting

## Playing the table

### Why can't I pass?

You may only pass when you have **no legal play and the boneyard is empty**.
While the boneyard has bones, a player with no legal play must draw one. Two
things change this:

- A {{supply:table_pass}} skips the draw and passes your turn, but only when
  you have no legal play.
- {{perk:catch_and_release}} can return an unplayable draw and end your turn.

### Why can't I play this bone? It matches!

Check these in order:

- **A double can't be played against another double.**
- **A spinner's short sides** only open once both of its long sides are
  covered (unless you hold {{perk:four_winds}}).
- **{{perk:anchor}}** locks your highest-pip bone while you have any other
  legal play.
- **{{perk:stumble}}** makes you draw before playing on the turn after you
  scored, while the boneyard has bones.
- **A Pip Shift or Pip Shuffle** that you committed this turn means you must
  play that bone.
- You may need to **rotate** the bone (right-click or `R`) to fit a vertical
  branch.

### Why did I only draw one bone? I still can't play.

That's the rule here: you draw **one bone per turn**. If it can't be played,
your turn ends. You aren't forced to keep drawing until you find a match.

### Why didn't my play score?

A play scores only if the open ends add up to a **multiple of five** after it.
Remember that an open double counts both halves, and a spinner's open short
sides count nothing until something is played there. {{skill:end_count}} and
{{skill:scoring_glow}} make this easy to see. Then check the maluses:
{{perk:jinx}} zeroes a total of exactly 5.

### Why is my score not a multiple of five?

Scores can end in any digit once perks and maluses are involved. {{perk:tax}}
takes single points, {{perk:collector}} adds 2 per double, {{perk:leak}} costs 2
per draw, and Pip Shield can give back an odd amount. The ledger shows every
line.

## Perks

### Why didn't my perk trigger?

Most perk bonuses need a **scoring play** first. Then check the perk's exact
condition on its page. Common reasons:

- **The play didn't score.** Bonus perks never turn a non-scoring play into a
  scoring one.
- **It counts the bone you played**, not the table: {{perk:doubles}},
  {{perk:blank}}, {{perk:odd_job}}, {{perk:even_flow}} and {{perk:lowball}}
  check only the bone you just placed.
- **A streak was broken.** Drawing from the boneyard resets {{perk:chain}},
  {{perk:momentum}} and {{perk:domino_effect}}; a non-scoring play also resets
  Domino Effect.
- **It was already used this hand.** Limited perks refill at the start of each
  hand. {{perk:turncoat}} also rests for a hand after use.
- **It needs arming.** {{perk:pip_nudge}}, {{perk:counterfeit}},
  {{perk:master_key}} and {{perk:time_loop}} only work after you click them.
  The armed perks only spend their charge on a play that needs them.
- **Its total must be exact.** {{perk:five_alive}} and {{perk:long_count}} need
  an open-end total of exactly 5; {{perk:jackpot}} needs 25 or more.
- **A malus took the points back.** {{perk:jinx}} wipes out a total of 5,
  including bonuses. The ledger shows both lines.

### Do duplicate perks stack?

Almost always. Each perk page has a *How it works* section that says exactly
how copies combine. A few, such as {{perk:wild_blank}} or {{perk:read}}, do
nothing extra with a second copy.

### Why is Midas Touch not doubling everything?

{{perk:midas}} doubles **perk bonuses only**, not the open-end total. To double
the whole play you want {{perk:golden_double}} (with a double) or
{{perk:equalizer}} (when behind). See {{page:scoring}}.

### Can I get rid of a malus?

Not during the match, but {{skill:malus_ward}} blocks the first malus effect
and recharges at higher ranks, and {{perk:shield}} returns points that scoring
maluses take. Every malus is gone when the match ends.

### Why do I never see legendary perks in drafts?

In single-player, each legendary perk must be unlocked first: complete its
three career trials, then buy it in the Perks compendium. See {{page:career}}.
Online matches don't use your unlocks: any legendary perk the match allows can
be offered.

## Menus and progress

### Why is Play locked?

Finish **Nana's tutorial** under Tutorials. It unlocks Play, Puzzles and
Multiplayer.

### Why is a mode locked?

Each mode lists the career trials that open it on the Modes screen. See
{{page:modes}}.

### Where did my match go?

Choose **CONTINUE** on the main menu. Matches are saved automatically. If you
switched computers, make sure you left the match with **Save and exit** and
let Steam Cloud finish syncing. See {{page:saving}}.

### I lost my puzzle progress.

Unfinished puzzles always restart when you come back. Solved puzzles stay
solved.

## Online

### I can't see my friend's lobby.

Both of you need Steam running and the **same version** of the game. Make sure
you have both finished Nana's tutorial, then use **Invite a friend** and send
the invite through Steam.

### My opponent disconnected. What happens?

The match pauses and waits for them to come back. Each match allows two
minutes of reconnecting in total; if that runs out, the match ends with no win
or loss. See {{page:online}}.

## Something went wrong

- If Steam reports a missing file, use **Verify integrity of game files** in
  Steam.
- If the game shows a crash screen, it may offer to copy or send a report. When
  you report a problem in the Steam Community discussions, include the game
  version and the error text, and don't post private information or your whole
  save folder.
- **Clean Slate** erases your career permanently. It is not a fix for
  problems.
