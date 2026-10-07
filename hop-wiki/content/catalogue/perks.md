# Perk notes

Hand-written "How it works" text for every perk, keyed by the perk's catalogue
ID. The wiki builder fails when a perk is missing here or when a section names
a perk the catalogue no longer has. Verify each statement against the game's
rules before changing it, and never describe how Rival decides its moves.

## doubles

When your scoring play uses a **double** (both halves show the same number,
including the double blank), the play gains **+5 points for each copy**.

- Only the bone you just played is checked, not the doubles already on the
  table.
- The open ends must still add up to a multiple of five; Double Trouble only
  adds to a play that already scores.
- Pairs naturally with {{perk:golden_double}}, which then doubles the whole
  play including this bonus, and with {{perk:collector}}.
- {{perk:cracked}} takes 5 points per copy back from any scoring double.

:::example
You play 4-4 and the open ends total 15. With two copies of Double Trouble the
play scores 15 + 10 = **25**.
:::

## blank

When your scoring play uses a bone with **at least one blank half** (0-1
through 0-6, and the double blank), the play gains **+5 points for each copy**.

- A blank that played as a wild card still counts as a blank bone.
- Combines well with {{perk:wild_blank}} and {{perk:counterfeit}}, which make
  blanks much easier to place.

## draw

Your **first play after a trip to the boneyard** gains **+5 points for each
copy** if it scores.

- It works whether you play the bone you just drew or another one.
- If the drawn bone cannot play, your turn passes, and the bonus waits for
  your next play.
- Using a {{supply:table_pass}} also counts as a trip for this perk.
- Any play clears the bonus, scoring or not, so only that one play can earn it.

## lowball

When your scoring play uses a bone with **3 pips or fewer in total** (0-0, 0-1,
0-2, 0-3, 1-1 and 1-2), the play gains **+5 points for each copy**.

## odd_job

When your scoring play uses a bone whose **two halves add up to an odd number**
(for example 2-3 or 1-6), the play gains **+5 points for each copy**.

- Holding both Odd Job and {{perk:even_flow}} guarantees one of them fires on
  every scoring play.

## even_flow

When your scoring play uses a bone whose **two halves add up to an even
number** (every double, plus bones such as 1-3 or 2-6), the play gains **+5
points for each copy**.

- The double blank (0 pips) counts as even.

## first_blood

Your **first play of each hand that actually scores** gains **+5 points for
each copy**.

- "Actually scores" means points were added to your score. A play that a malus
  reduced to zero (such as {{perk:jinx}} on a total of 5) does not use up First
  Blood; it waits for your next scoring play.
- It resets at the start of every hand.

## soft_landing

When you **lose a hand**, the points your remaining bones give the winner are
reduced by **5 for each copy**, before the award is rounded to a multiple of
five. The award can never drop below zero.

- It works on blocked hands as well as when the winner goes domino.
- It applies after {{perk:fortress}}'s cap and before maluses such as
  {{perk:heavy_hand}} and {{perk:exposed}}. See the hand award order on
  {{page:scoring}}.

:::example
You lose holding 6-5 and 3-2: 16 pips. With one Soft Landing the award is
16 - 5 = 11, which rounds up to **15** instead of 20.
:::

## five_alive

A scoring play whose open ends add up to **exactly 5** gains **+5 points for
each copy**, so a single copy turns a 5-point play into 10.

- {{perk:jinx}} wipes out a play that totals exactly 5, bonus included.
- {{perk:long_count}} also pays out on a total of exactly 5, so the two work
  together.

## insurance

After you **lose a hand**, your **first scoring play of the next hand** gains
**+5 points for each copy** you held when the hand was lost.

- The bonus is spent by your first play of the new hand whose open ends add up
  to a multiple of five, even if a malus reduces that play.
- Winning a hand clears it. Losing two hands in a row does not build up two
  bonuses.

## chain

A scoring play gains **+5 points for each copy** when it is your **second or
later play in a row without visiting the boneyard**.

- The streak counts your own plays only; Rival's turns in between do not break
  it.
- Drawing from the boneyard, using a {{supply:table_pass}}, or passing because
  the boneyard is empty resets the streak. So does the start of a new hand.
- Your very first play after a reset never qualifies.

## underdog

A scoring play gains **+5 points for each copy** when your match score is
**lower than Rival's** at the moment you play. Being tied does not count.

## boneyard_peek

Every time you go to the boneyard, **one face-down bone in the boneyard is
turned face-up for you** before you choose. You still pick which bone to take,
so you can take the revealed one or avoid it.

- The revealed bone is the next bone in the boneyard's fixed order, so it is
  shown again on later visits until someone takes it.
- Extra copies do not reveal more bones.
- This is a passive perk. It is a different thing from the
  {{supply:boneyard_lantern}} supply, which lights up one random bone for a
  single trip.

## light_fingers

On a boneyard visit, you **turn over one extra face-down bone**: you pick two,
both are revealed, and you **keep the one with fewer pips**. The other stays in
the boneyard. If both have the same pip total, you choose.

- It is used automatically on your first boneyard visit of each hand. Each
  copy gives one such visit per hand.
- On a visit that {{perk:sovereign_draw}}, {{perk:dead_mans_draw}} or
  {{perk:greedy}} already changes, Light Fingers sits out and keeps its use for
  a later visit.
- It needs at least one spare bone in the boneyard beyond what you must take.

## shield

When a malus lowers one of your scoring plays, Pip Shield **gives back up to 5
of the lost points for each copy**.

- It covers {{perk:cracked}}, {{perk:jinx}} and {{perk:tax}}, the maluses that
  act on a scoring play.
- It never gives back more than the maluses took from that play.
- It does nothing for maluses that act elsewhere, such as {{perk:leak}} or the
  hand award maluses.

:::example
You play a total of 5 with {{perk:five_alive}} (5 + 5 = 10) while holding
{{perk:jinx}}. Five Jinx takes all 10 points. One Pip Shield restores 5, so the
play still scores **5**.
:::

## branch_bank

A scoring play gains **+5 points for each copy** when you play on a **vertical
branch**: the arms that grow up and down from a spinner after its long sides
are filled.

- Every bone further along an upward or downward arm counts too.
- Plays on the main left and right line do not qualify.

## swap_stock

On your turn, **choose one of your bones and one face-down boneyard bone, and
they trade places.** You don't see the new bone until it lands in your hand.

- Each copy gives one swap per hand.
- Using it does not end your turn: you can still play or draw afterwards.
- The bone you give away goes back into the boneyard face-down.
- It needs at least one bone in the boneyard.

## salvage

When you draw from the boneyard and pick a **heavy bone (10 or more pips)**,
Salvager lets you **pick one more face-down bone, turns them over, and you keep
the one you want**.

- Each copy covers one heavy draw per hand.
- It only triggers when the boneyard still has another bone to offer.
- The heavy bones are 4-6, 5-5, 5-6 and 6-6.

## open_book

Once per hand, **choose one of your own hidden bones to reveal to Rival. In
return, one of Rival's hidden bones is chosen at random and revealed to you.**

- Both racks need at least three bones, and each needs at least one bone that
  is still hidden.
- Revealed bones stay face-up for as long as their owner holds them, so Rival
  can see the bone you showed.
- More copies do not give more uses; it stays once per hand.

## catch_and_release

When an **ordinary boneyard draw** gives you a bone that **cannot be played**,
you may **put it back face-up in the exact spot it came from and end your
turn** instead of keeping it.

- You get no replacement draw; your turn simply ends with your hand
  unchanged.
- The draw still counts as a draw: streaks reset and {{perk:leak}} still
  charges you.
- The returned bone stays face-up in the boneyard, so both players can see it
  and whoever draws that spot gets it.
- "Ordinary" means a plain one-bone draw. It is not offered when the draw was
  changed by {{perk:greedy}}, {{perk:sovereign_draw}},
  {{perk:dead_mans_draw}}, {{perk:light_fingers}} or {{perk:salvage}}, or when
  {{perk:stumble}} forced the draw.
- Once per hand, however many copies you hold.

## pip_shift

Once per hand for each copy, **drag one pip across a bone's divider**: one half
loses a pip and the other gains it. The total stays the same, and no half can
go below 0 or above 6. Doubles can be split too (3-3 can become 2-4).

- The game only lets you confirm a change that makes the bone playable right
  now.
- The shifted bone becomes **public** (Rival sees it), and you **must play it
  this turn**. You cannot draw or play another bone first.
- Perks then see the shifted bone: a 2-4 shifted to 3-3 counts as a double for
  {{perk:doubles}} and {{perk:golden_double}}.
- {{perk:pip_shuffle}} is the stronger version that moves any number of pips.

## swap_rival

On your turn, **choose one of your bones and one of Rival's face-down bones,
and they trade places.** You pick Rival's bone blind.

- After the trade **both bones are public**: you can see what you received and
  Rival can see what you gave away.
- Each copy gives one swap per hand. Using it does not end your turn.
- {{perk:turncoat}} is the legendary version that shows you Rival's whole rack
  first.

## pip_nudge

**Arm** Loaded End on your turn, then you may play a bone on an end it **misses
by exactly one pip** (for example a 4 against an open 5 or 3). The placement
preview shows the change before you commit.

- The charge is only spent when you actually make a play that would otherwise
  be illegal. If you make an ordinary play instead, the arming is cancelled
  and the charge is kept.
- Click the perk again to disarm it for free.
- A double still cannot be played against a double.
- Each copy gives one use per hand.

## counterfeit

**Arm** Counterfeit Pip, then one of your **blank bones may be played on any
open end** as if its blank matched.

- The double blank takes the end's value on both halves, so 0-0 played on a 4
  becomes a 4-4 for the open ends and for scoring.
- The charge is only spent by a play that would not have been legal anyway.
  If you make an ordinary play, the arming is cancelled and the charge is kept.
- Each copy gives one use per hand. {{perk:wild_blank}} makes this permanent.

## reroll

Once per draft for each copy, **upgrade the lowest-rarity positive card** in
the offer by one rarity tier: Common to Uncommon, Uncommon to Rare, and so on.

The new card is a random perk of that tier that you have unlocked. Online, it
can be any perk of that tier the match allows, so an Epic card can become a
Legendary one.

- It never upgrades the Malus card, and it never creates a second copy of a
  card already offered at the new tier.
- A Legendary card cannot be upgraded further.
- It is not available in All In or Legendary Table drafts.

## jackpot

A scoring play whose open ends add up to **25 or more** gains **+20 points for
each copy**.

## collector

On a scoring play, gain **+2 points for every different double you have
played this hand**, for each copy.

- The double you are playing right now counts if it is new.
- Playing the same double value twice only counts once; the count resets every
  hand.

:::example
You have already played 1-1 and 5-5 this hand and now score with 3-3. That is
three different doubles: +6 with one Collector, +12 with two.
:::

## royal_flush

A scoring play made **with the 6-6** gains **+30 points for each copy**.

## domino_effect

Each scoring play gains **+5 points for every scoring play you made in a row
just before it**, for each copy.

- Your first scoring play of a streak gains nothing, the second gains +5, the
  third +10, and so on.
- The streak breaks when you make a play that doesn't score, when you draw
  from the boneyard, and at the start of every hand. Rival's plays don't break
  it.

:::example
Three scoring plays in a row with one Domino Effect: +0, then +5, then +10.
With two copies: +0, +10, +20.
:::

## fortress

When you lose a hand, your remaining bones can award the winner **at most 10
points**.

- The cap is applied first; {{perk:soft_landing}} then reduces it further, and
  {{perk:heavy_hand}} and {{perk:exposed}} can push it back up.
- Extra copies change nothing.

## close

When you **go domino** (play your last bone), the award you collect from
Rival's remaining bones is **doubled for each copy**: two copies make it four
times as large.

- It only works when you go domino, not when you win a blocked hand.
- The doubled award is rounded up to a multiple of five.

## golden_double

A scoring play made **with a double** is **doubled in full** for each copy: the
open-end total, every perk bonus and the {{perk:midas}} extra all double.

- Two copies make the play four times as large.
- It happens after the perk bonuses are added and before
  {{perk:equalizer}} and any maluses. See {{page:scoring}}.

:::example
You play 5-5 and the ends total 20, with {{perk:doubles}}: 20 + 5 = 25. Golden
Double makes it **50**.
:::

## wild_blank

Your blank bones **may be played on any open end**. A blank half matches
whatever number it touches; the other half stays as printed.

- The double blank takes the end's value on both halves (0-0 played on a 3
  plays as a 3-3).
- It is permanent and needs no arming. Extra copies change nothing.
- {{perk:counterfeit}} is the one-use version.

## alchemy

Choose one of your bones and **change each half to its double-six
complement**: every number becomes 6 minus itself. A 1-4 becomes 5-2, a 6-6
becomes 0-0, and 3-3 stays 3-3.

- You see the result before confirming.
- The bone stays private and you don't have to play it this turn.
- Each copy gives one use per hand.

## pip_shuffle

Once per hand, **move any number of pips across a bone's divider**, keeping the
total the same and every half between 0 and 6. A 1-5 could become 0-6, 2-4 or
3-3.

- As with {{perk:pip_shift}}, you can only confirm a result that can be played
  now, the bone becomes public, and you must play it this turn.
- More copies do not add uses; it stays once per hand.

## dead_mans_draw

When you go to the boneyard holding **exactly one bone**, you pick **one extra
face-down bone for each copy**. All of them are turned over and you choose
which to keep.

- It stacks with {{perk:sovereign_draw}} and {{perk:light_fingers}}: their
  extra picks add together.

## echo

On a scoring play, Echo Chamber **adds your most recent perk bonus again**, once
for each copy.

- "Most recent" means the last bonus line added on your previous play that had
  one, after {{perk:midas}} doubling. It can come from an earlier hand in the
  same match.
- When Echo Chamber fires, the echo itself becomes your most recent bonus. With
  two or more copies the echo grows from play to play.
- Nothing is repeated until you have earned at least one perk bonus.

## momentum

**Every third play in a row without drawing** (your 3rd, 6th, 9th and so on)
gains **+15 points for each copy** if it scores.

- The count includes plays that didn't score. Drawing, a
  {{supply:table_pass}}, passing on an empty boneyard and a new hand all reset
  it.

## long_count

Every one of your plays that **does not score** banks one charge for each copy.
Your next play whose open ends add up to **exactly 5** gains **+5 points per
banked charge**, and the bank empties.

- Plays that score 10, 15 or more neither add to nor spend the bank.
- Any play with a total of exactly 5 empties the bank, even if
  {{perk:jinx}} wipes the points.
- The bank resets at the start of every hand.

:::example
With one copy you make three plays that don't score, then hit a total of 5:
5 + 15 = **20**. With {{perk:five_alive}} as well it would be 25.
:::

## read

Rival's bones that **could be played on the board right now glow**, while
staying face-down. You learn how many of Rival's bones fit the table, though
not which numbers they show.

- The glow updates as the board changes. Extra copies change nothing.

## immunity

When you lose a hand, your remaining bones **award the winner nothing**.

- It works on both blocked hands and when the winner goes domino.
- It overrides every other hand award effect, including {{perk:heavy_hand}}
  and {{perk:exposed}}.

## master_key

**Arm** Master Key, then play **any bone on any open end**, even if the numbers
don't match. The bone keeps its printed numbers.

- The charge is only spent by a play that would otherwise be illegal. An
  ordinary play cancels the arming and keeps the charge.
- A double still cannot be played against a double.
- Each copy gives one use per hand.

## turncoat

**See Rival's whole rack**, then choose one of your bones and one of Rival's
bones to swap.

- Once per hand however many copies you hold. After you use it, it **rests for
  the next hand** and is ready again the hand after that.
- Using it does not end your turn.
- Unlike {{perk:swap_rival}}, the traded bones are not revealed to the table.

## time_loop

**Arm** Time Loop before you play. If that play scores, you **immediately take
another turn**.

- The charge is only spent when the armed play scores. If it doesn't, the
  arming ends and the charge is kept for later.
- Each copy gives one use per hand.
- If the armed play was your last bone, the hand simply ends.
- With {{perk:stumble}}, the extra turn begins with Stumble's required draw.

## equalizer

While you are **30 or more points behind Rival** (before the play), your scoring
plays are **doubled for each copy**.

- It doubles the whole play: open ends, bonuses and any
  {{perk:golden_double}} doubling. Maluses are applied after it.

## four_winds

Normally a double only opens its short sides once **both** long sides are
covered. Four Winds lets you play on a double's short side as soon as **one**
long side is covered.

- Each copy gives one early opening per hand. It works on any double on the
  table, whoever played it.
- Once a double has been opened this way, its short sides stay open for every
  player who holds Four Winds.
- The new branch counts toward the open ends like any other branch.

## midas

On a scoring play, **all point bonuses from perks are doubled** for each copy:
two copies make them four times as large.

- The open-end total itself is not doubled, only the perk bonuses. Skill
  bonuses such as {{skill:coffin_corner}} and the points {{perk:shield}} gives
  back are not doubled either.
- {{perk:golden_double}} and {{perk:equalizer}} come after Midas Touch, so they
  double its result again.

:::example
Ends total 20 with {{perk:doubles}} (+5) and {{perk:chain}} (+5): 20 + 10 = 30.
Midas Touch adds another 10, so the play scores **40**. If it was a double
and you also hold {{perk:golden_double}}, it becomes **80**.
:::

## sovereign_draw

On **every** boneyard visit you pick **one extra face-down bone for each copy**.
All of them are turned over and you choose which to keep. The rest stay in
the boneyard.

- It stacks with {{perk:dead_mans_draw}} and {{perk:light_fingers}}.

## table_whisperer

While you hold a bone, each place you could play it shows whether that play
would give Rival **more, fewer or the same number of playable bones**, judged
against Rival's real rack.

- With two or more copies it shows the exact difference, such as "Rival plays
  −2".

## final_warning

When Rival is down to **one bone**, the **safest legal place** for the bone you
hold is marked.

- "Blocks rival" means Rival's last bone can't be played after your play.
- "Safest play" means the play that leaves Rival the smallest scoring reply.
- Extra copies change nothing.

## heavy_hand

**Malus.** When you lose a hand, the winner gets **5 extra points for each
copy** on top of your remaining pips.

- It applies after {{perk:fortress}} and {{perk:soft_landing}} and before
  {{perk:exposed}}.
- {{perk:immunity}} cancels it, and {{skill:malus_ward}} can block it.

## greedy

**Malus.** Every boneyard draw makes you **keep one extra bone for each copy**.

- If the boneyard runs short, you take what is left.
- {{skill:malus_ward}} can block it on one draw.

## cracked

**Malus.** A scoring play made **with a double loses 5 points for each copy**,
after every bonus and multiplier. It can't take the play below zero.

- {{perk:shield}} can give the points back, and {{skill:malus_ward}} can block
  it.

## leak

**Malus.** Every time you draw from the boneyard you **lose 2 points for each
copy** from your match score. Your score never drops below zero.

- Passing because the boneyard is empty is not a draw and costs nothing.
- {{perk:shield}} does not cover it. {{skill:malus_ward}} can block it.

## anchor

**Malus.** Your **highest-pip bone can't be played while you have any other
legal play**. You can play it once it is your only option.

- The rack recalculates every turn, so the anchored bone changes as you play.
- {{skill:malus_ward}} does not affect it.

## jinx

**Malus.** A play whose open ends add up to **exactly 5 scores nothing**,
bonuses included.

- Totals of 10, 15 and more are unaffected. Extra copies change nothing.
- {{perk:shield}} gives back up to 5 points per copy, and {{skill:malus_ward}}
  can block it.

## tax

**Malus.** Every bonus on a scoring play **costs 1 point for each copy of Perk
Tax**.

- Each bonus line on the play counts once, including multiplier lines such as
  {{perk:midas}}, {{perk:golden_double}} and {{perk:equalizer}}.
- Perk Tax can never take a play below its open-end total, and it never adds
  points. A play with no bonuses is not taxed.
- {{perk:shield}} can give the points back, and {{skill:malus_ward}} can block
  it.

:::example
Ends total 10 with {{perk:doubles}} and {{perk:even_flow}}: 10 + 10 = 20. Two
bonus lines and one copy of Perk Tax: the play scores **18**.
:::

## exposed

**Malus.** When you lose a hand, the award from your remaining bones goes up
**25% for each copy** (copies compound: two copies are ×1.5625), rounded up.

- It applies last, after {{perk:fortress}}, {{perk:soft_landing}} and
  {{perk:heavy_hand}}. The award is then rounded up to a multiple of five.
- {{perk:immunity}} cancels it, and {{skill:malus_ward}} can block it.

## stumble

**Malus.** After **any play that scores for you**, your **next turn must start
with a boneyard draw**. After that draw you may play as normal.

- Once the boneyard is empty the requirement lifts and you play normally.
- You can't use {{perk:catch_and_release}} on this draw.
- {{skill:malus_ward}} can block it.
- Extra copies change nothing.
