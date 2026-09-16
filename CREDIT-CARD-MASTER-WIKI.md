# Credit Card Master Wiki — v9 (numbers only)

Open `index.html`. 307 cards (272 active / 35 dead) scored for the Costco gold play.

## How a card is scored (Medi's locked rules, 2026-09-15)
- **Costco%@10k / @50k** = % back over a FULL MONTH with that much spend all on this one card; caps, tiers, monthly reward caps applied.
- **Floor%** = no boosts, points cashed at 1¢. **Best case** = every boost, points at TPG Sep-2026 ¢/pt.
- **Where**: 🏬 in-store (Visa credit or PIN debit) · 🌐 Costco.com only (Mastercard/Discover) · ✖ Amex.
- **+Taekus 1.80%** only if the card bill is debit-payable. UNCONFIRMED until a live $1–5 test.
- Crypto cards ranked in the main list with **Lockup $** (stake × token price on 2026-09-15) and monthly reward caps.
- ⚠ review = non-crypto over 6% or low-confidence over 6%.

## Rebuild
1. Source prose: `agent*.md`, `gapfill*.md` → `cards-data.json` (old v8 parser, kept for provenance).
2. `rebuild/batches/*.json` → 8 LLM extraction agents (prompt: `rebuild/EXTRACTION-PROMPT.md`) → `rebuild/out/*.json`.
3. `rebuild/spotcheck.json` = second-agent verification of the top 30 (fixes merged automatically).
4. `python rebuild/build.py` → `cards.json` + `index.html` (template: `rebuild/template.html`).

Constants in `build.py`: TAEKUS=1.80, MAX_SWIPE=5000, SANITY=6.0. Change and rerun.
