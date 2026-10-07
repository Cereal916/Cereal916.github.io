---
title: Domino rules
section: Playing
order: 10
description: The table rules of House of Pips: the double-six set, the hammer, matching, spinners, scoring on multiples of five, the boneyard, blocked hands and the hand award.
---

# Domino rules

House of Pips plays the scoring game Nana calls **Five-Up**: a game of matching
dominoes where you score whenever the open ends of the table add up to a
multiple of five. This page covers the plain rules. Perks, skills and supplies
change many of them; their pages say exactly how.

{{shot:table}}

## The bones

- The game uses one **double-six set**: 28 bones, every pairing of the numbers
  0 to 6 exactly once.
- Each half shows 0 to 6 **pips**. A bone whose halves match (such as 4-4) is a
  **double**; the double blank is 0-0.
- A bone's **pip total** is both halves added together: 6-5 is worth 11.
- Most modes deal **seven bones** to each player. Quick Draw
  deals five, and Custom lets you choose five to ten.

At the start of each hand you choose your own bones from the face-down set,
one at a time, or press **Random hand** to let the game pick. Rival's hand is
random. Whatever is left becomes the **boneyard**.

## The hammer

The **hammer** decides who plays first.

- Before a match, both players draw one face-down bone. The higher double takes
  the hammer. If neither drew a double, both draw again.
- The hammer holder plays the first bone of every hand.
- Whoever wins a hand takes the hammer for the next one. When **you** win, you
  may keep it or **pass it to Rival**; passing it earns you an extra
  compensation draft. See {{page:matches}}.

## Playing a bone

- The first bone of a hand can be any bone. It goes in the middle of the table.
- After that, a bone must **match the number on an open end**: a 6-3 can go
  next to an open 6 (leaving its 3 open) or an open 3.
- **Doubles are laid crosswise.** A double can't be played directly against
  another double.
- Pick a bone up and drop it on a glowing location, or select a location with
  the keyboard or controller. Right-click (or `R`) turns a bone you are
  holding by 90 degrees, which you need for some vertical branches.

## Spinners: every double branches

In Nana's house **every double is a spinner**. Once both of its long sides are
covered, its two short sides open too, so the table can grow in four
directions from that double. Those upward and downward arms are the
**vertical branches**.

The {{perk:four_winds}} legendary perk lets you open a double's short sides
early.

## Scoring

After every play, add up the numbers on all the **open ends**. If that total is
a **positive multiple of five** (5, 10, 15, ...), the player who just played
scores exactly that many points. This is a **scoring play**, and the table
calls it out as a Fiver.

How the open ends are counted:

- Each open end counts the number showing on it.
- A **double at the end of a line counts both halves**: an open 4-4 adds 8.
- The first bone of a hand counts both of its halves, so leading 5-5 scores 10
  and leading 6-4 scores 10.
- A spinner's short sides count **nothing** until a bone is played on them.
- Once both long sides of a double are covered, the double itself no longer
  counts; only the bones growing out of it do.

:::example
Nana's tutorial: the open ends are 4, 1 and 5. They total 10, a multiple of
five, so the play scores **10**. Later the ends are an open double 4-4 (8),
plus 1 and 1: again **10**.
:::

The **End Count** skill shows the open-end total at all times, and **Fiver
Sense** highlights plays that would score. See [Skill tree](skills.html).

## The boneyard

You may only draw when **you have no legal play**.

- Click the boneyard (or press `Space`) and **choose one face-down bone**.
- If the bone you drew (or any bone in your hand) can now be played, you play
  it. If not, **your turn ends**. You draw **once per turn**, not until you
  find a match.
- The boneyard can be drawn completely empty.
- When the boneyard is empty and you can't play, you **pass**.

{{shot:boneyard}}

## Ending a hand

A hand ends in one of two ways:

- **Going domino.** The first player to play their last bone wins the hand.
- **Blocked hand.** If both players pass in a row because nobody can play, the
  hand is blocked. The player with **fewer pips** left in hand wins it. If both
  totals are equal in a solo match, the hand goes to you.

## The hand award

The winner of a hand also scores the **loser's remaining pips, rounded up to the
next multiple of five**. A loser holding 6-5 and 3-2 (16 pips) gives the
winner 20 points. In a blocked hand the award is the loser's full pip total,
not the difference between the two hands.

Several perks change this award, such as {{perk:soft_landing}},
{{perk:fortress}}, {{perk:immunity}}, {{perk:close}}, {{perk:heavy_hand}} and
{{perk:exposed}}. {{page:scoring}} lists the order they apply in.

## Winning the match

The first player to reach the mode's **target score** while **ahead** wins the
match. If both players are tied at or above the target, play continues until
one of them leads. Classic Table plays to 150; see {{page:modes}} for the
others.
