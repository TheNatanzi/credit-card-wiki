# Does Taekus reward paying a credit-card bill (AFT / MCC 6012–6051)?

**VERDICT: UNCONFIRMED — leans NO / RISKY for the Taekus → Capital on Tap stack.**
No public source confirms Taekus pays rewards on a credit-card bill payment, and the reward
mechanism (interchange-share) plus the way debit→credit-card payments are usually coded
(Account Funding Transaction, MCC 6012/6051 — a cash-equivalent/debt-repayment class that
generates little or no interchange and is routinely reward-excluded) both point against it.
**Do not assume the stack works. It must be settled with a live $1–$5 test** (see "What would
confirm" at the bottom) before committing real volume.

_Researched 2026-09-15. All facts below are sourced; the load-bearing unknowns are stated explicitly._

---

## The core mechanism (this is what decides it)

Taekus rewards are **not** a flat "we pay X% on everything." They are a **share of the
interchange** the transaction generates:

- Taekus cards (personal, business, corporate) "operate under an **interchange share model**,"
  and because the sponsor bank has **under $10B in assets it is exempt from the Durbin
  amendment and keeps full (unregulated) interchange** on most transactions, which is what
  funds the rebate. (search summaries citing the MS community / Crunchbase profile)
- Consequence: **Taekus can only rebate you if the transaction actually generated meaningful
  interchange.** No interchange → nothing to share → no (or trivial) reward.

That single fact is why the answer hinges on **transaction coding**, not on Taekus's goodwill.

## What Taekus is (confirmed)

- **Debit / prepaid card, NOT a credit card.** Product is the "Taekus Prepaid Account and Debit
  Card." (CFPB prepaid-agreement listing; Taekus Commercial Debit Card Agreement PDF)
- **Issuer:** Stearns Bank National Association (sponsor bank). Program run by Taekus Corp /
  GoGreen FI LLC. (Commercial Debit Card Agreement, lines 52–60; CFPB listing)
- **Business/commercial use:** the commercial account agreement states the account is for
  business/commercial purposes, not personal/household. (agreement text)
- **Reputation:** widely called in the churning/MS community "the best debit card for
  manufactured spending," and it supports micropayment rebates (e.g. ~9¢ back on a 14¢
  transaction). It is invite-only. (search summaries; myFICO "Secret invite-only cards" thread)
- **Note on the agreement's "Bill payment — Feature not currently available" line:** that refers
  to Taekus's *own outbound* bill-pay feature (paying a biller *from* the Taekus account), **not**
  to swiping the Taekus debit card at a credit-card issuer's payment portal. Do not read it as
  an answer to this question. (Commercial Debit Card Agreement fee table)
- **The debit-card agreement does NOT contain the reward-earning / exclusion rules.** Rewards
  are governed by a separate rewards terms document that is behind the invite/login and was not
  publicly retrievable. **This is the single most important missing primary source.**

## How a debit-card payment to a credit card is coded (the crux)

When you pay a credit-card bill with a debit card, **the receiving side (the credit-card issuer's
payment processor) decides the coding**, and it is typically one of:

1. **Account Funding Transaction (AFT), MCC 6012 or 6051 ("Financial Institutions" / debt
   repayment).** Visa and Mastercard **mandated** that debt-repayment transactions on debit/prepaid
   cards be coded under MCC 6012/6051. These are treated as **cash-equivalent / debt repayment**,
   carry **low or no purchase interchange**, and are **commonly excluded from rewards** by issuers
   specifically to stop cash-out/MS abuse. (Worldpay "Financial Services MCC 6012/6051" docs;
   Nomupay MCC 6012; Host Merchant Services; NerdWallet MCC guide)
2. A normal **purchase (POS) transaction** at the biller's own MCC — which *would* generate
   ordinary interchange that Taekus could share.

**If Capital on Tap's inbound debit payment codes as (1) AFT/6012, Taekus's interchange-share
engine has little or nothing to rebate → effectively no reward.** If it codes as (2) a purchase,
Taekus would likely reward it. **Which one Capital on Tap uses could not be confirmed from public
sources.** Capital on Tap does accept debit-card payments (one-time via the Payments page in the
portal, or recurring direct debit) — so the *payment* is possible; the open question is purely the
*coding*. (Capital on Tap FAQ / Bill Pay pages)

## Community evidence

- The FlyerTalk manufactured-spending thread **"Paying Citi cards with debit cards including
  prepaid debit cards"** (116+ pages) is the canonical MS technique here. Its wiki flags that
  **several debit cards earn "no miles" / "(no cb)"** when used to pay a credit card — i.e.
  reward-earning on debit→credit-card payments is **card- and coding-specific and NOT guaranteed.**
  This is direct evidence that some debit cards get zeroed out on exactly this move. (FlyerTalk MS
  thread wiki)
- **No public data point was found** specifically confirming (or denying) that a **Taekus** card
  earns rewards on a **credit-card bill payment**, and none for the **Taekus → Capital on Tap**
  combination in particular. Reddit r/churning and Doctor of Credit searches returned nothing
  specific; the myFICO and FlyerTalk threads discuss Taekus generally but not this exact outcome.

## Why the answer is not a clean "yes"

The strategy assumed ~1.8% Taekus reward stacking on top of Capital on Tap's 2%. That stack only
holds if the Capital on Tap payment reaches Taekus as an **interchange-generating purchase.** The
default coding for debit-to-credit-card payments (AFT / MCC 6012–6051) is precisely the class that
generates minimal interchange and is routinely reward-excluded — so the base assumption behind the
stack is the thing most likely to fail.

## What would confirm it (do these before trusting the stack)

1. **Live micro-test (most decisive):** pay **$1–$5** of a Capital on Tap balance with the Taekus
   debit card, then check the **Taekus app rewards ledger** after it posts. If a rebate accrues
   proportional to the amount, rewards ARE earned; if $0, they are excluded.
2. **Read the MCC in the Taekus transaction feed** for that test payment — 6012/6051 = AFT
   (expect no/low reward); a retail/biller MCC = purchase (expect reward).
3. **Get Taekus's actual rewards terms / exclusions list** (behind the invite/login) — look for
   "account funding," "cash equivalent," "quasi-cash," "debt repayment," or MCC 6012/6051 in the
   excluded list.
4. **A churning data point** — a dated r/churning or Doctor of Credit report of Taekus rewarding a
   Capital on Tap (or any credit-card) payment.

Until at least #1 is done, treat the reward stack as **unproven**.

---

### Sources
- Taekus Commercial Debit Card Agreement (PDF, Stearns Bank / Taekus Corp): https://uploads-ssl.webflow.com/602af9837050241ae008b45c/64274d64f9d51a02d474fd75_FINAL%20V3_Taekus%20Commercial%20Debit%20Card%20%20Agreement%20(02-17-2023).pdf
- CFPB — Taekus Prepaid Account and Debit Card Agreement listing: https://www.consumerfinance.gov/data-research/prepaid-accounts/search-agreements/detail/254969/
- myFICO forum — "Secret invite-only cards: What's the deal with Taekus?": https://ficoforums.myfico.com/t5/Credit-Cards/Secret-invite-only-cards-What-s-the-deal-with-Taekus/td-p/6750147
- FlyerTalk (MS) — "Paying Citi cards with debit cards including prepaid debit cards": https://www.flyertalk.com/forum/manufactured-spending/1550209-paying-citi-cards-debit-cards-including-prepaid-debit-cards-116.html
- Worldpay — Financial Services incl. MCC 6012 / 6051: https://docs.worldpay.com/access/products/payments/enable-features/financial-services-mcc6012-mcc6051
- Nomupay — Merchant Category Code 6012: https://nomupay.com/support/merchant-category-code-6012/
- Host Merchant Services — What is Merchant Code 6012: https://hostmerchantservices.com/articles/what-is-merchant-code-6012/
- Capital on Tap — FAQ (debit-card payment): https://www.capitalontap.com/us/faq/
- Capital on Tap — Bill Pay: https://www.capitalontap.com/en/business-credit-cards/bill-pay/
- Crunchbase — Taekus profile: https://www.crunchbase.com/organization/taekus
