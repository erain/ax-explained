#!/usr/bin/env python3
"""Builds the self-contained AX Explained interactive tutorial HTML app."""

import json
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

fonts_css = (REPO_ROOT / "assets/fonts.css").read_text(encoding="utf-8").strip()

# Extract clean <g> inner paths from assets/axel.svg for inline mascot rendering
axel_raw = (REPO_ROOT / "assets/axel.svg").read_text(encoding="utf-8")
axel_g_match = re.search(
    r'(<g[^>]*id="layer1"[^>]*>.*</g>)\s*<metadata', axel_raw, re.DOTALL
)
axel_inner = axel_g_match.group(1) if axel_g_match else ""
# Strip inkscape/sodipodi attributes for compactness
axel_inner = re.sub(r'\s+(?:inkscape|sodipodi):[a-zA-Z-]+="[^"]*"', "", axel_inner)

REPO_URL = "https://github.com/google/ax"
BLOB_URL = "https://github.com/google/ax/blob/main/"
SUBSTRATE_URL = "https://github.com/agent-substrate/substrate"

HTML_HEAD = f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>AX Explained · how Google AX orchestrates sandboxed AI agents at scale</title>
<meta name="description" content="An interactive wire-level guide to Google AX (github.com/google/ax): every CLI command, gRPC call, PostgreSQL lease, Agent Substrate actor RPC, atenet-router mTLS hop, and gVisor sandbox runner action, step by step.">
<meta property="og:title" content="AX Explained · How Google AX Orchestrates Sandboxed AI Agents">
<meta property="og:description" content="Interactive 3D isometric & wire-protocol tutorial for Google AX (github.com/google/ax) and Agent Substrate.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#191615">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>
{fonts_css}
:root{{
  --bg:#F5F3EF; --fg:#191615; --rgb:25,22,21;
  --green:#047857; --amber:#B45309; --red:#B42318; --pink:#D65A84; --blue:#1D4ED8;
  --sans:'Geist','Inter',system-ui,-apple-system,sans-serif;
  --mono:'Geist Mono',ui-monospace,monospace;
  --over:'Fragment Mono','Geist Mono',ui-monospace,monospace;
}}
[data-theme="dark"]{{
  --bg:#191615; --fg:#F5F3EF; --rgb:245,243,239;
  --green:#34D399; --amber:#FBBF24; --red:#F97066; --pink:#EEA0BB; --blue:#60A5FA;
}}
:root{{ --f70:rgba(var(--rgb),.70); --f55:rgba(var(--rgb),.66); --f40:rgba(var(--rgb),.48); --f30:rgba(var(--rgb),.30); --f15:rgba(var(--rgb),.15); --f08:rgba(var(--rgb),.07); --f04:rgba(var(--rgb),.035); }}
*{{box-sizing:border-box}}
html,body{{margin:0;height:100%}}
body{{background:var(--bg);color:var(--fg);font:14px/1.5 var(--sans);-webkit-font-smoothing:antialiased;overflow:hidden}}
button{{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}}
button:focus-visible,tr:focus-visible{{outline:1.5px solid var(--fg);outline-offset:2px}}
.ov{{font:500 12px/1.2 var(--sans);color:var(--f55);font-variant-numeric:tabular-nums}}
.dim{{color:var(--f40)}}
.mono{{font-family:var(--mono)}}
svg{{display:block}}

/* layout */
.app{{display:grid;grid-template-rows:64px 1fr;grid-template-columns:minmax(0,1fr);height:100vh;width:100%;overflow:hidden}}
header{{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:0;border-bottom:1px solid var(--f15);padding:0 20px;min-width:0}}
header>*{{padding:0 18px;min-height:40px;display:flex;flex-direction:column;justify-content:center;border-left:1px solid var(--f15);min-width:0}}
header>:first-child{{border-left:0;padding-left:0}}
.brand{{flex-direction:row!important;align-items:center;justify-content:flex-start!important;gap:12px}}
.axel-logo{{height:30px;width:28px;flex:none;filter:drop-shadow(0 1px 2px rgba(0,0,0,.18))}}
.brand h1{{margin:0;font-weight:400;font-size:20px;letter-spacing:-.01em;line-height:1;white-space:nowrap}}
.brand .by{{display:inline-flex;align-items:center;gap:6px;color:var(--f55);text-decoration:none;font:12px/1 var(--mono);padding:4px 8px;border-radius:5px;border:1px solid var(--f15);opacity:.9;transition:opacity .15s,border-color .15s;white-space:nowrap}}
.brand .by:hover{{opacity:1;border-color:var(--f40);color:var(--fg)}}
.brand .by svg{{width:13px;height:13px;fill:currentColor}}
.theme{{border-left:0!important;flex-direction:row;gap:2px;align-items:center}}
.theme button{{width:32px;height:32px;border-radius:6px;display:grid;place-items:center;color:var(--f55)}}
.theme button:hover{{background:var(--f08);color:var(--fg)}}
.theme button[aria-pressed="true"]{{background:var(--f08);color:var(--fg)}}
.theme svg{{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6}}

main{{display:grid;grid-template-columns:316px minmax(0,1fr) 384px;min-height:0;min-width:0}}
.panel{{min-height:0;min-width:0;display:flex;flex-direction:column}}
.ph{{display:flex;align-items:baseline;justify-content:space-between;padding:18px 20px 12px}}
.ph h2{{margin:0;font-weight:400;font-size:19px;letter-spacing:-.01em;line-height:1.1}}
.ph .subtag{{font:11px var(--mono);color:var(--f55)}}

/* left */
#left{{border-right:1px solid var(--f15)}}
#list{{overflow-y:auto;overflow-x:hidden;flex:1;padding:6px 0 20px;border-top:1px solid var(--f08);scroll-padding-top:12px}}
.li{{border-bottom:1px solid var(--f08)}}
.lh{{width:100%;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;padding:10px 20px;text-align:left}}
.lh:hover{{background:var(--f04)}}
.li.open>.lh{{background:var(--f08)}}
.lt{{min-width:0}}
.lt b{{display:block;font-weight:400;font-size:14px;overflow-wrap:anywhere}}
.lt b small{{display:inline-block;font:11px var(--mono);color:var(--pink);margin-left:6px;padding:1px 5px;border-radius:4px;background:color-mix(in srgb,var(--pink) 12%,transparent);white-space:nowrap}}
.lt em{{display:block;font-style:normal;font-size:12px;color:var(--f55);overflow-wrap:anywhere}}
.ring{{width:12px;height:12px;border-radius:50%;border:1.5px solid var(--f30);flex:none}}
.ring.part{{border-color:var(--fg);background:conic-gradient(var(--fg) 0 50%,transparent 50%)}}
.ring.done{{border-color:var(--green);background:var(--green);box-shadow:inset 0 0 0 2px var(--bg)}}
.steps{{list-style:none;margin:0;padding:4px 12px 12px 20px;position:relative}}
.stp{{display:grid;grid-template-columns:20px 1fr;gap:12px;text-align:left;padding:6px 8px;border-radius:6px;width:100%;position:relative}}
.stp:hover{{background:var(--f04)}}
.stp .num{{width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font:10px var(--mono);border:1px solid var(--f30);color:var(--f55);margin-top:1px;background:var(--bg)}}
.stp.past .num{{border-color:var(--fg);color:var(--fg)}}
.stp.cur .num{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
.stp b{{display:block;font-weight:400;font-size:13px}}
.stp.cur b{{color:var(--fg);font-weight:500}}

/* center */
#center{{display:grid;grid-template-rows:minmax(0,1fr) 292px;grid-template-columns:minmax(0,1fr);min-width:0;min-height:0;overflow:hidden}}
.stage{{position:relative;min-height:0;border-bottom:1px solid var(--f15);overflow:hidden;display:grid;grid-template-rows:auto minmax(0,1fr)}}
.stagebar{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:8px 14px;padding:14px 20px 0;min-width:0}}
.stagebody{{position:relative;min-height:0}}
.views{{display:flex;flex:none;gap:2px;padding:3px;border-radius:8px;background:var(--f08);max-width:100%}}
.views button{{font-size:11.5px;padding:4px 8px;border-radius:5px;color:var(--f55);white-space:nowrap}}
.views button:hover{{color:var(--fg)}}
.views button[aria-pressed="true"]{{background:var(--bg);color:var(--fg);box-shadow:0 0 0 1px var(--f15),0 1px 2px rgba(0,0,0,.08)}}
#variants[hidden]{{display:none}}
.sbr{{display:flex;flex:0 1 auto;flex-wrap:wrap;justify-content:flex-end;gap:6px;margin-left:auto;max-width:100%}}
#viewnet{{position:absolute;inset:0}}
#net{{width:100%;height:100%}}
#caption{{flex:1 1 220px;min-width:200px;max-width:650px;min-height:66px}}
#caption .ct{{font-size:20px;letter-spacing:-.01em;margin:4px 0 2px;line-height:1.2}}
#caption p{{margin:0;font-size:13px;color:var(--f70);text-wrap:pretty}}
#caption p.plain{{color:var(--fg);opacity:.88;font-size:13.5px}}
.jump-era{{margin-top:6px;padding:4px 10px;border-radius:5px;border:1px solid var(--pink);color:var(--pink);font:500 11.5px var(--mono);display:inline-flex;align-items:center;gap:5px}}
.jump-era:hover{{background:color-mix(in srgb,var(--pink) 14%,transparent)}}
.gdot{{fill:var(--f15)}}
.edge{{stroke:var(--f30);stroke-width:1}}
.edge.used{{stroke:var(--f40)}}
.edge.on{{stroke:var(--fg);stroke-width:1.6}}
.edge.hostedge{{stroke-dasharray:2 4}}
.node .nb{{fill:var(--bg);stroke:var(--f30);stroke-width:1}}
.node.on .nb{{stroke:var(--fg);stroke-width:1.5}}
.nl{{font:18px var(--sans);fill:var(--fg)}}
#seq .nl{{font-size:14.5px}}
.ns{{font:13px var(--mono);fill:var(--f55)}}
.node{{transition:opacity .2s;cursor:pointer}}
.ahp{{fill:var(--f55)}}
.trail{{stroke-width:1.7}}
.pkt .pb{{fill:var(--bg);stroke-width:1.6}}
.pkt .pt{{font:13px var(--mono);fill:var(--fg)}}
.pkt .pd{{stroke:none}}
.k-req .pb,.trail.k-req{{stroke:var(--fg)}} .k-req .pd{{fill:var(--fg)}}
.k-res .pb,.trail.k-res{{stroke:var(--f70)}} .k-res .pd{{fill:none;stroke:var(--fg);stroke-width:1.6}}
.k-sql .pb,.trail.k-sql{{stroke:var(--blue)}} .k-sql .pd{{fill:var(--blue)}}
.k-sub .pb,.trail.k-sub{{stroke:var(--green)}} .k-sub .pd{{fill:var(--green)}}
.k-err .pb,.trail.k-err{{stroke:var(--amber)}} .k-err .pd{{fill:var(--amber)}}
.k-note .pb,.trail.k-note{{stroke:var(--pink);stroke-dasharray:3 3}} .k-note .pd{{fill:var(--pink)}}
.k-http .pb,.trail.k-http{{stroke:var(--f70)}} .k-http .pd{{fill:var(--f55)}}
.k-host .pb,.trail.k-host{{stroke:var(--f40);stroke-dasharray:1 3}} .k-host .pd{{fill:var(--f40)}}
.pkt.arrived{{opacity:.92}}

/* isometric models */
.iso .bx polygon,.iso>.mdl>path,.iso>.mdl>ellipse.ft,.iso>.mdl>circle.ft{{stroke:var(--f55);stroke-width:.85;stroke-linejoin:round}}
.iso .ft{{fill:color-mix(in srgb,var(--fg) 4%,var(--bg))}}
.iso .fl{{fill:color-mix(in srgb,var(--fg) 11%,var(--bg))}}
.iso .fr{{fill:color-mix(in srgb,var(--fg) 20%,var(--bg))}}
.iso .shd{{fill:rgba(var(--rgb),.07)}}
.iso .led{{fill:var(--f40)}} .iso .led2{{fill:var(--f15)}}
.iso .ln{{fill:none;stroke:var(--f40);stroke-width:1.2;stroke-linecap:round}}
.iso .ln2{{fill:none;stroke:var(--f40);stroke-width:1.1}}
.iso .scr{{fill:color-mix(in srgb,var(--fg) 82%,var(--bg))}}
.iso .code{{fill:none;stroke:var(--bg);stroke-width:2;stroke-linecap:round;opacity:.75}}
.iso .kbd{{fill:var(--f08);stroke:var(--f30);stroke-width:.8}}
.iso .spark{{fill:var(--f55)}}
.iso .core{{fill:var(--f08);stroke:var(--f40);stroke-width:1}}
.iso .pit{{fill:color-mix(in srgb,var(--fg) 24%,var(--bg))}}
.iso .hl{{fill:none;stroke:var(--bg);stroke-width:1.6;stroke-linecap:round;opacity:.9}}
.iso .mono3{{font:600 11.5px var(--mono);fill:var(--fg)}}
.iso.on .bx polygon,.iso.on>.mdl>path,.iso.on>.mdl>ellipse.ft,.iso.on>.mdl>circle.ft{{stroke:var(--fg);stroke-width:1.45}}
.iso.on .led,.iso.on .spark{{fill:var(--green)}}
.iso.on .code{{stroke:var(--green);opacity:1}}
.iso.on .lit .ft{{fill:color-mix(in srgb,var(--green) 16%,var(--bg))}}
.iso.on .shd{{fill:rgba(var(--rgb),.14)}}
.halo{{paint-order:stroke;stroke:var(--bg);stroke-width:5px;stroke-linejoin:round}}
.iso .nl{{font-size:18.5px}}
.iso .ns{{font-size:13px}}

/* zones */
.zone .zb{{fill:color-mix(in srgb,var(--fg) 2.5%,var(--bg));stroke:var(--f30);stroke-width:1}}
.zone.z-control .zb{{stroke:var(--pink);stroke-opacity:.55}}
.zone.z-substrate .zb{{stroke:var(--green);stroke-opacity:.55}}
.zone.z-sandbox .zb{{fill:color-mix(in srgb,var(--green) 3%,var(--bg));stroke:var(--green);stroke-dasharray:6 4;stroke-opacity:.75}}
.zone.z-remote .zb,.zone.z-external .zb{{fill:var(--bg);stroke-dasharray:6 5;stroke:var(--f40)}}
.zl{{font:11.5px var(--over);letter-spacing:.11em;fill:var(--fg)}}
.zone.z-control .zl,.sz-control{{fill:var(--pink)}}
.zone.z-substrate .zl,.sz-substrate,.zone.z-sandbox .zl,.sz-sandbox{{fill:var(--green)}}
.zsub{{font:12px var(--mono);fill:var(--f55)}}
#seq .zl{{font-size:9px;fill:var(--f55)}}
.wire rect{{fill:var(--bg);stroke:var(--f30)}}
.wire text{{font:12.5px var(--mono);fill:var(--f70)}}

/* deprecated / historical */
.deptag{{display:inline-block;font:11.5px/1.4 var(--mono);font-style:normal;color:var(--amber);padding:0 5px;border-radius:4px;background:color-mix(in srgb,var(--amber) 12%,transparent);vertical-align:1px;white-space:nowrap}}
.depnote{{margin:6px 0 0!important;font-size:12px!important;color:var(--amber)!important;opacity:.95}}
.depbox{{border:1px dashed color-mix(in srgb,var(--amber) 60%,transparent);border-radius:6px;padding:8px 10px;margin:0 0 10px}}
.depbox p{{margin:5px 0 0;font-size:12px;color:var(--f70);line-height:1.45}}
#flowt tbody tr.dep s{{text-decoration-color:var(--amber)}}
.pkt.dep .pb{{stroke-dasharray:5 3}}
.pdep{{font:9.5px var(--over);letter-spacing:.12em;fill:var(--amber);paint-order:stroke;stroke:var(--bg);stroke-width:4px}}

#seqwrap{{position:absolute;inset:0;overflow:auto}}
#seq{{width:100%}}
.life{{stroke:var(--f15);stroke-dasharray:3 4}}
#seq .nb{{fill:var(--bg);stroke:var(--f30)}}
.sm line{{stroke-width:1.4;marker-end:url(#sah)}}
.sm text{{font:12.5px var(--mono);fill:var(--f70)}}
.sm.k-req line{{stroke:var(--fg)}} .sm.k-res line{{stroke:var(--f70)}} .sm.k-err line{{stroke:var(--amber)}}
.sm.k-sql line{{stroke:var(--blue)}} .sm.k-sub line{{stroke:var(--green)}}
.sm.k-note line{{stroke:var(--pink);stroke-dasharray:3 3}} .sm.k-http line{{stroke:var(--f70)}} .sm.k-host line{{stroke:var(--f40);stroke-dasharray:1 3}}
.sm{{cursor:pointer}}
.sm.fut{{opacity:.18}}
.sm.cur text{{fill:var(--fg);font-weight:500}}
.sm.cur line{{stroke-width:2.3}}
.sstep{{font:10px var(--mono);fill:var(--f40)}}
.sm.dep line{{stroke-dasharray:6 3}}
.sm .sdep{{font:9.5px var(--over);letter-spacing:.1em;fill:var(--amber)}}

/* flow table */
.flow{{display:flex;flex-direction:column;min-height:0;min-width:0}}
.fh{{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 16px 10px 20px;border-bottom:1px solid var(--f15)}}
.fh h2{{margin:0;font-weight:400;font-size:15.5px;white-space:nowrap}}
#flowcount{{font-size:12px;color:var(--f55);margin-left:6px;font-variant-numeric:tabular-nums}}
#legend{{display:flex;gap:4px 10px;flex-wrap:wrap;font-size:11px;color:var(--f55);flex:1;justify-content:flex-end;margin-right:4px}}
#legend span{{display:inline-flex;align-items:center;gap:5px;white-space:nowrap}}
.ctrl{{display:flex;gap:5px;flex:none}}
.ctrl button{{height:30px;padding:0 10px;border:1px solid var(--f15);border-radius:6px;font-size:12px;display:inline-flex;align-items:center;gap:5px}}
.ctrl button:hover:not(:disabled){{border-color:var(--f55)}}
.ctrl button:active:not(:disabled){{transform:translateY(1px)}}
.ctrl button:disabled{{opacity:.35;cursor:default}}
.ctrl svg{{width:13px;height:13px;fill:currentColor}}
.ctrl #btn-play{{background:var(--fg);color:var(--bg);border-color:var(--fg);min-width:82px;justify-content:center}}
.ctrl #btn-prev{{padding:0 7px}}
.ctrl #btn-speed{{font-family:var(--mono);min-width:38px;justify-content:center}}
#tablewrap{{overflow:auto;flex:1}}
table{{width:100%;border-collapse:collapse}}
#flowt{{table-layout:fixed}}
#flowt thead th{{position:sticky;top:0;z-index:1;background:var(--bg);font:500 11px var(--sans);text-align:left;padding:8px 10px;border-bottom:1px solid var(--f15);color:var(--fg);white-space:nowrap}}
#flowt tbody td{{padding:6px 10px;font-size:12.5px;color:var(--f70);border-bottom:1px solid var(--f08);white-space:nowrap;max-width:340px;overflow:hidden;text-overflow:ellipsis}}
#flowt thead th:first-child,#flowt tbody td:first-child{{padding-left:20px;width:46px}}
tbody tr{{cursor:pointer}}
tbody tr:hover td{{background:var(--f04)}}
tbody tr.fut td{{color:var(--f30)}}
tbody tr.fut .dot{{opacity:.55}}
tbody tr.cur td{{background:var(--f08);color:var(--fg)}}
tbody tr.sel td{{background:var(--f08);color:var(--fg)}}
.dot{{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;font:10px var(--mono);color:var(--bg)}}
#legend .dot{{width:8px;height:8px}}
.dot.k-req{{background:var(--fg)}}
.dot.k-res{{background:transparent;border:1.4px solid var(--fg);color:var(--fg)}}
.dot.k-sql{{background:var(--blue);color:#fff}}
.dot.k-sub{{background:var(--green);color:#06281E}}
.dot.k-err{{background:var(--amber);color:#191615}}
.dot.k-note{{background:transparent;border:1.4px dashed var(--pink);color:var(--pink)}}
.dot.k-http{{background:var(--f55);border-radius:4px}}
.dot.k-host{{background:transparent;border:1.4px dotted var(--f55);color:var(--f70)}}

/* right */
#right{{border-left:1px solid var(--f15);overflow-y:auto;overflow-x:hidden;background:var(--bg);position:relative;z-index:1;min-width:0}}
.ovw{{padding:18px 20px 14px;border-bottom:1px solid var(--f15)}}
.ovh{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}}
#ov-title{{margin:0;font-weight:400;font-size:32px;letter-spacing:-.02em;line-height:1.02}}
#ov-name{{font-size:13px;color:var(--f70);margin:5px 0 9px}}
#ov-sum{{margin:0 0 10px;font-size:12.8px;line-height:1.5;color:var(--f70);text-wrap:pretty}}
.facts-wrap{{margin:8px 0 10px;border:1px solid var(--f15);border-radius:6px;background:var(--f04)}}
.facts-wrap summary{{cursor:pointer;padding:6px 10px;font:500 11.5px var(--mono);color:var(--fg);user-select:none;list-style:none;display:flex;justify-content:space-between;align-items:center}}
.facts-wrap summary::-webkit-details-marker{{display:none}}
.facts-wrap summary::after{{content:"+";color:var(--f55);font-size:13px}}
.facts-wrap[open] summary::after{{content:"−"}}
.facts-dl{{margin:0;padding:8px 10px 10px;border-top:1px solid var(--f08);display:grid;grid-template-columns:minmax(78px,auto) minmax(0,1fr);gap:5px 10px;font-size:11.8px}}
.facts-dl dt{{font-family:var(--mono);font-size:11px;color:var(--fg);font-weight:500}}
.facts-dl dd{{margin:0;color:var(--f70);line-height:1.4;min-width:0;overflow-wrap:anywhere}}
.insp-h{{padding:14px 20px 8px;display:flex;justify-content:space-between;align-items:center}}
.insp-h h2{{margin:0;font-weight:400;font-size:15.5px}}
.copy-btn{{font:11px var(--mono);color:var(--f55);padding:3px 8px;border:1px solid var(--f15);border-radius:4px}}
.copy-btn:hover{{color:var(--fg);border-color:var(--f40)}}
#insp{{padding:0 20px 22px}}
.empty{{color:var(--f55);font-size:13px}}
.ih{{display:flex;align-items:center;gap:10px}}
.ih .dot{{width:10px;height:10px}}
.im{{font:13.5px var(--mono);flex:1;word-break:break-all;color:var(--fg)}}
.isz{{font:11px var(--mono);color:var(--f55)}}
.ir{{font-size:12px;color:var(--f55);margin:3px 0 10px}}
.json{{margin:0;font:11.5px/1.55 var(--mono);background:var(--f04);border:1px solid var(--f08);border-radius:6px;padding:12px;overflow:auto;max-height:330px;white-space:pre-wrap;word-break:break-word;color:var(--f70)}}
.json .k{{color:var(--fg)}} .json .s{{color:var(--f70)}} .json .n,.json .l{{color:var(--green)}}
.notes{{margin:12px 0 0;display:grid;grid-template-columns:minmax(72px,auto) minmax(0,1fr);gap:6px 12px;font-size:12px}}
.notes dt{{font-family:var(--mono);font-size:11px;color:var(--fg);padding-top:1px}}
.notes dd{{margin:0;color:var(--f70);line-height:1.45;min-width:0;overflow-wrap:anywhere}}
.gh{{padding:18px 20px 6px;font:500 11.5px var(--over);letter-spacing:.06em;text-transform:uppercase;color:var(--f55)}}
.gh.ns{{color:var(--f55);border-top:1px solid var(--f15);margin-top:8px}}
.nstag{{display:inline-block;font:500 12px/1.4 var(--sans);color:var(--pink)}}
.nsbox{{margin:10px 0 6px;padding:0 0 0 12px;border-left:2px solid var(--pink)}}
.nsbox p{{margin:4px 0 0;font-size:12.5px;line-height:1.45;color:var(--f70)}}
.nsbox code{{font:11.5px var(--mono)}}
.foot{{padding:14px 20px 20px;border-top:1px solid var(--f15);font-size:12px;color:var(--f55);line-height:1.55}}
.foot a{{color:var(--fg);text-underline-offset:2px}}
.foot kbd{{font:10px var(--mono);border:1px solid var(--f15);border-radius:3px;padding:0 4px}}

#btn-lessons,#btn-ver{{display:none}}
.hver:empty{{display:none}}
header .tm{{margin:0;display:flex;align-items:center;gap:14px}}
header .tmh{{margin:0;display:block;font-size:12px;color:var(--f55);white-space:nowrap}}
header .tmh b{{display:none}}
header .tml{{width:396px}}
header .tml button{{min-height:44px;font-size:11px;gap:4px;white-space:nowrap}}
header .tml::before{{top:11.5px}}
body.intro .hver{{display:none!important}}

@media (max-width:1360px){{ #legend{{display:none}} #flowcount{{display:none}} }}
@media (max-width:1240px){{ main{{grid-template-columns:256px minmax(0,1fr) 326px}} header .tmh{{display:none}} header .tml{{width:352px}} }}
@media (max-width:980px){{ body{{overflow:auto}} .app{{height:auto;overflow:visible}} main{{grid-template-columns:1fr}} #center{{grid-template-rows:560px 320px}} #left,#right{{border:0;border-bottom:1px solid var(--f15)}} #list{{max-height:360px}} header{{grid-template-columns:auto 1fr auto}} }}

/* focus mode: sidebars slide away while playing */
main{{transition:grid-template-columns .5s cubic-bezier(.2,.7,.2,1)}}
#left,#right{{transition:opacity .3s}}
body.focus main{{grid-template-columns:0px minmax(0,1fr) 0px}}
body.focus #left,body.focus #right{{opacity:0;overflow:hidden;pointer-events:none}}

/* intro view */
#intro{{display:none}}
#btn-intro{{font-size:12.5px;color:var(--f55);padding:4px 10px;border-radius:6px;margin-left:4px;border:1px solid var(--f15);white-space:nowrap}}
#btn-intro:hover{{color:var(--fg);background:var(--f08)}}
body.intro #btn-intro{{display:none}}
body.intro main{{grid-template-columns:minmax(390px,540px) minmax(0,1fr) 0px}}
body.intro #intro{{display:flex;align-items:center;border-right:1px solid var(--f15);overflow:auto}}
body.intro #left,body.intro #right{{display:none}}
body.intro #center{{grid-template-rows:minmax(0,1fr) 0}}
body.intro .flow,body.intro .sbr{{display:none}}
.intro-inner{{padding:40px 44px 36px}}
.intro-kicker{{margin:0 0 12px;font:12px var(--mono);color:var(--pink);display:inline-flex;align-items:center;gap:8px}}
#intro h2{{margin:0 0 14px;font-weight:400;font-size:48px;letter-spacing:-.03em;line-height:1}}
.intro-lead{{margin:0 0 22px;font-size:16px;line-height:1.55;color:var(--f70);text-wrap:pretty}}
.intro-facts{{display:grid;grid-template-columns:auto 1fr;gap:9px 16px;margin:0 0 26px;font-size:13.5px}}
.intro-facts dt{{font-weight:500;font-family:var(--mono);font-size:12.5px;color:var(--fg)}}
.intro-facts dd{{margin:0;color:var(--f70);line-height:1.45}}
#intro-start{{height:44px;padding:0 20px;border-radius:10px;background:var(--fg);color:var(--bg);font-size:14.5px;display:inline-flex;align-items:center;gap:10px;font-weight:500}}
#intro-start:hover{{opacity:.92}}
.intro-jump{{margin:16px 0 0;font-size:12.5px;color:var(--f55);line-height:1.6}}
.intro-jump a{{color:var(--fg);text-underline-offset:2px;text-decoration-color:var(--f30)}}

.risk{{display:inline-grid;place-items:center;width:18px;height:18px;margin:-2px 0 0 2px;vertical-align:middle;border-radius:4px;color:var(--amber);transition:color .15s}}
.risk svg{{width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linejoin:round;stroke-linecap:round}}
.risk:hover,.risk:focus-visible,.risk[aria-expanded="true"]{{color:var(--red)}}
tr.fut .risk{{opacity:.5}}
#riskpop{{position:fixed;z-index:60;padding:12px 14px;border-radius:10px;background:var(--bg);border:1px solid var(--f15);box-shadow:0 8px 28px rgba(0,0,0,.22);font-size:13px;line-height:1.45;color:var(--f70)}}
#riskpop b{{display:block;color:var(--fg);font-weight:500;margin-bottom:4px}}
#riskpop p{{margin:0 0 8px}}
#riskpop a,.riskline a{{color:var(--fg);text-underline-offset:2px;text-decoration-color:var(--f30)}}
.riskline{{display:grid;grid-template-columns:auto 1fr;gap:6px;margin-top:14px;padding-top:12px;border-top:1px solid var(--f08);font-size:12.5px;line-height:1.5;color:var(--f55)}}
.riskline p{{margin:0}}.riskline b{{font-weight:500;color:var(--amber)}}

.tm{{margin:0 20px 14px}}
.tmh{{display:flex;justify-content:space-between;align-items:baseline;font-size:12px;color:var(--f55);margin-bottom:8px}}
.tmh b{{font:500 12px var(--mono);color:var(--fg)}}
.tml{{position:relative;display:grid;grid-template-columns:repeat(4,1fr)}}
.tml::before{{content:"";position:absolute;left:12%;right:12%;top:11.5px;height:1px;background:var(--f30)}}
.tml button{{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;padding:2px 0;font-size:11px;color:var(--f55);min-height:40px;font-family:var(--mono);white-space:nowrap}}
.tml button span{{white-space:nowrap}}
.tml button i{{width:11px;height:11px;margin-top:4px;border-radius:50%;background:var(--bg);border:1.5px solid var(--f40);transition:transform .15s}}
.tml button:hover{{color:var(--fg)}} .tml button:hover i{{border-color:var(--fg)}}
.tml button[aria-pressed="true"]{{color:var(--fg);font-weight:500}}
.tml button[aria-pressed="true"] i{{transform:scale(1.4);background:var(--pink);border-color:var(--pink);box-shadow:0 0 0 3px var(--bg)}}
.li.gone .lt b,.li.gone .lt em{{opacity:.55}}
.stage.absent #net,.stage.absent #seq{{opacity:.25;filter:grayscale(1)}}
#mbar{{display:none}}
.srcs a,.nextbox a,.wipbox a{{color:var(--fg);text-underline-offset:2px;text-decoration-color:var(--f30)}}
.srcs a:hover,.nextbox a:hover,.wipbox a:hover{{text-decoration-color:var(--fg)}}
#ov-more{{margin-top:4px;display:flex;flex-direction:column;gap:12px}}
#ov-more:empty{{display:none}}
.srcs{{display:grid;grid-template-columns:auto 1fr;column-gap:12px;font-size:12px;align-items:baseline}}
.srcs .lnk{{display:flex;flex-wrap:wrap;gap:4px 10px;font-family:var(--mono);font-size:11.5px}}
.srcs .lbl{{font:500 11px var(--sans);color:var(--fg);margin-right:2px}}
.nextbox,.wipbox{{padding:12px 0 0;border-top:1px solid var(--f08)}}
.nexttag,.wiptag{{display:block;font:500 12.5px var(--sans);color:var(--fg)}}
.nextbox ul,.wipbox ul{{margin:6px 0 6px;padding-left:16px;font-size:12px;line-height:1.5;color:var(--f70)}}
.nextbox li,.wipbox li{{margin:3px 0;text-wrap:pretty}}
.wipbox em{{font-style:normal;font-size:11.5px;color:var(--pink);white-space:nowrap;font-family:var(--mono)}}
.gh.wn{{border-top:1px solid var(--f15);margin-top:8px}}
.wnl{{display:block;padding:8px 20px;text-decoration:none;color:var(--fg);border-bottom:1px solid var(--f08)}}
.wnl:hover{{background:var(--f04)}}
.wnl b{{display:block;font-weight:500;font-size:13px}}
.wnl em{{display:block;font-style:normal;font-size:12px;color:var(--f55)}}

@media (max-width:640px){{
  body{{padding-bottom:calc(72px + env(safe-area-inset-bottom))}}
  body.intro main{{grid-template-columns:minmax(0,1fr)!important}}
  body.intro #intro{{border-right:0;border-bottom:1px solid var(--f15)}}
  .intro-inner{{padding:24px 16px}}
  #intro h2{{font-size:38px}}
  .intro-lead{{font-size:16px}}
  body.intro #mbar{{display:none}}
  body.intro{{padding-bottom:0}}
  body.intro #center{{grid-template-rows:auto 0!important}}
  #btn-intro{{display:none}}
  #mbar{{display:grid;grid-template-columns:44px 60px 44px minmax(0,1fr) minmax(0,128px);gap:6px;align-items:center;position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:var(--bg);border-top:1px solid var(--f15)}}
  #mbar button{{height:48px;border-radius:10px;display:inline-flex;align-items:center;justify-content:center;gap:8px;font-size:14px;color:var(--fg);border:1px solid var(--f15)}}
  #mbar button:disabled{{opacity:.35}}
  #mbar svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
  #mb-play{{background:var(--fg);color:var(--bg)!important;border-color:var(--fg)!important}}
  #mb-play svg{{fill:currentColor;stroke:none}}
  #mb-log{{justify-content:space-between!important;padding:0 14px;min-width:0}}
  #mb-log[aria-expanded="true"]{{background:var(--f08)}}
  #mb-count{{font:13px var(--mono);color:var(--f55)}}
  #mb-lesson{{padding:0 10px;min-width:0}}
  #mb-lname{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
  .fh .ctrl{{display:none}}
  body.log-open .flow{{position:fixed;left:0;right:0;bottom:calc(68px + env(safe-area-inset-bottom));height:min(62vh,520px);z-index:45;background:var(--bg);border-top:1px solid var(--f15);border-radius:14px 14px 0 0;box-shadow:0 -12px 32px rgba(0,0,0,.25)}}
  body.log-open .flow #tablewrap{{flex:1;min-height:0}}
  header{{padding:0 16px;grid-template-columns:1fr auto!important}}
  main{{grid-template-columns:minmax(0,1fr)!important}}
  #center,.stage,.stagebody,#viewnet,#seqwrap,.flow{{min-width:0;max-width:100vw}}
  header>*{{padding:0 0 0 12px}}
  .brand{{gap:8px}}
  .brand h1{{font-size:17px;white-space:nowrap}}
  .ph h2,.ph .subtag{{display:none}}
  .ph{{padding:12px 16px}}
  .mpick{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;width:100%}}
  #btn-lessons,#btn-ver{{display:inline-flex;align-items:center;justify-content:space-between;gap:8px;height:42px;padding:0 14px;border:1px solid var(--f15);border-radius:10px;font-size:14px;color:var(--fg);min-width:0}}
  #btn-ver{{font:12.5px var(--mono);color:var(--f70)}}
  #btn-lessons span,#btn-ver span{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
  #btn-lessons::after,#btn-ver::after{{content:"";flex:none;width:7px;height:7px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-2px) rotate(45deg)}}
  #btn-lessons[aria-expanded="true"]::after,#btn-ver[aria-expanded="true"]::after{{transform:translateY(2px) rotate(-135deg)}}
  #left:not(.ver-open) .tm{{display:none}}
  .tm .tmh{{display:none}}
  #left:not(.expanded) #list{{display:none}}
  #center{{grid-template-rows:auto auto!important;overflow:visible}}
  .stage{{overflow:visible}}
  .stagebar{{flex-direction:column;align-items:stretch;gap:12px;padding:14px 16px 0}}
  .sbr{{justify-content:flex-start;order:-1;margin-left:0}}
  #caption{{max-width:none}}
  .stagebody{{height:auto}}
  #viewnet{{position:relative;inset:auto}}
  #seqwrap{{position:relative;inset:auto;overflow-x:auto}}
  #net{{width:100%;height:auto;display:block;padding:4px 0 8px}}
  #seq{{width:760px;display:block}}
  .flow{{height:340px}}
}}
@media (prefers-reduced-motion:reduce){{ *{{transition:none!important;scroll-behavior:auto!important}} }}
</style>
</head>
<body>
<div class="app">
<header>
  <div class="brand">
    <svg class="axel-logo" viewBox="0 0 550 600" role="img" aria-label="Axel the AX axolotl">{axel_inner}</svg>
    <h1>AX Explained</h1>
    <button type="button" id="btn-intro">What is AX?</button>
    <a class="by" href="{REPO_URL}" target="_blank" rel="noopener" aria-label="google/ax on GitHub">
      <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
      <span>google/ax</span>
    </a>
  </div>
  <div class="hver" id="hver"></div>
  <div class="theme">
    <button type="button" id="btn-light" title="Light mode" aria-label="Light mode"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
    <button type="button" id="btn-dark" title="Dark mode" aria-label="Dark mode"><svg viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg></button>
  </div>
</header>
<main>
  <section id="intro" aria-label="What is AX?">
    <div class="intro-inner">
      <p class="intro-kicker"><span>ax.io/v1alpha1 · Declarative Agent Orchestrator</span></p>
      <h2>What is AX?</h2>
      <p class="intro-lead">AX (<a href="{REPO_URL}" target="_blank" rel="noopener" style="color:var(--fg)">github.com/google/ax</a>) is a declarative orchestrator built to run millions of sandboxed autonomous agent workloads per Kubernetes cluster on top of <a href="{SUBSTRATE_URL}" target="_blank" rel="noopener" style="color:var(--fg)">Agent Substrate</a>.</p>
      <dl class="intro-facts">
        <dt>Task</dt><dd>an isolated gVisor sandbox running your agent container with CPU &amp; memory limits</dd>
        <dt>Workspace</dt><dd>Git repositories, inline guidance files (<code>AGENTS.md</code>), MCP servers, and skills pre-wired in <code>/workspace</code></dd>
        <dt>Model</dt><dd>LLM provider + model identifier + Kubernetes Secret binding (<code>gemini-api-secret</code>)</dd>
        <dt>Why not CRDs?</dt><dd>millions of short-lived agent tasks overwhelm Kubernetes <code>etcd</code>; AX stores specs in PostgreSQL and overlays live Actor status from Agent Substrate</dd>
        <dt>Zero-compute idle</dt><dd>tasks start <code>Suspended</code>; <code>ax suspend</code> checkpoints <code>/workspace</code> to object storage and frees 100% of worker CPU/RAM until <code>ax resume</code></dd>
      </dl>
      <button type="button" id="intro-start">Start the lessons <span aria-hidden="true">→</span></button>
      <p class="intro-jump">or jump to <a href="#split-state">Why not CRDs?</a> · <a href="#create">CreateTask</a> · <a href="#ssh">ax ssh &amp; mTLS</a> · <a href="#create@v0.3.1">the architecture time machine</a> · <a href="#guardrails">Break it</a></p>
    </div>
  </section>
  <section id="left" class="panel" aria-label="Lessons">
    <div class="ph"><h2>Google AX Architecture</h2><span class="subtag">15 lessons</span><div class="mpick"><button type="button" id="btn-lessons" aria-expanded="false" aria-controls="list"><span id="bl-name">Lessons</span></button><button type="button" id="btn-ver" aria-expanded="false" aria-controls="tm-line"><span id="bv-name">Era</span></button></div></div>
    <div class="tm" id="tm" role="group" aria-label="Architecture version"><div class="tmh"><span>Architecture Era</span><b id="tm-cur"></b></div><div class="tml" id="tm-line"></div></div>
    <div id="list"></div>
  </section>
  <section id="center">
    <div class="stage">
      <div class="stagebar"><div id="caption" aria-live="polite"></div><div class="sbr"><div class="views" id="variants" role="group" aria-label="Mode" hidden></div><div class="views"><button type="button" data-view="network" aria-pressed="true">Network</button><button type="button" data-view="sequence" aria-pressed="false">Sequence</button></div></div></div>
      <div class="stagebody"><div id="viewnet"><svg id="net" viewBox="0 0 1000 560" preserveAspectRatio="xMidYMid meet" aria-label="Isometric architecture diagram"></svg></div>
      <div id="seqwrap" hidden><svg id="seq" viewBox="0 0 1000 520" preserveAspectRatio="xMidYMin meet" aria-label="Wire sequence diagram"></svg></div></div>
    </div>
    <div class="flow">
      <div class="fh">
        <h2>Wire flow <span id="flowcount"></span></h2>
        <div id="legend">
          <span><i class="dot k-req"></i>CLI / gRPC req</span>
          <span><i class="dot k-res"></i>gRPC res</span>
          <span><i class="dot k-sql"></i>Postgres SQL</span>
          <span><i class="dot k-sub"></i>Substrate RPC</span>
          <span><i class="dot k-http"></i>HTTP / mTLS</span>
          <span><i class="dot k-err"></i>Error / Guardrail</span>
        </div>
        <div class="ctrl">
          <button type="button" id="btn-play" title="Play / pause (space)"></button>
          <button type="button" id="btn-prev" title="Previous message (←)" aria-label="Previous message"><svg viewBox="0 0 24 24"><path d="M15 5l-8 7 8 7z"/></svg></button>
          <button type="button" id="btn-step" title="Next message (→)">Step<svg viewBox="0 0 24 24"><path d="M9 5l8 7-8 7z"/></svg></button>
          <button type="button" id="btn-reset" title="Back to the start">Reset</button>
          <button type="button" id="btn-speed" title="Playback speed">1x</button>
        </div>
      </div>
      <div id="tablewrap"><table id="flowt"><colgroup><col style="width:50px"><col style="width:15%"><col style="width:15%"><col style="width:28%"><col></colgroup><thead><tr><th>#</th><th>From</th><th>To</th><th>Wire / Method</th><th>Detail</th></tr></thead><tbody id="tbody"></tbody></table></div>
    </div>
  </section>
  <aside id="right" class="panel" aria-label="Overview">
    <div class="ovw">
      <div class="ovh"><h3 id="ov-title"></h3></div>
      <div id="ov-name"></div>
      <div id="ov-ns" class="nsbox" hidden><span class="nstag">Inside the gVisor Sandbox</span><p>Runs inside the isolated WorkerPool container as PID 1 (<code>/usr/local/bin/ax-task-runner</code>). Agent code reads <code>127.0.0.1:8099</code> over loopback with zero SDK dependencies.</p></div>
      <p id="ov-sum"></p>
      <div id="ov-facts"></div>
      <div id="ov-more"></div>
    </div>
    <div class="insp-h"><h2>Wire Payload</h2><button type="button" class="copy-btn" id="btn-copy">Copy JSON</button></div>
    <div id="insp"></div>
    <div class="foot">AX <code>ax.io/v1alpha1</code> (<a href="{REPO_URL}" target="_blank" rel="noopener">github.com/google/ax</a> @ <code>241bc4d</code>) + <a href="{SUBSTRATE_URL}" target="_blank" rel="noopener">Agent Substrate v1.0</a>.<br>Shortcuts: <kbd>Space</kbd> play/pause · <kbd>←</kbd> <kbd>→</kbd> step · Click any row or node to inspect.</div>
  </aside>
</main>
<div id="riskpop" role="dialog" aria-live="polite" hidden></div>
<nav id="mbar" aria-label="Playback">
  <button type="button" id="mb-prev" aria-label="Previous message"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
  <button type="button" id="mb-play" aria-label="Play"></button>
  <button type="button" id="mb-next" aria-label="Next message"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
  <button type="button" id="mb-log" aria-expanded="false" aria-controls="tablewrap"><span>Log</span><span id="mb-count"></span></button>
  <button type="button" id="mb-lesson"><span id="mb-lname"></span><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6"/></svg></button>
</nav>
</div>
"""

print("Header prepared, length:", len(HTML_HEAD))

JS_PART_1 = r"""<script>// AX Explained lesson data — every message on the wire across ax CLI, ax-server, PostgreSQL, Agent Substrate, atenet-router, and the gVisor sandbox.
const SPEC = "241bc4d";
const REPO = "https://github.com/google/ax";
const BLOB = "https://github.com/google/ax/blob/main/";

const A = {
  user:     { label: "Developer", sub: "writes YAML & runs ax", icon: "user" },
  cli:      { label: "ax CLI", sub: "cmd/ax · gRPC client", icon: "host" },
  server:   { label: "ax-server", sub: "gRPC :8080 + /healthz", icon: "server", mono: "AX" },
  postgres: { label: "PostgreSQL", sub: "jsonb store + locks", icon: "postgres", mono: "PG" },
  ateapi:   { label: "Substrate API", sub: "api.ate-system:443", icon: "ateapi", mono: "ATE" },
  router:   { label: "atenet-router", sub: "stateless proxy :443/:80", icon: "gateway" },
  runner:   { label: "ax-task-runner", sub: "gVisor sandbox · PID 1", icon: "runner" },
  agent:    { label: "Agent Process", sub: "child process in /workspace", icon: "llm" },
  gcs:      { label: "Snapshot Store", sub: "durable volume bucket", icon: "key", mono: "GCS" },
  git:      { label: "Git Remote", sub: "github.com", icon: "tile", mono: "GIT" },
  mcp:      { label: "MCP Server", sub: "tool server", icon: "tile", mono: "MCP" },
  k8s:      { label: "K8s API / CSR", sub: "PodCertificateRequest", icon: "tile", mono: "K8S" },
  redis:    { label: "Redis Streams", sub: "v0.3 task queue", icon: "tile", mono: "RDS" },
  otel:     { label: "OTel Collector", sub: "traces, logs & events", icon: "tile", mono: "OTL" }
};
const at = (id, x, y, extra) => Object.assign({ id, x, y }, A[id], extra || {});

const Z = {
  local:     (ids, sub) => ({ kind: "local", label: "Your machine", sub: sub || "kubectl ctx", ids }),
  control:   (ids, sub) => ({ kind: "control", label: "ax-system", sub: sub || "control plane", ids }),
  substrate: (ids, sub) => ({ kind: "substrate", label: "ate-system", sub: sub || "Substrate v1.0", ids }),
  sandbox:   (ids, sub) => ({ kind: "sandbox", label: "gVisor Sandbox", sub: sub || "WorkerPool", ids }),
  external:  (ids, sub) => ({ kind: "external", label: "External", sub: sub || "upstream", ids })
};

const LESSONS = [
  // ───────────── 1. START HERE
  {
    id: "overview", code: "What is AX?", name: "One manifest, one diagram", group: "start",
    summary: "AX (github.com/google/ax) is a declarative orchestrator for running millions of sandboxed autonomous agent workloads on Kubernetes + Agent Substrate. You declare a Workspace, Model, and Task in YAML; ax-server persists specs in PostgreSQL and provisions a sandboxed Actor on Agent Substrate. New tasks start Suspended (zero compute); resuming schedules a gVisor worker, clones Git into /workspace, and runs the agent while letting you shell in over mTLS.",
    facts: [
      ["In one line", "kubectl-shaped orchestrator for millions of stateful, sandboxed AI agents"],
      ["Primitives", "Task (sandbox), Workspace (Git + files + MCP + skills), Model (LLM + K8s Secret)"],
      ["Why not CRDs?", "Kubernetes etcd struggles past ~10k–100k churned objects; AX stores specs in PostgreSQL and overlays live Actor state from Agent Substrate"],
      ["Sandbox runtime", "Agent Substrate WorkerPool (gVisor) with ax-task-runner as PID 1"],
      ["Start state", "New tasks start Suspended; ax resume schedules a worker and boots /workspace"],
      ["Zero-compute idle", "ax suspend checkpoints /workspace to object storage and frees 100% of CPU/RAM"]
    ],
    links: [
      ["README.md", BLOB + "README.md"],
      ["DESIGN.md", BLOB + "DESIGN.md"],
      ["docs/concepts.md", BLOB + "docs/concepts.md"]
    ],
    actors: [
      at("user", 130, 175, { sub: "you" }),
      at("cli", 130, 415, { sub: "ax apply / resume / ssh" }),
      at("server", 440, 210, { sub: "ax.v1alpha1.AX :8080" }),
      at("postgres", 440, 435, { sub: "tasks, workspaces, locks" }),
      at("ateapi", 785, 175, { sub: "CreateActor / ResumeActor" }),
      at("runner", 785, 425, { sub: "PID 1 + /workspace" })
    ],
    zones: [
      Z.local(["user", "cli"], "laptop"),
      Z.control(["server", "postgres"], "control plane"),
      Z.substrate(["ateapi"], "orchestration"),
      Z.sandbox(["runner"], "10.20.3.67")
    ],
    wires: { "cli|server": "gRPC :8080", "server|postgres": "pgx SQL", "server|ateapi": "mTLS :443", "ateapi|runner": "schedule" },
    steps: [
      { title: "Declare & Apply", desc: "You run ax apply -f task.yaml. The CLI decodes the YAML and calls CreateTask on ax-server.", msgs: [
        { from: "user", to: "cli", kind: "host", dt: 0, method: "ax apply -f", info: "ax apply -f examples/simple.yaml", json: { command: "ax apply -f examples/simple.yaml", apiVersion: "ax.io/v1alpha1", kind: "Task", metadata: { name: "simple-task", atespace: "default" } },
          notes: [["ax apply", "Accepts multi-document YAML (Workspace, Model, Task) from a file or stdin."]] },
        { from: "cli", to: "server", kind: "req", dt: 12, info: "gRPC CreateTask (simple-task)", json: { grpc: "ax.v1alpha1.AX/CreateTask", request: { atespace: "default", task: { metadata: { name: "simple-task", atespace: "default" }, spec: { image: "gcr.io/ax-substrate/ate-images/ax-task-runner@sha256:3a0dea6a…", command: ["sh", "-c", "echo $ENVIRONMENT"], debug: true } } } },
          notes: [["CreateTask", "Tasks are immutable once created. Image must be pinned by @sha256 digest."]] }
      ]},
      { title: "Persist & Provision (Suspended)", desc: "ax-server acquires a Postgres lease, stores the Task, creates an ActorTemplate and Actor on Agent Substrate, and immediately suspends it.", msgs: [
        { from: "server", to: "postgres", kind: "sql", dt: 8, info: "INSERT INTO tasks (phase: Pending)", json: { sql: "INSERT INTO tasks (atespace, name, data, saved_at) VALUES ($1, $2, $3::jsonb, clock_timestamp())", params: ["default", "simple-task", { status: { phase: "Pending", taskId: "task-9f8e1a2b" } }] },
          notes: [["protojson", "Resources are stored as jsonb documents so adding API fields never requires a schema migration."]] },
        { from: "server", to: "ateapi", kind: "sub", dt: 45, method: "Substrate/CreateActor", info: "CreateActorTemplate + CreateActor + SuspendActor", json: { service: "ate.api.v1.Control", calls: ["EnsureAtespace(default)", "CreateActorTemplate(simple-task-tmpl-7c4e19a2)", "CreateActor(simple-task)", "SuspendActor(simple-task)"] },
          notes: [["Start Suspended", "New tasks do not consume a worker until you explicitly call ax resume."]] },
        { from: "server", to: "cli", kind: "res", dt: 10, info: "task/simple-task created (Suspended)", json: { grpc: "ax.v1alpha1.AX/CreateTaskResponse", status: { phase: "Suspended", taskId: "task-9f8e1a2b", actor: "simple-task" } } }
      ]},
      { title: "Resume & Boot Sandbox", desc: "You run ax resume task simple-task. Substrate assigns a gVisor worker, boots ax-task-runner, and ax-server polls /readyz until the workspace is initialized.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 400, info: "gRPC ResumeTask (simple-task)", json: { grpc: "ax.v1alpha1.AX/ResumeTask", request: { atespace: "default", name: "simple-task" } } },
        { from: "server", to: "ateapi", kind: "sub", dt: 90, info: "ResumeActor → worker 10.20.3.67", json: { rpc: "ate.api.v1.Control/ResumeActor", actor: "default/simple-task", assignedWorker: "10.20.3.67", state: "ACTOR_STATE_READY" } },
        { from: "ateapi", to: "runner", kind: "sub", dt: 180, method: "exec ax-task-runner (PID 1)", info: "boot PID 1 (/usr/local/bin/ax-task-runner)", json: { pid1: "/usr/local/bin/ax-task-runner", env: ["AX_TASK_YAML=…", "AX_WORKSPACE_YAML=…"], mounts: ["/workspace (DurableDir)"], listeners: ["0.0.0.0:80 (probes + guest gRPC)", "127.0.0.1:8099 (loopback metadata)"] } },
        { from: "server", to: "runner", kind: "http", dt: 60, method: "GET /readyz?check=workspace", info: "GET /readyz?check=workspace → 200 OK", json: { request: "GET http://10.20.3.67:80/readyz?check=workspace", response: { status: "200 OK", body: "ok" } },
          notes: [["/readyz", "Returns 503 while cloning Git repos on maiden boot, then 200 OK once .git/.ax/initialized is written."]] },
        { from: "server", to: "cli", kind: "res", dt: 12, method: "AX/ResumeTaskResponse", info: "task/simple-task resumed (Running)", json: { status: { phase: "Running", actor: "simple-task", workerIp: "10.20.3.67", conditions: [{ type: "WorkspaceReady", status: "True" }, { type: "Ready", status: "True", reason: "TaskRunning" }] } } }
      ]},
      { title: "Inspect over ax ssh", desc: "Because spec.debug is true, you can run commands or open an interactive PTY inside the sandbox via Guest ProcessService.", msgs: [
        { from: "cli", to: "runner", kind: "req", dt: 500, info: "ax ssh simple-task -- ls -la /workspace", json: { grpc: "ateenv.v1alpha.ProcessService/StartProcess", headers: { "ate-target-actor": "default/simple-task" }, command: "/bin/ls", args: ["-la", "/workspace"], tty: false } },
        { from: "runner", to: "cli", kind: "res", dt: 25, info: "stdout: .ax/ AGENTS.md · exit 0", json: { grpc: "ateenv.v1alpha.ProcessService/StreamProcessOutput", stdout: "drwxr-xr-x 3 root root 4096 Nov  5 22:00 .\ndrwxr-xr-x 2 root root 4096 Nov  5 22:00 .ax\n-rw-r--r-- 1 root root  112 Nov  5 22:00 AGENTS.md\n", exitCode: 0 } }
      ]},
      { title: "Suspend & Checkpoint", desc: "When idle, ax suspend checkpoints the /workspace volume to object storage and releases the gVisor worker.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 600, info: "gRPC SuspendTask (simple-task)", json: { grpc: "ax.v1alpha1.AX/SuspendTask", request: { atespace: "default", name: "simple-task" } } },
        { from: "server", to: "ateapi", kind: "sub", dt: 120, info: "SuspendActor (SNAPSHOT_FIDELITY_VOLUMES)", json: { rpc: "ate.api.v1.Control/SuspendActor", actor: "default/simple-task", snapshotFidelity: "SNAPSHOT_FIDELITY_VOLUMES", workerReleased: true } },
        { from: "server", to: "cli", kind: "res", dt: 10, method: "AX/SuspendTaskResponse", info: "task/simple-task suspended (0 CPU/RAM)", json: { status: { phase: "Suspended", workerIp: "", conditions: [{ type: "WorkspaceReady", status: "True" }, { type: "Ready", status: "False", reason: "TaskSuspended" }] } } }
      ]}
    ]
  },

  // ───────────── 2. CORE ARCHITECTURE
  {
    id: "primitives", code: "The 3 Primitives", name: "Workspace, Model, and Task", group: "core", tag: "v1alpha1",
    summary: "AX gives you three declarative ax.io/v1alpha1 resources that can live in a single multi-document YAML file. Workspaces and Models are mutable templates updated in-place via UpdateWorkspace and UpdateModel; Tasks are immutable execution units created via CreateTask that snapshot their bound Workspace on creation.",
    facts: [
      ["apiVersion", "ax.io/v1alpha1 across all three resource kinds"],
      ["Workspace", "Mutable: spec.git[], spec.files[], spec.mcp.servers[], spec.skills"],
      ["Model", "Mutable: spec.provider, spec.model, spec.secretKey (K8s Secret ref)"],
      ["Task", "Immutable: spec.image (@sha256), spec.workspace.name, spec.config, spec.resources.limits, spec.debug"],
      ["Default limits", "If omitted, ax-server defaults a Task to cpu: 1000m and memory: 512Mi"],
      ["Foreign key check", "CreateTask verifies spec.workspace.name exists in the same atespace before saving (#461)"]
    ],
    links: [
      ["docs/concepts.md", BLOB + "docs/concepts.md"],
      ["docs/manifests.md", BLOB + "docs/manifests.md"],
      ["api/v1alpha1/types.proto", BLOB + "pkg/apis/v1alpha1/types.go"]
    ],
    actors: [
      at("cli", 145, 295, { sub: "yaml.NewDecoder loop" }),
      at("server", 480, 185, { sub: "ax.v1alpha1.AX" }),
      at("postgres", 480, 430, { sub: "workspaces, models, tasks" }),
      at("ateapi", 820, 295, { sub: "ActorTemplate + Actor" })
    ],
    zones: [
      Z.local(["cli"], "client-side split"),
      Z.control(["server", "postgres"], "control plane"),
      Z.substrate(["ateapi"], "orchestration")
    ],
    wires: { "cli|server": "gRPC :8080", "server|postgres": "pgx SQL", "server|ateapi": "gRPC :443" },
    steps: [
      { title: "Apply Workspace", desc: "ax apply reads the first YAML document (kind: Workspace), checks if it exists via GetWorkspace, and upserts it with UpdateWorkspace.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "GetWorkspace + UpdateWorkspace (golang)", json: { grpc: "ax.v1alpha1.AX/UpdateWorkspace", workspace: { apiVersion: "ax.io/v1alpha1", kind: "Workspace", metadata: { name: "golang", atespace: "default" }, spec: { git: [{ name: "origin", repo: "https://github.com/golang/go.git", branch: "my-fix" }], files: [{ path: "AGENTS.md", content: "- Run `go test` to ensure tests pass.\n- Do not modify the public API.\n" }], mcp: { servers: [{ name: "code-search", endpoint: "http://cs-mcp.default.svc:8080/mcp" }] } } } },
          notes: [["Client-side diff", "ax apply compares spec before & after UpdateWorkspace to print created, configured, or unchanged."]] },
        { from: "server", to: "postgres", kind: "sql", dt: 7, info: "UPSERT INTO workspaces (default/golang)", json: { sql: "INSERT INTO workspaces (atespace, name, data, saved_at) VALUES ($1, $2, $3, clock_timestamp()) ON CONFLICT (atespace, name) DO UPDATE SET data = EXCLUDED.data, saved_at = EXCLUDED.saved_at" } },
        { from: "server", to: "cli", kind: "res", dt: 5, method: "AX/UpdateWorkspaceResponse", info: "workspace/golang created", json: { output: "workspace/golang created" } }
      ]},
      { title: "Apply Model", desc: "The second document (kind: Model) binds a provider and model identifier to a Kubernetes Secret name without embedding raw API keys in YAML.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 20, info: "UpdateModel (default-model)", json: { grpc: "ax.v1alpha1.AX/UpdateModel", model: { apiVersion: "ax.io/v1alpha1", kind: "Model", metadata: { name: "default-model", atespace: "default" }, spec: { provider: "google", model: "gemini-3.8-flash", secretKey: "gemini-api-secret" } } },
          notes: [["secretKey", "Names the Kubernetes Secret holding the API key; raw credentials never sit in PostgreSQL."]] },
        { from: "server", to: "postgres", kind: "sql", dt: 6, info: "UPSERT INTO models (default/default-model)", json: { sql: "INSERT INTO models (atespace, name, data, saved_at) VALUES ('default', 'default-model', $1::jsonb, clock_timestamp()) ON CONFLICT DO UPDATE …" } },
        { from: "server", to: "cli", kind: "res", dt: 5, method: "AX/UpdateModelResponse", info: "model/default-model configured", json: { output: "model/default-model configured" } }
      ]},
      { title: "Validate & Create Task", desc: "The third document (kind: Task) references workspace: golang. ax-server validates that the Workspace exists, bakes both YAMLs into the ActorTemplate env, and creates the Task.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 25, info: "CreateTask (test → workspace: golang)", json: { grpc: "ax.v1alpha1.AX/CreateTask", task: { apiVersion: "ax.io/v1alpha1", kind: "Task", metadata: { name: "test", atespace: "default" }, spec: { image: "ghcr.io/my-org/coding-agent@sha256:6772a1f2e8b0…", workspace: { name: "golang" }, config: { goal: "Fix what's broken please." }, resources: { limits: { cpu: "1000m", memory: "512Mi" } }, debug: true } } },
          notes: [["spec.config", "Arbitrary structured JSON/YAML (google.protobuf.Struct, up to 16 KiB) read by the runner or agent."]] },
        { from: "server", to: "postgres", kind: "sql", dt: 5, info: "SELECT data FROM workspaces WHERE name='golang'", json: { sql: "SELECT data FROM workspaces WHERE atespace = 'default' AND name = 'golang'", result: "1 row (verified before saving task)" },
          notes: [["Workspace check (#461)", "If the referenced Workspace does not exist, CreateTask fails immediately with NotFound instead of leaving a broken task."]] },
        { from: "server", to: "ateapi", kind: "sub", dt: 40, method: "Substrate/CreateActor", info: "CreateActorTemplate + CreateActor + SuspendActor", json: { template: "test-tmpl-4a91c02e", env: { AX_TASK_YAML: "<serialized Task YAML>", AX_WORKSPACE_YAML: "<serialized Workspace YAML>" }, initialPhase: "Suspended" } },
        { from: "server", to: "cli", kind: "res", dt: 8, method: "AX/CreateTaskResponse", info: "task/test created", json: { output: "task/test created" } }
      ]}
    ]
  },

  {
    id: "split-state", code: "Why Not CRDs?", name: "PostgreSQL + Substrate split-state", group: "core", tag: "DESIGN.md",
    summary: "Storing millions of short-lived agent tasks as Kubernetes Custom Resources pushes etcd past its comfort zone (single-digit GB limits and write-rate bottlenecks). AX splits state cleanly: PostgreSQL stores only what AX owns, while live runtime state (Running/Suspended phase, workerIP, Ready condition) is read directly from Agent Substrate and overlaid on every GetTask and ListTasks call.",
    facts: [
      ["etcd bottleneck", "K8s etcd caps around ~8 GB and struggles under high write churn from millions of short-lived tasks"],
      ["Stored in Postgres", "spec, metadata, status.taskId, status.conditions[WorkspaceReady], and AX-owned phases (Pending, Failed, Terminating)"],
      ["Stripped by storedStatus()", "status.actor, status.workerIp, status.conditions[Ready], and actor-owned phases (Running, Suspended)"],
      ["Overlaid on Read", "applyActor() merges live Substrate Actor state into the Task on GetTask / ListTasks"],
      ["ListTasks N+1 fix", "ListTasks groups page items by atespace and makes 1 ListActors call per atespace"],
      ["Zero drift", "If a worker crashes or suspends in Substrate, ax get tasks sees it immediately with zero reconciliation lag"]
    ],
    links: [
      ["DESIGN.md", BLOB + "DESIGN.md"],
      ["internal/server/server.go", BLOB + "internal/server/server.go"],
      ["internal/store/postgres/schema.sql", BLOB + "internal/store/postgres/schema.sql"]
    ],
    actors: [
      at("cli", 145, 295, { sub: "ax get tasks" }),
      at("server", 480, 185, { sub: "storedStatus / applyActor" }),
      at("postgres", 480, 430, { sub: "AX-owned fields only" }),
      at("ateapi", 820, 295, { sub: "live Actor runtime state" })
    ],
    zones: [
      Z.local(["cli"], "client"),
      Z.control(["server", "postgres"], "control plane"),
      Z.substrate(["ateapi"], "orchestration")
    ],
    wires: { "cli|server": "gRPC", "server|postgres": "storedStatus()", "server|ateapi": "ListActors / GetActor" },
    steps: [
      { title: "Strip Before Write (storedStatus)", desc: "Whenever ax-server saves a Task to PostgreSQL, storedStatus() strips actor, workerIP, the Ready condition, and Running/Suspended phases so Postgres never holds a stale copy of runtime state.", msgs: [
        { from: "server", to: "postgres", kind: "sql", dt: 0, method: "SQL UPSERT (storedStatus)", info: "saveTask → storedStatus(task) strips actor fields", json: { helper: "storedStatus(task)", keptInPostgres: { metadata: { name: "test", atespace: "default" }, spec: { image: "…" }, status: { taskId: "task-9f8e1a2b", conditions: [{ type: "WorkspaceReady", status: "True", reason: "Succeeded" }] } }, strippedBeforeSave: ["status.phase (when Running/Suspended)", "status.actor", "status.workerIp", "status.conditions[type=Ready]"] },
          notes: [["Why strip?", "If Postgres stored phase=Running or workerIp=10.20.3.67, any actor crash or reschedule in Substrate would make Postgres lie until a background sync ran."]] }
      ]},
      { title: "Query Stored Tasks", desc: "When you run ax get tasks, ax-server first queries the paginated jsonb rows from PostgreSQL ordered by saved_at DESC.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 120, info: "gRPC ListTasks (atespace: default, pageSize: 50)", json: { grpc: "ax.v1alpha1.AX/ListTasks", request: { atespace: "default", pageSize: 50 } } },
        { from: "server", to: "postgres", kind: "sql", dt: 6, info: "SELECT data FROM tasks WHERE atespace='default' ORDER BY saved_at DESC", json: { sql: "SELECT data FROM tasks WHERE atespace = $1 ORDER BY saved_at DESC, name ASC LIMIT 51", rowsReturned: 3, note: "Each row has spec, metadata, taskId, and WorkspaceReady—but phase is empty for provisioned tasks!" } }
      ]},
      { title: "Batch-Fetch Live Actors", desc: "Instead of calling GetActor N times, listTasks groups the page by atespace and makes a single ListActors call to Agent Substrate.", msgs: [
        { from: "server", to: "ateapi", kind: "sub", dt: 14, info: "ListActors (1 call for all tasks in 'default')", json: { rpc: "ate.api.v1.Control/ListActors", request: { parent: "atespaces/default" }, actors: [
          { name: "atespaces/default/actors/test", state: "ACTOR_STATE_READY", workerIp: "10.20.3.67" },
          { name: "atespaces/default/actors/nightly-audit", state: "ACTOR_STATE_SUSPENDED", workerIp: "" },
          { name: "atespaces/default/actors/broken-run", state: "ACTOR_STATE_CRASHED", workerIp: "" }
        ] },
          notes: [["O(1) Substrate RPCs", "Whether the page has 1 task or 100 tasks in the default atespace, ax-server makes just one ListActors RPC."]] }
      ]},
      { title: "Overlay & Compute Ready (applyActor)", desc: "applyActor() merges each Actor's live state with the stored WorkspaceReady condition to compute Phase and Ready on the fly.", msgs: [
        { from: "server", to: "cli", kind: "res", dt: 8, method: "AX/ListTasksResponse", info: "merged tasks: Running, Suspended, Failed (ActorCrashed)", json: { tasks: [
          { name: "test", phase: "Running", actor: "test", workerIp: "10.20.3.67", ready: "True (TaskRunning = ACTOR_STATE_READY && WorkspaceReady)" },
          { name: "nightly-audit", phase: "Suspended", actor: "nightly-audit", workerIp: "", ready: "False (TaskSuspended)" },
          { name: "broken-run", phase: "Failed", actor: "broken-run", workerIp: "", ready: "False (ActorCrashed)" }
        ] },
          notes: [["Ready formula", "Ready is True if and only if Substrate reports ACTOR_STATE_READY AND AX's stored WorkspaceReady condition is True."]] }
      ]}
    ]
  },

  {
    id: "locking", code: "Distributed Leases", name: "PostgreSQL locks & 10s renewal", group: "core", tag: "postgres/lock.go",
    summary: "Multiple ax-server replicas coordinate without etcd, ZooKeeper, or PostgreSQL session-level advisory locks. Every mutation acquires a row lease in the locks table using PostgreSQL's own clock_timestamp(), and a background goroutine renews the 30s lease every 10s (LockTTL/3) across slow microVM snapshot and restore RPCs.",
    facts: [
      ["Key format", "<kind>/<atespace>/<name> (e.g., task/default/test)"],
      ["Why not advisory locks?", "pg_advisory_lock pins a pooled connection across slow Substrate RPCs and drops silently if the connection resets"],
      ["Clock source", "PostgreSQL clock_timestamp() — ax-server replicas do not need synchronized wall clocks"],
      ["Default TTL & Renewal", "LockTTL = 30s, renewed every LockTTL/3 (10s) by a background goroutine"],
      ["Contention", "Waiters poll every LockRetryInterval (100ms); no LISTEN/NOTIFY required (PgBouncer-friendly)"]
    ],
    links: [
      ["internal/store/postgres/lock.go", BLOB + "internal/store/postgres/lock.go"],
      ["internal/lock/lock.go", BLOB + "internal/lock/lock.go"]
    ],
    actors: [
      at("cli", 145, 295, { sub: "ax resume task test" }),
      at("server", 480, 185, { sub: "s.store.Lock(ctx, …)" }),
      at("postgres", 480, 430, { sub: "locks table (clock_timestamp)" }),
      at("ateapi", 820, 295, { sub: "slow microVM RPC" })
    ],
    zones: [
      Z.local(["cli"], "caller"),
      Z.control(["server", "postgres"], "control plane"),
      Z.substrate(["ateapi"], "orchestration")
    ],
    wires: { "cli|server": "gRPC", "server|postgres": "pgx pool", "server|ateapi": "long RPC" },
    steps: [
      { title: "Acquire Lease (tryLock)", desc: "ax-server generates a 16-byte random hex token and executes an atomic INSERT ... ON CONFLICT DO UPDATE that succeeds only if no row exists or the existing row's expires_at has passed.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "ResumeTask (default/test)", json: { grpc: "ax.v1alpha1.AX/ResumeTask", request: { atespace: "default", name: "test" } } },
        { from: "server", to: "postgres", kind: "sql", dt: 4, info: "INSERT INTO locks ... WHERE locks.expires_at <= clock_timestamp()", json: { sql: "INSERT INTO locks (key, token, expires_at)\nVALUES ($1, $2, clock_timestamp() + $3 * interval '1 millisecond')\nON CONFLICT (key) DO UPDATE\nSET token = EXCLUDED.token, expires_at = EXCLUDED.expires_at\nWHERE locks.expires_at <= clock_timestamp()", params: ["task/default/test", "a8f39c1204b7e6d19023fa81c4509b1e", 30000], rowsAffected: 1 },
          notes: [["clock_timestamp()", "All expiry math uses the database's clock, so clock skew between ax-server pods never corrupts a lease."], ["RowsAffected == 1", "1 means the lease was acquired; 0 means another holder is active and the caller enters the 100ms retry ticker."]] }
      ]},
      { title: "Renew During Slow Substrate RPC", desc: "While ResumeTask waits on Agent Substrate and workspace Git cloning (which can take 15–60s), makeUnlock's background goroutine extends expires_at every 10s.", msgs: [
        { from: "server", to: "ateapi", kind: "sub", dt: 5000, method: "Substrate/ResumeActor", info: "ResumeActor + poll /readyz (running >10s…)", json: { operation: "reconciler.Resume(ctx, task, ws)", elapsed: "10.0s", note: "waiting for maiden Git clone" } },
        { from: "server", to: "postgres", kind: "sql", dt: 10000, info: "UPDATE locks SET expires_at = clock_timestamp() + 30s (tick 1)", json: { sql: "UPDATE locks SET expires_at = clock_timestamp() + $3 * interval '1 millisecond'\nWHERE key = $1 AND token = $2", params: ["task/default/test", "a8f39c1204b7e6d19023fa81c4509b1e", 30000], rowsAffected: 1 },
          notes: [["Why short TTL + renewal?", "A fixed 5-minute TTL would wedge the task for 5 minutes if ax-server crashed mid-call. A 30s lease renewed every 10s bounds crash recovery to <=30s while supporting arbitrarily long operations."]] }
      ]},
      { title: "Release Lease (unlock)", desc: "Once ResumeTask finishes, defer unlock() cancels the renewal goroutine, waits for it to exit, and deletes the lock row matching both key and token.", msgs: [
        { from: "server", to: "postgres", kind: "sql", dt: 4000, info: "DELETE FROM locks WHERE key = $1 AND token = $2", json: { sql: "DELETE FROM locks WHERE key = $1 AND token = $2", params: ["task/default/test", "a8f39c1204b7e6d19023fa81c4509b1e"], rowsAffected: 1 },
          notes: [["AND token = $2", "Ensures a slow holder whose lease expired during a DB outage can never accidentally delete a new holder's lock."]] },
        { from: "server", to: "cli", kind: "res", dt: 6, method: "AX/ResumeTaskResponse", info: "ResumeTaskResponse (Running)", json: { status: { phase: "Running", workerIp: "10.20.3.67" } } }
      ]}
    ]
  },

  // ───────────── 3. TASK LIFECYCLE
  {
    id: "create", code: "CreateTask", name: "Validation, template digesting & start-suspended", group: "lifecycle", tag: "reconciler.Suspend",
    summary: "Creating a Task validates the manifest, saves an initial Pending record in PostgreSQL, builds a content-addressed ActorTemplate (<task>-tmpl-<sha256[:4]>) with AX_TASK_YAML and AX_WORKSPACE_YAML baked into environment variables, creates the Actor on Agent Substrate, and immediately suspends it so new tasks cost zero compute until resumed.",
    facts: [
      ["Name rules", "RFC 1123 DNS label (1–63 lowercase alphanumeric or '-', max 48 chars so <task>-tmpl-<8hex> fits 63 chars)"],
      ["Env size cap", "Serialized AX_TASK_YAML must be <= 31 KiB (31,744 bytes) to fit inside Linux MAX_ARG_STRLEN (128 KiB)"],
      ["Template name", "<task>-tmpl-<first 4 bytes of sha256(ActorTemplate) as 8 hex chars>"],
      ["Entrypoint", "Always /usr/local/bin/ax-task-runner (never spec.command directly)"],
      ["Initial phase", "reconciler.Suspend leaves the newly created Actor in ACTOR_STATE_SUSPENDED"]
    ],
    links: [
      ["internal/server/server.go", BLOB + "internal/server/server.go"],
      ["internal/controller/reconciler.go", BLOB + "internal/controller/reconciler.go"],
      ["internal/substrate/client.go", BLOB + "internal/substrate/client.go"]
    ],
    actors: [
      at("cli", 145, 295, { sub: "ax apply -f task.yaml" }),
      at("server", 465, 185, { sub: "CreateTask + Suspend" }),
      at("postgres", 465, 430, { sub: "tasks + workspaces" }),
      at("ateapi", 820, 295, { sub: "Atespace, Template, Actor" })
    ],
    zones: [
      Z.local(["cli"], "client"),
      Z.control(["server", "postgres"], "control plane"),
      Z.substrate(["ateapi"], "orchestration")
    ],
    wires: { "cli|server": "gRPC :8080", "server|postgres": "pgx SQL", "server|ateapi": "ate.api.v1.Control" },
    steps: [
      { title: "Validate & Save Pending", desc: "ax-server validates RFC 1123 naming, resource limits, and the 31 KiB YAML cap, checks that the Workspace exists, and saves the Task in phase Pending with WorkspaceReady=False (Initializing).", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "CreateTask (test)", json: { grpc: "ax.v1alpha1.AX/CreateTask", request: { atespace: "default", task: { metadata: { name: "test" }, spec: { image: "ghcr.io/my-org/agent@sha256:6772a1f2…", workspace: { name: "golang" }, debug: true } } } } },
        { from: "server", to: "postgres", kind: "sql", dt: 8, info: "Save Task (phase: Pending, WorkspaceReady: Initializing)", json: { sql: "INSERT INTO tasks (atespace, name, data, saved_at) VALUES ('default', 'test', $1::jsonb, clock_timestamp())", data: { status: { phase: "Pending", taskId: "task-9f8e1a2b", conditions: [{ type: "WorkspaceReady", status: "False", reason: "Initializing" }] } } } }
      ]},
      { title: "EnsureAtespace & Digest Template", desc: "reconciler.Suspend ensures the target Atespace exists in Substrate, serializes Task and Workspace to YAML, and hashes the ActorTemplate spec to name it test-tmpl-4a91c02e.", msgs: [
        { from: "server", to: "ateapi", kind: "sub", dt: 15, info: "GetAtespace / CreateAtespace (default)", json: { rpc: "ate.api.v1.Control/GetAtespace", name: "atespaces/default", status: "OK (exists)" } },
        { from: "server", to: "ateapi", kind: "sub", dt: 22, info: "CreateActorTemplate (test-tmpl-4a91c02e)", json: { rpc: "ate.api.v1.Control/CreateActorTemplate", parent: "atespaces/default", actorTemplateId: "test-tmpl-4a91c02e", actorTemplate: { container: { image: "ghcr.io/my-org/agent@sha256:6772a1f2…", command: ["/usr/local/bin/ax-task-runner"], env: [{ name: "AX_TASK_YAML", value: "apiVersion: ax.io/v1alpha1\nkind: Task…" }, { name: "AX_WORKSPACE_YAML", value: "apiVersion: ax.io/v1alpha1\nkind: Workspace…" }], resources: { cpuMillis: 1000, memoryBytes: 536870912 } }, durableDirs: ["/workspace"] } },
          notes: [["Why /usr/local/bin/ax-task-runner?", "Substrate always boots ax-task-runner as PID 1, which reads AX_TASK_YAML, sets up /workspace, and then spawns your spec.command."], ["Content-addressed template", "Hashing the template spec into test-tmpl-<8hex> makes template creation idempotent on retries."]] }
      ]},
      { title: "CreateActor & SuspendActor", desc: "ax-server creates the Actor from the template and immediately calls SuspendActor so the new task sits in Suspended state without holding a gVisor worker.", msgs: [
        { from: "server", to: "ateapi", kind: "sub", dt: 30, info: "CreateActor (default/test)", json: { rpc: "ate.api.v1.Control/CreateActor", parent: "atespaces/default", actorId: "test", actor: { template: "atespaces/default/actorTemplates/test-tmpl-4a91c02e", labels: { "ax.io/task": "test", "ax.io/task-id": "task-9f8e1a2b" } } } },
        { from: "server", to: "ateapi", kind: "sub", dt: 35, info: "SuspendActor (default/test)", json: { rpc: "ate.api.v1.Control/SuspendActor", name: "atespaces/default/actors/test", state: "ACTOR_STATE_SUSPENDED" } },
        { from: "server", to: "cli", kind: "res", dt: 10, method: "AX/CreateTaskResponse", info: "CreateTaskResponse (phase: Suspended)", json: { status: { phase: "Suspended", taskId: "task-9f8e1a2b", actor: "test", conditions: [{ type: "WorkspaceReady", status: "False", reason: "Initializing" }, { type: "Ready", status: "False", reason: "TaskSuspended" }] } } }
      ]}
    ]
  },

  {
    id: "resume", code: "ResumeTask", name: "Worker placement & /readyz polling", group: "lifecycle", tag: "reconciler.Resume",
    summary: "When you run ax resume task <name>, ax-server calls ResumeActor on Agent Substrate, which schedules the actor onto a warm gVisor worker in the WorkerPool. If WorkspaceReady is not yet True, ax-server polls GET /readyz?check=workspace every 500ms (racing direct workerIP:80 and atenet-router) until maiden workspace setup finishes.",
    facts: [
      ["Worker assignment", "Substrate assigns a free gVisor sandbox from the WorkerPool and returns workerIP (e.g., 10.20.3.67)"],
      ["Dual-path probe", "waitForWorkspaceReady probes http://<workerIP>:80/readyz?check=workspace and http://atenet-router/readyz?check=workspace concurrently"],
      ["Why dual-path?", "Direct workerIP works in multi-node GKE where pod-to-worker routing is flat; atenet-router works in single-node Kind where worker IPs live inside the containerd bridge"],
      ["503 vs 200", "Runner returns 503 Service Unavailable while cloning Git, then 200 OK once .git/.ax/initialized is written"],
      ["Fast-path resume", "On subsequent resumes, WorkspaceReady is already True in Postgres, so ax-server skips polling!"]
    ],
    links: [
      ["internal/controller/reconciler.go", BLOB + "internal/controller/reconciler.go"],
      ["runner/runner.go", BLOB + "runner/runner.go"],
      ["docs/networking.md", BLOB + "docs/networking.md"]
    ],
    actors: [
      at("cli", 115, 295, { sub: "ax resume task test" }),
      at("server", 360, 295, { sub: "reconciler.Resume" }),
      at("ateapi", 615, 175, { sub: "ResumeActor" }),
      at("router", 615, 425, { sub: "atenet-router :80" }),
      at("runner", 870, 295, { sub: "worker 10.20.3.67:80" })
    ],
    zones: [
      Z.local(["cli"], "laptop"),
      Z.control(["server"], "control plane"),
      Z.substrate(["ateapi", "router"], "Substrate"),
      Z.sandbox(["runner"], "10.20.3.67")
    ],
    wires: { "cli|server": "gRPC", "server|ateapi": "ResumeActor", "server|router": "ate-target-actor", "server|runner": "direct :80", "router|runner": "proxy :80" },
    steps: [
      { title: "ResumeActor on Substrate", desc: "ax-server locks task/default/test and calls EnsureActor + ResumeActor. Substrate binds a free gVisor worker (10.20.3.67) and starts the container.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "gRPC ResumeTask (default/test)", json: { grpc: "ax.v1alpha1.AX/ResumeTask", request: { atespace: "default", name: "test" } } },
        { from: "server", to: "ateapi", kind: "sub", dt: 85, info: "ResumeActor → workerIP 10.20.3.67", json: { rpc: "ate.api.v1.Control/ResumeActor", name: "atespaces/default/actors/test", response: { state: "ACTOR_STATE_READY", workerIp: "10.20.3.67" } } }
      ]},
      { title: "503 While Cloning Git", desc: "ax-task-runner starts :80 immediately so health probes succeed, but /readyz?check=workspace returns 503 while SetupWorkspace clones Git in the background.", msgs: [
        { from: "server", to: "runner", kind: "http", dt: 100, method: "GET /readyz?check=workspace", info: "GET http://10.20.3.67:80/readyz?check=workspace", json: { request: "GET http://10.20.3.67:80/readyz?check=workspace", timeout: "2s" } },
        { from: "runner", to: "server", kind: "err", dt: 12, method: "503 Service Unavailable", info: "503 Service Unavailable (workspace initializing)", json: { status: "503 Service Unavailable", body: "workspace not ready\n", reason: "git fetch origin my-fix still running in /workspace" },
          notes: [["Why /healthz vs /readyz?", "/healthz returns 200 OK immediately so Substrate knows the container booted; /readyz?check=workspace gates AX's WorkspaceReady condition."]] }
      ]},
      { title: "Router + Direct Probe -> 200 OK", desc: "500ms later, SetupWorkspace finishes writing /workspace/.git/.ax/initialized and flips ready.Store(true). The next poll via atenet-router or direct workerIP gets 200 OK.", msgs: [
        { from: "server", to: "router", kind: "http", dt: 500, method: "GET /readyz (atenet-router)", info: "GET /readyz?check=workspace (ate-target-actor: default/test)", json: { request: "GET http://atenet-router.ate-system.svc.cluster.local:80/readyz?check=workspace", headers: { "ate-target-actor": "default/test" } } },
        { from: "router", to: "runner", kind: "http", dt: 4, method: "GET 10.20.3.67:80/readyz", info: "proxy → 10.20.3.67:80/readyz?check=workspace", json: { proxy: "10.20.3.67:80", path: "/readyz?check=workspace" } },
        { from: "runner", to: "router", kind: "http", dt: 5, method: "200 OK", info: "200 OK (ready == true)", json: { status: "200 OK", body: "ok" } },
        { from: "router", to: "server", kind: "http", dt: 4, method: "200 OK", info: "200 OK", json: { status: "200 OK", body: "ok" } }
      ]},
      { title: "Persist WorkspaceReady=True", desc: "ax-server persists WorkspaceReady=True in PostgreSQL and returns the live Running status to the CLI.", msgs: [
        { from: "server", to: "cli", kind: "res", dt: 15, method: "AX/ResumeTaskResponse", info: "ResumeTaskResponse (Phase: Running, Ready: True)", json: { status: { phase: "Running", taskId: "task-9f8e1a2b", actor: "test", workerIp: "10.20.3.67", conditions: [{ type: "WorkspaceReady", status: "True", reason: "Succeeded", message: "Workspace initialized" }, { type: "Ready", status: "True", reason: "TaskRunning", message: "Actor is running and workspace is ready" }] } },
          notes: [["Persisted once", "Now that WorkspaceReady=True is saved in Postgres, future Suspend/Resume cycles skip /readyz polling completely."]] }
      ]}
    ]
  },

  {
    id: "suspend", code: "SuspendTask", name: "Graceful SIGTERM & volume checkpointing", group: "lifecycle", tag: "0 compute idle",
    summary: "Suspending a Task pauses execution with zero idle compute cost. Substrate sends SIGTERM to PID 1 (ax-task-runner), which forwards SIGTERM to the entire agent process group (-pid), waits up to 10s before SIGKILL, checkpoints the durable /workspace filesystem to object storage (SNAPSHOT_FIDELITY_VOLUMES), and returns the gVisor worker to the pool.",
    facts: [
      ["Process group signal", "ax-task-runner spawns spec.command with Setpgid: true and forwards SIGTERM/SIGINT to -cmd.Process.Pid"],
      ["Grace period", "shutdownGracePeriod = 10s before SIGKILL (-pgid)"],
      ["Snapshot fidelity", "SNAPSHOT_FIDELITY_VOLUMES checkpoints DurableDir (/workspace) to object storage"],
      ["Maiden marker survival", "Because .git/.ax/initialized (or .ax/initialized) lives inside /workspace, restoring the volume preserves agent edits without re-cloning!"],
      ["Compute cost", "0 CPU / 0 RAM while Suspended — only object storage bytes for /workspace"]
    ],
    links: [
      ["runner/runner.go", BLOB + "runner/runner.go"],
      ["internal/workspace/setup.go", BLOB + "internal/workspace/setup.go"]
    ],
    actors: [
      at("cli", 115, 295, { sub: "ax suspend task test" }),
      at("server", 365, 295, { sub: "SuspendTask" }),
      at("ateapi", 620, 180, { sub: "SuspendActor" }),
      at("gcs", 620, 425, { sub: "volume snapshot" }),
      at("runner", 870, 295, { sub: "PID 1 + agent pgid" })
    ],
    zones: [
      Z.local(["cli"], "laptop"),
      Z.control(["server"], "control plane"),
      Z.substrate(["ateapi", "gcs"], "Substrate"),
      Z.sandbox(["runner"], "10.20.3.67")
    ],
    wires: { "cli|server": "gRPC", "server|ateapi": "SuspendActor", "ateapi|runner": "SIGTERM", "runner|gcs": "checkpoint" },
    steps: [
      { title: "Request SuspendTask", desc: "You run ax suspend task test. ax-server locks the task and calls reconciler.Suspend → SuspendActor on Agent Substrate.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "gRPC SuspendTask (default/test)", json: { grpc: "ax.v1alpha1.AX/SuspendTask", request: { atespace: "default", name: "test" } } },
        { from: "server", to: "ateapi", kind: "sub", dt: 15, info: "SuspendActor (atespaces/default/actors/test)", json: { rpc: "ate.api.v1.Control/SuspendActor", name: "atespaces/default/actors/test" } }
      ]},
      { title: "Forward SIGTERM to Process Group", desc: "Substrate signals the sandbox container. ax-task-runner catches SIGTERM and forwards it to the negative process group ID (-pgid) so the agent and all its child subprocesses shut down cleanly.", msgs: [
        { from: "ateapi", to: "runner", kind: "sub", dt: 20, method: "kill(-pgid, SIGTERM)", info: "SIGTERM → PID 1 forwards kill(-pgid, SIGTERM)", json: { signal: "SIGTERM", handler: "syscall.Kill(-cmd.Process.Pid, sig)", gracePeriod: "10s (then SIGKILL if still running)" },
          notes: [["Why -pgid?", "Coding agents spawn compilers, test runners, and subshells. Signaling -pgid terminates the whole tree cleanly before the volume is snapshotted."]] }
      ]},
      { title: "Snapshot /workspace & Free Worker", desc: "Substrate snapshots the /workspace DurableDir (including the agent's uncommitted code edits and .git/.ax/initialized) to object storage and releases worker 10.20.3.67 back to the pool.", msgs: [
        { from: "runner", to: "gcs", kind: "sub", dt: 140, method: "Checkpoint /workspace", info: "upload /workspace snapshot (SNAPSHOT_FIDELITY_VOLUMES)", json: { fidelity: "SNAPSHOT_FIDELITY_VOLUMES", durableDirs: ["/workspace"], preservedFiles: ["/workspace/.git/.ax/initialized", "/workspace/AGENTS.md", "/workspace/src/fix.go (agent edits)"] },
          notes: [["Volume marker (#518)", "Keeping the marker at /workspace/.git/.ax/initialized guarantees it survives a volumes-only snapshot/restore so maiden setup never overwrites agent edits on wake."]] },
        { from: "ateapi", to: "server", kind: "sub", dt: 18, method: "ACTOR_STATE_SUSPENDED", info: "Actor state: ACTOR_STATE_SUSPENDED", json: { state: "ACTOR_STATE_SUSPENDED", workerIp: "" } },
        { from: "server", to: "cli", kind: "res", dt: 8, method: "AX/SuspendTaskResponse", info: "task/test suspended", json: { status: { phase: "Suspended", workerIp: "", conditions: [{ type: "WorkspaceReady", status: "True" }, { type: "Ready", status: "False", reason: "TaskSuspended" }] } } }
      ]}
    ]
  },

  {
    id: "delete", code: "DeleteTask & Crash Revert", name: "Template GC & RevertActor recovery", group: "lifecycle", tag: "2 modes",
    summary: "Deleting a Task marks it Terminating in PostgreSQL first, deletes the Actor on Agent Substrate, garbage-collects all per-task ActorTemplates matching ^<task>-tmpl-[0-9a-f]{8}$ with exponential backoff, and finally removes the database row. If instead an Actor crashes at runtime, EnsureActor calls RevertActor to roll back to its last good snapshot.",
    facts: [
      ["Terminating phase", "Persisted before touching Substrate so partial teardowns are visible"],
      ["Template regex GC", "Deletes only templates matching ^<task>-tmpl-[0-9a-f]{8}$ so sibling tasks are never touched"],
      ["Retry backoff", "deleteTaskTemplates retries 10 times (200ms → 2s cap) while Substrate finishes async actor teardown"],
      ["Crash recovery", "When Actor state is ACTOR_STATE_CRASHED, EnsureActor calls RevertActor before resuming"]
    ],
    links: [
      ["internal/controller/reconciler.go", BLOB + "internal/controller/reconciler.go"],
      ["internal/substrate/client.go", BLOB + "internal/substrate/client.go"]
    ],
    variants: [
      {
        id: "gc", label: "DeleteTask & Template GC", hint: "Normal ax delete task teardown and template garbage collection",
        actors: [
          at("cli", 145, 295, { sub: "ax delete task test" }),
          at("server", 465, 185, { sub: "DeleteTask + reconciler.Delete" }),
          at("postgres", 465, 430, { sub: "Terminating → DELETE" }),
          at("ateapi", 820, 295, { sub: "DeleteActor + DeleteActorTemplate" })
        ],
        zones: [
          Z.local(["cli"], "client"),
          Z.control(["server", "postgres"], "control plane"),
          Z.substrate(["ateapi"], "orchestration")
        ],
        wires: { "cli|server": "gRPC", "server|postgres": "pgx SQL", "server|ateapi": "Substrate RPC" },
        steps: [
          { title: "Mark Terminating", desc: "ax-server locks the task and updates its stored phase to Terminating before calling Substrate, so concurrent readers see that teardown is in flight.", msgs: [
            { from: "cli", to: "server", kind: "req", dt: 0, info: "gRPC DeleteTask (default/test)", json: { grpc: "ax.v1alpha1.AX/DeleteTask", request: { atespace: "default", name: "test" } } },
            { from: "server", to: "postgres", kind: "sql", dt: 6, info: "UPDATE tasks SET phase = 'Terminating'", json: { sql: "UPDATE tasks SET data = $3::jsonb WHERE atespace = 'default' AND name = 'test'", status: { phase: "Terminating" } } }
          ]},
          { title: "DeleteActor & GC Templates", desc: "reconciler.Delete calls DeleteActor, then lists ActorTemplates in the atespace and deletes every template matching ^test-tmpl-[0-9a-f]{8}$.", msgs: [
            { from: "server", to: "ateapi", kind: "sub", dt: 25, info: "DeleteActor (atespaces/default/actors/test)", json: { rpc: "ate.api.v1.Control/DeleteActor", name: "atespaces/default/actors/test" } },
            { from: "server", to: "ateapi", kind: "sub", dt: 40, info: "ListActorTemplates + DeleteActorTemplate (test-tmpl-4a91c02e)", json: { rpc: "ate.api.v1.Control/DeleteActorTemplate", matchedRegex: "^test-tmpl-[0-9a-f]{8}$", deleted: ["atespaces/default/actorTemplates/test-tmpl-4a91c02e"], retryPolicy: "up to 10 attempts (200ms..2s) if template still referenced during async actor teardown" } }
          ]},
          { title: "Delete Row from Postgres", desc: "Once Substrate cleanup succeeds (or returns NotFound), ax-server deletes the row from PostgreSQL.", msgs: [
            { from: "server", to: "postgres", kind: "sql", dt: 6, info: "DELETE FROM tasks WHERE atespace='default' AND name='test'", json: { sql: "DELETE FROM tasks WHERE atespace = $1 AND name = $2", params: ["default", "test"] } },
            { from: "server", to: "cli", kind: "res", dt: 5, method: "AX/DeleteTaskResponse", info: "task/test deleted", json: { output: "task/test deleted" } }
          ]}
        ]
      },
      {
        id: "crash", label: "Crash → RevertActor", hint: "Recovering a crashed actor via RevertActor without losing its last volume snapshot",
        actors: [
          at("cli", 145, 295, { sub: "ax resume task test" }),
          at("server", 460, 295, { sub: "EnsureActor recovery" }),
          at("ateapi", 785, 185, { sub: "GetActor / RevertActor" }),
          at("gcs", 785, 425, { sub: "last good snapshot" })
        ],
        zones: [
          Z.local(["cli"], "client"),
          Z.control(["server"], "control plane"),
          Z.substrate(["ateapi", "gcs"], "Substrate")
        ],
        wires: { "cli|server": "gRPC", "server|ateapi": "EnsureActor", "ateapi|gcs": "restore snapshot" },
        steps: [
          { title: "Detect ACTOR_STATE_CRASHED", desc: "While inspectable via GetTask, an Actor in ACTOR_STATE_CRASHED reports Phase=Failed (Reason: ActorCrashed). Running ax resume triggers EnsureActor.", msgs: [
            { from: "cli", to: "server", kind: "req", dt: 0, info: "gRPC ResumeTask (crashed task 'test')", json: { grpc: "ax.v1alpha1.AX/ResumeTask", request: { atespace: "default", name: "test" } } },
            { from: "server", to: "ateapi", kind: "sub", dt: 12, info: "GetActor → ACTOR_STATE_CRASHED", json: { rpc: "ate.api.v1.Control/GetActor", name: "atespaces/default/actors/test", state: "ACTOR_STATE_CRASHED" } }
          ]},
          { title: "RevertActor to Last Snapshot", desc: "EnsureActor calls RevertActor on Agent Substrate, rolling the actor back to its last checkpointed volume snapshot instead of recreating it from scratch.", msgs: [
            { from: "server", to: "ateapi", kind: "sub", dt: 45, info: "RevertActor (atespaces/default/actors/test)", json: { rpc: "ate.api.v1.Control/RevertActor", name: "atespaces/default/actors/test" } },
            { from: "ateapi", to: "gcs", kind: "sub", dt: 60, method: "Restore /workspace snapshot", info: "restore last checkpointed /workspace volume", json: { action: "rollback volume to last snapshot", stateAfterRevert: "ACTOR_STATE_SUSPENDED" } }
          ]},
          { title: "ResumeActor", desc: "With the crashed state cleared by RevertActor, ResumeActor schedules a fresh gVisor worker and boots the restored workspace.", msgs: [
            { from: "server", to: "ateapi", kind: "sub", dt: 70, info: "ResumeActor → ACTOR_STATE_READY", json: { rpc: "ate.api.v1.Control/ResumeActor", state: "ACTOR_STATE_READY", workerIp: "10.20.3.71" } },
            { from: "server", to: "cli", kind: "res", dt: 10, method: "AX/ResumeTaskResponse", info: "task/test resumed (recovered)", json: { status: { phase: "Running", workerIp: "10.20.3.71" } } }
          ]}
        ]
      }
    ]
  },
"""

print("Appended JS_PART_1")

JS_PART_2 = r"""
  // ───────────── 4. INSIDE THE SANDBOX
  {
    id: "runner", code: "The Runner Contract", name: "PID 1, maiden setup & .git/.ax/initialized", group: "sandbox", tag: "runner.go",
    summary: "Every Task container boots /usr/local/bin/ax-task-runner as PID 1. It opens two HTTP listeners (:80 for health/readiness probes and guest gRPC; 127.0.0.1:8099 for loopback metadata), runs maiden workspace initialization (writing inline files, git init/fetch/checkout, and the .git/.ax/initialized marker), and spawns spec.command in its own process group. Even after the command exits, PID 1 stays alive so ax ssh and metadata keep working.",
    facts: [
      ["PID 1 binary", "/usr/local/bin/ax-task-runner (embeds runner.Run(ctx, cfg))"],
      ["Listener 1 (:80)", "0.0.0.0:80 (HTTP/1.1 + h2c): /healthz, /readyz, and (when debug: true) Guest ProcessService & FileSystemService"],
      ["Listener 2 (:8099)", "127.0.0.1:8099 loopback only: /metadata/v1alpha1/ax/task and /metadata/v1alpha1/ax/workspace"],
      ["Maiden marker (#518)", "/workspace/.git/.ax/initialized (for Git repos) or /workspace/.ax/initialized; refuses symlinks via markerLinked()"],
      ["Immortal PID 1", "When spec.command exits, runner logs the exit code and waits for ctx.Done() instead of exiting the container"]
    ],
    links: [
      ["runner/runner.go", BLOB + "runner/runner.go"],
      ["internal/workspace/setup.go", BLOB + "internal/workspace/setup.go"],
      ["docs/sandbox.md", BLOB + "docs/sandbox.md"],
      ["docs/runner.md", BLOB + "docs/runner.md"]
    ],
    actors: [
      at("ateapi", 145, 295, { sub: "boots container" }),
      at("runner", 480, 185, { sub: "ax-task-runner (PID 1)" }),
      at("agent", 480, 425, { sub: "spec.command (child pgid)" }),
      at("git", 825, 185, { sub: "github.com/golang/go" })
    ],
    zones: [
      Z.substrate(["ateapi"], "Substrate"),
      Z.sandbox(["runner", "agent"], "/workspace"),
      Z.external(["git"], "HTTPS")
    ],
    wires: { "ateapi|runner": "PID 1 env", "runner|git": "git fetch", "runner|agent": "exec + :8099" },
    steps: [
      { title: "Boot PID 1 & Open Listeners", desc: "ax-task-runner starts as PID 1, parses AX_TASK_YAML and AX_WORKSPACE_YAML from env, starts 0.0.0.0:80 (probes + guest gRPC if debug: true) and 127.0.0.1:8099 (loopback metadata).", msgs: [
        { from: "ateapi", to: "runner", kind: "sub", dt: 0, method: "exec ax-task-runner (PID 1)", info: "start /usr/local/bin/ax-task-runner (PID 1)", json: { pid: 1, binary: "/usr/local/bin/ax-task-runner", env: { AX_TASK_YAML: "apiVersion: ax.io/v1alpha1\nkind: Task…", AX_WORKSPACE_YAML: "apiVersion: ax.io/v1alpha1\nkind: Workspace…" }, listeners: { probeAndGuest: "0.0.0.0:80 (h2c)", metadata: "127.0.0.1:8099 (loopback)" } } }
      ]},
      { title: "Maiden Workspace Setup", desc: "SetupWorkspace checks markerLinked() to refuse symlinks, writes spec.files (skipping any existing files on rerun), clones spec.git via git init + remote add + fetch --depth 1 + checkout -f FETCH_HEAD, and writes /workspace/.git/.ax/initialized.", msgs: [
        { from: "runner", to: "git", kind: "http", dt: 40, method: "git fetch origin my-fix", info: "git fetch --depth 1 origin my-fix", json: { cwd: "/workspace", commands: ["writeFiles: /workspace/AGENTS.md (0644)", "git init /workspace", "git remote add origin https://github.com/golang/go.git", "git fetch --depth 1 origin my-fix", "git checkout -f FETCH_HEAD"], markerWritten: "/workspace/.git/.ax/initialized" },
          notes: [["Why .git/.ax/initialized?", "Placing the marker inside .git/.ax keeps it on the durable /workspace volume across Suspend/Resume while hiding it from git status, git add -A, and git clean -fdx."], ["Symlink defense", "markerLinked() checks os.Lstat on both the directory and marker file so an untrusted repo or agent cannot symlink it outside /workspace."]] }
      ]},
      { title: "Flip /readyz & Spawn Agent Process Group", desc: "Once SetupWorkspace returns, runner sets ready.Store(true) (making :80/readyz return 200 OK) and spawns spec.command in /workspace with Setpgid: true and AX_METADATA_URL=http://127.0.0.1:8099.", msgs: [
        { from: "runner", to: "agent", kind: "host", dt: 15, method: "exec spec.command (Setpgid)", info: "spawn spec.command (cwd=/workspace, Setpgid=true)", json: { exec: ["my-coding-agent", "--goal", "Fix what's broken please."], cwd: "/workspace", sysProcAttr: { Setpgid: true }, env: ["AX_METADATA_URL=http://127.0.0.1:8099", "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"] },
          notes: [["PID 1 stays alive", "Even after spec.command finishes (exit 0 or non-zero), ax-task-runner remains running as PID 1 so /metadata and ax ssh stay reachable until SuspendTask or DeleteTask."]] }
      ]}
    ]
  },

  {
    id: "metadata", code: "Loopback Metadata & Harnesses", name: "127.0.0.1:8099 & claude-code-runner", group: "sandbox", tag: "2 harnesses",
    summary: "Inside the sandbox, agent code discovers its Task and Workspace configuration by making plain HTTP GET requests to 127.0.0.1:8099 ($AX_METADATA_URL)—modeled on GCP's instance metadata server so any language works with zero SDKs. Custom images can also embed the Go runner package directly, like examples/claude-code which translates spec.config and Workspace MCP servers into a headless claude --print invocation.",
    facts: [
      ["Loopback address", "http://127.0.0.1:8099 ($AX_METADATA_URL) — unreachable from outside the container"],
      ["Endpoints", "/metadata/v1alpha1/ax/task, /metadata/v1alpha1/ax/workspace, and /metadata/v1alpha1/ax/ (index)"],
      ["Content-Type", "application/yaml; charset=utf-8 (GET and HEAD only; POST/PUT return 405)"],
      ["Custom Go harness", "Import github.com/google/ax/runner and pass a custom Config{Task, Workspace, Command, Env}"],
      ["Claude Code example", "cmd/claude-code-runner converts camelCase spec.config keys into --kebab-case flags + --mcp-config"]
    ],
    links: [
      ["internal/metadata/server.go", BLOB + "internal/metadata/server.go"],
      ["cmd/claude-code-runner/main.go", BLOB + "cmd/claude-code-runner/main.go"],
      ["examples/claude-code/task.yaml", BLOB + "examples/claude-code/task.yaml"]
    ],
    variants: [
      {
        id: "default", label: "Default (:8099)", hint: "Any language reads YAML from 127.0.0.1:8099 over loopback",
        actors: [
          at("runner", 185, 295, { sub: "127.0.0.1:8099 metadata" }),
          at("agent", 485, 295, { sub: "agent process in /workspace" }),
          at("mcp", 825, 295, { sub: "cs-mcp.default.svc:8080" })
        ],
        zones: [
          Z.sandbox(["runner", "agent"], "loopback :8099"),
          Z.external(["mcp"], "MCP service")
        ],
        wires: { "runner|agent": "127.0.0.1:8099", "agent|mcp": "MCP HTTP" },
        steps: [
          { title: "Read Task Spec & Goal", desc: "The agent process reads $AX_METADATA_URL/metadata/v1alpha1/ax/task over loopback to inspect its spec.config goal and parameters.", msgs: [
            { from: "agent", to: "runner", kind: "http", dt: 0, method: "GET /metadata/v1alpha1/ax/task", info: "GET http://127.0.0.1:8099/metadata/v1alpha1/ax/task", json: { request: "GET http://127.0.0.1:8099/metadata/v1alpha1/ax/task" } },
            { from: "runner", to: "agent", kind: "http", dt: 2, method: "200 OK (Task YAML)", info: "200 OK · application/yaml (Task)", json: { status: "200 OK", headers: { "Content-Type": "application/yaml; charset=utf-8" }, yaml: { apiVersion: "ax.io/v1alpha1", kind: "Task", metadata: { name: "test", atespace: "default" }, spec: { config: { goal: "Fix what's broken please.", maxIterations: 20 }, workspace: { name: "golang" } } } },
              notes: [["Zero SDK dependency", "Any Python, Node, Go, or shell script can curl $AX_METADATA_URL without linking an AX client library."]] }
          ]},
          { title: "Read Workspace & MCP Endpoints", desc: "Next, the agent fetches /metadata/v1alpha1/ax/workspace to discover pre-cloned Git repos, skill paths, and MCP server endpoints.", msgs: [
            { from: "agent", to: "runner", kind: "http", dt: 5, method: "GET /metadata/v1alpha1/ax/workspace", info: "GET http://127.0.0.1:8099/metadata/v1alpha1/ax/workspace", json: { request: "GET http://127.0.0.1:8099/metadata/v1alpha1/ax/workspace" } },
            { from: "runner", to: "agent", kind: "http", dt: 2, method: "200 OK (Workspace YAML)", info: "200 OK · application/yaml (Workspace)", json: { status: "200 OK", headers: { "Content-Type": "application/yaml; charset=utf-8" }, yaml: { apiVersion: "ax.io/v1alpha1", kind: "Workspace", metadata: { name: "golang" }, spec: { git: [{ repo: "https://github.com/golang/go.git", branch: "my-fix" }], mcp: { servers: [{ name: "code-search", endpoint: "http://cs-mcp.default.svc:8080/mcp" }] } } } } },
            { from: "agent", to: "mcp", kind: "http", dt: 25, method: "POST /mcp (tools/call)", info: "POST /mcp · tools/call", json: { request: "POST http://cs-mcp.default.svc:8080/mcp", method: "tools/call" } }
          ]}
        ]
      },
      {
        id: "claude", label: "Claude Code", hint: "Custom Go runner (cmd/claude-code-runner) that embeds runner.Run()",
        actors: [
          at("runner", 185, 295, { sub: "claude-code-runner PID 1" }),
          at("agent", 485, 295, { sub: "claude --print" }),
          at("mcp", 825, 295, { sub: "--mcp-config server" })
        ],
        zones: [
          Z.sandbox(["runner", "agent"], "claude-code image"),
          Z.external(["mcp"], "MCP service")
        ],
        wires: { "runner|agent": "exec claude", "agent|mcp": "streamable HTTP" },
        steps: [
          { title: "Synthesize CLI Flags from spec.config", desc: "cmd/claude-code-runner reads AX_TASK_YAML and AX_WORKSPACE_YAML, converts camelCase keys in spec.config (maxTurns, dangerouslySkipPermissions, settings) into kebab-case flags, and builds --mcp-config from Workspace.spec.mcp.", msgs: [
            { from: "runner", to: "agent", kind: "host", dt: 0, method: "exec claude --print", info: "buildCommand(task.spec.config, ws.spec.mcp)", json: { binary: "/usr/local/bin/claude-code-runner", inputConfig: { prompt: "Read the repo, run pytest, fix failing tests, write /workspace/claude-output.md", model: "claude-opus-5-5", maxTurns: 50, dangerouslySkipPermissions: true, settings: { includeCoAuthoredBy: false } }, synthesizedArgs: ["claude", "--print", "--dangerously-skip-permissions", "--max-turns=50", "--model=claude-opus-5-5", "--settings={\"includeCoAuthoredBy\":false}", "--mcp-config={\"mcpServers\":{\"docs\":{\"type\":\"http\",\"url\":\"http://docs-mcp.default.svc:8080/mcp\"}}}", "--", "Read the repo, run pytest…"] },
              notes: [["Embedded runner.Run()", "claude-code-runner sets task.Spec.Command to the synthesized claude command and calls runner.Run(ctx, cfg) so probes, maiden setup, and metadata all work identically."]] }
          ]},
          { title: "Run Headless Session in /workspace", desc: "Claude Code runs non-interactively in /workspace with CLAUDE.md guidance, calls MCP servers, edits code, and writes its markdown report to /workspace/claude-output.md.", msgs: [
            { from: "agent", to: "mcp", kind: "http", dt: 120, method: "POST /mcp (tools/list)", info: "POST /mcp (from synthesized --mcp-config)", json: { url: "http://docs-mcp.default.svc:8080/mcp", method: "tools/list" } },
            { from: "agent", to: "runner", kind: "host", dt: 800, method: "exit 0 (PID 1 stays alive)", info: "wrote /workspace/claude-output.md · exit 0", json: { reportPath: "/workspace/claude-output.md", exitCode: 0, note: "PID 1 stays alive so you can run: ax ssh claude-code -- cat /workspace/claude-output.md" } }
          ]}
        ]
      }
    ]
  },

  // ───────────── 5. NETWORKING, TUNNELS & SSH
  {
    id: "tunnels", code: "Context Auto-Tunnels", name: "kubectx, ~/.ax/tunnels & /healthz reuse", group: "networking", tag: "internal/tunnel",
    summary: "You never have to run kubectl port-forward manually to use ax. When $AX_SERVER is unset, ax reads your active Kubernetes context (kubectx), checks ~/.ax/tunnels/<ctx>.json for a cached background tunnel, probes GET /healthz (400ms timeout) to verify it is still alive, or spawns a detached kubectl port-forward -n ax-system svc/ax-server :8080.",
    facts: [
      ["State directory", "~/.ax/tunnels/<sanitized-kubectx>.json + .log"],
      ["Reuse check", "PID alive (kill -0) AND GET http://127.0.0.1:<port>/healthz returns 200 OK within 400ms"],
      ["Detached spawn", "kubectl --context <ctx> -n ax-system port-forward svc/ax-server :8080 with Setsid: true"],
      ["kubectx aware", "Switching clusters with kubectx automatically routes ax to that cluster's tunnel"],
      ["Inspect / stop", "ax ctx, ax tunnel list, and ax tunnel stop manage background tunnels"]
    ],
    links: [
      ["internal/tunnel/tunnel.go", BLOB + "internal/tunnel/tunnel.go"],
      ["cmd/ax/main.go", BLOB + "cmd/ax/main.go"]
    ],
    actors: [
      at("user", 135, 295, { sub: "kubectx prod-cluster" }),
      at("cli", 430, 295, { sub: "~/.ax/tunnels/prod-cluster.json" }),
      at("k8s", 785, 175, { sub: "kubectl port-forward" }),
      at("server", 785, 425, { sub: "svc/ax-server:8080" })
    ],
    zones: [
      Z.local(["user", "cli"], "laptop"),
      Z.external(["k8s"], "K8s API"),
      Z.control(["server"], "control plane")
    ],
    wires: { "user|cli": "ax get tasks", "cli|k8s": "spawns tunnel", "cli|server": "127.0.0.1:54321 → :8080" },
    steps: [
      { title: "Check Cached Tunnel State", desc: "You run ax get tasks. The CLI resolves the active kube context (prod-cluster) and checks ~/.ax/tunnels/prod-cluster.json.", msgs: [
        { from: "user", to: "cli", kind: "host", dt: 0, method: "ax get tasks", info: "ax get tasks (context: prod-cluster)", json: { command: "ax get tasks", activeKubeContext: "prod-cluster", stateFile: "~/.ax/tunnels/prod-cluster.json", cachedState: "none (or stale PID)" } }
      ]},
      { title: "Spawn Detached kubectl port-forward", desc: "On a cache miss, tunnel.Ensure spawns a detached background process (Setsid: true) running kubectl port-forward svc/ax-server :8080 and parses 'Forwarding from 127.0.0.1:<port>' from stdout.", msgs: [
        { from: "cli", to: "k8s", kind: "http", dt: 35, method: "kubectl port-forward :8080", info: "kubectl --context prod-cluster -n ax-system port-forward svc/ax-server :8080", json: { spawn: ["kubectl", "--context", "prod-cluster", "-n", "ax-system", "port-forward", "svc/ax-server", ":8080"], sysProcAttr: { Setsid: true }, stdoutLine: "Forwarding from 127.0.0.1:54321 -> 8080", savedJson: { context: "prod-cluster", namespace: "ax-system", address: "127.0.0.1:54321", pid: 48291, startedAt: "2026-11-05T22:10:00Z" } },
          notes: [["Why :8080 (ephemeral local port)?", "Letting the OS pick a free local port (e.g. 54321) means you can hold open tunnels to dev, staging, and prod clusters simultaneously without port collisions."]] }
      ]},
      { title: "Verify /healthz & Send gRPC", desc: "The CLI probes GET http://127.0.0.1:54321/healthz (400ms timeout) and then dials gRPC over 127.0.0.1:54321. Subsequent ax commands reuse this tunnel in <2ms!", msgs: [
        { from: "cli", to: "server", kind: "http", dt: 8, method: "GET /healthz", info: "GET http://127.0.0.1:54321/healthz → 200 OK", json: { request: "GET http://127.0.0.1:54321/healthz", timeout: "400ms", response: "200 OK" } },
        { from: "cli", to: "server", kind: "req", dt: 6, info: "gRPC ListTasks over 127.0.0.1:54321", json: { grpc: "ax.v1alpha1.AX/ListTasks", target: "127.0.0.1:54321" } },
        { from: "server", to: "cli", kind: "res", dt: 10, method: "AX/ListTasksResponse", info: "ListTasksResponse", json: { tasks: [{ name: "simple-task", phase: "Running" }] } }
      ]}
    ]
  },

  {
    id: "atenet", code: "Stateless Actor Routing", name: "atenet-router & ate-target-actor", group: "networking", tag: "2 modes",
    summary: "Tasks do not get individual Kubernetes Services or Ingresses—creating a million Services would melt kube-proxy and CoreDNS. Instead, every HTTP or gRPC request to a task goes through Agent Substrate's stateless atenet-router Service in ate-system. A single header, ate-target-actor: <atespace>/<task>, selects the target actor, wakes it if suspended, and proxies the request to its worker IP.",
    facts: [
      ["Router Service", "atenet-router.ate-system.svc.cluster.local (:80 HTTP / :443 mTLS)"],
      ["Routing header", "ate-target-actor: <atespace>/<task> (e.g., default/task123)"],
      ["Host preservation", "Host and :authority headers are passed untouched to your container"],
      ["Wake-on-request", "If the target actor is Suspended, atenet-router resumes it automatically before proxying"],
      ["Zero K8s Services", "1 cluster-wide Service routes to 1,000,000+ actors"]
    ],
    links: [
      ["docs/networking.md", BLOB + "docs/networking.md"],
      ["internal/controller/reconciler.go", BLOB + "internal/controller/reconciler.go"]
    ],
    variants: [
      {
        id: "cluster", label: "In-Cluster DNS", hint: "Calling a task from inside the cluster via atenet-router.ate-system.svc",
        actors: [
          at("server", 155, 295, { label: "In-Cluster Caller", sub: "ax-server or pod" }),
          at("ateapi", 495, 175, { sub: "resolve / wake actor" }),
          at("router", 495, 420, { sub: "atenet-router:80" }),
          at("runner", 835, 295, { sub: "task123 on 10.20.3.67:80" })
        ],
        zones: [
          Z.control(["server"], "cluster pod"),
          Z.substrate(["router", "ateapi"], "Substrate"),
          Z.sandbox(["runner"], "10.20.3.67")
        ],
        wires: { "server|router": "ate-target-actor", "router|ateapi": "lookup/wake", "router|runner": "proxy :80" },
        steps: [
          { title: "Send Request with ate-target-actor", desc: "Any pod in the cluster sends an HTTP or gRPC request to atenet-router.ate-system.svc.cluster.local with the header ate-target-actor: default/task123.", msgs: [
            { from: "server", to: "router", kind: "http", dt: 0, method: "GET /readyz (ate-target-actor)", info: "GET /readyz (Header: ate-target-actor: default/task123)", json: { curl: "curl -H 'ate-target-actor: default/task123' http://atenet-router.ate-system.svc.cluster.local/readyz", headers: { Host: "atenet-router.ate-system.svc.cluster.local", "ate-target-actor": "default/task123" } },
              notes: [["Header-based routing", "Because routing uses ate-target-actor instead of DNS per task, CoreDNS and kube-proxy tables stay constant-size at million-task scale."]] }
          ]},
          { title: "Resolve (or Auto-Wake) & Proxy", desc: "atenet-router resolves default/task123 to worker 10.20.3.67 (waking the actor first if it was suspended) and proxies the request to 10.20.3.67:80.", msgs: [
            { from: "router", to: "ateapi", kind: "sub", dt: 6, method: "Resolve default/task123", info: "resolve default/task123 → 10.20.3.67", json: { actor: "default/task123", state: "ACTOR_STATE_READY", workerIp: "10.20.3.67" } },
            { from: "router", to: "runner", kind: "http", dt: 4, method: "GET 10.20.3.67:80/readyz", info: "GET http://10.20.3.67:80/readyz", json: { upstream: "10.20.3.67:80", path: "/readyz" } },
            { from: "runner", to: "router", kind: "http", dt: 3, method: "200 OK", info: "200 OK", json: { status: "200 OK", body: "ok" } },
            { from: "router", to: "server", kind: "http", dt: 3, method: "200 OK", info: "200 OK", json: { status: "200 OK", body: "ok" } }
          ]}
        ]
      },
      {
        id: "laptop", label: "Laptop Tunnel", hint: "Reaching a task from your laptop via kubectl port-forward svc/atenet-router",
        actors: [
          at("cli", 155, 295, { label: "Your Laptop", sub: "localhost:8001" }),
          at("router", 495, 295, { sub: "svc/atenet-router:80" }),
          at("runner", 835, 295, { sub: "task123 on 10.20.3.67:80" })
        ],
        zones: [
          Z.local(["cli"], "port-forward :8001"),
          Z.substrate(["router"], "Substrate"),
          Z.sandbox(["runner"], "10.20.3.67")
        ],
        wires: { "cli|router": "127.0.0.1:8001 → :80", "router|runner": "proxy :80" },
        steps: [
          { title: "Port-Forward svc/atenet-router", desc: "From your machine, port-forward svc/atenet-router in ate-system and send the same ate-target-actor header to localhost:8001.", msgs: [
            { from: "cli", to: "router", kind: "http", dt: 0, method: "GET localhost:8001/readyz", info: "curl -H 'ate-target-actor: default/task123' http://localhost:8001/readyz", json: { commands: ["kubectl -n ate-system port-forward svc/atenet-router 8001:80", "curl -H 'ate-target-actor: default/task123' http://localhost:8001/readyz"], headers: { "ate-target-actor": "default/task123" } } }
          ]},
          { title: "Proxy to Sandbox & Return", desc: "atenet-router forwards the HTTP request to worker 10.20.3.67:80 and streams the 200 OK response back through your local tunnel.", msgs: [
            { from: "router", to: "runner", kind: "http", dt: 8, method: "GET 10.20.3.67:80/readyz", info: "proxy → 10.20.3.67:80/readyz", json: { upstream: "10.20.3.67:80", path: "/readyz" } },
            { from: "runner", to: "router", kind: "http", dt: 4, method: "200 OK", info: "200 OK", json: { status: "200 OK", body: "ok" } },
            { from: "router", to: "cli", kind: "http", dt: 5, method: "200 OK", info: "200 OK", json: { status: "200 OK", body: "ok" } }
          ]}
        ]
      }
    ]
  },

  {
    id: "ssh", code: "ax ssh & Ephemeral mTLS", name: "PodCertificateRequest & Guest ProcessService", group: "networking", tag: "router_tls.go",
    summary: "Running ax ssh <task> shells into a running sandbox without running sshd inside the container. When the worker IP isn't directly routable from your laptop, the CLI mints a short-lived ECDSA P-256 client certificate via Kubernetes PodCertificateRequest (matching ax-server's SPIFFE identity), opens a port-forward to svc/atenet-router:443, and streams stdin/stdout/signals over Agent Substrate's Guest ProcessService.",
    facts: [
      ["Precondition", "Task must have spec.debug: true (off by default) and Phase == Running"],
      ["Server CA trust", "ClusterTrustBundle servicedns.podcert.ate.dev:cluster.local"],
      ["Client mTLS cert", "Ephemeral K8s PodCertificateRequest (podidentity.podcert.ate.dev/identity) for SA ax-system/ax-server"],
      ["Cert caching (#541)", "Cached in-process until time.Now().After(cert.NotAfter), then transparently rotated"],
      ["Guest RPCs", "ateenv.v1alpha.ProcessService: StartProcess, WriteProcessInput, StreamProcessOutput, ResizeTty, SignalProcess"],
      ["Ctrl-C handling", "Single Ctrl-C sends SignalProcess(SIGINT) to remote process; double Ctrl-C within 1s exits local CLI"]
    ],
    links: [
      ["cmd/ax/ssh.go", BLOB + "cmd/ax/ssh.go"],
      ["internal/tunnel/router_tls.go", BLOB + "internal/tunnel/router_tls.go"],
      ["runner/runner.go", BLOB + "runner/runner.go"]
    ],
    actors: [
      at("cli", 115, 295, { sub: "ax ssh test" }),
      at("server", 370, 165, { sub: "GetTask (check debug)" }),
      at("k8s", 370, 440, { sub: "PodCertificateRequest" }),
      at("router", 630, 295, { sub: "atenet-router :443 mTLS" }),
      at("runner", 875, 295, { sub: "Guest ProcessService :80" })
    ],
    zones: [
      Z.local(["cli"], "laptop PTY"),
      Z.control(["server"], ":8080"),
      Z.external(["k8s"], "CSR API"),
      Z.substrate(["router"], "mTLS :443"),
      Z.sandbox(["runner"], "sandbox :80")
    ],
    wires: { "cli|server": "GetTask", "cli|k8s": "mint cert", "cli|router": "mTLS :443", "router|runner": "h2c :80" },
    steps: [
      { title: "Verify Running & spec.debug: true", desc: "ax ssh calls GetTask on ax-server to verify that the task is Running, has a workerIP, and was created with spec.debug: true.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "GetTask (default/test)", json: { grpc: "ax.v1alpha1.AX/GetTask", request: { atespace: "default", name: "test" } } },
        { from: "server", to: "cli", kind: "res", dt: 8, method: "AX/GetTaskResponse", info: "Running · workerIP: 10.20.3.67 · debug: true", json: { spec: { debug: true }, status: { phase: "Running", workerIp: "10.20.3.67" } },
          notes: [["Why check debug first?", "When spec.debug is false, ax-task-runner does not register Guest ProcessService on :80. Checking up front avoids opening a router tunnel for a task that will refuse SSH."]] }
      ]},
      { title: "Mint Ephemeral PodCertificateRequest", desc: "Because 10.20.3.67 is a cluster-internal worker IP, routerTLSConfig reads ClusterTrustBundle and creates an ephemeral PodCertificateRequest for ax-system/ax-server, polls until issued, and deletes the CSR.", msgs: [
        { from: "cli", to: "k8s", kind: "http", dt: 25, method: "POST PodCertificateRequest", info: "Create PodCertificateRequest (podidentity.podcert.ate.dev/identity)", json: { apiVersion: "certificates.k8s.io/v1alpha1", kind: "PodCertificateRequest", metadata: { generateName: "ax-cli-", namespace: "ax-system" }, spec: { signerName: "podidentity.podcert.ate.dev/identity", podName: "ax-server-6d8f9b7c4-x2k9p", podUID: "f41d8cd9-8f00-b204-e980-0998ecf8427e", serviceAccountName: "ax-server", serviceAccountUID: "91c8f757-4b7d-42c0-a88e-9bf3e3320d51", maxExpirationSeconds: 3600, pkixPublicKey: "<ECDSA P-256 public key>" } },
          notes: [["Why borrow ax-server's identity?", "atenet-router's --ingress-allowed-spiffe-ids allowlists spiffe://cluster.local/ns/ax-system/sa/ax-server. Minting a short-lived PodCertificateRequest lets your CLI authenticate to the router without copying static keys."]] },
        { from: "k8s", to: "cli", kind: "http", dt: 40, method: "200 OK (X.509 SVID)", info: "Issued X.509 SVID chain + delete CSR", json: { spiffeId: "spiffe://cluster.local/ns/ax-system/sa/ax-server", validFor: "1h (cached until cert.NotAfter)", cleanup: "DELETE PodCertificateRequest ax-cli-7x9qm" } }
      ]},
      { title: "Stream Guest ProcessService over mTLS", desc: "The CLI port-forwards svc/atenet-router:443, sets metadata ate-target-actor: default/test, and runs StartProcess + StreamProcessOutput (plus ResizeTty and SignalProcess for interactive PTYs).", msgs: [
        { from: "cli", to: "router", kind: "req", dt: 18, info: "mTLS gRPC StartProcess (ate-target-actor: default/test)", json: { grpc: "ateenv.v1alpha.ProcessService/StartProcess", metadata: { "ate-target-actor": "default/test" }, request: { command: "/bin/sh", args: ["-c", "ls -la /workspace"], cwd: "/workspace", tty: true, rows: 42, cols: 140 } } },
        { from: "router", to: "runner", kind: "req", dt: 4, method: "Process/StartProcess (h2c)", info: "proxy h2c → 10.20.3.67:80 ProcessService", json: { upstream: "10.20.3.67:80", service: "ateenv.v1alpha.ProcessService" } },
        { from: "runner", to: "router", kind: "res", dt: 15, method: "Process/StreamProcessOutput", info: "StreamProcessOutput (stdout chunks + exitCode: 0)", json: { processId: "proc-1", data: "total 16\ndrwxr-xr-x 4 root root 4096 Nov  5 22:15 .\ndrwxr-xr-x 8 root root 4096 Nov  5 22:15 .git\n-rw-r--r-- 1 root root   68 Nov  5 22:15 AGENTS.md\n", exitCode: 0 } },
        { from: "router", to: "cli", kind: "res", dt: 4, method: "Process/StreamProcessOutput", info: "stdout rendered in terminal · exit 0", json: { exitCode: 0 } }
      ]}
    ]
  },

  // ───────────── 6. BREAK IT: GUARDRAILS & GOTCHAS
  {
    id: "guardrails", code: "Security & Gotchas", name: "5 failure modes every AX user hits", group: "security", tag: "Break it",
    summary: "AX and Agent Substrate enforce strict invariants so untrusted agents cannot corrupt snapshots, spoof workspace markers, or expose guest shells unintentionally. Step through the 5 classic failure modes—tag-only images, resource requests, SSH with debug: false, missing WorkerPools, and plaintext secrets in spec.config—to see the exact wire error and fix for each.",
    facts: [
      ["1. Tag-only image", "Substrate rejects :latest or :v1 — images MUST be pinned by @sha256 digest"],
      ["2. Resource requests", "Task.spec.resources.requests is rejected (InvalidArgument); set limits only"],
      ["3. SSH w/o debug", "Guest ProcessService is off unless spec.debug: true"],
      ["4. No WorkerPool", "ax apply succeeds (Suspended), but ax resume fails with ResourceExhausted if no WorkerPool is ready"],
      ["5. Secrets in config", "spec.config is plain text returned by GetTask; use Model.spec.secretKey or Secret env injection"]
    ],
    links: [
      ["SECURITY.md", BLOB + "SECURITY.md"],
      ["pkg/apis/v1alpha1/types.go", BLOB + "pkg/apis/v1alpha1/types.go"],
      ["docs/installation.md", BLOB + "docs/installation.md"]
    ],
    actors: [
      at("cli", 145, 295, { sub: "ax apply / resume / ssh" }),
      at("server", 485, 295, { sub: "validation & reconciler" }),
      at("ateapi", 825, 175, { sub: "Substrate admission" }),
      at("runner", 825, 425, { sub: "sandbox :80" })
    ],
    zones: [
      Z.local(["cli"], "client"),
      Z.control(["server"], "control plane"),
      Z.substrate(["ateapi"], "Substrate"),
      Z.sandbox(["runner"], "WorkerPool")
    ],
    wires: { "cli|server": "gRPC", "server|ateapi": "CreateActorTemplate / Resume", "server|runner": ":80" },
    steps: [
      { title: "1. Tag-Only Image Rejected (@sha256 Required)", desc: "You apply a Task with image: ghcr.io/my-org/agent:v1. Agent Substrate rejects tag-only images because a mutated tag would mismatch checkpointed volume/actor snapshots.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "CreateTask (image: ghcr.io/my-org/agent:v1)", json: { grpc: "ax.v1alpha1.AX/CreateTask", spec: { image: "ghcr.io/my-org/agent:v1" } } },
        { from: "server", to: "ateapi", kind: "sub", dt: 18, info: "CreateActorTemplate (tag-only image)", json: { rpc: "ate.api.v1.Control/CreateActorTemplate", image: "ghcr.io/my-org/agent:v1" } },
        { from: "ateapi", to: "server", kind: "err", dt: 10, info: "InvalidArgument: image must be pinned by digest", json: { code: "InvalidArgument", message: "container.image \"ghcr.io/my-org/agent:v1\" must be pinned by digest (@sha256:...)" },
          notes: [["Fix", "Always pin Task.spec.image to an immutable digest: ghcr.io/my-org/agent@sha256:6772a1f2…"]] },
        { from: "server", to: "cli", kind: "err", dt: 6, method: "AX/CreateTaskResponse (Failed)", info: "Phase: Failed (Reason: TemplateCreationFailed)", json: { status: { phase: "Failed", conditions: [{ type: "Ready", status: "False", reason: "TemplateCreationFailed", message: "image must be pinned by digest" }] } } }
      ]},
      { title: "2. spec.resources.requests Rejected (Limits Only)", desc: "Unlike Kubernetes Pods, Agent Substrate sizes microVM/gVisor sandboxes strictly from limits. Setting spec.resources.requests returns InvalidArgument immediately.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 40, method: "AX/CreateTask", info: "CreateTask with resources.requests.cpu: 500m", json: { grpc: "ax.v1alpha1.AX/CreateTask", spec: { resources: { requests: { cpu: "500m" }, limits: { cpu: "2", memory: "4Gi" } } } } },
        { from: "server", to: "cli", kind: "err", dt: 3, info: "InvalidArgument: resources.requests is not supported", json: { code: "InvalidArgument", validator: "ValidateTask (pkg/apis/v1alpha1/types.go)", message: "spec.resources.requests is not supported; set spec.resources.limits only (cpu < 1000 cores, memory > 0)" },
          notes: [["Fix", "Specify only spec.resources.limits: { cpu: \"2\", memory: \"4Gi\" } (or omit to use the 1000m / 512Mi default)."]] }
      ]},
      { title: "3. ax ssh Refused When spec.debug is false", desc: "By default, spec.debug is false so production tasks do not expose arbitrary command execution or file reads on port 80.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 40, info: "ax ssh prod-task -- whoami", json: { grpc: "ax.v1alpha1.AX/GetTask", name: "prod-task" } },
        { from: "server", to: "cli", kind: "err", dt: 5, method: "Error: debug is false", info: "Error: task 'prod-task' does not have spec.debug enabled", json: { spec: { debug: false }, cliError: "task \"prod-task\" does not have debug enabled (set spec.debug: true to use ax ssh)" },
          notes: [["Security boundary", "When debug: false, ax-task-runner serves ONLY /healthz and /readyz on :80; ProcessService and FileSystemService are never registered."]] }
      ]},
      { title: "4. Resume Fails Without a WorkerPool", desc: "make deploy installs ax-server and PostgreSQL, but does not create a WorkerPool. Without one, ax apply succeeds (Suspended), and ax resume fails with ResourceExhausted.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 40, info: "ax resume task simple-task", json: { grpc: "ax.v1alpha1.AX/ResumeTask", name: "simple-task" } },
        { from: "server", to: "ateapi", kind: "sub", dt: 20, info: "ResumeActor (0 workers in pool)", json: { rpc: "ate.api.v1.Control/ResumeActor", name: "atespaces/default/actors/simple-task" } },
        { from: "ateapi", to: "server", kind: "err", dt: 15, info: "ResourceExhausted: no free workers available", json: { code: "ResourceExhausted", message: "no free workers available in any matching WorkerPool" },
          notes: [["Fix", "Apply examples/workerpool.yaml (apiVersion: ate.dev/v1, kind: WorkerPool) and wait for kubectl get workerpools -A to show READY."]] },
        { from: "server", to: "cli", kind: "err", dt: 6, method: "Error: ResourceExhausted", info: "Failed to resume (task stays Suspended)", json: { error: "rpc error: code = ResourceExhausted desc = no free workers available" } }
      ]},
      { title: "5. Plaintext Secrets in spec.config & >31 KiB YAML Cap", desc: "Task.spec.config is plain text returned by GetTask/ListTasks and capped so serialized AX_TASK_YAML fits in 31 KiB. Never put raw API keys or large blobs in spec.config.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 40, method: "AX/CreateTask", info: "CreateTask (spec.config > 16 KiB or containing API key)", json: { grpc: "ax.v1alpha1.AX/CreateTask", spec: { config: { apiKey: "AIzaSy… (DANGER: visible to all GetTask callers!)", largeBlob: "<>31 KiB serialized AX_TASK_YAML>" } } } },
        { from: "server", to: "cli", kind: "err", dt: 4, info: "InvalidArgument: serialized task YAML exceeds 31744 bytes", json: { code: "InvalidArgument", validator: "ValidateTask (maxTaskEnvBytes = 31 * 1024)", message: "serialized task YAML exceeds 31744 bytes (Linux MAX_ARG_STRLEN 128 KiB env limit)" },
          notes: [["Fix for secrets", "Reference a Kubernetes Secret via Model.spec.secretKey instead of embedding secrets in spec.config."], ["Fix for large files", "Put guidance files in Workspace.spec.files or a Git repository instead of Task.spec.config."]] }
      ]}
    ]
  },

  // ───────────── 7. COMING TO AX: ROADMAP (M0–M2)
  {
    id: "roadmap", code: "M0–M2 Roadmap", name: "Log streaming, OTel, Setup Actor split & Branching", group: "next", tag: "2026–27",
    summary: "Where AX is headed next: M0 Core Telemetry adds real-time task log streaming (AX/StreamTaskLogs & ax logs -f), W3C trace propagation (--trace), and OTel lifecycle events (ax.task.state_changed). Next-gen Actor Architecture splits maiden Git/MCP setup into a dedicated least-privilege Setup Actor, adds SPIFFE workload identity per task, auto-suspends idle sandboxes, and enables stateful task branching.",
    facts: [
      ["M0 Core Telemetry", "AX/StreamTaskLogs (ax logs <task> -f), OTel ax.task.state_changed events, --trace W3C traceparent, RESIDENCY & OUTCOME CLI columns"],
      ["Setup Actor Split", "Dedicated setup actor clones Git & materializes skills with repo creds, then hands off /workspace to a minimal-privilege task actor"],
      ["SPIFFE Task Identity", "Per-task X.509-SVIDs for zero-trust mTLS between tasks, MCP servers, and internal backends"],
      ["Idle Auto-Suspend", "Monitor CPU/I/O/network/SSH activity and automatically SuspendActor when idle"],
      ["Stateful Branching", "Fork a running or suspended task's memory + /workspace volume into N parallel speculative tasks"]
    ],
    links: [
      ["docs/roadmap.md", BLOB + "docs/roadmap.md"],
      ["SECURITY.md", BLOB + "SECURITY.md"]
    ],
    actors: [
      at("cli", 130, 295, { sub: "ax logs -f / --trace" }),
      at("server", 425, 180, { sub: "StreamTaskLogs + OTel" }),
      at("otel", 425, 425, { sub: "traces & state_changed" }),
      at("ateapi", 785, 180, { sub: "Setup Actor + BranchActor" }),
      at("runner", 785, 425, { sub: "least-privilege task actor" })
    ],
    zones: [
      Z.local(["cli"], "CLI"),
      Z.control(["server", "otel"], "observability"),
      Z.substrate(["ateapi"], "Substrate"),
      Z.sandbox(["runner"], "SPIFFE sandbox")
    ],
    wires: { "cli|server": "StreamTaskLogs (--trace)", "server|otel": "OTLP spans & events", "server|ateapi": "Setup / Branch", "server|runner": "tail logs" },
    steps: [
      { title: "M0: Live Log Streaming (ax logs -f) & --trace", desc: "You run ax logs test -f --trace. The CLI injects a W3C traceparent header, and ax-server streams live stdout/stderr from the task alongside OTel spans.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "gRPC StreamTaskLogs (follow: true, traceparent)", json: { grpc: "ax.v1alpha1.AX/StreamTaskLogs", metadata: { traceparent: "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01" }, request: { atespace: "default", name: "test", follow: true, tailLines: 100 } } },
        { from: "server", to: "runner", kind: "http", dt: 12, method: "Tail container logs", info: "stream task container stdout/stderr", json: { source: "ax.log.source = task", stream: "live chunked log stream" } },
        { from: "server", to: "cli", kind: "res", dt: 20, method: "AX/StreamTaskLogsResponse", info: "TaskLogChunk stream (stdout/stderr lines)", json: { chunks: ["[2026-11-05T22:20:01Z] PASS: TestStoreLockRenewal (0.14s)", "[2026-11-05T22:20:02Z] All 42 tests passing."] } }
      ]},
      { title: "M0: OTel State Events & RESIDENCY / OUTCOME", desc: "Every phase or residency transition emits a structured ax.task.state_changed OpenTelemetry event, and ax get tasks surfaces RESIDENCY (Active/Suspended) separately from OUTCOME (Succeeded/Failed).", msgs: [
        { from: "server", to: "otel", kind: "note", dt: 15, info: "OTLP event: ax.task.state_changed", json: { eventName: "ax.task.state_changed", attributes: { "ax.atespace": "default", "ax.task.name": "test", "ax.task.id": "task-9f8e1a2b", "ax.task.phase.from": "Suspended", "ax.task.phase.to": "Running", "ax.task.residency": "Active", "ax.task.outcome": "Pending" } },
          notes: [["Residency vs Outcome", "Because PID 1 stays alive after spec.command exits, separating RESIDENCY (sandbox running vs suspended) from OUTCOME (agent command exit 0 vs non-zero) makes task state unambiguous."]] }
      ]},
      { title: "Least-Privilege Setup Actor Split", desc: "Instead of giving the untrusted agent container Git credentials, a dedicated Setup Actor clones repos and materializes MCP/skills first, then hands the prepared /workspace volume to a network-restricted Execution Actor.", msgs: [
        { from: "server", to: "ateapi", kind: "sub", dt: 60, method: "Substrate/RunSetupActor", info: "Run SetupActor (Git creds) → hand off /workspace → ExecutionActor", json: { phase1_setupActor: { credentials: ["git-deploy-key", "skill-registry-token"], egress: "github.com, registry.internal", outputVolume: "vol-test-workspace" }, phase2_executionActor: { credentials: ["none (SPIFFE workload SVID only)"], egress: "allowlisted MCP & model gateway only", mountedVolume: "vol-test-workspace" } } }
      ]},
      { title: "Idle Auto-Suspend & Stateful Task Branching", desc: "Substrate monitors I/O and SSH activity to auto-suspend idle tasks, and BranchTask forks a checkpointed task into multiple parallel speculative execution branches.", msgs: [
        { from: "server", to: "ateapi", kind: "sub", dt: 90, method: "Substrate/BranchActor", info: "Fork snapshot test → test-branch-a, test-branch-b", json: { operation: "Stateful Task Branching", parentTask: "default/test", parentSnapshot: "snap-7f3a91c0", branches: ["default/test-branch-regex-fix", "default/test-branch-parser-refactor"], note: "Both branches start warm from the exact same /workspace filesystem and memory checkpoint!" } }
      ]}
    ]
  }
];
"""

print("Appended JS_PART_2")

JS_PART_3 = r"""
const TM = {}, TM_SINCE = {
  locking: "a496fc1"
};
const VERSIONS = [
  ["v0.3.1", "v0.3 · Redis"],
  ["a496fc1", "Oct ’26 · v0.6"],
  ["241bc4d", "main · v1.0"],
  ["roadmap", "2026–27 · Next"]
];

// Architecture Time Machine overrides
TM.create = {
  "v0.3.1": {
    summary: "In AX v0.3.1 (before direct execution + PostgreSQL), ax-server did not talk to Agent Substrate directly. Instead, CreateTask wrote the task to storage and pushed an event onto a Redis Stream (XADD ax:tasks), which a separate ax-controller deployment consumed via XREADGROUP.",
    actors: [
      at("cli", 145, 295, { sub: "ax apply -f task.yaml" }),
      at("server", 465, 185, { sub: "ax-server (API only)" }),
      at("redis", 465, 430, { sub: "Redis Streams queue" }),
      at("ateapi", 820, 295, { sub: "ax-controller → Substrate" })
    ],
    zones: [
      Z.local(["cli"], "client"),
      Z.control(["server", "redis"], "v0.3 queue"),
      Z.substrate(["ateapi"], "Substrate")
    ],
    wires: { "cli|server": "gRPC", "server|redis": "XADD", "redis|ateapi": "XREADGROUP → reconcile" },
    steps: [
      { title: "Enqueue on Redis Stream (Deprecated)", dep: "Removed when ax-controller and Redis were replaced by direct execution in ax-server under PostgreSQL leases.", desc: "ax-server validates the Task and appends a reconcile event to Redis Streams instead of calling Substrate directly.", msgs: [
        { from: "cli", to: "server", kind: "req", dt: 0, info: "CreateTask (test)", json: { grpc: "ax.v1alpha1.AX/CreateTask", name: "test" } },
        { from: "server", to: "redis", kind: "note", dt: 5, method: "XADD ax:tasks", info: "XADD ax:tasks * task default/test", json: { redis: "XADD ax:tasks * kind Task atespace default name test" } },
        { from: "server", to: "cli", kind: "res", dt: 4, method: "AX/CreateTaskResponse (Pending)", info: "202 Accepted (Pending async controller)", json: { status: { phase: "Pending" } } }
      ]},
      { title: "Async ax-controller Reconcile", dep: "Replaced by synchronous reconciler.Suspend / reconciler.Resume inside ax-server.", desc: "A separate ax-controller pod reads from the consumer group and provisions the actor asynchronously.", msgs: [
        { from: "redis", to: "ateapi", kind: "sub", dt: 250, method: "XREADGROUP → CreateActor", info: "XREADGROUP → CreateActor", json: { consumerGroup: "ax-controllers", action: "async CreateActor on Substrate" } }
      ]}
    ],
    diff: [
      "Required running both Redis and a separate ax-controller Deployment",
      "Errors from Substrate (like tag-only images) surfaced asynchronously after ax apply returned",
      "Replaced by direct-execution ax-server + PostgreSQL distributed locks"
    ]
  },
  "a496fc1": {
    diff: [
      "Direct-execution ax-server + PostgreSQL jsonb store & leases",
      "Used Substrate v0.6.0 (pkg/proto/ateapipb) and generic Reconcile(ctx, task, ws)",
      "Maiden-run marker lived at /ax/initialized-workspace (lost across volumes-only resume until #518)"
    ]
  },
  "roadmap": {
    diff: [
      "CreateTask will provision a least-privilege Setup Actor before the Execution Actor",
      "Tasks receive cryptographic SPIFFE workload identities (X.509-SVIDs)",
      "Emits ax.task.state_changed OTel events on creation"
    ]
  }
};

TM.runner = {
  "a496fc1": {
    diff: [
      "Maiden-run marker was written to /ax/initialized-workspace on the root container filesystem",
      "Because Suspend/Resume uses SNAPSHOT_FIDELITY_VOLUMES (/workspace only), resuming a suspended task lost /ax and re-ran maiden setup (#518)",
      "Fixed in 241bc4d: marker now lives on the durable volume at /workspace/.git/.ax/initialized (or /workspace/.ax/initialized)"
    ]
  }
};

TM.ssh = {
  "a496fc1": {
    diff: [
      "router_tls.go cached the PodCertificateRequest client cert indefinitely in-process without checking cert.NotAfter",
      "ax ssh hardcoded ax-system instead of honoring --namespace",
      "Fixed in 6e970c5 (#541) and b82f57e (#544)"
    ]
  }
};

const EXTRA = {
  overview: {
    next: [
      "M0 Core Telemetry: AX/StreamTaskLogs (ax logs -f) and --trace W3C trace context propagation",
      "RESIDENCY & OUTCOME columns in ax get tasks to distinguish container residency from command exit code"
    ],
    wip: [
      ["Core Telemetry (ax#13, ax#346, ax#452)", "M0 P0", REPO + "/issues/13"],
      ["Setup Actor Split & Least Privilege", "Roadmap", BLOB + "docs/roadmap.md"]
    ]
  },
  primitives: {
    next: [
      "First-class Sandbox / SandboxConfig resource for kernel/syscall constraints and security profiles",
      "Automatic injection of non-Gemini Model secret credentials into task containers"
    ]
  },
  "split-state": {
    next: [
      "RESIDENCY (Active / Suspended) and OUTCOME (Succeeded / Failed) status fields wired to exit detection (ax#346)"
    ]
  },
  runner: {
    next: [
      "Splitting maiden workspace initialization into a separate Setup Actor so the task container never holds Git repo credentials"
    ]
  },
  ssh: {
    next: [
      "Per-task SPIFFE IDs (X.509-SVIDs) and mTLS client authentication across tasks and MCP servers"
    ]
  }
};
for (const l of LESSONS) Object.assign(l, EXTRA[l.id] || {});

const WHATS_NEXT = [
  ["M0 Core Telemetry", "ax logs -f, OTel state_changed events & --trace · lesson", "#roadmap"],
  ["Claude Code Harness", "Headless claude --print runner in /workspace · lesson", "#metadata:claude"],
  ["Security & Gotchas", "5 failure modes every AX user hits · lesson", "#guardrails"],
  ["Official Repository", "github.com/google/ax (Apache-2.0)", REPO],
  ["Agent Substrate", "github.com/agent-substrate/substrate", "https://github.com/agent-substrate/substrate"]
];

const GROUP_HEAD = {
  start: "Start here",
  core: "Core architecture",
  lifecycle: "Task lifecycle",
  sandbox: "Inside the gVisor sandbox",
  networking: "Networking, tunnels & SSH",
  security: "Break it: guardrails & gotchas",
  next: "Coming to AX: roadmap"
};

const RISKS = {
  digest: {
    title: "Mutable image tag rejected",
    text: "Agent Substrate checkpoints and restores container + volume state. If a Task used a mutable tag like :latest, resuming on a different node could pull a different image layer than the snapshot expects. Always pin @sha256."
  },
  debug: {
    title: "Guest ProcessService attack surface",
    text: "Setting spec.debug: true exposes ateenv.v1alpha.ProcessService and FileSystemService on port 80 inside the sandbox. Leave debug: false (the default) for production tasks."
  },
  secrets: {
    title: "Plaintext spec.config exposure",
    text: "Task.spec.config is stored as plain jsonb in PostgreSQL, baked into AX_TASK_YAML, and returned to any caller of GetTask/ListTasks. Never put API keys in spec.config; use Model.spec.secretKey or Kubernetes Secrets."
  },
  symlink: {
    title: "Maiden marker symlink traversal (#518)",
    text: "Because /workspace holds untrusted repo contents and agent edits, SetupWorkspace calls markerLinked() (os.Lstat) on .git/.ax/initialized and refuses to read or write through symbolic links."
  },
  fencing: {
    title: "Best-effort lease renewal without fencing token",
    text: "If PostgreSQL is unreachable for longer than LockTTL (30s), a held lease can expire while a slow Substrate call is still in flight. Renewal logs the loss and token-checked DELETE prevents clobbering the next holder."
  }
};

function markRisks(msgs, L) {
  if (L.absent) return;
  for (const m of msgs) {
    const txt = JSON.stringify(m.json || {});
    if (txt.includes("@sha256") && L.id === "create") m.risk = "digest";
    else if (txt.includes("spec.config") || (m.json && m.json.task && m.json.task.spec && m.json.task.spec.config)) m.risk = "secrets";
    else if (txt.includes("markerLinked") || txt.includes(".git/.ax/initialized")) m.risk = "symlink";
    else if (L.id === "locking" && txt.includes("UPDATE locks")) m.risk = "fencing";
    else if (L.id === "ssh" && txt.includes("debug")) m.risk = "debug";
  }
}

const PLAIN = {
  "overview|Declare & Apply": "You write a short YAML file naming the container image and workspace, then run ax apply. The CLI sends a typed gRPC request to ax-server.",
  "overview|Persist & Provision (Suspended)": "ax-server saves the Task in PostgreSQL and registers an Actor on Agent Substrate, but immediately suspends it so it costs zero CPU and memory until you need it.",
  "overview|Resume & Boot Sandbox": "Running ax resume schedules a gVisor sandbox from the WorkerPool, clones your Git repo into /workspace, and waits for /readyz to report 200 OK.",
  "overview|Inspect over ax ssh": "When debug: true is set on the Task, ax ssh lets you run commands or open an interactive terminal inside the sandbox over mTLS.",
  "overview|Suspend & Checkpoint": "Running ax suspend checkpoints the /workspace filesystem to object storage and returns the gVisor worker to the pool—zero compute while idle."
};
</script>
"""

JS_PART_4 = r"""<script>(() => {
const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const NS = "http://www.w3.org/2000/svg";
const svgEl = (tag, attrs = {}) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };

const KIND = {
  req: "gRPC / CLI Request",
  res: "gRPC Response",
  sql: "PostgreSQL (pgx)",
  sub: "Agent Substrate RPC",
  http: "HTTP / mTLS",
  host: "Local / Exec",
  note: "Telemetry / Event",
  err: "Guardrail / Error"
};

const methodOf = (m) => {
  if (m.method) return m.method;
  const j = m.json || {};
  if (j.grpc) return j.grpc.replace("ax.v1alpha1.AX/", "AX/").replace("ateenv.v1alpha.ProcessService/", "Process/");
  if (j.rpc) return j.rpc.replace("ate.api.v1.Control/", "Substrate/");
  if (j.sql) return "SQL " + j.sql.trim().split(/\s+/)[0];
  if (j.command) return j.command.split(" ").slice(0, 3).join(" ");
  if (j.request) {
    const p = j.request.split(" ");
    if (p[1] && p[1].startsWith("http")) {
      try { const u = new URL(p[1]); return p[0] + " " + u.pathname + u.search; } catch {}
    }
    return p.slice(0, 2).join(" ");
  }
  if (j.status && typeof j.status === "string" && j.status.length <= 28) return j.status;
  if (j.code) return "Error: " + j.code;
  if (j.eventName) return j.eventName;
  return (m.info || "").split("·")[0].trim().slice(0, 28) || m.kind;
};

// ── 30° isometric 3D models
const C30 = 0.866, S30 = 0.5;
const P = (x, y, z) => [(x - y) * C30, (x + y) * S30 - z];
const pts = (a) => a.map((p) => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" ");
const poly = (a, cls) => `<polygon points="${pts(a)}" class="${cls}"/>`;
const mtx = (a, b, c, d, o) => `matrix(${a},${b},${c},${d},${o[0].toFixed(1)},${o[1].toFixed(1)})`;
const faceL = (b, inner) => `<g transform="${mtx(C30, S30, 0, 1, P(b.x, b.y + b.d, b.z + b.h))}">${inner}</g>`;
const faceR = (b, inner) => `<g transform="${mtx(C30, -S30, 0, 1, P(b.x + b.w, b.y + b.d, b.z + b.h))}">${inner}</g>`;
const faceT = (b, inner) => `<g transform="${mtx(C30, S30, -C30, S30, P(b.x, b.y, b.z + b.h))}">${inner}</g>`;
function box(x, y, z, w, d, h, extra = "") {
  const b = { x, y, z, w, d, h };
  const t = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)];
  const r = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)];
  const l = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)];
  b.svg = `<g class="bx ${extra}">${poly(l, "fl")}${poly(r, "fr")}${poly(t, "ft")}</g>`;
  return b;
}
const shadow = (rx) => `<ellipse cx="0" cy="${(rx * 0.08).toFixed(1)}" rx="${rx}" ry="${(rx * 0.56).toFixed(1)}" class="shd"/>`;

const MODELS = {
  server(a) {
    const w = 46, n = 3, h = 13, g = 4; let o = shadow(46);
    for (let i = 0; i < n; i++) {
      const b = box(-w / 2, -w / 2, i * (h + g), w, w, h, i === n - 1 ? "lit" : "");
      o += b.svg + faceL(b, `<circle cx="6" cy="${h / 2}" r="2" class="led"/><circle cx="12" cy="${h / 2}" r="2" class="led2"/><path d="M19 ${h / 2}h${w - 25}" class="ln"/>`) + faceR(b, `<path d="M6 4.5h${w - 12}M6 8.5h${w - 12}" class="ln"/>`);
      if (i === n - 1 && a.mono) o += faceT(b, `<text x="${w / 2}" y="${w / 2 + 5}" text-anchor="middle" class="mono3">${esc(a.mono)}</text>`);
    }
    return o;
  },
  postgres() {
    const w = 44, n = 3, h = 11, g = 3; let o = shadow(44);
    for (let i = 0; i < n; i++) {
      const b = box(-w / 2, -w / 2, i * (h + g), w, w, h, i === n - 1 ? "lit" : "");
      o += b.svg + faceL(b, `<circle cx="7" cy="${h / 2}" r="2" class="led"/><path d="M14 ${h / 2}h${w - 20}" class="ln"/>`) + faceR(b, `<rect x="8" y="3" width="${w - 16}" height="5" rx="2" class="ln2"/>`);
      if (i === n - 1) o += faceT(b, `<text x="${w / 2}" y="${w / 2 + 5}" text-anchor="middle" class="mono3">PG</text>`);
    }
    return o;
  },
  ateapi() {
    let o = shadow(52);
    const w = 54;
    for (let i = 0; i < 2; i++) {
      const b = box(-w / 2, -w / 2, i * 16, w, w, 10, i === 1 ? "lit" : "");
      o += b.svg + faceL(b, `<circle cx="7" cy="5" r="2" class="led"/><path d="M14 5h${w - 20}" class="ln"/>`) + faceR(b, `<path d="M8 5h${w - 16}" class="ln"/>`);
      if (i === 1) o += faceT(b, `<rect x="10" y="10" width="34" height="34" rx="3" class="core"/><text x="27" y="31" text-anchor="middle" class="mono3">ATE</text>`);
    }
    return o;
  },
  runner() {
    let o = shadow(54);
    const b = box(-29, -29, 0, 58, 58, 34, "lit");
    o += b.svg + faceT(b, `<rect x="5" y="5" width="48" height="48" rx="3" class="pit"/><rect x="12" y="12" width="34" height="34" rx="2" class="core"/>`) + faceL(b, `<text x="29" y="21" text-anchor="middle" class="mono3">PID 1</text>`) + faceR(b, `<path d="M8 10h22M8 16h30M8 22h16" class="code"/>`);
    return o;
  },
  tile(a) {
    const w = 46, h = 12, g = 4; let o = shadow(44);
    for (let i = 0; i < 2; i++) {
      const b = box(-w / 2, -w / 2, i * (h + g), w, w, h);
      o += b.svg + faceL(b, `<circle cx="6" cy="${h / 2}" r="2" class="led"/><path d="M13 ${h / 2}h${w - 19}" class="ln"/>`);
      if (i === 1) o += faceT(b, `<text x="${w / 2}" y="${w / 2 + 5}" text-anchor="middle" class="mono3">${esc(a.mono || "")}</text>`);
    }
    return o;
  },
  host() {
    let o = shadow(52);
    const base = box(-28, -22, 0, 56, 44, 5);
    o += base.svg + faceT(base, `<rect x="16" y="8" width="34" height="22" rx="2" class="kbd"/><rect x="26" y="33" width="14" height="7" rx="1.5" class="kbd"/>`);
    const scr = box(-28, -22, 5, 3, 44, 38);
    o += scr.svg + faceR(scr, `<rect x="3" y="3" width="38" height="31" rx="2" class="scr"/><path d="M8 11h16M8 17h24M8 23h12" class="code"/>`);
    return o;
  },
  llm() {
    let o = shadow(50);
    const pins = [];
    for (let i = -20; i <= 16; i += 9) pins.push(box(-3 + i + 3, 26, 1, 4, 6, 3, "pin"), box(26, i, 1, 6, 4, 3, "pin"));
    for (let i = -20; i <= 16; i += 9) pins.push(box(-30, i, 1, 4, 4, 3, "pin"), box(i, -30, 1, 4, 4, 3, "pin"));
    o += pins.filter((b) => b.x < -26 || b.y < -26).map((b) => b.svg).join("");
    const base = box(-26, -26, 0, 52, 52, 8);
    o += base.svg;
    o += pins.filter((b) => !(b.x < -26 || b.y < -26)).map((b) => b.svg).join("");
    const die = box(-15, -15, 8, 30, 30, 6);
    o += die.svg + faceT(die, `<path d="M15 4 Q16.5 13.5 26 15 Q16.5 16.5 15 26 Q13.5 16.5 4 15 Q13.5 13.5 15 4Z" class="spark"/>`);
    return o;
  },
  user() {
    return shadow(24) + `<path d="M-15 0 L-13 -30 A13 7.5 0 0 1 13 -30 L15 0 A15 8.6 0 0 1 -15 0Z" class="fr"/><path d="M0 8.6 A15 8.6 0 0 1 -15 0 L-13 -30 A13 7.5 0 0 0 0 -22.5Z" class="fl"/><ellipse cx="0" cy="-30" rx="13" ry="7.5" class="ft"/><circle cx="0" cy="-49" r="11" class="ft"/><path d="M-6 -55a7 7 0 0 1 9 -3" class="hl"/>`;
  },
  key() {
    let o = shadow(42);
    const b = box(-24, -24, 0, 48, 48, 38);
    o += b.svg + faceL(b, `<circle cx="24" cy="15" r="5" class="scr"/><path d="M21.5 18 L20 28 H28 L26.5 18Z" class="scr"/>`) + faceR(b, `<path d="M6 8h36M6 14h36M6 20h24" class="ln"/>`) + faceT(b, `<text x="24" y="28" text-anchor="middle" class="mono3">GCS</text>`);
    return o;
  },
  gateway() {
    let o = shadow(58);
    const w = 62;
    for (let i = 0; i < 3; i++) {
      const b = box(-w / 2, -w / 2, i * 14, w, w, 6, i === 2 ? "lit" : "");
      if (i) o += box(-w / 2 + 4, -w / 2 + 4, i * 14 - 8, 4, 4, 8, "pin").svg + box(w / 2 - 8, w / 2 - 8, i * 14 - 8, 4, 4, 8, "pin").svg;
      o += b.svg;
      if (i === 2) o += faceT(b, `<rect x="15" y="15" width="32" height="32" rx="3" class="core"/><rect x="24" y="24" width="14" height="14" rx="2" class="spark"/>`);
    }
    return o;
  }
};

const textW = (s, px, mono) => String(s).length * px * (mono ? 0.6 : 0.52);
function layoutActor(a) {
  const kind = a.icon || "server";
  const mdl = (MODELS[kind] || MODELS.server)(a);
  const K = 1.38;
  const [front, top0] = { server: [30, -70], postgres: [28, -64], ateapi: [32, -62], runner: [34, -62], tile: [30, -52], host: [33, -68], llm: [32, -34], user: [16, -61], key: [28, -64], gateway: [38, -69] }[kind] || [30, -70];
  const half = K * ({ server: 41, postgres: 40, ateapi: 46, runner: 51, tile: 42, host: 44, llm: 50, user: 25, key: 42, gateway: 55 }[kind] || 42);
  const mh = (front - top0) * K, total = mh + 46;
  const groundY = a.y - total / 2 - top0 * K;
  const labelY = groundY + front * K + 22, subY = labelY + 18;
  const lw = Math.max(half * 2, textW(a.label, 18.5), textW(a.sub, 13, true));
  return Object.assign(a, { _k: K, _m: mdl, _gy: groundY, _ly: labelY, _sy: subY, ex: a.x, ey: groundY + (front + top0) / 2 * K, hw: half + 4, hh: mh / 2 + 4,
    bx0: a.x - lw / 2, bx1: a.x + lw / 2, by0: a.y - total / 2, by1: subY + 6 });
}

// ── state
const st = { version: SPEC, lesson: LESSONS[0], idx: -1, playing: false, speed: 1, view: "network", selected: null, selectedActor: null, done: new Set(), seen: new Set(), timer: null };
const vIdx = (v) => VERSIONS.findIndex(([x]) => x === v);
const atVersion = (l, ver) => {
  if (ver === SPEC) return l;
  const since = TM_SINCE[l.id];
  if (since && vIdx(ver) < vIdx(since)) {
    const baseActors = l.actors || (l.variants && l.variants[0].actors) || [];
    const baseZones = l.zones || (l.variants && l.variants[0].zones) || [];
    return Object.assign({}, l, { absent: since, variants: undefined, actors: baseActors, zones: baseZones, steps: [{ title: "Not in this era", desc: `${l.code} arrived in ${since}. Advance the Architecture Era timeline above to inspect it.`, msgs: [] }] });
  }
  const o = (TM[l.id] || {})[ver];
  return o ? Object.assign({}, l, o, { id: l.id, tmDiff: o.diff }) : Object.assign({}, l, { tmSame: true });
};
const variantOf = {};
const resolve = (l, vid) => {
  l = atVersion(l, st.version);
  const vs = l.variants || [], v = vs.find((x) => x.id === vid) || vs[0];
  return v ? Object.assign({}, l, v, { id: l.id, vid: v.id }) : l;
};
const isNarrow = () => matchMedia("(max-width:640px)").matches;
const portrait = (L) => {
  if (!isNarrow()) return L;
  const cols = [];
  [...L.actors].sort((a, b) => a.x - b.x).forEach((a) => { const c = cols.find((c) => Math.abs(c - a.x) < 90); if (c === undefined) cols.push(a.x); });
  const row = (x) => cols.findIndex((c) => Math.abs(c - x) < 90);
  return Object.assign({}, L, { portrait: true, actors: L.actors.map((a) => Object.assign({}, a, { x: 130 + (a.y - 100) * 1.25, y: 140 + row(a.x) * 285 })) });
};
const flat = (L) => L.steps.flatMap((s, si) => s.msgs.map((m) => Object.assign({ step: si, dep: s.dep }, m)));
let MSGS = [];

const riskBtn = (k) => `<button type="button" class="risk" data-risk="${k}" aria-label="Guardrail: ${RISKS[k].title}" aria-haspopup="dialog"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.2 14.3 13.3H1.7z"/><path d="M8 6.6v3.1M8 11.6v.1"/></svg></button>`;

function renderList() {
  const cur = MSGS[st.idx];
  let html = "", last = null;
  for (const l of LESSONS) {
    if (l.group !== last) {
      last = l.group;
      html += `<div class="gh${["security", "next"].includes(l.group) ? " ns" : ""}">${esc(GROUP_HEAD[l.group])}</div>`;
    }
    const open = l.id === st.lesson.id;
    const since = TM_SINCE[l.id], gone = since && vIdx(st.version) < vIdx(since);
    const ringCls = st.done.has(l.id) ? "done" : st.seen.has(l.id) ? "part" : "";
    let steps = "";
    if (open) steps = `<ol class="steps">${st.lesson.steps.map((x, i) => {
      const state = cur && cur.step === i ? "cur" : cur && cur.step > i ? "past" : "";
      return `<li><button type="button" class="stp ${state}" data-step="${i}"><span class="num">${i + 1}</span><span><b>${esc(x.title)}${x.dep ? ` <i class="deptag">legacy</i>` : ""}</b></span></button></li>`;
    }).join("")}</ol>`;
    html += `<div class="li ${open ? "open" : ""}${gone ? " gone" : ""}"><button type="button" class="lh" data-l="${l.id}" aria-expanded="${open}"><span class="lt"><b>${esc(l.code)}${l.tag ? `<small>${esc(l.tag)}</small>` : ""}</b><em>${gone ? "Arrives in " + since : esc(l.name)}</em></span><span class="ring ${ringCls}"></span></button>${steps}</div>`;
  }
  html += `<div class="gh wn">Resources &amp; Next</div>` + WHATS_NEXT.map(([t, d, u]) => `<a class="wnl" href="${esc(u)}"${u.startsWith("#") ? "" : ' target="_blank" rel="noopener"'}><b>${esc(t)}${u.startsWith("#") ? " →" : " ↗"}</b><em>${esc(d)}</em></a>`).join("");
  $("#list").innerHTML = html;
  if (!$("#left").classList.contains("expanded")) {
    $("#bl-name").textContent = st.lesson.code;
    $("#btn-lessons").setAttribute("aria-label", "Lessons. Current: " + st.lesson.code);
  }
}

function renderOverview() {
  const L = st.lesson;
  $("#ov-title").textContent = L.code;
  $("#ov-name").innerHTML = esc(L.name);
  $("#ov-sum").textContent = L.summary;
  $("#ov-ns").hidden = L.group !== "sandbox";
  if (L.facts && L.facts.length) {
    $("#ov-facts").innerHTML = `<details class="facts-wrap"><summary><span>Key facts &amp; invariants (${L.facts.length})</span></summary><dl class="facts-dl">${L.facts.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("")}</dl></details>`;
  } else {
    $("#ov-facts").innerHTML = "";
  }
  const ext = (u, t) => `<a href="${esc(u)}" target="_blank" rel="noopener">${esc(t)}</a>`;
  let more = "";
  if (L.links) more += `<div class="srcs"><span class="lbl">google/ax</span><span class="lnk">${L.links.map(([t, u]) => ext(u, t + " ↗")).join("")}</span></div>`;
  if (st.version !== SPEC) {
    if (L.absent) more += `<div class="nextbox tmbox"><span class="nexttag">Not in ${st.version}</span><ul><li>${esc(L.code)} arrived in ${esc(L.absent)}.</li></ul></div>`;
    else if (L.tmDiff) more += `<div class="nextbox tmbox"><span class="nexttag">In era ${st.version}</span><ul>${L.tmDiff.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>`;
  }
  if (L.next && st.version === SPEC) more += `<div class="nextbox"><span class="nexttag">Planned on Roadmap</span><ul>${L.next.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>`;
  if (L.wip) more += `<div class="wipbox"><span class="wiptag">Active Tracks</span><ul>${L.wip.map(([t, s, u]) => `<li>${ext(u, t)} <em>${esc(s)}</em></li>`).join("")}</ul></div>`;
  $("#ov-more").innerHTML = more;
}

function hl(json) {
  const s = JSON.stringify(json, null, 2);
  return esc(s).replace(/(&quot;(?:[^&]|&(?!quot;))*?&quot;)(\s*:)?|\b(true|false|null)\b|(-?\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b)/gi, (m, str, colon, lit, num) => {
    if (str) return colon ? `<span class="k">${str}</span>${colon}` : `<span class="s">${str}</span>`;
    if (lit) return `<span class="l">${lit}</span>`;
    return `<span class="n">${num}</span>`;
  });
}

function renderInspector() {
  const box = $("#insp");
  const i = st.selected != null ? st.selected : st.idx;
  const m = MSGS[i];
  if (!m) {
    box.innerHTML = `<p class="empty">Press <b>Play</b> or <b>Step</b> (or click any row below) to inspect the wire payload.</p>`;
    return;
  }
  const from = actor(m.from) || { label: m.from }, to = actor(m.to) || { label: m.to };
  const method = methodOf(m);
  box.innerHTML = `<div class="ih"><span class="dot k-${m.kind}"></span><span class="im">${esc(method)}</span><span class="isz">${size(m)}</span></div>
    <div class="ir">${esc(from.label)} → ${esc(to.label)} · ${KIND[m.kind] || m.kind} · #${i + 1}</div>
    ${m.dep ? `<div class="depbox"><span class="deptag">Historical Era</span><p>${esc(m.dep)}</p></div>` : ""}<pre class="json" id="insp-json">${hl(m.json)}</pre>
    ${m.notes ? `<dl class="notes">${m.notes.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join("")}</dl>` : ""}${m.risk ? `<div class="riskline">${riskBtn(m.risk)}<p><b>Guardrail: ${esc(RISKS[m.risk].title)}.</b> ${esc(RISKS[m.risk].text)} <a href="#guardrails">See all guardrails →</a></p></div>` : ""}`;
}

const size = (m) => { const b = new TextEncoder().encode(JSON.stringify(m.json)).length; return b > 1024 ? (b / 1024).toFixed(1) + " KB" : b + " B"; };
function renderTable() {
  const rows = MSGS.map((m, i) => {
    const cls = [i === st.idx ? "cur" : "", i > st.idx ? "fut" : "", i === st.selected ? "sel" : "", m.dep ? "dep" : ""].join(" ");
    const method = methodOf(m);
    const fa = actor(m.from) || { label: m.from }, ta = actor(m.to) || { label: m.to };
    return `<tr class="${cls}" data-i="${i}" tabindex="0"><td><span class="dot k-${m.kind}">${i + 1}</span></td><td>${esc(fa.label)}</td><td>${esc(ta.label)}</td><td class="mono">${m.dep ? `<s>${esc(method)}</s> <i class="deptag">legacy</i>` : esc(method)}</td><td>${esc(m.info)}${m.risk ? " " + riskBtn(m.risk) : ""}</td></tr>`;
  }).join("");
  $("#tbody").innerHTML = rows;
  const cur = $("#tbody tr.cur");
  if (cur) {
    const wrap = $("#tablewrap"), head = wrap.querySelector("thead").offsetHeight;
    const top = Math.max(0, cur.offsetTop - head - (wrap.clientHeight - head) / 2 + cur.offsetHeight / 2);
    wrap.scrollTo({ top, behavior: "smooth" });
  }
}

const actor = (id) => st.lesson.actors.find((a) => a.id === id);
function edgePts(a, b) {
  const dx = b.ex - a.ex, dy = b.ey - a.ey;
  const clip = (n, sx, sy) => { const tx = n.hw / Math.abs(sx || 1e-6), ty = n.hh / Math.abs(sy || 1e-6); const k = Math.min(tx, ty); return [n.ex + sx * k, n.ey + sy * k]; };
  const len = Math.hypot(dx, dy) || 1, ux = dx / len, uy = dy / len;
  const off = 5;
  const ox = -uy * off, oy = ux * off;
  const p1 = clip(a, ux, uy), p2 = clip(b, -ux, -uy);
  return [p1[0] + ox, p1[1] + oy, p2[0] + ox, p2[1] + oy];
}

function renderNetwork() {
  const svg = $("#net");
  svg.innerHTML = "";
  const L = st.lesson, cur = MSGS[st.idx];
  const defs = svgEl("defs");
  defs.innerHTML = `<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" class="gdot"/></pattern><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahp"/></marker>`;
  svg.appendChild(defs);
  svg.appendChild(svgEl("rect", { x: -400, y: -100, width: 1800, height: 800, fill: "url(#dots)" }));
  L.actors.forEach(layoutActor);
  if (L.portrait) L.actors.forEach((a) => Object.assign(a, { ey: (a.by0 + a.by1) / 2, hw: (a.bx1 - a.bx0) / 2 + 8, hh: (a.by1 - a.by0) / 2 + 8 }));

  const zg = svgEl("g", { class: "zones" });
  const zBoxes = [];
  for (const z of L.zones || []) {
    const ms = z.ids.map(actor).filter(Boolean);
    if (!ms.length) continue;
    let x0 = Math.min(...ms.map((m) => m.bx0)) - 16, x1 = Math.max(...ms.map((m) => m.bx1)) + 16;
    const need = 36 + z.label.length * 8.1 + (z.sub ? z.sub.length * 6.9 + 14 : 0);
    if (x1 - x0 < need) { const c = (x0 + x1) / 2; x0 = c - need / 2; x1 = c + need / 2; }
    if (!L.portrait) {
      if (x0 < 10) { x1 += 10 - x0; x0 = 10; }
      if (x1 > 990) { x0 -= x1 - 990; x1 = 990; }
    }
    let y0 = Math.min(...ms.map((m) => m.by0)) - 34, y1 = Math.max(...ms.map((m) => m.by1)) + 10;
    if (!L.portrait) {
      y0 = Math.max(8, y0);
      y1 = Math.min(552, y1);
    }
    zBoxes.push({ x0, y0, x1, y1 });
    const g = svgEl("g", { class: "zone z-" + z.kind });
    g.innerHTML = `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" rx="16" class="zb"/>` +
      `<text x="${x0 + 16}" y="${y0 + 22}" class="zl">${esc(z.label.toUpperCase())}</text>${z.sub ? `<text x="${x0 + 24 + z.label.length * 8.1}" y="${y0 + 22}" class="zsub">${esc(z.sub)}</text>` : ""}`;
    zg.appendChild(g);
  }
  svg.appendChild(zg);

  const pairs = new Map();
  MSGS.forEach((m, i) => {
    const k = [m.from, m.to].sort().join("|");
    if (!pairs.has(k)) pairs.set(k, { a: m.from, b: m.to, used: false, host: m.kind === "host" });
    if (i <= st.idx) pairs.get(k).used = true;
    if (m.kind !== "host") pairs.get(k).host = false;
  });
  const g = svgEl("g");
  for (const [, p] of pairs) {
    const a = actor(p.a), b = actor(p.b);
    if (!a || !b) continue;
    const active = cur && [cur.from, cur.to].sort().join("|") === [p.a, p.b].sort().join("|");
    const [x1, y1, x2, y2] = L.portrait ? (() => { const q = edgePts(a, b); const r = edgePts(b, a); return [(q[0] + r[2]) / 2, (q[1] + r[3]) / 2, (q[2] + r[0]) / 2, (q[3] + r[1]) / 2]; })() : [a.ex, a.ey, b.ex, b.ey];
    g.appendChild(svgEl("line", { x1, y1, x2, y2, class: "edge" + (active ? " on" : p.used ? " used" : "") + (p.host ? " hostedge" : "") }));
  }
  svg.appendChild(g);

  const wires = L.wires || {};
  for (const k in wires) {
    const [i, j] = k.split("|"), a = actor(i), b = actor(j);
    if (!a || !b) continue;
    const w = textW(wires[k], 12.5, true) + 18;
    let mx = (a.ex + b.ex) / 2, my = (a.ey + b.ey) / 2;
    for (const frac of [0.5, 0.36, 0.64, 0.28, 0.72, 0.22, 0.78]) {
      const cx = a.ex + (b.ex - a.ex) * frac, cy = a.ey + (b.ey - a.ey) * frac;
      const wx0 = cx - w / 2, wx1 = cx + w / 2, wy0 = cy - 11, wy1 = cy + 11;
      const hitZoneHeader = zBoxes.some((z) => Math.min(wx1, z.x1) - Math.max(wx0, z.x0) > 4 && Math.min(wy1, z.y0 + 30) - Math.max(wy0, z.y0) > 2);
      const hitActorLabel = L.actors.some((act) => Math.min(wx1, act.bx1) - Math.max(wx0, act.bx0) > 4 && Math.min(wy1, act.by1) - Math.max(wy0, act._ly - 16) > 2);
      if (!hitZoneHeader && !hitActorLabel) { mx = cx; my = cy; break; }
    }
    const t = svgEl("g", { class: "wire", transform: `translate(${mx},${my})` });
    t.innerHTML = `<rect x="${-w / 2}" y="-11" width="${w}" height="22" rx="11"/><text y="4" text-anchor="middle">${esc(wires[k])}</text>`;
    svg.appendChild(t);
  }

  for (const a of L.actors) {
    const on = cur && (cur.from === a.id || cur.to === a.id);
    const n = svgEl("g", { class: "node iso" + (on ? " on" : ""), "data-actor": a.id });
    n.innerHTML = `<g class="mdl" transform="translate(${a.x},${a._gy}) scale(${a._k})">${a._m}</g><text x="${a.x}" y="${a._ly}" text-anchor="middle" class="nl halo">${esc(a.label)}</text><text x="${a.x}" y="${a._sy}" text-anchor="middle" class="ns halo">${esc(a.sub)}</text>`;
    svg.appendChild(n);
  }

  if (L.portrait) {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    svg.querySelectorAll(".zones, .node").forEach((el) => { const b = el.getBBox(); if (!b.width) return; x0 = Math.min(x0, b.x); y0 = Math.min(y0, b.y); x1 = Math.max(x1, b.x + b.width); y1 = Math.max(y1, b.y + b.height); });
    const minW = 640; if (x1 - x0 < minW) { const c = (x0 + x1) / 2; x0 = c - minW / 2; x1 = c + minW / 2; }
    if (x1 > x0) { const pad = 18; svg.setAttribute("viewBox", `${x0 - pad} ${y0 - pad} ${x1 - x0 + 2 * pad} ${y1 - y0 + 2 * pad}`); svg.style.aspectRatio = `${x1 - x0 + 2 * pad} / ${y1 - y0 + 2 * pad}`; }
  } else if (svg.getAttribute("viewBox") !== "0 0 1000 560") { svg.setAttribute("viewBox", "0 0 1000 560"); svg.style.aspectRatio = ""; }

  const cap = $("#caption");
  fitCaption(L, cap);
  cap.innerHTML = capHTML(L, cur ? cur.step : 0);
  cap.hidden = false;
}

function capHTML(L, i) {
  const s = L.steps[i] || L.steps[0];
  const rk = (MSGS.find((m) => m.step === i && m.risk) || {}).risk;
  const pw = PLAIN[L.id + "|" + s.title];
  return `<div class="ov">Step ${i + 1} of ${L.steps.length}${rk ? " " + riskBtn(rk) : ""}${s.dep ? ` <span class="deptag">Historical Era</span>` : ""}</div><div class="ct">${esc(s.title)}</div><p class="plain">${esc(pw || s.desc)}</p>${L.absent ? `<button type="button" class="jump-era" data-ver="${esc(L.absent)}">Switch to ${esc(L.absent)} →</button>` : ""}${s.dep ? `<p class="depnote">${esc(s.dep)}</p>` : ""}`;
}

let capKey = "";
function fitCaption(L, cap) {
  const w = cap.clientWidth;
  const key = L.id + ":" + (L.vid || "") + ":" + st.version + ":" + w;
  if (!w || key === capKey) return;
  capKey = key;
  const keep = cap.innerHTML;
  cap.style.minHeight = "0";
  let h = 0;
  for (let i = 0; i < L.steps.length; i++) { cap.innerHTML = capHTML(L, i); h = Math.max(h, cap.offsetHeight); }
  cap.innerHTML = keep;
  cap.style.minHeight = Math.max(70, Math.ceil(h)) + "px";
}
const refitCaption = () => { capKey = ""; const c = $("#caption"); if (c && st.lesson) fitCaption(st.lesson, c); };
window.addEventListener("resize", refitCaption);
matchMedia("(max-width:640px)").addEventListener("change", () => { const i = st.idx; setLesson(st.lesson.id, st.lesson.vid); if (i >= 0) go(i, false); });
if (document.fonts) { document.fonts.ready.then(refitCaption); document.fonts.addEventListener("loadingdone", refitCaption); }

let anim = null;
function animatePacket(m) {
  const svg = $("#net");
  if (anim) { cancelAnimationFrame(anim.raf); anim.g.remove(); anim.trail.remove(); anim = null; }
  const a = actor(m.from), b = actor(m.to);
  if (!a || !b) return;
  const [x1, y1, x2, y2] = edgePts(a, b);
  const label = methodOf(m);
  const g = svgEl("g", { class: "pkt k-" + m.kind + (m.dep ? " dep" : "") });
  const w = Math.max(64, label.length * 7.8 + 32);
  g.innerHTML = `<rect x="${-w / 2}" y="-14" width="${w}" height="28" rx="14" class="pb"/><circle cx="${-w / 2 + 14}" cy="0" r="4.5" class="pd"/><text x="${-w / 2 + 25}" y="4.5" class="pt">${esc(label)}</text>${m.dep ? `<text x="0" y="-21" text-anchor="middle" class="pdep">LEGACY</text>` : ""}`;
  svg.appendChild(g);
  const trail = svgEl("line", { x1, y1, x2: x1, y2: y1, class: "trail k-" + m.kind, "marker-end": "url(#ah)" });
  svg.insertBefore(trail, g);
  const dur = 850 / st.speed, t0 = performance.now();
  const ease = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const tick = (now) => {
    const t = reduce ? 1 : Math.min(1, (now - t0) / dur), e = ease(t);
    const x = x1 + (x2 - x1) * e, y = y1 + (y2 - y1) * e;
    g.setAttribute("transform", `translate(${x},${y})`);
    trail.setAttribute("x2", x); trail.setAttribute("y2", y);
    if (t < 1) anim.raf = requestAnimationFrame(tick);
    else g.classList.add("arrived");
  };
  anim = { g, trail, raf: requestAnimationFrame(tick) };
}

function renderSequence() {
  const svg = $("#seq");
  const L = st.lesson, n = L.actors.length;
  const colW = 1000 / n, top = 92, rowH = 38;
  const zoneOf = (id) => (L.zones || []).find((z) => z.ids.includes(id));
  const H = Math.max(520, top + MSGS.length * rowH + 34);
  svg.setAttribute("viewBox", `0 0 1000 ${H}`);
  svg.style.height = H + "px";
  let h = `<defs><marker id="sah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="ahp"/></marker></defs>`;
  const cx = {};
  L.actors.forEach((a, i) => {
    const x = colW * i + colW / 2; cx[a.id] = x;
    const z = zoneOf(a.id);
    h += `<line x1="${x}" y1="${top - 14}" x2="${x}" y2="${H - 10}" class="life"/><g transform="translate(${x - 72},14)"><rect width="144" height="38" rx="6" class="nb"/><text x="72" y="24" text-anchor="middle" class="nl">${esc(a.label)}</text>${z ? `<text x="72" y="56" text-anchor="middle" class="zl sz-${z.kind}">${esc(z.label.toUpperCase())}</text>` : ""}</g>`;
  });
  let lastStep = -1;
  MSGS.forEach((m, i) => {
    const y = top + 14 + i * rowH, x1 = cx[m.from], x2 = cx[m.to];
    if (x1 == null || x2 == null) return;
    if (m.step !== lastStep) { h += `<text x="8" y="${y + 4}" class="sstep">${m.step + 1}</text>`; lastStep = m.step; }
    const vis = i <= st.idx, cur = i === st.idx;
    const label = m.info || methodOf(m);
    const dir = x2 > x1 ? 1 : -1;
    h += `<g class="sm k-${m.kind} ${vis ? "" : "fut"} ${cur ? "cur" : ""} ${m.dep ? "dep" : ""}" data-i="${i}"><line x1="${x1 + dir * 4}" y1="${y}" x2="${x2 - dir * 4}" y2="${y}" marker-end="url(#sah)"/><text x="${(x1 + x2) / 2}" y="${y - 7}" text-anchor="middle">${m.dep ? `<tspan class="sdep">LEGACY </tspan>` : ""}${esc(label.length > 46 ? label.slice(0, 45) + "…" : label)}</text></g>`;
  });
  svg.innerHTML = h;
  const curEl = svg.querySelector(".sm.cur");
  if (curEl) { const wrap = $("#seqwrap"); const y = top + st.idx * rowH; if (y > wrap.scrollTop + wrap.clientHeight - 60 || y < wrap.scrollTop) wrap.scrollTo({ top: Math.max(0, y - 120), behavior: "smooth" }); }
}

function renderTimeline() {
  $("#bv-name").textContent = "Era " + st.version;
  $("#tm-cur").innerHTML = `${st.version}${st.version === SPEC ? " · main" : ""}`;
  $("#tm-line").innerHTML = VERSIONS.map(([v, short]) => `<button type="button" data-ver="${v}" aria-pressed="${v === st.version}" title="AX ${v}"><i></i><span>${esc(short)}</span></button>`).join("");
}

function renderVariants() {
  const box = $("#variants"), vs = st.lesson.variants || [];
  box.hidden = !vs.length;
  box.innerHTML = vs.map((v) => `<button type="button" data-variant="${v.id}" aria-pressed="${v.id === st.lesson.vid}" title="${esc(v.hint || v.label)}">${esc(v.label)}</button>`).join("");
}

function renderAll(animate) {
  $(".stage").classList.toggle("absent", !!st.lesson.absent);
  document.body.classList.toggle("focus", st.playing && !document.body.classList.contains("intro") && !isNarrow());
  renderTimeline(); renderVariants(); renderList(); renderOverview(); renderInspector(); renderTable();
  $("#viewnet").hidden = st.view !== "network"; $("#seqwrap").hidden = st.view !== "sequence";
  document.querySelectorAll("[data-view]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.view === st.view));
  if (st.view === "network") { renderNetwork(); if (animate && MSGS[st.idx]) animatePacket(MSGS[st.idx]); }
  else renderSequence();
  const atEnd = st.idx >= MSGS.length - 1, li = LESSONS.findIndex((l) => l.id === st.lesson.id), nxt = LESSONS[(li + 1) % LESSONS.length];
  $("#btn-prev").disabled = st.idx <= 0;
  $("#btn-step").disabled = atEnd;
  $("#btn-speed").textContent = st.speed + "x";
  $("#flowcount").textContent = `${MSGS.length} messages · ${st.lesson.steps.length} steps`;
  $("#mb-play").innerHTML = st.playing ? `<svg viewBox="0 0 24 24"><path d="M7 5h3v14H7zM14 5h3v14h-3z"/></svg>` : `<svg viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z"/></svg>`;
  $("#mb-play").setAttribute("aria-label", st.playing ? "Pause" : atEnd ? "Replay" : "Play");
  $("#mb-prev").disabled = st.idx <= 0; $("#mb-next").disabled = atEnd;
  $("#mb-count").textContent = `${Math.max(0, st.idx + 1)}/${MSGS.length}`;
  $("#mb-lname").textContent = nxt.code;
  $("#mb-lesson").setAttribute("aria-label", "Next lesson: " + nxt.code);
  $("#btn-play").innerHTML = st.playing ? `<svg viewBox="0 0 24 24"><path d="M7 5h3v14H7zM14 5h3v14h-3z"/></svg>Pause` : `<svg viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z"/></svg>${st.idx >= MSGS.length - 1 && st.idx >= 0 ? "Replay" : "Play"}`;
}

let riskPinned = null;
function showRisk(btn, pin) {
  const k = btn.dataset.risk, pop = $("#riskpop");
  if (!RISKS[k]) return;
  if (pin && riskPinned === btn) { hideRisk(); return; }
  pop.innerHTML = `<b>${esc(RISKS[k].title)}</b><p>${esc(RISKS[k].text)}</p><a href="#guardrails">See all 5 guardrails →</a>`;
  pop.hidden = false;
  const r = btn.getBoundingClientRect(), w = Math.min(310, innerWidth - 24);
  pop.style.width = w + "px";
  const left = Math.max(12, Math.min(innerWidth - w - 12, r.left + r.width / 2 - w / 2));
  const below = r.bottom + 8 + pop.offsetHeight < innerHeight - 80;
  pop.style.left = left + "px"; pop.style.top = (below ? r.bottom + 8 : r.top - pop.offsetHeight - 8) + "px";
  riskPinned = pin ? btn : null;
}
function hideRisk() { $("#riskpop").hidden = true; riskPinned = null; }
document.addEventListener("pointerover", (e) => { const b = e.target.closest && e.target.closest(".risk"); if (b && e.pointerType === "mouse" && !riskPinned) showRisk(b, false); });
document.addEventListener("pointerout", (e) => { const b = e.target.closest && e.target.closest(".risk"); if (b && e.pointerType === "mouse" && !riskPinned && !(e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest("#riskpop"))) hideRisk(); });
document.addEventListener("pointerdown", (e) => { if (!e.target.closest("#riskpop, .risk")) hideRisk(); });
window.addEventListener("scroll", () => { if (!$("#riskpop").hidden) hideRisk(); }, true);

function go(i, animate = true) {
  st.idx = Math.max(-1, Math.min(MSGS.length - 1, i));
  st.selected = null;
  if (st.idx >= 0) st.seen.add(st.lesson.id);
  if (st.idx === MSGS.length - 1 && MSGS.length > 0) st.done.add(st.lesson.id);
  renderAll(animate);
}
function stop() { st.playing = false; clearTimeout(st.timer); }
function loop() {
  if (!st.playing) return;
  if (st.idx >= MSGS.length - 1) {
    stop(); renderAll(false);
    if (document.body.classList.contains("intro")) {
      st.timer = setTimeout(() => { if (document.body.classList.contains("intro")) { st.idx = -1; st.playing = true; loop(); } }, 2400);
    }
    return;
  }
  go(st.idx + 1);
  const m = MSGS[st.idx], next = MSGS[st.idx + 1];
  const pause = next && next.step !== m.step ? 2100 : 1250;
  st.timer = setTimeout(loop, pause / st.speed);
}
function play() {
  if (st.playing) { stop(); renderAll(false); return; }
  if (st.idx >= MSGS.length - 1) st.idx = -1;
  st.playing = true; loop();
}
function setLesson(id, vid) {
  stop();
  const base = LESSONS.find((l) => l.id === id) || LESSONS[0];
  if (vid) variantOf[base.id] = vid;
  st.lesson = portrait(resolve(base, variantOf[base.id]));
  MSGS = flat(st.lesson); markRisks(MSGS, st.lesson); st.idx = -1; st.selected = null;
  if (anim) { cancelAnimationFrame(anim.raf); anim = null; }
  renderAll(false);
  const open = document.querySelector(".li.open");
  if (open) {
    const list = $("#list"), top = open.offsetTop - list.offsetTop - 8;
    if (top < list.scrollTop || top > list.scrollTop + list.clientHeight - 200) list.scrollTo({ top, behavior: "smooth" });
  }
  $("#seqwrap").scrollTop = 0;
  go(0, false);
}

document.addEventListener("click", (e) => {
  const t = e.target.closest("button, tr[data-i], .sm, .node[data-actor]");
  if (!t) return;
  if (t.dataset.risk) { e.stopPropagation(); showRisk(t, true); return; }
  if (t.dataset.actor) {
    const aid = t.dataset.actor;
    const hit = MSGS.findIndex((m, idx) => idx >= st.idx && (m.from === aid || m.to === aid));
    const targetIdx = hit >= 0 ? hit : MSGS.findIndex((m) => m.from === aid || m.to === aid);
    if (targetIdx >= 0) { stop(); go(targetIdx); }
    return;
  }
  if (t.dataset.l) {
    document.body.classList.remove("intro");
    const L = $("#left");
    if (L.classList.contains("expanded")) { L.classList.remove("expanded"); $("#btn-lessons").setAttribute("aria-expanded", "false"); }
    setLesson(t.dataset.l);
    writeHash();
    if (isNarrow()) $("#center").scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (t.dataset.ver) {
    $("#left").classList.remove("ver-open");
    $("#btn-ver").setAttribute("aria-expanded", "false");
    st.version = t.dataset.ver;
    const vid = st.lesson.vid;
    setLesson(st.lesson.id, vid);
    writeHash();
    return;
  }
  if (t.dataset.variant) { setLesson(st.lesson.id, t.dataset.variant); writeHash(); return; }
  if (t.dataset.step != null) { stop(); const i = MSGS.findIndex((m) => m.step === +t.dataset.step); if (i >= 0) go(i); return; }
  if (t.dataset.view) { st.view = t.dataset.view; renderAll(false); return; }
  if (t.dataset.i != null) {
    stop();
    const i = +t.dataset.i;
    if (i <= st.idx) { st.selected = i; renderAll(false); renderInspector(); } else go(i);
    return;
  }
  switch (t.id) {
    case "btn-play": case "mb-play": play(); break;
    case "intro-start": exitIntro("primitives"); break;
    case "btn-intro": enterIntro(); break;
    case "mb-prev": case "btn-prev": stop(); go(st.idx - 1, false); break;
    case "mb-next": case "btn-step": stop(); go(st.idx + 1); break;
    case "mb-log": { const on = document.body.classList.toggle("log-open"); t.setAttribute("aria-expanded", on); if (on) renderTable(); break; }
    case "mb-lesson": { const li = LESSONS.findIndex((l) => l.id === st.lesson.id); const nxt = LESSONS[(li + 1) % LESSONS.length]; setLesson(nxt.id); writeHash(); window.scrollTo({ top: $("#center").offsetTop - 8, behavior: "smooth" }); break; }
    case "btn-lessons": { const on = $("#left").classList.toggle("expanded"); $("#left").classList.remove("ver-open"); $("#btn-ver").setAttribute("aria-expanded", "false"); t.setAttribute("aria-expanded", on); $("#bl-name").textContent = on ? "Close" : st.lesson.code; break; }
    case "btn-ver": { const on = $("#left").classList.toggle("ver-open"); t.setAttribute("aria-expanded", on); if ($("#left").classList.contains("expanded")) { $("#left").classList.remove("expanded"); $("#btn-lessons").setAttribute("aria-expanded", "false"); $("#bl-name").textContent = st.lesson.code; } break; }
    case "btn-reset": stop(); go(0, false); break;
    case "btn-speed": st.speed = st.speed === 1 ? 2 : st.speed === 2 ? 0.5 : 1; renderAll(false); break;
    case "btn-copy": {
      const i = st.selected != null ? st.selected : st.idx;
      const m = MSGS[i];
      if (m && navigator.clipboard) {
        navigator.clipboard.writeText(JSON.stringify(m.json, null, 2));
        t.textContent = "Copied!";
        setTimeout(() => { t.textContent = "Copy JSON"; }, 1200);
      }
      break;
    }
    case "btn-light": document.documentElement.dataset.theme = "light"; syncTheme(); break;
    case "btn-dark": document.documentElement.dataset.theme = "dark"; syncTheme(); break;
  }
});

document.addEventListener("keydown", (e) => {
  if (e.target.closest("input, textarea")) return;
  if (e.key === "Escape" && !$("#riskpop").hidden) { hideRisk(); return; }
  if (e.key === "Escape" && document.body.classList.contains("log-open")) { document.body.classList.remove("log-open"); $("#mb-log").setAttribute("aria-expanded", "false"); return; }
  if (e.key === " ") { e.preventDefault(); play(); }
  else if (e.key === "ArrowRight") { stop(); go(st.idx + 1); }
  else if (e.key === "ArrowLeft") { stop(); go(st.idx - 1, false); }
  else if (e.key === "Enter" && e.target.matches("tr[data-i]")) e.target.click();
});

function syncTheme() {
  const d = document.documentElement.dataset.theme === "dark";
  $("#btn-light").setAttribute("aria-pressed", !d);
  $("#btn-dark").setAttribute("aria-pressed", d);
}

// ── boot
syncTheme();
function parseHash() {
  const [a, ver] = location.hash.replace("#", "").split("@");
  const [id, v] = a.split(":");
  return { id, v, ver: VERSIONS.some(([x]) => x === ver) ? ver : SPEC };
}
function writeHash() {
  history.replaceState(null, "", "#" + st.lesson.id + (st.lesson.vid && st.lesson.variants && st.lesson.vid !== st.lesson.variants[0].id ? ":" + st.lesson.vid : "") + (st.version !== SPEC ? "@" + st.version : ""));
}
window.addEventListener("hashchange", () => {
  hideRisk();
  const h = parseHash();
  if (!LESSONS.some((l) => l.id === h.id)) return;
  document.body.classList.remove("intro");
  if (location.hash.includes("@")) st.version = h.ver;
  setLesson(h.id, h.v);
  writeHash();
});
const headerPicker = matchMedia("(min-width:981px)");
function placeTimeline() {
  const tm = $("#tm");
  if (!headerPicker.matches) { if (tm.parentElement.id !== "left") $(".ph").after(tm); }
  else if (tm.parentElement.id !== "hver") $("#hver").appendChild(tm);
}
placeTimeline();
headerPicker.addEventListener("change", placeTimeline);

function enterIntro() {
  document.body.classList.add("intro");
  setLesson("overview");
  history.replaceState(null, "", location.pathname + location.search);
  st.idx = -1;
  st.playing = true;
  setTimeout(loop, 650);
}
function exitIntro(id) {
  document.body.classList.remove("intro");
  setLesson(id || "primitives");
  writeHash();
}
const H0 = parseHash();
st.version = H0.ver;
if (LESSONS.some((l) => l.id === H0.id) && H0.id !== "overview") setLesson(H0.id, H0.v);
else enterIntro();
})();
</script>
</body>
</html>
"""

out_html = HTML_HEAD + JS_PART_1 + JS_PART_2 + JS_PART_3 + JS_PART_4
out_path = REPO_ROOT / "index.html"
out_path.write_text(out_html, encoding="utf-8")

favicon_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 112 72">{axel_inner}</svg>\n'
(REPO_ROOT / "favicon.svg").write_text(favicon_svg, encoding="utf-8")

print("Wrote", out_path, "size:", len(out_html.encode("utf-8")), "bytes")
