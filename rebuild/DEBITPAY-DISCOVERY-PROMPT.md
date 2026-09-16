# Prompt: does this issuer accept a DEBIT CARD to pay the credit-card bill?

Copy this whole file into a fresh agent. Replace `<ISSUERS>` with the list to check.

---

## The question

For each issuer in `<ISSUERS>`, establish whether a cardholder can pay their credit-card bill **with a debit card** in 2026, on any channel, and how strong the evidence is. We do NOT hold these cards, so you cannot log in. Everything below is a way to answer without an account.

Why it matters: a rewards debit card (interchange-share) may pay ~1.8% on that payment, stacking on top of the card's own cashback. Only the payment rail decides whether the play exists.

## Rule of evidence (non-negotiable)

| Verdict | What it takes |
|---|---|
| **Y** | The issuer's own page, agreement, IVR recording, app screen, or a dated first-hand report from someone who actually did it |
| **N** | The issuer **explicitly states** debit is not accepted, or an exhaustive official payment-methods list omits it |
| **?** | Anything else, including "it settles by ACH so probably not" |

**Never write N from an inference.** "Corporate cards settle by ACH autopay" is not a statement that debit is refused. An unverified issuer is a lead worth keeping, not a dead end. A WalletHub user answer, a content farm, or an AI search summary is never enough for Y or N on its own.

## Part 1 — has anyone already researched this?

Before doing your own digging, find the existing work. Search hard for:

- Doctor of Credit: "pay credit card with debit card", "debit card payment", plus each issuer name. **Read the comments**, which carry the data points.
- FlyerTalk Manufactured Spending forum, especially the long-running megathread *Paying Citi cards with debit cards including prepaid debit cards* (thread 1550209, 119+ pages). Read the **last few pages** for current status, and look for sibling threads covering other issuers.
- myFICO forums, creditcardforum.com, Frequent Miler, MilesTalk, US Credit Card Guide, GC Galore, Miles Per Day.
- Reddit r/churning and r/manufacturedspending. **Reddit may be network-blocked**; if every route returns 403, say so plainly and move on rather than inventing data. Try Google cache, quoted excerpts on other sites, and Reddit-mirroring aggregators.
- Any community-maintained spreadsheet or wiki listing issuers by payment method.

Report what already exists before adding your own findings, and cite it.

## Part 2 — how to verify WITHOUT holding the card

Work down this list, strongest first. Record which method produced each answer.

1. **The CFPB credit card agreement database.** Every issuer must file its cardmember agreements quarterly: https://www.consumerfinance.gov/credit-cards/agreements/ . Full text, free, authoritative. Search the agreement for "debit", "payment method", "acceptable payment". Absence is weak evidence; an explicit clause is strong.
2. **The issuer's own payment / FAQ / help pages.** Search `site:<issuer>.com pay "debit card"`. If the site blocks automated fetching (403), pull the same page out of a search engine's indexed text, or try the print version, the mobile subdomain, or the help-center JSON API.
3. **The automated phone line (IVR).** This is the strongest trick available without an account: most issuer payment IVRs read the tender menu **before** asking you to authenticate. Find the published payment phone number and document what the menu offers. You cannot place the call yourself, so instead search for transcripts, forum posts quoting the menu, and the issuer's own "what you can do by phone" page. Flag the number so a human can call and listen in under a minute.
4. **The payment processor behind the portal.** Many issuers outsource bill payment to ACI Speedpay, Fiserv Biller Solutions / CheckFreePay, or Western Union. Those processors publish **biller directories that list accepted tender types per biller**. Identify the processor (look at the payment page's domain, script hosts, or terms) and then check that processor's biller page. This often answers the question outright.
5. **Walk-in bill-pay networks.** CheckFreePay and MoneyGram at Walmart accept cash or debit at a counter for a wide list of billers. Check whether the issuer is in their biller list, and note the fee.
6. **App store screenshots and reviews.** Issuer app listings often show the "Make a payment" screen. Reviews frequently mention payment-method changes.
7. **The Wayback Machine.** Compare a payment-methods page across 2023, 2024, 2025 and 2026 to catch a rail that was quietly removed, and date the change.
8. **Pre-sales live chat.** The issuer's public chat widget answers payment questions before you are a customer. Note that you cannot use it yourself; flag it for a human.
9. **The fee schedule.** Some issuers disclose a "debit card payment fee" or "expedited payment fee". A disclosed fee is proof the rail exists.

## Part 3 — also capture

- **Channel**: online, app, phone IVR, phone agent, branch, store register, third-party walk-in.
- **Fee** for the debit payment.
- **Limits**: per payment, per day, per card.
- **How it codes**: purchase MCC, bill-pay, or an Account Funding Transaction (MCC 6012 / 6051). This decides whether a rewards debit card pays anything, so flag it wherever a source speaks to it.
- **Commercial vs consumer debit**: Citi blocked **commercial** debit cards as a payment source on 2026-01-30 while consumer debit still worked. Check whether other issuers draw the same line.
- **Whether the policy is per-product or issuer-wide.** Citi is rolling debit-pay back card by card, so an issuer-level answer can be wrong for one product.
- **Date** of every data point.

## Output

Write a strict JSON array to the path given in your task, one object per issuer:

```json
{
 "issuer": "...",
 "products": "which cards this covers, or 'all'",
 "verdict": "Y" | "N" | "?",
 "channel": "online|app|phone-ivr|phone-agent|branch|store|third-party|none|unknown",
 "fee_usd": 0,
 "limit_note": "...",
 "codes_as": "purchase|bill-pay|AFT|unknown",
 "commercial_debit_ok": "Y|N|?",
 "per_product": true,
 "as_of": "YYYY-MM",
 "method": "which of the Part 2 methods produced this",
 "evidence": "<=200 chars, plain words",
 "prior_research": "who already documented this, or 'none found'",
 "phone_to_check": "payment number a human should call, or null",
 "confidence": "high|med|low",
 "sources": ["url", "..."]
}
```

Validate with `python -c "import json;json.load(open(PATH,encoding='utf-8'))"` before finishing. Write the file yourself; do not delegate to sub-agents.

Reply with only: counts of Y/N/?, then one line per issuer as `issuer: verdict, channel, method, confidence`.
