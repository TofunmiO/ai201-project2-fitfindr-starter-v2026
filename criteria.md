# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. Note: key here is query that matches so where in my code could a query not match a listing -->
The keywords function and the wanted & strong comparison in search_listings (tools.py) match whole words only. If a plural or synonym is the only word that would have matched ("jean" vs "jeans"), every listing scores 0 and the list comes back empty. My loop handles that safely by stopping, but that try still doesn't complete all three tools.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? Is there a specific rule in your tools.py? Name where it lives and what speciifcally makes it 5 of 5-->
This path uses no model. In search_listings (tools.py), the if score > 0: rule drops any listing sharing no whole word with the query, and the final return gives [] when nothing is left. Then the if not results: check in run_agent (agent.py) stops the loop before suggest_outfit. All three steps are plain code with no randomness, so a query that matches nothing stops the same way every time.
---

## 3. Something about state
In at least 4 of 5 tries, the outfit text returned by suggest_outfit contains a distinctive word from the selected item's title (for example "baby" or "butterfly" for Y2K Baby Tee — Butterfly Print, but not a generic word like "top" or "tee" on its own)
<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->



**Why this target:**
The item reaches suggest_outfit through session["selected_item"], and the tool builds its prompt from that item's title, category, colors and tags. The outfit text is the only place in my code that shows what actually reached the tool, so I check it there: if the wrong item had arrived, the outfit would describe a different piece. A state failure looks like a tool problem, so this lets me tell the two apart. I set it at 4 of 5 and not 5 of 5 because the outfit comes from a model, which may describe the item in different words from its title.


---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->
In 5 of 5 tries, the fit card states the selected item's real price and platform, and no other price. For the Y2K Baby Tee, that means it says "$18" (or "18 dollars") and "Depop", in any capitalization.

**Why this target:**
The caption is a post about one specific find, so its facts have to be right: a wrong price or platform makes it false. The prompt in create_fit_card hands the model the item's price and platform and asks it to mention them, so I expect it to every time. But the caption comes from a model, and nothing in the code checks it afterward, so a try could drop a fact or invent a different price. I set 5 of 5 because a wrong fact is a failure.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
 In 5 of 5 tries, every listing returned for a query with a stated price ceiling costs at most that ceiling.


**Why this target:**
The price limit is enforced by plain code. search_listings (tools.py) skips any listing where price > max_price, and the search has no randomness, so the same query gives the same results every time. I set 5 of 5 because a listing over the user's limit is wrong, not a matter of taste. The way it could still fail is upstream: parse_query (agent.py) only reads a price written with a $, so a limit phrased another way would be ignored and the search would run with no ceiling.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
