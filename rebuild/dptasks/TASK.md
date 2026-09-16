# Task: verify the debit-pay rail for an assigned set of credit cards

1. Read `C:\Claude\credit-card-wiki\rebuild\DEBITPAY-DISCOVERY-PROMPT.md` in full. It is the method and the rule of evidence. Follow it exactly.
2. Read your assigned card list at `C:\Claude\credit-card-wiki\rebuild\dptasks\<GROUP>.json`.
3. Answer, for EACH card in that list: can a cardholder pay that credit-card bill with a DEBIT CARD in 2026?

## Hard rules
- **N only when the issuer explicitly refuses debit, or an exhaustive official payment-methods list omits it.** Never write N from an inference like "it settles by ACH".
- **Y needs the issuer's own page/agreement/app screen/IVR, or a dated first-hand report.** WalletHub user answers, content farms and AI search summaries are NEVER enough on their own.
- Anything else stays `?`. A `?` is a live lead, not a failure.
- **Per-product, not per-issuer.** Citi is rolling debit-pay back card by card, so answer each card. If the evidence is genuinely issuer-wide, say so in the note and apply it to each card.
- **Do the work yourself.** Do NOT spawn sub-agents. Two prior agents delegated and exited without writing their file.
- Note commercial vs consumer debit where it differs (Citi blocked commercial debit cards 2026-01-30).
- Reddit is network-blocked here. If every route 403s, say so; do not invent data.

## Output
Write a strict JSON array to `C:\Claude\credit-card-wiki\rebuild\dp_out_z_<GROUP>.json`, ONE OBJECT PER CARD, using exactly this shape (card name must match the input list verbatim):

```json
{
 "card": "exact name from the input list",
 "fixes": {"debit_pay": "Y"},
 "channel": "online|app|phone-ivr|phone-agent|branch|store|third-party|none|unknown",
 "fee_usd": 0,
 "posts_as": "purchase|bill-pay|AFT|unknown",
 "commercial_debit_ok": "Y|N|?",
 "changed": "when the policy changed, or 'no change found'",
 "as_of": "YYYY-MM",
 "method": "which DEBITPAY-DISCOVERY-PROMPT Part 2 method produced this",
 "prior_research": "who already documented this, or 'none found'",
 "phone_to_check": "payment number a human should call, or null",
 "note": "<=250 chars, plain words, why this verdict",
 "confidence": "high|med|low",
 "sources": ["url"]
}
```

`fixes.debit_pay` must be `"Y"`, `"N"` or `"?"`. Include every card, even the ones that stay `?`.

Validate before finishing:
`python -c "import json,io;d=json.load(io.open(r'C:\Claude\credit-card-wiki\rebuild\dp_out_z_<GROUP>.json',encoding='utf-8'));print(len(d))"`

Reply with only: counts of Y/N/?, then one line per card as `card: verdict, channel, method, confidence`.
