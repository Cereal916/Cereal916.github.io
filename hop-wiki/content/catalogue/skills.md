# Skill notes

Hand-written "How it works" text for every skill-tree node, keyed by catalogue
ID. The wiki builder fails when a skill is missing here or a section names an
unknown skill.

## end_count

Shows the **current total of all open ends** on the table at all times, so you
can see at a glance how far you are from the next multiple of five.

## playable_glow

Every bone in your rack that **can be played right now** is highlighted, so you
never have to hunt for a legal play.

## placement_glow

When you pick up a bone, every **valid drop box** for it glows. Drop boxes that
need the bone rotated are marked "Rotate to play".

## scoring_glow

When you pick up a bone, the places where it would **score** flare pink before
you commit, and the tooltip shows the base score.

## pip_forecast

Hovering a place to play shows the **open-end total the table would have**
after that play, even when it would not score.

## rarity_luck

Raises the relative odds of **Uncommon, Rare, Epic and Legendary** cards in your
perk drafts by 12% per rank. Commons become correspondingly less frequent.

- Legendary perks still only appear once you have unlocked them.

## rare_focus

Raises the relative odds of **Rare, Epic and Legendary** cards by a further 15%
per rank, on top of {{skill:rarity_luck}}.

## legendary_touch

Raises the relative odds of **Legendary** cards by a further 25% per rank. It
only affects legendary perks you have already unlocked.

## draft_rerolls

Gives you **one free reroll per rank in every draft**. A reroll replaces one
positive card with a fresh card; the Malus card can't be rerolled.

- Rerolls are not offered in All In or Legendary Table drafts, or after you
  reserve a card with {{skill:fortune_mortgage}}.

## take_all

Adds a **Take all** choice to standard drafts: you take **every positive card
and the Malus** instead of one card.

- It is not available in Legendary Table drafts or after you reserve a card
  with {{skill:fortune_mortgage}}. All In matches always take everything.

## opening_fate

At the start of a match, there is a **10% chance per rank** (up to 30%) that
you begin with a **bonus Common perk**, chosen at random from the commons you
have unlocked.

## bone_memory

Shows, for each number from 0 to 6, **how many bones you haven't seen played
yet contain that number**: bones in Rival's rack and in the boneyard. Bones
Rival has revealed are included.

- It is a counting aid: it never shows where a bone is.

## branch_reader

Hovering a place to play shows how many **follow-up plays** your rack would
have afterwards.

- **Rank 1** marks the location that leaves you the most follow-ups.
- **Rank 2** also labels that count on the board.
- **Rank 3** also marks your **best bone to play** in blue. When two options
  are tied, the one that scores wins.

## lucky_recovery

Each **hand you lose in a row** (up to three) raises the relative odds of
**Uncommon or better** cards in your next draft by 25% per rank. The draft
screen shows the current boost. Winning a hand resets the streak.

## fate_echo

Every time you gain a **new positive perk**, there is a **10% chance per rank**
that it echoes: you get a **temporary second copy for the next hand**, which
disappears after that hand.

## malus_ward

Automatically **blocks the first malus that would affect you**, then needs to
recharge.

- **Rank 1:** blocks once per match.
- **Rank 2:** recharges four hands after it blocks something.
- **Rank 3:** recharges two hands after it blocks something.
- It can block {{perk:greedy}}, {{perk:leak}}, {{perk:stumble}},
  {{perk:cracked}}, {{perk:jinx}}, {{perk:tax}}, {{perk:heavy_hand}} and
  {{perk:exposed}}. It can't block {{perk:anchor}}, which limits which bones you
  may play rather than costing you points.
- On a scoring play it blocks only the first malus that would take points off;
  any others still apply. The table shows "MALUS WARD READY" while it is
  charged.

## fortune_mortgage

In a standard draft, **reserve one positive card for later, then choose
another card from the same offer now**. The reserved perk comes back as the
first card of your next eligible draft.

- Each rank gives one use per match.
- After reserving, you must finish the draft with a different positive card:
  not the Malus, and not Take all.
- Legendary Table drafts never bring a reserved card back.

## coffin_corner

A scoring play that **fills the fourth and last side of a spinner** gains **+10
points per rank**.

- The bonus is added after maluses, and only if the play still scores.
- It is a skill bonus, so {{perk:midas}} doesn't double it.
