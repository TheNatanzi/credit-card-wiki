# -*- coding: utf-8 -*-
"""index.html -> artifact.html : strip the html/head/body skeleton, add dark-theme tokens."""
import re,os,sys
sys.stdout.reconfigure(encoding="utf-8")
W=r"C:\Claude\credit-card-wiki"
s=open(os.path.join(W,"index.html"),encoding="utf-8").read()
s=s[s.index("<title>"):]
s=s.replace("</head><body>","",1)
s=s.rsplit("</body></html>",1)[0]

LIGHT=""":root{--bg:#f4f6f2;--card:#fff;--ink:#1f2a24;--mut:#6b7a70;--grn:#2e7d52;--grn2:#e6f2ea;--amber:#b8860b;--amberbg:#fdf6e3;--red:#b23b3b;--line:#e2e8e2;--pos:#1c7a44;--hover:#fafcfa;--faint:#c8ccc8;--bizbg:#ececfa;--bizfg:#3a3a8a;--dbbg:#fdeee6;--dbfg:#a4560f;--ppbg:#f0e6fd;--ppfg:#6b3a9a;--dedbg:#fbeceb;--crbg:#fff3d6;--crfg:#8a5a00;--tipbg:#1f2a24;--tipfg:#fff;--rule:#1f2a24;--rulefg:#fff}"""
DARK="""--bg:#101310;--card:#191d18;--ink:#e7ece5;--mut:#94a390;--grn:#5fb888;--grn2:#1d2d23;--amber:#d9a441;--amberbg:#2d2413;--red:#e0736e;--line:#2a312a;--pos:#6fc79a;--hover:#1f241e;--faint:#4a524a;--bizbg:#1e2140;--bizfg:#a8b0ee;--dbbg:#33231a;--dbfg:#e0a877;--ppbg:#2a2140;--ppfg:#c0a5e8;--dedbg:#3a1f1e;--crbg:#332a16;--crfg:#e0be74;--tipbg:#e7ece5;--tipfg:#101310;--rule:#e7ece5;--rulefg:#101310"""

old=s[s.index(":root{"):s.index("}",s.index(":root{"))+1]
s=s.replace(old,LIGHT+"\n@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){"+DARK+"}}\n:root[data-theme=\"dark\"]{"+DARK+"}",1)

# literals -> tokens so both themes resolve
for a,b in [("#1c7a44","var(--pos)"),("#fafcfa","var(--hover)"),("#c8ccc8","var(--faint)"),
            ("#eef;color:#3a3a8a","var(--bizbg);color:var(--bizfg)"),
            ("#fdeee6;color:#a4560f","var(--dbbg);color:var(--dbfg)"),
            ("#f0e6fd;color:#6b3a9a","var(--ppbg);color:var(--ppfg)"),
            ("#fbeceb;color:var(--red)","var(--dedbg);color:var(--red)"),
            ("#fff3d6;color:#8a5a00","var(--crbg);color:var(--crfg)"),
            ("background:#1f2a24;color:#fff;padding:9px 11px","background:var(--tipbg);color:var(--tipfg);padding:9px 11px"),
            ("background:#1f2a24;color:#fff\">★ Medi ruled","background:var(--rule);color:var(--rulefg)\">★ Medi ruled"),
            (".tile{background:var(--card)",".tile{background:var(--card)"),
            ("th{background:var(--grn);color:#fff","th{background:var(--grn);color:var(--card)"),
            (".chip.on{background:var(--grn);color:#fff",".chip.on{background:var(--grn);color:var(--card)"),
            (".pop{display:none;position:fixed;left:50%;top:80px;transform:translateX(-50%);background:#fff",
             ".pop{display:none;position:fixed;left:50%;top:80px;transform:translateX(-50%);background:var(--card)"),
            (".pop button{margin-right:6px;padding:6px 12px;border-radius:8px;border:1px solid var(--grn);background:var(--grn);color:#fff",
             ".pop button{margin-right:6px;padding:6px 12px;border-radius:8px;border:1px solid var(--grn);background:var(--grn);color:var(--card)"),
            ("box-shadow:2px 0 4px -2px rgba(0,0,0,.15)","box-shadow:2px 0 4px -2px rgba(0,0,0,.28)"),
            (".acc[open] summary{border-bottom:1px solid var(--line);background:#fafcfa}",".acc[open] summary{border-bottom:1px solid var(--line);background:var(--hover)}"),
            (".bar{height:9px;border-radius:5px;background:var(--grn2)",".bar{height:9px;border-radius:5px;background:var(--grn2)"),
            (".bar.h i{background:#c8d8cc}.bar.f i{background:#9fbfa9}",".bar.h i{background:var(--faint)}.bar.f i{background:var(--mut)}"),
            ("body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45","body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45"),
            ("padding:0 16px 60px}","padding-block:0 60px;padding-inline:16px}"),
            ("input[type=search]{flex:1;min-width:200px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:14px}",
             "input[type=search]{flex:1;min-width:200px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:14px;background:var(--card);color:var(--ink)}"),
            (".chip{border:1px solid var(--line);background:var(--card);",".chip{border:1px solid var(--line);background:var(--card);color:var(--ink);"),
            (".pop input{width:100%;margin:8px 0;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:13px}",
             ".pop input{width:100%;margin:8px 0;padding:8px;border:1px solid var(--line);border-radius:8px;font-size:13px;background:var(--bg);color:var(--ink)}"),
            (".pop #popx{background:#fff;color:var(--ink)",".pop #popx{background:var(--card);color:var(--ink)"),
            ('.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0;position:sticky;top:0;',
             '.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0;position:sticky;top:env(safe-area-inset-top,0px);'),
            ("a:focus,button:focus","a:focus,button:focus")]:
    s=s.replace(a,b)
s=s.replace("</style>",""":focus-visible{outline:2px solid var(--grn);outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
@media (max-width:560px){.tiles{grid-template-columns:repeat(2,1fr)}h1{font-size:20px}}
</style>""",1)
open(os.path.join(W,"artifact.html"),"w",encoding="utf-8").write(s)
print("artifact.html",len(s)//1024,"KB | dark tokens:",s.count("prefers-color-scheme"),"| skeleton removed:", "<!DOCTYPE" not in s)
