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
**Moment 3**

- *What I asked for:*
 After my verdicts were all MET, I asked Claude to argue the opposite verdict as strongly as it could.
- *What came back:*
Arguments against each criterion. The strongest were that criterion 5 never tested the boundary and that some fit cards sounded like a seller.
- *What I changed:*
 I put both points in my Diagnoses section and fixed the seller voice. I kept the verdicts, since the sentences as written were satisfied.

**Moment 4**

- *What came back:*
Claude suggested adding "the writer found this item secondhand… the buyer, not the seller" to the fit card prompt. I asked where it got "secondhand" from.
- *What came back:*
It said it inferred it from the README and docstrings ("thrift shopper", "the item the user is considering"), and that "buyer" was an assumption, since nothing in the data says a purchase happened.
- *What I changed:*
 I had it soften the wording to "The writer is a shopper posting about a thrift find. They are not selling it…", and then I re-ran the whole test.
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
| 1 | Matching query completes | 4 of 5 | MET (5/5) | All 5 tries ran parse_query, search_listings, suggest_outfit and create_fit_card and ended with a non-empty fit card. |
| 2 | Impossible query stops early | 5 of 5 | MET (5/5) | All 5 tries stopped at the branch with no suggest_outfit step and printed a "Things to change" message naming broader words, size and price. |
| 3 | Outfit names the selected item | 4 of 5 | MET (5/5) | Every outfit said "baby tee", "butterfly tee" or "Y2K baby tee" for the selected Y2K Baby Tee, not a generic word like "top" or "tee". |
| 4 | Fit card states the real price and platform | 5 of 5 | MET (5/5) | Every fit card said $18 and Depop and no other price. |
| 5 | Every result within the price ceiling | 5 of 5 | MET (5/5) | The results file lists only the first three titles, so I checked all 10 returned prices with a separate search_listings run: the highest was $26, none over $30. Reproduce with `python check_prices.py`. |

**Diagnoses**

I missed nothing: all five criteria were met against their targets. One pattern showed up anyway, and it is in the model's output, not in a tool or the loop. In 3 of the 5 captions in the criterion 4 run, the fit card sounds like a seller ("I'm listing it on Depop today", "on my Depop"). The cause is in my `create_fit_card` prompt: it passes `Platform: depop` but never says the user is the buyer who found the item, so the model guesses a seller's voice. The price and platform are stated correctly, so criterion 4 as written is still met, but the card is not what I wanted.

My targets were probably low. Criteria 1 and 2 were given to me, so I don't count their targets as mine. Of the three I wrote, criterion 3 had a target of 4 of 5 and passed 5 of 5, so I would raise it to 5 of 5. I would also tighten criterion 4 so a caption only passes if it states the price and platform and has no seller wording, in 5 of 5 captions. Criterion 5 is already 5 of 5, so what I would tighten there is the test: its highest result was $26 against a $30 ceiling, so no listing was near the boundary and a `<` instead of `<=` mistake would not have shown. A ceiling just below a listing's price would test it. I have left all the criteria as written.

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

In `tools.py`, I added two sentences to the `create_fit_card` prompt: "The writer is a shopper posting about a thrift find. They are not selling it: do not say they are listing or selling the item." The platform line now also says "(where they found it)". Nothing else changed: same item data, same system prompt, same price and platform requirement.

**Which failure it was meant to fix:**

The seller voice from my diagnosis. In 3 of the 5 captions in the criterion 4 run, the fit card sounded like a seller ("I'm listing it on Depop today", "on my Depop"). It was a failure in the model's output, caused by my prompt: it passed `Platform: depop` but never said who the writer is, so the model guessed a seller. Criterion 4 as written was still met, because the price and platform were correct, so this was a quality problem my criteria did not catch.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. outfit names the selected item | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card states the real price and platform | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. every result within the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

**Run logs side by side.** Before: `results/run_2026-10-18_2154_before.md`. After: `results/run_2026-10-18_2339_after.md`. Both ran 5 tries per scenario with caching off at temperature 0.9.

| Criterion | Before | After |
|---|---|---|
| 1. matching query completes (4 of 5) | 5/5 | 5/5 |
| 2. impossible query stops early (5 of 5) | 5/5 | 5/5 |
| 3. outfit names the selected item (4 of 5) | 5/5 | 5/5 |
| 4. fit card states the real price and platform (5 of 5) | 5/5 | 5/5 |
| 5. every result within the price ceiling (5 of 5) | 5/5 | 5/5 |
| *Not a criterion:* fit card sounds like a seller | 3 of 5 captions | 0 of 5 captions |

Yes, it helped, on the thing it was meant to fix. None of my five criteria changed, because none of them measures the voice. I counted the seller voice by scanning the 5 captions in the criterion 4 scenario for "listing", "listed", "selling", "for sale", "my Depop" and "just dropped". Before, 3 of 5 had it. After, none did, and every caption still said $18 and Depop, so the facts did not get worse.

Before (Try 3): "Found this Y2K butterfly baby tee for just $18 and I’m obsessed. I’m listing it on Depop today, but honestly debating keeping it for myself to wear with baggy jeans and chunky sneakers. Such a nostalgic, effortless street style vibe!"

After (Try 1): "Found this sweet little butterfly print Y2K baby tee on Depop for just $18 and I'm obsessed. I'm thinking about styling it with baggy dark-wash jeans and a cropped zip hoodie for total nostalgic streetwear vibes, or grounding it with some edgy combat boots and khaki trousers. Such a good little score!"

This is a small sample: 5 captions each, from a model at temperature 0.9. It shows the change moved the pattern, not that the seller voice can never come back. Criterion 5 is unchanged by design, since the change only touched `create_fit_card`.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->
All my criteria met. However, there are still some things broken 
- A bare "size 8" is ignored. parse_query('platform sneakers size 8') returns size: None, so the filter is skipped silently. This is the starter's own example query.
- A price without $ is ignored. "jacket nothing over thirty dollars" returns max_price: None, so the search has no ceiling and says nothing. The parse_query docstring admits this limitation.
- Singular and plural don't match. 'jean' returns 0 results but 'jeans' returns 3. 'sneaker' returns 0 and 'sneakers' 2. 'tees' returns 0 but 'tee' returns 5. A query whose only matching word is the wrong form comes back empty, and the loop stops. If other words match (like "jean jacket", which gave 4 results), it still works.

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
