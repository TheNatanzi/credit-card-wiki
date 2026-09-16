# Deep research: "what is really behind the number" (top cards, ≥2.1% at Costco)

You get a few card records from C:/Claude/credit-card-wiki/rebuild/deep-targets.json (already extracted numbers).
Your job: verify EVERYTHING that decides what a Bay Area (California) resident actually nets when putting
$10,000/month and $50,000/month of Costco WAREHOUSE purchases (MCC 5300, gold bars ~$3,800 each, several swipes) on this card.
Use WebSearch + WebFetch on the ISSUER's own pages first (terms, fee schedule, rewards T&C, help center), then 2026 reviews (Doctor of Credit, NerdWallet, TPG, Reddit r/churning, r/CryptoCurrency).

## Bases to cover for EACH card
1. **Availability**: can a US / California resident get it today? (Many crypto cards are non-US. Bybit is NOT US.) Waitlist? Invite-only? Business-only?
2. **Tier ladder**: every tier with its rate, how you qualify (stake $ / VIP level / monthly spend / balance / subscription), and the MONTHLY reward or point CAP for that tier. Caps kill high rates: Bybit 10% caps at 600 USDT/mo.
3. **All costs**: annual/monthly fee, subscription (Gold, Metal, One), staking lockup $ and lock duration, top-up / load fee %, crypto conversion spread %, card issuance fee, inactivity fee, ATM/FX, plus the cost of holding a volatile token.
4. **Costco reality**: network (Visa / Mastercard / Discover / Amex; new Capital One Venture accounts are on Discover since Feb 2026), does the reward apply to MCC 5300 warehouse (not grocery 5411), any exclusion for "large purchases", "gift cards", "precious metals", "bullion"? PIN-debit at Costco register ok?
5. **Bill payment by debit card** (credit cards only): any channel online/phone/branch accepts a debit card? That enables the Taekus stack.
6. **Risk flags**: account shutdown reports for MS / gold buying, clawback clauses, "we may cap rewards at our discretion", prepaid cards that block $3,800 swipes (per-transaction limits!), daily spend limits, load limits.
7. **Per-transaction and daily limits**: max single purchase and max daily spend. A $2,000/day limit makes $50k/month impossible.

## Output (strict JSON array, one object per card, `card` echoed exactly)
```
{
 "card": "<exact echo>",
 "us_ok": "Y"|"N"|"?",
 "status": "active"|"dead",
 "network": "visa"|"mastercard"|"amex"|"discover"|"other"|"unknown",
 "debit_pay": "Y"|"N"|"?",
 "fee_usd": <annual $ incl. required subscription>,
 "fx_pct": <number>,
 "extra_cost_pct": <number>,          // % lost per $ spent on top-up/conversion/spread/load. 0 if none.
 "txn_max_usd": <number|null>,        // max single purchase, null if none/unknown
 "daily_max_usd": <number|null>,      // max daily spend, null if none/unknown
 "tiers": [                            // lowest to highest; include the no-stake tier first
   {"name": "...", "min_spend_month_usd": <number|null>, "lockup_usd": <number|null>, "lock_months": <number|null>,
    "rate_pct": <number>, "reward_cap_month_usd": <number|null>, "monthly_cost_usd": <number>}
 ],
 "costco_ok": "Y"|"N"|"?",            // reward actually earned at MCC 5300 warehouse
 "special": [                          // the SPECIAL CIRCUMSTANCES Medi must know, plain words, <=7 items, <=140 chars each
   {"kind": "cap"|"cost"|"eligibility"|"limit"|"risk"|"costco"|"tip", "text": "..."}
 ],
 "real10_pct": <number>,               // YOUR computed real % back on $10,000/month after caps, tier reachable at that spend, minus extra_cost_pct (not fee)
 "real50_pct": <number>,               // same for $50,000/month
 "confidence": "high"|"med"|"low",
 "sources": ["url", ...]               // 2-6 urls, issuer pages first
}
```
Rules: numbers only in numeric fields; if a fact cannot be found, use your best estimate and add a "risk" special saying it is unverified. Never leave `special` empty: every card has at least one catch (or say "no catch found on issuer site" as kind "tip").
Write the array to the output path given in your task. Validate with `python -c "import json;json.load(open(PATH,encoding='utf-8'))"`. Reply with ONLY: count written + one line per card "<card>: real10 / real50, biggest catch".
