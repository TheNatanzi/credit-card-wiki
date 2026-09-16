# Structured extraction task (credit-card wiki rebuild)

You are given a JSON array of credit/debit card records with PROSE fields (base, boosted, grocery, costco, debitpay, annualfee, fxfee, special, caps...). Convert EVERY record into one strict-JSON object with NUMBERS ONLY. Same order, same count. Echo `card` exactly.

Reference for points values: `C:/Claude/credit-card-wiki/points-valuations.md` (TPG Sep-2026 ¢/pt). Use WebSearch/WebFetch only when the prose lacks a number you need (e.g. live crypto token price for lockup, FX fee %, cap). Do not rewrite prose; you output numbers.

## Output object schema (all keys required)
```
{
 "card": "<exact echo>",
 "issuer": "<short issuer name>",
 "network": "visa"|"mastercard"|"amex"|"discover"|"other"|"unknown",
 "product": "credit"|"debit"|"prepaid",
 "biz": "P"|"B",                      // business card -> B, else P
 "status": "active"|"dead",           // dead = discontinued / shut down / waitlist-never-launched
 "reward_unit": "cash"|"points"|"crypto",
 "cpp_max": <number>,                 // ¢ per point at realistic BEST use (TPG value). cash or crypto -> 1.0
 "cpp_floor": <number>,               // ¢ per point when CASHED OUT / statement credit. cash -> 1.0. points cashable at 1¢ -> 1.0. If NOT cashable at 1¢ (hotel/airline miles) use the TPG low-range value.
 "base_x": <number>,                  // flat ALL-spend earn rate, units per $1 (2 = 2% or 2x). No boosts, no stake.
 "costco_x_max": <number>,            // earn rate at a Costco WAREHOUSE register (MCC 5300, NOT 5411 grocery) with EVERY achievable boost applied: relationship tiers (BofA Platinum Honors, US Bank $100k balance), biggest crypto stake tier, top spend tier. Category bonuses (grocery/dining/travel/gas) do NOT apply unless prose says Costco/wholesale clubs explicitly count. Costco GAS rates never count.
 "costco_x_min": <number>,            // same, but ZERO boosts: no relationship balance, no stake, lowest tier. Usually == base_x.
 "costco_cap_usd": <number|null>,     // spend $ cap on the costco_x rates (bonus reverts to base_x above it). null = no cap.
 "cap_period": "month"|"cycle"|"quarter"|"year"|"none",
 "reward_cap_usd_month": <number|null>, // hard $ cap on rewards paid per month (crypto cards often). null = none. Convert weekly x4.33, yearly /12.
 "min_txn_usd": <number|null>,        // bonus rate needs a SINGLE purchase >= this $ (e.g. "2.5% on $5k+ purchases"). null if none.
 "fee_usd": <number>,                 // annual fee $, 0 if none. Monthly fees x12.
 "fx_pct": <number>,                  // foreign transaction fee %. 0 if none. If prose says "has FX fee" but no number -> 3.
 "debit_pay": "Y"|"N"|"?",            // can the card BILL be paid with a debit card (any channel: online/phone/branch). "?" only if truly unknown.
 "lockup_usd": <number|null>,         // crypto: $ value of stake/lock required for costco_x_max tier (stake amount × live token price today). null for non-crypto or no stake.
 "source": "<url>",
 "why": "<=110 chars, the one line that explains the Costco number>",
 "confidence": "high"|"med"|"low",
 "needs_research": ["field", ...]     // fields you had to guess. [] if none.
}
```

## Hard rules (Medi's locked rules)
1. Never leave a field null when a number is derivable. Guess -> list it in needs_research.
2. Do NOT zero Mastercard/Discover — the page decides where the card works (Costco.com takes them). You only output the rate.
3. Do NOT let "5% travel", "3% grocery (excl. wholesale)", "Costco gas 4x" leak into costco_x. Costco warehouse counts ONLY for: flat all-spend rates, purchase-size tiers, relationship boosts, or a bonus whose prose explicitly includes Costco / warehouse clubs / MCC 5300.
4. Relationship boosts (BofA Preferred Rewards 75%, US Bank Smartly balance tiers, Robinhood Gold, crypto stake) go in costco_x_max only; costco_x_min = unboosted.
5. Points: costco_x_* are in POINTS per $; the page multiplies by cpp. Cash: percent number.
6. Crypto cards: put the top-tier rate in costco_x_max and its stake $ in lockup_usd (look up today's token price with WebSearch, note date in why). Put the no-stake tier in costco_x_min. Monthly reward caps go in reward_cap_usd_month.
7. status="dead" if prose says discontinued, closed to new applicants, shut down, or a never-launched waitlist.
8. Sanity: a non-crypto costco_x_max above 6 (i.e. >6%) must be double-checked and confidence set "low" unless the prose is explicit.

## Output
Write the JSON array to the output path given in your task. Validate it with `python -c "import json;json.load(open(PATH,encoding='utf-8'))"` before finishing. Reply with only: count written, list of cards with confidence low, and any card you could not place.
