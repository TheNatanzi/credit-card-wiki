# -*- coding: utf-8 -*-
"""Build rebuild/deep/out_G.json from the 4 sub-agent research passes (2026-09-16)."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\Claude\credit-card-wiki"

def C(card, **k):
    d = dict(card=card, us_ok="Y", status="active", fx_pct=0, extra_cost_pct=0,
             txn_max_usd=None, daily_max_usd=None, costco_ok="Y", confidence="med")
    d.update(k)
    return d

def T(name, rate, cap=None, mc=0):
    return {"name": name, "min_spend_month_usd": None, "lockup_usd": None, "lock_months": None,
            "rate_pct": rate, "reward_cap_month_usd": cap, "monthly_cost_usd": mc}

def S(k, t):
    return {"kind": k, "text": t}

G = [
C("Capital on Tap Business (US)", network="visa", debit_pay="Y", fee_usd=0, real10_pct=3.6, real50_pct=3.0,
  tiers=[T("Standard, no AutoPay", 1.5), T("Weekly AutoPay enrolled", 2.0)],
  special=[
    S("limit", "Advertised up to $50,000 but typical approvals are far lower; the limit grows by periodic review after 3-6 months, not at signup."),
    S("tip", "AutoPay terms: a mid-cycle manual or debit payment does NOT cancel AutoPay enrollment, so 2% should survive the debit rail. No user report confirms this exact combo."),
    S("eligibility", "Needs an LLC or Corp with an EIN, a 25%+ owner, 6+ months trading and about $30k a year in revenue. Sole proprietors reported not eligible."),
    S("cost", "No fee found for a one-time debit-card payment on the Payments page, but it is not explicitly guaranteed fee-free."),
    S("risk", "Trustpilot shows accounts suspended or closed with little warning; WebBank actively monitors risk."),
    S("tip", "Weekly payoff recycles a modest limit about 4 times a month, which is how you reach high monthly volume on a small line."),
  ],
  sources=["https://www.capitalontap.com/us/faq/",
           "https://thepointsguy.com/credit-cards/reviews/capital-on-tap-business-credit-card-review",
           "https://www.capitalontap.com/en/blog/posts/why-we-suspend-or-close-accounts/"]),

C("Costco Anywhere Visa Business Card by Citi", network="visa", debit_pay="Y", fee_usd=65, real10_pct=3.8, real50_pct=3.4,
  tiers=[T("Costco warehouse and Costco.com", 2.0), T("All other purchases", 1.0)],
  special=[
    S("limit", "Reported starting limits run roughly $1,500 to $5,000, occasionally near $25,000 for strong files."),
    S("eligibility", "Requires an active paid Costco Business membership at $65 a year; each employee authorized user needs their own membership."),
    S("cost", "Debit payment is phone-only on 800-950-5114 and posts the same day; no convenience fee found."),
    S("costco", "Warehouse purchases at MCC 5300 including gold bars get the full 2%; only FX, travelers checks, money orders, wires and gambling are excluded."),
    S("tip", "Same-day posting lets you pay down mid-cycle and recycle a smaller limit several times a month."),
  ],
  sources=["https://www.citi.com/credit-cards/costco-anywhere-visa-business-card",
           "https://www.citi.com/credit-cards/credit-card-rewards/earn-cash-back-with-costco-credit-card"]),

C("Costco Anywhere Visa Card by Citi", network="visa", debit_pay="Y", fee_usd=65, real10_pct=3.8, real50_pct=3.3,
  tiers=[T("Costco warehouse and Costco.com", 2.0), T("All other purchases", 1.0)],
  special=[
    S("limit", "Reported limits run from about $500 up to roughly $11,900; no guaranteed starting figure."),
    S("eligibility", "Needs a paid Costco Gold Star or Executive membership in your own name. Personal application, no business required, so it is the easiest of the three."),
    S("cost", "Debit payment by phone on 800-950-5114 posts immediately; no convenience fee found."),
    S("costco", "Warehouse purchases at MCC 5300 including gold bars earn the full 2%."),
    S("risk", "Personal card, so sustained high balances hit your personal utilization and can trigger a Citi line review."),
    S("tip", "Same-day debit payments let a smaller personal limit be recycled several times a month."),
  ],
  sources=["https://www.citi.com/credit-cards/costco-anywhere-visa-card",
           "https://www.citi.com/credit-cards/credit-card-rewards/earn-cash-back-with-costco-credit-card"]),

C("Wells Fargo Active Cash", network="visa", debit_pay="?", fee_usd=0, fx_pct=3, real10_pct=2.0, real50_pct=2.0, confidence="low",
  tiers=[T("Flat 2% on everything", 2.0)],
  special=[
    S("limit", "Guaranteed minimum $1,000; average reported about $6,091 with $3,000 most common. Reviews about every 6 months."),
    S("cap", "The Wells Fargo FAQ lists only app, online and phone payment. No Wells Fargo page confirms debit at a branch."),
    S("risk", "A second source claims Wells Fargo accepts only bank transfers. The branch-debit claim is contested, so this stays a lead, not a confirmed rail."),
    S("risk", "Forum reports say branch and teller payments sometimes miscode, for example as a cash advance."),
    S("tip", "Flat and uncapped, so Costco MCC 5300 earns the full 2% with no category exclusion."),
  ],
  sources=["https://www.wellsfargo.com/help/credit-cards/credit-card-faqs/",
           "https://www.wellsfargo.com/credit-cards/active-cash/guide-to-benefits/"]),

C("Wells Fargo Signify Business Cash", network="mastercard", debit_pay="?", fee_usd=0, fx_pct=3, real10_pct=2.0, real50_pct=2.0, confidence="low",
  tiers=[T("Flat 2% on all business purchases", 2.0)],
  special=[
    S("limit", "Guaranteed minimum $2,500; reports up to about $14,000 for strong income."),
    S("eligibility", "Sole proprietor is fine with an SSN, no EIN needed. Wells Fargo typically wants about a year of history and a 700+ score."),
    S("cap", "Same unverified branch-debit claim as the personal cards; no Wells Fargo page confirms it."),
    S("tip", "Unlimited flat 2% with no caps or categories, so Costco earns the full rate."),
    S("risk", "Approval pulls the owner's personal credit and a Small Business Financial Exchange report, tying the spend to your own file."),
  ],
  sources=["https://www.wellsfargo.com/biz/business-credit/credit-cards/signify-business-cash-credit-card-terms-conditions/",
           "https://www.doctorofcredit.com/wells-fargo-signify-business-credit-cards/"]),

C("Wells Fargo Autograph", network="visa", debit_pay="?", fee_usd=0, real10_pct=1.0, real50_pct=1.0, confidence="low",
  tiers=[T("Base 1x, Costco is not a bonus category", 1.0)],
  special=[
    S("costco", "Costco MCC 5300 is not in the 3x categories, so it earns base 1x only, per the Wells Fargo terms."),
    S("limit", "Guaranteed minimum $1,000; average around $8,971, with reports from $2,500 to $20,000."),
    S("cost", "Correction: the Wells Fargo terms state the foreign transaction fee is None, not 3%."),
    S("tip", "Points cash out near 1 cent each; no higher cash-out rate is documented."),
    S("cap", "Same unverified branch-only debit claim as the other Wells Fargo cards."),
  ],
  sources=["https://www.wellsfargo.com/credit-cards/autograph-visa/terms/"]),

C("Wells Fargo Autograph Journey", network="visa", debit_pay="?", fee_usd=95, real10_pct=1.0, real50_pct=1.0, confidence="low",
  tiers=[T("Base 1x, Costco is not a bonus category", 1.0, mc=7.92)],
  special=[
    S("costco", "Costco misses the 5x hotel, 4x airline and 3x dining bonuses and earns base 1x only."),
    S("cost", "Correction: the foreign transaction fee is None per the Wells Fargo terms."),
    S("tip", "The 1.75 cents per point figure is unconfirmed; 2026 sources put portal and cash redemption near 1 cent."),
    S("cap", "A $95 annual fee plus the same unverified branch-only debit claim."),
  ],
  sources=["https://www.wellsfargo.com/credit-cards/autograph-journey-visa/terms/"]),

C("Wells Fargo Business Elite Signature", network="visa", debit_pay="?", fee_usd=125, status="dead", real10_pct=1.5, real50_pct=1.5,
  tiers=[T("Cash-back option, chosen at opening", 1.5, mc=10.42)],
  special=[
    S("eligibility", "Closed to new applicants since the 2023 Wells Fargo business-card sunset. Replaced by Signify Business Cash."),
    S("eligibility", "$1 million or more in annual sales is a stated hard threshold, so a small business will not qualify."),
    S("cap", "The 1.5% cash back is a redemption choice made at account opening, not a default."),
    S("tip", "Correction: the foreign transaction fee is 0%, not 3%, per the Wells Fargo product page."),
    S("tip", "The branch-only debit claim could not be verified; treat it as unconfirmed."),
  ],
  sources=["https://www.doctorofcredit.com/wells-fargo-business-elite-credit-card-review-1000-sign-bonus-1-5-cash-back-purchases/"]),

C("Alliant Cashback Visa Signature", network="visa", debit_pay="Y", fee_usd=0, status="dead", real10_pct=1.5, real50_pct=1.5,
  tiers=[T("Flat rate for all cardholders, after 2025-11-01", 1.5)],
  special=[
    S("eligibility", "The 2.5% checking-account tier was eliminated card-wide on 2025-11-01. Every cardholder is now on a flat 1.5%."),
    S("eligibility", "Closed to new applicants as of 2026. Only legacy holders keep it."),
    S("cost", "Debit-pay stands: the Alliant help page says members can make a one-time payment using a debit card or an external bank account. Payment line 800-328-1935. A second pass called it ACH-only, but that describes Bill Pay, a different product."),
    S("costco", "No wholesale-club exclusion in the Alliant terms, so Costco earns the same flat rate."),
    S("risk", "Alliant has a documented pattern of closing accounts flagged for suspected manufactured spending."),
    S("limit", "Limit data is thin; a 2019 review cited a $10,000 minimum. The current typical limit is unconfirmed."),
  ],
  sources=["https://www.alliantcreditunion.org/help/where-can-i-call-to-make-a-credit-card-payment",
           "https://www.doctorofcredit.com/alliant-2-5-card-will-become-1-6-on-all-purchases-effective-9-1-25/",
           "https://www.cnbc.com/select/alliant-cashback-visa-signature-review/"]),

C("Citi Custom Cash", network="mastercard", debit_pay="Y", fee_usd=0, fx_pct=3, status="dead", real10_pct=1.0, real50_pct=1.0, confidence="high",
  tiers=[T("Top category 5%, grocery MCC 5411 only, not Costco", 5.0, cap=25),
         T("Base rate, applies to Costco MCC 5300", 1.0)],
  special=[
    S("eligibility", "Closed to new applications since 2026-05-28 per Citi. Existing holders are unaffected, and a product change from another Citi card may still work."),
    S("costco", "The Citi grocery terms explicitly exclude warehouse clubs, so Costco earns the base 1% only."),
    S("cap", "The 5% cap is $500 of spend per cycle, worth $25. Moot at Costco, which never qualifies for 5%."),
    S("limit", "Reported limits run about $500 to $7,400, averaging around $6,158, far below a $10k to $50k month in one cycle."),
    S("tip", "Phone debit-card bill pay on 800-950-5114 is confirmed real and posts immediately. Fee and per-call limit unconfirmed."),
  ],
  sources=["https://www.nerdwallet.com/credit-cards/news/citi-custom-cash-closed-to-new-applications",
           "https://wallethub.com/answers/cc/pay-citibank-credit-card-with-a-debit-card-1000333-2140756675/"]),

C("Target Circle Card (Credit / Mastercard)", network="mastercard", debit_pay="Y", fee_usd=0, real10_pct=0.85, real50_pct=0.4,
  tiers=[T("Base rate on non-Target spend including Costco", 1.0)],
  special=[
    S("limit", "Typical starting limit about $2,000 to $8,000; some reports up to $20,000 after years of increases."),
    S("eligibility", "This is the Target Mastercard usable anywhere, not the Target-only Circle card."),
    S("costco", "The 5% Target discount is Target-only. Costco earns the 1% base, not the 2% gas and dining bonus."),
    S("tip", "Debit bill payment is reported by phone and in store, not confirmed as self-service on the TD Bank site."),
    S("cost", "TD Bank added a 3% foreign fee to some cards in 2026, but this one is still listed at $0."),
  ],
  sources=["https://www.target.com/circlecard",
           "https://wallethub.com/answers/cc/pay-target-red-card-with-debit-card-2140736799/"]),

C("Wells Fargo Choice Privileges Mastercard", network="mastercard", debit_pay="?", fee_usd=0, real10_pct=0.5, real50_pct=0.5, confidence="low",
  tiers=[T("Base 1x including Costco", 0.6)],
  special=[
    S("cost", "Base points redeem near 0.6 to 0.85 cents, so the real value of the base earn is well under 1%."),
    S("costco", "The 5x grocery bonus is supermarket MCC 5411 only. Costco earns base 1x."),
    S("limit", "Wells Fargo guarantees a $1,000 minimum; no reliable data on typical limits."),
    S("tip", "Wells Fargo debit-card payment is claimed branch-only and is unconfirmed."),
    S("risk", "Branch-only paydown would badly limit the payment speed a high-volume month needs."),
  ],
  sources=["https://www.nerdwallet.com/credit-cards/reviews/choice-privileges-card"]),

C("Wells Fargo Choice Privileges Select Mastercard", network="mastercard", debit_pay="?", fee_usd=95, real10_pct=0.5, real50_pct=0.5, confidence="low",
  tiers=[T("Base 1x including Costco", 0.6, mc=8)],
  special=[
    S("cost", "A $95 annual fee, and base points redeem near 0.6 to 0.85 cents."),
    S("costco", "The 5x grocery bonus is MCC 5411 only; Costco earns base 1x."),
    S("limit", "Guaranteed $1,000 minimum; no hard data on typical limits for this tier."),
    S("tip", "Wells Fargo debit payment is claimed branch-only and is unconfirmed."),
    S("risk", "Branch-only paydown limits the velocity a high-volume month needs."),
  ],
  sources=["https://www.nerdwallet.com/credit-cards/reviews/choice-privileges-select-card"]),

C("Sam's Club Mastercard", network="mastercard", debit_pay="?", fee_usd=0, real10_pct=1.0, real50_pct=0.35,
  tiers=[T("Base 1% on other purchases including Costco", 1.0)],
  special=[
    S("cap", "Sams Cash is capped at $5,000 per calendar YEAR across all categories and cards for the same member. A hard ceiling."),
    S("limit", "Limits skew low: average about $5,323, most common starting limit around $1,000."),
    S("costco", "Costco earns the 1% other-purchases rate; the Sams Club 3% and gas 5% bonuses do not apply."),
    S("tip", "Synchrony debit bill payment is inconsistently documented; bank ACH is the clearly confirmed method."),
    S("risk", "Synchrony is known for broad credit tightening and account closures."),
  ],
  sources=["https://www.synchronybankterms.com/syfterms/pdf/Sams_Club_Mastercard_Account_Agreement_and_Pricing_Addendum.pdf",
           "https://scene7.samsclub.com/is/content/samsclub/sams-cash-with-mastercard"]),
]

out = os.path.join(W, "rebuild", "deep", "out_G.json")
json.dump(G, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(G), "cards written to", out)
