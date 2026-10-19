# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr helps a thrift shopper find a piece and work out how to wear it. The user types a plain-language request such as "vintage graphic tee under $30", optionally with a size, and the agent searches a catalog of 40 second-hand listings for matches. It picks the best match and suggests one or two outfits that combine it with pieces from the user's own wardrobe, or general styling advice if they haven't entered one. Then it writes a short, post-ready caption about the find. If nothing in the catalog matches, the agent stops and says what the user could change (broader words, a different size or a higher price).


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
Looks through all the listings, finds the listings that match your description, size and price limit, and returns the best matches (or an empty list if none).
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
description (str), size (str or None, optional), max_price (float or None, optional)
- **Returns:**
list of listing dicts, best match first and at most 10, each with id, title, description, category, style_tags, size, condition, price, colors, brand (can be None) and platform.
- **When it has nothing:**
Returns an empty list [], not None and not an error

### `suggest_outfit`

- **What it does:**
Asks the model to suggest one or two outfits that combine a thrifted listing with pieces from the user's wardrobe, or general styling ideas if the wardrobe is empty.
- **Inputs:**
new_item (dict, a listing with title, category, colors, style_tags, size and price), wardrobe (dict with an items key holding a list of dicts, each with name, category, colors, style_tags and optional notes)
- **Returns:**
A non-empty string of one or two outfit suggestions. When the wardrobe has items, it names the pieces the user already owns.
- **When it has nothing:**
If the wardrobe is empty, missing or None, it returns a string of general styling advice for the item, never "" and never an error. If the model sends back nothing, it returns a fixed fallback sentence, so it's never empty.
### `create_fit_card`

- **What it does:**
Asks the model to write a short social-media caption about the thrifted find, based on the item and the outfit suggestion.
- **Inputs:**
outfit (str, the text from suggest_outfit), new_item (dict, a listing with title, price and platform).
- **Returns:**
A string of two to four sentences written like a real post, mentioning the item, its price and its platform once each.
- **When it has nothing:**
 If outfit is empty or only whitespace, it returns the string "No fit card yet: there was no outfit suggestion to write about." It does not raise. If the model sends back nothing, it returns a fixed fallback sentence.
---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->
- **Branch rule:**
 If search_listings returns an empty list, put a message in session["error"] that names what the user could change (broader words, a different size, a higher price), and return the session without calling suggest_outfit or create_fit_card. Otherwise, take the first result, put it in session["selected_item"], and go on to suggest_outfit, then create_fit_card.
- **Where it lives:** `agent.py::run_agent`
in the if not results: check.
- **How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
Regex
- **What moves through the session:** <!-- which fields, in what order -->
What moves through the session, in order:
     - query (str, what the user typed) and wardrobe (dict, the user's closet)
     - parsed (dict: description, size, max_price)
     - search_results (list of listing dicts)
     - selected_item (dict, the first search result)
     - outfit_suggestion (str, outfit text)
     - fit_card (str, the caption)
     - error (str or None, set only when the run ends early)

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Outfit 1:** Pair the butterfly baby tee with the baggy straight-leg jeans, dark wash (bottoms, dark blue, in…
      →    10 wardrobe item(s))
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Found this absolute gem of a Y2K butterfly baby tee while digging through the racks, and it's giving major off…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1:** Pair the butterfly baby tee with the baggy straight-leg jeans, dark wash (bottoms, dark blue, indigo) and layer the vintage black denim jacket (outerwear, black) on top. Finish the look with the chunky white sneakers (shoes, white) for an effortless Y2K street style vibe.

**Outfit 2:** Tuck the baby tee into the wide-leg khaki trousers (bottoms, khaki, tan) secured with the brown leather belt (accessories, brown). Slip on the black combat boots (shoes, black) and throw the black cropped zip hoodie (tops, black) over your shoulders for a casual, contrast-heavy aesthetic.

  Fit card: Found this absolute gem of a Y2K butterfly baby tee while digging through the racks, and it's giving major off-duty Bratz doll energy. You can style it super easy with baggy dark wash denim and chunky sneaks, or tuck it into khaki trousers with combat boots for that perfect contrast. Grabbed this baby tee for just $18 over on my Depop before someone else snags it!

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'bandtee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors':['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'GraphicTee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphictee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layeringunder a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015','title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'],'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

**Outfit 1: Casual Streetwear**
Pair the vintage Levi's 501 jeans with the white ribbed tank top and layer the oversized grey crewneck sweatshirt on top. Finish the look with the chunky white sneakers and the black crossbody bag.

**Outfit 2: Edgy Denim-on-Denim**
Style the vintage Levi's 501 jeans with the black cropped zip hoodie and the vintage black denim jacket layered over it. Ground the outfit with the black combat boots and cinch the waist with the brown leather belt.

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"


Nothing beats the effortless 90s off-duty model vibe of a good medium wash. These vintage Levi's 501 jeans are up on Depop right now for $38. Just add crisp white sneakers and a simple tee and you're good to go.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
 I asked Claude to implement search_listings by following the TODO in tools.py: filter by price and size, score by keyword overlap, drop zero scores, sort, and return an empty list when nothing matches.
- *What came back:*
A working function that reused my _size_tokens and _size_matches helpers and added weighted scoring (title, category and tags count double). Claude also pointed out a bug in my size helper: it returned true when the wanted size and the listing size shared any token, so "US 8" also matched "US 9" because both contain "US".
- *What I changed:*
I accepted the rewrite after seeing the reasoning. A requested size must now match as whole tokens, so "M" matches "S/M" and "M/L" but not "XL". I asked for a check of the price ceiling and size cases before moving on.

**Moment 2**

- *What I asked for:*
 I had already built run_agent myself. I pasted the milestone instructions and asked Claude to verify whether my implementation met them.
- *What came back:*
Claude confirmed that it had been implemented and found two hand-offs, the parsed query and the search results, that went through local variables and not the session, which the instruction says not to do.
- *What I changed:*
 I approved the fix, on conditions I set: Claude had to confirm there were no unused variables left and that everything it added worked and wasn't failing silently. Claude's scan found only an unused import config from the starter, and it re-ran a matching query, a no-match query and an empty-wardrobe query to confirm the behavior was the same. The checks also exposed a gap in my parse_query: a bare "size 8" isn't read as a size, so the filter is silently skipped. I couldn't tell which country's sizing "8" meant, so I held off on changing it.
<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
|    empty wardrobe | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 3. outfit names the selected item | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 4. fit card states the real price and platform | 5 of 5 |  PASS | PASS | PASS | PASS | PASS | MET |
| 5. every result within the price ceiling | 5 of 5 | PASS | PASS  | PASS | PASS | PASS | MET |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Every block below is Try 1 of that scenario in `results/run_2026-10-18_2154_before.md`, written by `run_eval.py::main` (which calls `agent.py::run_agent`).

**Criterion 1 — matching query completes** (`agent.py::run_agent`, trace; `tools.py::create_fit_card`, caption). Query: `vintage graphic tee under $30`

```text
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Outfit 1: Y2K Streetwear** Pair the butterfly baby tee with the baggy straight-leg jeans, dark wash (bottoms…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Literal peak 2000s energy right here. Just scored this butterfly baby tee on Depop for $18 and it’s giving maj…
```

```text
Fit card: Literal peak 2000s energy right here. Just scored this butterfly baby tee on Depop for $18 and it’s giving major Y2K streetwear. Throw it on with baggy jeans and chunky sneaks or some khaki trousers and combat boots for the ultimate effortless throwback.
```

**Criterion 2 — impossible query stops early** (`agent.py::run_agent`, branch; `agent.py::_nothing_found_message`, message). Query: `designer ballgown size XXS under $5`

```text
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit
```

```text
Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.
```

**Criterion 3 — outfit names the selected item** (`tools.py::suggest_outfit`)

```text
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)

**Outfit 1: Y2K Casual-Chic**
Pair the baby tee with the baggy straight-leg jeans, dark wash (bottoms, dark blue, indigo) cinched with the brown leather belt. Layer on the slightly cropped vintage black denim jacket (outerwear, black) and finish with the chunky white sneakers (shoes, white) and the black crossbody bag.

**Outfit 2: Streetwear Contrast**
Tuck the butterfly tee into the wide-leg khaki trousers (bottoms, khaki, tan) and throw the oversized grey crewneck sweatshirt (tops, grey, charcoal) loosely over your shoulders. Ground the look with the black combat boots (shoes, black) and carry the black crossbody bag.
```

**Criterion 4 — fit card states the real price and platform** (`tools.py::create_fit_card`)

```text
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)

Y2K fairy is logging on. Found this little butterfly baby tee on depop for just $18, and it’s giving major 2000s mall-rat energy. Layer it over some wide-leg khakis with your favorite combat boots, or keep it classic with baggy indigo denim.
```

**Criterion 5 — every result within the price ceiling** (`tools.py::search_listings`, checked separately because the results file lists only the first three titles). Query: `vintage graphic tee under $30`, ceiling $30

```text
lst_002  $18  Y2K Baby Tee — Butterfly Print
lst_033  $19  Vintage Band Tee — Faded Grey
lst_006  $24  Graphic Tee — 2003 Tour Bootleg Style
lst_015  $26  Vintage Graphic Hoodie — Faded Black
lst_014  $12  Leather Belt — Brown, Braided
lst_034  $14  Bucket Hat — Reversible, Brown Plaid
lst_017  $15  Mesh Long-Sleeve Top — Black
lst_020  $16  Henley Long Sleeve — Washed Burgundy
lst_024  $18  Vintage Polo Shirt — Forest Green
lst_012  $20  Oversized Crewneck Sweatshirt — Vintage Navy
```


---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
(.venv) tofunmio@Oluwatofunmis-MacBook-Air ai201-project2-fitfindr-starter-v2026 % python app.py ask 'vintage graphic tee under $30' --trace

[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
      →    10 match(es)
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: **Outfit 1:** Pair the butterfly baby tee with the baggy straight-leg jeans, dark wash (bottoms, dark blue, in…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Y2K Baby Tee — Butterfly Print ($18.0, depop)
      out: Found this absolute gem of a Y2K butterfly baby tee while digging through the racks, and it's giving major off…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   **Outfit 1:** Pair the butterfly baby tee with the baggy straight-leg jeans, dark wash (bottoms, dark blue, indigo) and layer the vintage black denim jacket (outerwear, black) on top. Finish the look with the chunky white sneakers (shoes, white) for an effortless Y2K street style vibe.

**Outfit 2:** Tuck the baby tee into the wide-leg khaki trousers (bottoms, khaki, tan) secured with the brown leather belt (accessories, brown). Slip on the black combat boots (shoes, black) and throw the black cropped zip hoodie (tops, black) over your shoulders for a casual, contrast-heavy aesthetic.

  Fit card: Found this absolute gem of a Y2K butterfly baby tee while digging through the racks, and it's giving major off-duty Bratz doll energy. You can style it super easy with baggy dark wash denim and chunky sneaks, or tuck it into khaki trousers with combat boots for that perfect contrast. Grabbed this baby tee for just $18 over on my Depop before someone else snags it!

0 model calls this session, 2 served from cache
```

**Empty search**

```
(.venv) tofunmio@Oluwatofunmis-MacBook-Air ai201-project2-fitfindr-starter-v2026 % python app.py ask 'designer ballgown size XXS under $5' --trace

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    0 match(es)
[3] branch
      →    search returned []: stopping before suggest_outfit

  Nothing in the listings matched description 'designer ballgown', size XXS, under $5.
Things to change: try broader words — 'jacket' finds more than 'cropped corduroy jacket'; drop the size, or try a neighbouring one; raise the price ceiling above $5.

0 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->
`search_listings` is registered in `mcp_server.py`, and `run_agent` now calls it only through `call_tool`; the line that called `_search`, which fell back to a direct call, is commented out. Nothing behaved differently: results matched direct calls for four queries, including the empty list and `None` brands.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
