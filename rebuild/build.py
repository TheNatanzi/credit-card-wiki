# -*- coding: utf-8 -*-
"""Credit Card Master Wiki v9 build: merge LLM-extracted batches -> compute -> cards.json -> index.html"""
import json, glob, os, sys, math, datetime
sys.stdout.reconfigure(encoding="utf-8")
WIKI=r"C:\Claude\credit-card-wiki"; OUT=os.path.join(WIKI,"rebuild","out")
TAEKUS=1.80          # +% when card bill is debit-payable (flip to 0 if live test fails)
MAX_SWIPE=5000       # largest single swipe we assume when a bonus needs a min purchase size
SANITY=6.0

rows=[]
files=sorted(glob.glob(os.path.join(OUT,"*.json")))
for f in files:
    b=json.load(open(f,encoding="utf-8"))
    for r in b:
        r["_batch"]=os.path.basename(f); r["card"]=r["card"].replace("**","").strip(); r["issuer"]=(r.get("issuer") or "").replace("**","").strip()
    rows+=b
print("merged",len(rows),"cards from",len(files),"batches")
import re as _re
ALIAS={
 "venmo credit card crypto cashback":"venmo credit card",
 "costco anywhere visa card by citi":"costco anywhere visa",
 "current debit current":"current visa debit card",
 "capital one walmart rewards mastercard discontinued":"capital one walmart rewards mastercard",
 "step visa card":"step card",
 "amazon prime visa":"prime visa",
 "cash app card cash card":"cash app card",
 "cash app card afterpay card":"cash app card",
 "chime card debit":"chime visa debit card",
 "dave debit card":"dave debit mastercard",
 "hilton aspire":"hilton honors american express aspire card",
 "hilton business":"hilton honors american express business card",
 "hilton honors no fee":"hilton honors american express card",
 "hilton surpass":"hilton honors american express surpass card",
 "marriott bonvoy bevy":"marriott bonvoy american express card bevy",
 "marriott bonvoy brilliant":"marriott bonvoy brilliant american express card",
 "marriott bonvoy business":"marriott bonvoy business american express card",
 "revolut debit us":"revolut us card standard premium metal",
 "sofi checking debit sofi smart card":"sofi debit card checking money",
 "varo debit varo perks":"varo visa debit card",
 "venmo debit card venmo stash":"venmo debit mastercard"}
def _key(c):
    k=_re.sub(r"[^a-z0-9 ]"," ",c.lower()); k=_re.sub(r"\s+"," ",k).strip(); return ALIAS.get(k,k)
seen={}
for r in rows:
    k=_key(r["card"]); r["_key"]=k
    if k in seen:
        old=seen[k]; better=len(r.get("needs_research") or [])<len(old.get("needs_research") or [])
        r["_dup"]=not better; old["_dup"]=better
        if better: seen[k]=r
    else: seen[k]=r; r["_dup"]=False
dups=[r["card"] for r in rows if r["_dup"]]
rows=[r for r in rows if not r["_dup"]]
print("deduped",len(dups),"->",len(rows),"|",", ".join(sorted(set(dups))))

# apply spot-check fixes (rebuild/spotcheck.json: [{card, verdict, fixes:{field:val}}])
_sc=os.path.join(WIKI,"rebuild","spotcheck.json"); nfix=0
if os.path.exists(_sc):
    for f in json.load(open(_sc,encoding="utf-8")):
        if f.get("verdict")=="fix" and f.get("fixes"):
            for r in rows:
                if r["card"].strip()==f["card"].replace("**","").strip():
                    r.update(f["fixes"]); r["_spotfix"]=f.get("note",""); nfix+=1
print("spot-check fixes applied:",nfix)

# deep research (rebuild/deep/out_*.json): tier ladder, US eligibility, limits, special circumstances
deep={}
for f in sorted(glob.glob(os.path.join(WIKI,"rebuild","deep","out_*.json"))):
    for d in json.load(open(f,encoding="utf-8")): deep[d["card"].replace("**","").strip()]=d
for r in rows:
    d=deep.get(r["card"].strip())
    if not d: continue
    r["deep"]=d
    for k in ("us_ok","status","network","debit_pay","fx_pct","extra_cost_pct","txn_max_usd","daily_max_usd","costco_ok","confidence"):
        if d.get(k) not in (None,""): r[k]=d[k]
    if d.get("fee_usd") not in (None,""): r["fee_usd"]=d["fee_usd"]
    r["special"]=d.get("special") or []; r["tiers"]=d.get("tiers") or []; r["sources"]=d.get("sources") or []
print("deep-researched cards:",len([r for r in rows if r.get("deep")]))

# debit-pay verification pass (rebuild/debitpay-verified.json) then Medi rulings (rebuild/medi-rulings.json) — rulings win
_dpfiles=sorted(glob.glob(os.path.join(WIKI,"rebuild","dp_out_*.json")))
for fp,label in [(f,"verified") for f in _dpfiles]+[(os.path.join(WIKI,"rebuild","medi-rulings.json"),"ruling")]:
    n=0
    if os.path.exists(fp):
        for f in json.load(open(fp,encoding="utf-8")):
            for r in rows:
                if r["card"].strip()==f["card"].strip():
                    r.update(f.get("fixes") or {})
                    if f.get("note"): r.setdefault("notes",[]).append(label+": "+f["note"])
                    if f.get("channel"): r["dp_channel"]=f["channel"]
                    if label=="ruling": r["medi_ruled"]=True
                    n+=1
    print(label,os.path.basename(fp),"applied:",n)

def num(v,d=0.0):
    try: return float(v) if v is not None and v!="" else d
    except: return d

def where(r):
    n=r.get("network","unknown"); p=r.get("product","credit")
    if n in ("amex","discover"): return "none"   # Costco.com dropped Discover 2023-11-15
    if p=="debit": return "store" if n!="unknown" else "?"
    if n=="visa": return "store"
    if n=="mastercard": return "online"
    return "?"

def month_cap(r):
    cap=r.get("costco_cap_usd"); per=r.get("cap_period","none")
    if cap in (None,"",0): return math.inf
    cap=num(cap); return {"month":cap,"cycle":cap,"quarter":cap/3,"year":cap/12}.get(per,cap)

def pct(S,x_bonus,x_base,cpp,r):
    cap=month_cap(r)
    mt=r.get("min_txn_usd")
    if mt not in (None,"") and num(mt)>MAX_SWIPE: x_bonus=x_base
    bonus_spend=min(S,cap)
    reward=bonus_spend*x_bonus*cpp/100+max(0,S-bonus_spend)*x_base*cpp/100
    rc=r.get("reward_cap_usd_month")
    if rc not in (None,""): reward=min(reward,num(rc))
    return round(reward/S*100,2)

for r in rows:
    w=where(r); r["where"]=w
    cm,cf=num(r.get("cpp_max"),1.0),num(r.get("cpp_floor"),1.0)
    bx,xmax,xmin=num(r.get("base_x")),num(r.get("costco_x_max")),num(r.get("costco_x_min"))
    if xmax<xmin: xmax,xmin=xmin,xmax
    if w=="none":
        r["c10"]=r["c50"]=r["f10"]=r["f50"]=0.0
    else:
        r["c10"]=pct(10000,xmax,bx,cm,r); r["c50"]=pct(50000,xmax,bx,cm,r)
        r["f10"]=pct(10000,xmin,bx,cf,r); r["f50"]=pct(50000,xmin,bx,cf,r)
    if r.get("tiers"):
        def tier_pct(S,allow_lockup):
            spend=S
            if r.get("daily_max_usd"): spend=min(spend,num(r["daily_max_usd"])*30)
            if r.get("txn_max_usd") and num(r["txn_max_usd"])<3800: return 0.0
            ts=[t for t in r["tiers"] if (allow_lockup or not t.get("lockup_usd")) and (t.get("min_spend_month_usd") in (None,"") or num(t["min_spend_month_usd"])<=spend)]
            if not ts: ts=[r["tiers"][0]]
            t=max(ts,key=lambda t:num(t.get("rate_pct")))
            reward=spend*num(t["rate_pct"])/100
            if t.get("reward_cap_month_usd") not in (None,""): reward=min(reward,num(t["reward_cap_month_usd"]))
            reward-=spend*num(r.get("extra_cost_pct"))/100+num(t.get("monthly_cost_usd"))
            return round(max(reward,0)/S*100,2)
        blocked = w=="none" or r.get("us_ok")=="N" or (r.get("costco_ok")=="N" and w!="online")
        if not blocked:
            d=r["deep"]  # researcher's real % (knows POS caps, boost-only caps, redemption value) is the headline number
            r["c10"]=max(0.0,round(num(d.get("real10_pct"),tier_pct(10000,True)),2))
            r["c50"]=max(0.0,round(num(d.get("real50_pct"),tier_pct(50000,True)),2))
            r["f10"]=min(tier_pct(10000,False),r["c10"]); r["f50"]=min(tier_pct(50000,False),r["c50"])
        else: r["c10"]=r["c50"]=r["f10"]=r["f50"]=0.0
        top=max(r["tiers"],key=lambda t:num(t.get("rate_pct")))
        r["headline_pct"]=num(top.get("rate_pct")); r["lockup_usd"]=top.get("lockup_usd")
    elif r.get("us_ok")=="N" or r.get("costco_ok")=="N":
        r["c10"]=r["c50"]=r["f10"]=r["f50"]=0.0
    r["base_pct"]=round(bx*cm,2)
    r["taekus"]=TAEKUS if (r.get("debit_pay")=="Y" and r.get("product")=="credit") else 0.0
    fee=num(r.get("fee_usd")); r["fee_usd"]=fee
    r["net50"]=round(r["c50"]+r["taekus"]-fee/(50000*12)*100,2)
    r["fx_pct"]=num(r.get("fx_pct"))
    r["cap_month_usd"]=None if month_cap(r)==math.inf else round(month_cap(r))
    r["lockup_usd"]=None if r.get("lockup_usd") in (None,"") else round(num(r.get("lockup_usd")))
    if "headline_pct" not in r: r["headline_pct"]=round(num(r.get("costco_x_max"))*cm,2)
    r["review"]=bool((r.get("reward_unit")!="crypto" and r["c50"]>SANITY) or (r.get("confidence")=="low" and r["c50"]>SANITY))
    r["is_crypto"]=r.get("reward_unit")=="crypto"

rows.sort(key=lambda r:(-r["net50"],-r["c50"],r["card"]))
json.dump(rows,open(os.path.join(WIKI,"cards.json"),"w",encoding="utf-8"),indent=1,ensure_ascii=False)
act=[r for r in rows if r.get("status")=="active"]
print("active",len(act),"dead",len(rows)-len(act),"review-flagged",sum(r["review"] for r in rows),
      "low-conf",sum(r.get("confidence")=="low" for r in rows))
print("TOP 15 active by NET@50k:")
for r in act[:15]: print(f'  net {r["net50"]:5.2f}%  (costco {r["c50"]:5.2f} + tk {r["taekus"]:.2f})  {r["where"]:6}  {r["card"]}')

# ---------------- HTML ----------------
stamp=datetime.date.today().isoformat()
data_js=json.dumps(rows,ensure_ascii=False)
HTML=open(os.path.join(WIKI,"rebuild","template.html"),encoding="utf-8").read()
store=sum(1 for r in act if r["where"]=="store"); dp=sum(1 for r in act if r["debit_pay"]=="Y"); stack=sum(1 for r in act if r["where"]=="store" and r["debit_pay"]=="Y")
rep={"__DATA__":data_js,"__N__":str(len(rows)),"__ACT__":str(len(act)),"__STORE__":str(store),"__DP__":str(dp),"__STACK__":str(stack),
     "__CRY__":str(sum(r["is_crypto"] for r in act)),"__RV__":str(sum(r["review"] for r in act)),"__TK__":f"{TAEKUS:.2f}","__SW__":f"{MAX_SWIPE:,}","__SAN__":str(SANITY),"__STAMP__":stamp,"__DEEP__":str(len([r for r in act if r.get("deep")]))}
for k,v in rep.items(): HTML=HTML.replace(k,v)
open(os.path.join(WIKI,"index.html"),"w",encoding="utf-8").write(HTML)
print("wrote index.html",len(HTML)//1024,"KB")
