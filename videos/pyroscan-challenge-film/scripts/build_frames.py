"""Build the ten deterministic HyperFrames sub-compositions for PyroScan."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "compositions" / "frames"


def frame(frame_id: str, duration: int, body: str, css: str, js: str) -> str:
    # HTML class names and querySelector selectors cannot start with the numeric
    # scene ids used by the timeline. Keep the composition id stable, but prefix
    # every scene-local DOM token with ``f`` at generation time.
    prefix = f"f{frame_id}"
    body = body.replace(frame_id, prefix)
    css = css.replace(frame_id, prefix)
    js = js.replace(frame_id, prefix)
    return f"""<template>
  <style>
    @font-face {{ font-family: 'Inter'; src: url('assets/fonts/Inter-Regular.ttf') format('truetype'); font-weight: 400; }}
    @font-face {{ font-family: 'Inter'; src: url('assets/fonts/Inter-Medium.ttf') format('truetype'); font-weight: 500; }}
    @font-face {{ font-family: 'Inter'; src: url('assets/fonts/Inter-SemiBold.ttf') format('truetype'); font-weight: 600; }}
    @font-face {{ font-family: 'Inter'; src: url('assets/fonts/Inter-Bold.ttf') format('truetype'); font-weight: 700; }}
    #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; font-family: 'Inter', sans-serif; color: #eff3ef; }}
    .{prefix}-bg {{ position: absolute; inset: 0; background: radial-gradient(circle at 72% 18%, rgba(109,230,173,.09), transparent 34%), #111412; }}
    .{prefix}-bg::before {{ content: ''; position: absolute; inset: 0; background-image: linear-gradient(rgba(198,215,202,.045) 1px, transparent 1px), linear-gradient(90deg, rgba(198,215,202,.045) 1px, transparent 1px); background-size: 72px 72px; }}
    .{prefix}-content {{ position: absolute; inset: 0; overflow: hidden; }}
    .{prefix}-eyebrow {{ font-size: 15px; letter-spacing: .18em; color: #d7f85d; font-weight: 600; text-transform: uppercase; }}
    .{prefix}-mono {{ font-size: 13px; letter-spacing: .14em; color: #8e9991; font-weight: 500; text-transform: uppercase; }}
    .{prefix}-chrome {{ position: absolute; left: 74px; right: 74px; top: 54px; display: flex; align-items: center; justify-content: space-between; padding-bottom: 18px; border-bottom: 1px solid rgba(198,215,202,.18); }}
    .{prefix}-screen {{ border: 1px solid rgba(215,248,93,.28); border-radius: 18px; background: #0b0e0c; box-shadow: 0 34px 80px rgba(0,0,0,.48); overflow: hidden; }}
    .{prefix}-screen img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    {css}
  </style>
  <div id="root" data-composition-id="{frame_id}" data-width="1920" data-height="1080" data-duration="{duration}">
    <div id="{prefix}-background" class="clip {prefix}-bg" data-start="0" data-duration="{duration}" data-track-index="0"></div>
    <div id="{prefix}-content-layer" class="clip {prefix}-content" data-start="0" data-duration="{duration}" data-track-index="1">
      {body}
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    (() => {{
      const tl = gsap.timeline({{paused: true}});
      {js}
      window.__timelines["{frame_id}"] = tl;
    }})();
  </script>
</template>"""


FRAMES: dict[str, str] = {}


FRAMES["01-before-the-fire"] = frame(
    "01-before-the-fire",
    10,
    """
      <div class="01-before-the-fire-chrome"><span class="01-before-the-fire-eyebrow">PYROSCAN · READINESS MODE</span><span class="01-before-the-fire-mono">01 / BEFORE</span></div>
      <div class="01-before-the-fire-word 01-before-the-fire-before">before</div>
      <div class="01-before-the-fire-word 01-before-the-fire-fire">the fire</div>
      <svg class="01-before-the-fire-contour" viewBox="0 0 900 430" aria-hidden="true"><path id="01-before-the-fire-path" d="M72 304 C196 88 520 52 773 206 C884 274 831 380 653 357 C490 336 443 230 274 250 C177 262 131 329 72 304 Z"/></svg>
      <div class="01-before-the-fire-final"><span>rehearse</span><span>first.</span></div>
      <img class="01-before-the-fire-mark" src="assets/pyroscan-mark.svg" alt="PyroScan mark" />
      <div class="01-before-the-fire-proof"><i></i> decisions before consequences</div>
    """,
    """
      .01-before-the-fire-word { position:absolute; left:110px; top:270px; font-size:210px; line-height:.9; letter-spacing:-.065em; font-weight:700; }
      .01-before-the-fire-fire { color:#ffb75c; }
      .01-before-the-fire-contour { position:absolute; width:900px; height:430px; left:820px; top:220px; fill:rgba(255,112,72,.035); }
      .01-before-the-fire-contour path { fill:none; stroke:#ff7048; stroke-width:3; }
      .01-before-the-fire-final { position:absolute; left:110px; top:235px; display:grid; font-size:205px; line-height:.84; letter-spacing:-.065em; font-weight:700; color:#d7f85d; }
      .01-before-the-fire-mark { position:absolute; left:116px; top:710px; width:70px; height:70px; }
      .01-before-the-fire-proof { position:absolute; left:215px; top:732px; font-size:20px; color:#8e9991; letter-spacing:.02em; }
      .01-before-the-fire-proof i { display:inline-block; width:34px; height:2px; margin:0 12px 6px 0; background:#d7f85d; }
    """,
    """
      const before = document.querySelector('.01-before-the-fire-before');
      const fire = document.querySelector('.01-before-the-fire-fire');
      const finalWords = document.querySelectorAll('.01-before-the-fire-final span');
      const path = document.getElementById('01-before-the-fire-path');
      const length = path.getTotalLength();
      gsap.set([fire, '.01-before-the-fire-final', '.01-before-the-fire-mark', '.01-before-the-fire-proof'], {opacity:0});
      gsap.set(path, {strokeDasharray:length, strokeDashoffset:length});
      tl.fromTo(before,{x:-90,opacity:0},{x:0,opacity:1,duration:1.1,ease:'power3.out'},0.08);
      tl.set(before,{autoAlpha:0},2.5);
      tl.fromTo(fire,{x:80,opacity:0},{x:0,opacity:1,duration:.9,ease:'power3.out'},2.5);
      tl.to(path,{strokeDashoffset:0,duration:2.6,ease:'power2.inOut'},2.7);
      tl.set(fire,{autoAlpha:0},5.5);
      tl.set('.01-before-the-fire-final',{autoAlpha:1},5.5);
      tl.fromTo(finalWords,{y:78,opacity:0},{y:0,opacity:1,duration:1.0,stagger:.65,ease:'power3.out'},5.5);
      tl.fromTo('.01-before-the-fire-mark',{scale:.55,opacity:0},{scale:1,opacity:1,duration:.8,ease:'power3.out'},6.6);
      tl.fromTo('.01-before-the-fire-proof',{x:-24,opacity:0},{x:0,opacity:1,duration:.7,ease:'power3.out'},7.25);
    """,
)


FRAMES["02-disconnected-context"] = frame(
    "02-disconnected-context",
    14,
    """
      <div class="02-disconnected-context-chrome"><span class="02-disconnected-context-eyebrow">THE OLD HANDOFF</span><span class="02-disconnected-context-mono">CONTEXT LOSS</span></div>
      <div class="02-disconnected-context-world">
        <section class="02-disconnected-context-station 02-disconnected-context-human"><span>01</span><b>LOCAL<br/>KNOWLEDGE</b><div class="02-disconnected-context-note">LP-3 access constraint<br/><small>known by the team</small></div></section>
        <section class="02-disconnected-context-station 02-disconnected-context-map"><span>02</span><b>MAP<br/>EVIDENCE</b><svg viewBox="0 0 260 300"><path d="M130 12 C175 25 208 72 198 114 C228 150 206 203 180 235 C161 259 143 287 126 292 C110 278 98 249 79 225 C51 191 38 148 59 111 C51 71 86 27 130 12Z"/><path d="M76 171 C108 136 151 129 198 166"/><path d="M72 201 C112 168 160 165 204 196"/></svg></section>
        <section class="02-disconnected-context-station 02-disconnected-context-ai"><span>03</span><b>AI<br/>CHAT</b><div class="02-disconnected-context-prompt"><i>›</i><em id="02-disconnected-context-typed"></em><u></u></div></section>
        <svg class="02-disconnected-context-links" viewBox="0 0 2380 380"><path id="02-disconnected-context-link-a" d="M380 190 C610 190 650 190 845 190"/><path id="02-disconnected-context-link-b" d="M1385 190 C1570 190 1645 190 1905 190"/></svg>
      </div>
      <div class="02-disconnected-context-loss">every handoff <strong>loses context.</strong></div>
    """,
    """
      .02-disconnected-context-world { position:absolute; left:120px; top:190px; width:2380px; height:540px; }
      .02-disconnected-context-station { position:absolute; top:0; width:430px; height:500px; padding:42px; border:1px solid rgba(198,215,202,.18); background:rgba(10,13,11,.92); }
      .02-disconnected-context-station>span { color:#d7f85d; font-size:13px; letter-spacing:.16em; }
      .02-disconnected-context-station>b { display:block; margin-top:34px; font-size:68px; line-height:.92; letter-spacing:-.045em; }
      .02-disconnected-context-human { left:0; } .02-disconnected-context-map { left:920px; } .02-disconnected-context-ai { left:1840px; }
      .02-disconnected-context-note { margin-top:76px; padding:22px; border-left:3px solid #71b7ef; color:#eff3ef; font-size:22px; line-height:1.4; background:rgba(113,183,239,.08); }
      .02-disconnected-context-note small { color:#8e9991; }
      .02-disconnected-context-map svg { position:absolute; width:220px; right:38px; bottom:28px; fill:rgba(109,230,173,.035); stroke:#6de6ad; stroke-width:2; }
      .02-disconnected-context-prompt { position:absolute; left:40px; right:40px; bottom:46px; min-height:96px; padding:26px; border:1px solid rgba(215,248,93,.24); color:#d7f85d; font-size:20px; }
      .02-disconnected-context-prompt i { margin-right:10px; } .02-disconnected-context-prompt em { font-style:normal; color:#eff3ef; }
      .02-disconnected-context-prompt u { display:inline-block; width:9px; height:24px; margin-left:5px; background:#d7f85d; text-decoration:none; }
      .02-disconnected-context-links { position:absolute; inset:40px 0 0; width:2380px; height:380px; fill:none; stroke:#d7f85d; stroke-width:2; stroke-dasharray:10 12; }
      .02-disconnected-context-loss { position:absolute; left:116px; top:786px; font-size:46px; letter-spacing:-.03em; color:#8e9991; }
      .02-disconnected-context-loss strong { color:#ffb75c; }
    """,
    """
      const world = document.querySelector('.02-disconnected-context-world');
      const pA = document.getElementById('02-disconnected-context-link-a');
      const pB = document.getElementById('02-disconnected-context-link-b');
      [pA,pB].forEach(p=>{const l=p.getTotalLength();gsap.set(p,{strokeDasharray:l,strokeDashoffset:l});});
      gsap.set(['.02-disconnected-context-map','.02-disconnected-context-ai','.02-disconnected-context-loss'],{opacity:0});
      tl.fromTo('.02-disconnected-context-human',{x:-90,opacity:0},{x:0,opacity:1,duration:1,ease:'power3.out'},.1);
      tl.to(pA,{strokeDashoffset:0,duration:1.7,ease:'power2.inOut'},1.3);
      tl.to(world,{x:-690,duration:1.8,ease:'power3.inOut'},3.0);
      tl.set('.02-disconnected-context-map',{autoAlpha:1},3.0);
      tl.fromTo('.02-disconnected-context-map',{scale:.94,opacity:0},{scale:1,opacity:1,duration:.9,ease:'power3.out'},3.15);
      tl.to(world,{x:-1440,duration:1.8,ease:'power3.inOut'},6.4);
      tl.set('.02-disconnected-context-ai',{autoAlpha:1},6.35);
      tl.fromTo('.02-disconnected-context-ai',{scale:.94,opacity:0},{scale:1,opacity:1,duration:.9,ease:'power3.out'},6.55);
      const typed=document.getElementById('02-disconnected-context-typed'); const copy='reason about the incident'; const proxy={n:0};
      tl.to(proxy,{n:copy.length,duration:2.1,ease:'none',onUpdate:()=>typed.textContent=copy.slice(0,Math.floor(proxy.n))},7.2);
      tl.to(pB,{strokeDashoffset:0,duration:1.6,ease:'power2.inOut'},8.0);
      tl.to([pA,pB],{strokeDashoffset:120,duration:.45,ease:'power2.in'},9.85);
      tl.fromTo('.02-disconnected-context-loss',{y:35,opacity:0},{y:0,opacity:1,duration:.9,ease:'power3.out'},10.0);
    """,
)


FRAMES["03-one-shared-twin"] = frame(
    "03-one-shared-twin",
    16,
    """
      <div class="03-one-shared-twin-chrome"><span class="03-one-shared-twin-eyebrow">PYROSCAN // INCIDENT TWIN</span><span class="03-one-shared-twin-mono">ONE SHARED SURFACE</span></div>
      <div class="03-one-shared-twin-viewport 03-one-shared-twin-screen"><img src="assets/01-how-it-works.png" alt="PyroScan shared incident surface" /></div>
      <div class="03-one-shared-twin-label"><b>LA PALMA</b><span>PUBLIC CONTEXT · SYNTHETIC WHAT-IF</span></div>
      <div class="03-one-shared-twin-roles"><span>HUMAN GROUNDS</span><i></i><span>AGENT REHEARSES</span><i></i><span>HUMAN DECIDES</span></div>
    """,
    """
      .03-one-shared-twin-viewport { position:absolute; left:86px; top:132px; width:1748px; height:720px; }
      .03-one-shared-twin-viewport img { object-position:center 20%; }
      .03-one-shared-twin-label { position:absolute; left:122px; top:176px; padding:15px 18px; background:rgba(9,11,10,.84); border-left:3px solid #ffb75c; }
      .03-one-shared-twin-label b,.03-one-shared-twin-label span { display:block; } .03-one-shared-twin-label b { font-size:22px; } .03-one-shared-twin-label span { margin-top:4px; color:#8e9991; font-size:12px; letter-spacing:.12em; }
      .03-one-shared-twin-roles { position:absolute; left:300px; right:300px; top:788px; height:70px; display:flex; align-items:center; justify-content:center; gap:22px; padding:0 28px; background:#111412; border:1px solid rgba(215,248,93,.22); }
      .03-one-shared-twin-roles span { font-size:15px; letter-spacing:.12em; font-weight:600; color:#eff3ef; }
      .03-one-shared-twin-roles i { width:120px; height:2px; background:#d7f85d; }
    """,
    """
      gsap.set(['.03-one-shared-twin-label','.03-one-shared-twin-roles'],{opacity:0});
      tl.fromTo('.03-one-shared-twin-viewport',{scale:1.72,x:-110,y:120,opacity:.7},{scale:1,x:0,y:0,opacity:1,duration:6.8,ease:'power3.inOut'},.05);
      tl.fromTo('.03-one-shared-twin-label',{x:-30,opacity:0},{x:0,opacity:1,duration:.8,ease:'power3.out'},7.1);
      tl.set('.03-one-shared-twin-roles',{autoAlpha:1},8.5);
      tl.fromTo('.03-one-shared-twin-roles span',{y:24,opacity:0},{y:0,opacity:1,duration:.75,stagger:1.05,ease:'power3.out'},8.5);
      tl.fromTo('.03-one-shared-twin-roles i',{scaleX:0},{scaleX:1,duration:.8,stagger:1.05,ease:'power2.inOut'},9.25);
    """,
)


FRAMES["04-webmcp-protocol"] = frame(
    "04-webmcp-protocol",
    18,
    """
      <div class="04-webmcp-protocol-chrome"><span class="04-webmcp-protocol-eyebrow">WEBMCP · INTENT LEVEL</span><span class="04-webmcp-protocol-mono">PAGE → TOOLS → SHARED STATE</span></div>
      <div class="04-webmcp-protocol-person 04-webmcp-protocol-human"><b>HUMAN</b><span>local context</span></div>
      <div class="04-webmcp-protocol-person 04-webmcp-protocol-agent"><b>CHATGPT</b><span>bounded exploration</span></div>
      <div class="04-webmcp-protocol-hub"><img src="assets/pyroscan-mark.svg" alt="PyroScan mark"/><b>LIVE<br/>BOARD</b><span>same page · same state</span></div>
      <svg class="04-webmcp-protocol-lines" viewBox="0 0 1920 720" aria-hidden="true"><g id="04-webmcp-protocol-line-group"><path d="M270 360 C480 360 520 360 700 360"/><path d="M1650 360 C1440 360 1400 360 1220 360"/><path d="M960 300 L960 160"/><path d="M960 420 L960 570"/><path d="M860 330 L660 190"/><path d="M1060 330 L1260 190"/><path d="M860 390 L660 550"/><path d="M1060 390 L1260 550"/></g></svg>
      <div class="04-webmcp-protocol-tool 04-webmcp-protocol-t1">READ</div><div class="04-webmcp-protocol-tool 04-webmcp-protocol-t2">INSPECT</div><div class="04-webmcp-protocol-tool 04-webmcp-protocol-t3">ANNOTATE</div><div class="04-webmcp-protocol-tool 04-webmcp-protocol-t4">SIMULATE</div><div class="04-webmcp-protocol-tool 04-webmcp-protocol-t5">COMPARE</div><div class="04-webmcp-protocol-tool 04-webmcp-protocol-t6">STAGE</div>
      <div class="04-webmcp-protocol-proof"><span>NO SERVER TO INSTALL</span><i></i><span>NO BRITTLE CLICK SCRIPT</span></div>
    """,
    """
      .04-webmcp-protocol-person { position:absolute; top:400px; width:260px; text-align:center; }
      .04-webmcp-protocol-person b,.04-webmcp-protocol-person span { display:block; } .04-webmcp-protocol-person b { font-size:30px; } .04-webmcp-protocol-person span { margin-top:8px; color:#8e9991; font-size:15px; }
      .04-webmcp-protocol-human { left:80px; } .04-webmcp-protocol-agent { right:80px; }
      .04-webmcp-protocol-hub { position:absolute; left:760px; top:286px; width:400px; height:260px; display:grid; place-items:center; text-align:center; border:1px solid rgba(215,248,93,.42); background:radial-gradient(circle,rgba(215,248,93,.09),transparent 72%),#0b0e0c; }
      .04-webmcp-protocol-hub img { width:62px; height:62px; } .04-webmcp-protocol-hub b { margin-top:-10px; font-size:54px; line-height:.86; letter-spacing:-.045em; } .04-webmcp-protocol-hub span { margin-top:-18px; color:#8e9991; font-size:13px; letter-spacing:.12em; }
      .04-webmcp-protocol-lines { position:absolute; inset:100px 0 0; width:1920px; height:720px; fill:none; stroke:rgba(215,248,93,.55); stroke-width:2; }
      .04-webmcp-protocol-tool { position:absolute; min-width:190px; height:54px; display:grid; place-items:center; border:1px solid rgba(198,215,202,.18); background:#111412; font-size:14px; letter-spacing:.15em; color:#d7f85d; }
      .04-webmcp-protocol-t1 { left:865px; top:170px; } .04-webmcp-protocol-t2 { left:440px; top:214px; } .04-webmcp-protocol-t3 { right:440px; top:214px; } .04-webmcp-protocol-t4 { left:430px; top:650px; } .04-webmcp-protocol-t5 { right:430px; top:650px; } .04-webmcp-protocol-t6 { left:865px; top:716px; }
      .04-webmcp-protocol-proof { position:absolute; left:575px; right:575px; top:820px; display:flex; justify-content:center; align-items:center; gap:24px; color:#8e9991; font-size:13px; letter-spacing:.13em; }
      .04-webmcp-protocol-proof i { width:8px; height:8px; border-radius:50%; background:#d7f85d; }
    """,
    """
      const tools=gsap.utils.toArray('.04-webmcp-protocol-tool'); const lines=gsap.utils.toArray('#04-webmcp-protocol-line-group path');
      gsap.set([tools,'.04-webmcp-protocol-person','.04-webmcp-protocol-proof'],{opacity:0});
      lines.forEach(p=>{const l=p.getTotalLength();gsap.set(p,{strokeDasharray:l,strokeDashoffset:l});});
      tl.fromTo('.04-webmcp-protocol-hub',{scale:.86,opacity:0},{scale:1,opacity:1,duration:1,ease:'power3.out'},.1);
      tl.fromTo('.04-webmcp-protocol-person',{y:32,opacity:0},{y:0,opacity:1,duration:.8,stagger:.35,ease:'power3.out'},1.8);
      tools.forEach((el,i)=>tl.fromTo(el,{scale:.82,opacity:0},{scale:1,opacity:1,duration:.55,ease:'power3.out'},3.0+i*1.35));
      lines.forEach((p,i)=>tl.to(p,{strokeDashoffset:0,duration:.9,ease:'power2.inOut'},3.45+i*.85));
      tl.fromTo('.04-webmcp-protocol-hub',{boxShadow:'0 0 0 rgba(215,248,93,0)'},{boxShadow:'0 0 70px rgba(215,248,93,.22)',duration:1.1,ease:'power2.out'},11.8);
      tl.fromTo('.04-webmcp-protocol-proof',{y:22,opacity:0},{y:0,opacity:1,duration:.9,ease:'power3.out'},14.7);
    """,
)


FRAMES["05-local-knowledge"] = frame(
    "05-local-knowledge",
    22,
    """
      <div class="05-local-knowledge-chrome"><span class="05-local-knowledge-eyebrow">REAL TOOL JOURNEY · 01</span><span class="05-local-knowledge-mono">INTENT → VISIBLE STATE</span></div>
      <div class="05-local-knowledge-prompt"><span>ASK</span><b id="05-local-knowledge-prompt-text"></b><i></i></div>
      <div class="05-local-knowledge-receipt"><span id="05-local-knowledge-tool-name">inspect_zone</span><b id="05-local-knowledge-tool-result">EL PASO FOCUSED</b></div>
      <div class="05-local-knowledge-app 05-local-knowledge-screen"><img class="05-local-knowledge-state-a" src="assets/02-inspect-zone.png" alt="El Paso focused through WebMCP"/><img class="05-local-knowledge-state-b" src="assets/03-human-context.png" alt="LP-3 route constraint added through WebMCP"/></div>
      <div class="05-local-knowledge-highlight 05-local-knowledge-highlight-zone">EL PASO</div>
      <div class="05-local-knowledge-highlight 05-local-knowledge-highlight-note">LP-3 CONSTRAINT · VISIBLE</div>
      <div class="05-local-knowledge-future"><span>SIMULATE</span><span>COMPARE</span><span>STAGE</span></div>
      <div class="05-local-knowledge-footer">VISIBLE TO HUMAN <i></i> AVAILABLE TO AGENT</div>
    """,
    """
      .05-local-knowledge-prompt { position:absolute; left:150px; right:150px; top:142px; height:84px; display:grid; grid-template-columns:100px 1fr 10px; align-items:center; padding:0 28px; border:1px solid rgba(215,248,93,.28); background:#0b0e0c; }
      .05-local-knowledge-prompt span { color:#d7f85d; font-size:13px; letter-spacing:.16em; } .05-local-knowledge-prompt b { font-size:19px; font-weight:500; } .05-local-knowledge-prompt i { width:8px; height:25px; background:#d7f85d; }
      .05-local-knowledge-receipt { position:absolute; left:76px; top:302px; width:300px; padding:22px; border-left:3px solid #d7f85d; background:rgba(215,248,93,.055); }
      .05-local-knowledge-receipt span,.05-local-knowledge-receipt b { display:block; } .05-local-knowledge-receipt span { color:#d7f85d; font-size:15px; } .05-local-knowledge-receipt b { margin-top:9px; font-size:21px; }
      .05-local-knowledge-app { position:absolute; left:420px; top:272px; width:1424px; height:608px; }
      .05-local-knowledge-app img { position:absolute; inset:0; }
      .05-local-knowledge-highlight { position:absolute; padding:9px 13px; border:2px solid #ffb75c; background:rgba(9,11,10,.86); color:#ffb75c; font-size:13px; letter-spacing:.12em; }
      .05-local-knowledge-highlight-zone { left:808px; top:565px; } .05-local-knowledge-highlight-note { left:455px; top:696px; }
      .05-local-knowledge-future { position:absolute; left:78px; top:520px; display:grid; gap:10px; }
      .05-local-knowledge-future span { width:258px; padding:15px 18px; border:1px solid rgba(198,215,202,.18); color:#8e9991; font-size:13px; letter-spacing:.13em; }
      .05-local-knowledge-footer { position:absolute; left:620px; top:900px; display:flex; align-items:center; gap:18px; color:#eff3ef; font-size:14px; letter-spacing:.14em; }
      .05-local-knowledge-footer i { width:80px; height:2px; background:#d7f85d; }
    """,
    """
      const a=document.querySelector('.05-local-knowledge-state-a'); const b=document.querySelector('.05-local-knowledge-state-b');
      gsap.set([b,'.05-local-knowledge-receipt','.05-local-knowledge-highlight','.05-local-knowledge-future span','.05-local-knowledge-footer'],{opacity:0});
      const prompt='Inspect El Paso. Add an LP-3 blocked-road exercise note.'; const proxy={n:0}; const p=document.getElementById('05-local-knowledge-prompt-text');
      tl.to(proxy,{n:prompt.length,duration:3.2,ease:'none',onUpdate:()=>p.textContent=prompt.slice(0,Math.floor(proxy.n))},.1);
      tl.fromTo('.05-local-knowledge-app',{y:44,opacity:0},{y:0,opacity:1,duration:1,ease:'power3.out'},3.4);
      tl.fromTo('.05-local-knowledge-receipt',{x:-30,opacity:0},{x:0,opacity:1,duration:.8,ease:'power3.out'},4.2);
      tl.fromTo('.05-local-knowledge-highlight-zone',{scale:.8,opacity:0},{scale:1,opacity:1,duration:.65,ease:'power3.out'},5.4);
      tl.to(a,{opacity:0,duration:.45,ease:'power2.inOut'},9.5); tl.to(b,{opacity:1,duration:.45,ease:'power2.inOut'},9.5);
      tl.set('#05-local-knowledge-tool-name',{textContent:'add_board_annotation'},9.55); tl.set('#05-local-knowledge-tool-result',{textContent:'LP-3 NOTE ADDED'},9.55);
      tl.set('.05-local-knowledge-highlight-zone',{autoAlpha:0},9.55);
      tl.fromTo('.05-local-knowledge-highlight-note',{scale:.86,opacity:0},{scale:1,opacity:1,duration:.75,ease:'power3.out'},10.1);
      tl.fromTo('.05-local-knowledge-future span',{x:-24,opacity:0},{x:0,opacity:1,duration:.55,stagger:1.0,ease:'power3.out'},15.4);
      tl.fromTo('.05-local-knowledge-footer',{y:20,opacity:0},{y:0,opacity:1,duration:.8,ease:'power3.out'},19.4);
    """,
)


FRAMES["06-bounded-what-if"] = frame(
    "06-bounded-what-if",
    20,
    """
      <div class="06-bounded-what-if-chrome"><span class="06-bounded-what-if-eyebrow">REAL TOOL JOURNEY · 02</span><span class="06-bounded-what-if-mono">SIMULATE_SPREAD</span></div>
      <div class="06-bounded-what-if-receipt"><b>60 MIN</b><span>NORTHEAST SHIFT</span></div>
      <div class="06-bounded-what-if-app 06-bounded-what-if-screen"><img src="assets/04-simulate-spread.png" alt="Real 60-minute northeast shift state"/></div>
      <svg class="06-bounded-what-if-rings" viewBox="0 0 520 520"><ellipse id="06-bounded-what-if-r1" cx="260" cy="260" rx="92" ry="70"/><ellipse id="06-bounded-what-if-r2" cx="260" cy="260" rx="150" ry="112"/><ellipse id="06-bounded-what-if-r3" cx="260" cy="260" rx="214" ry="158"/></svg>
      <div class="06-bounded-what-if-meaning"><b>BOUNDED<br/>WHAT-IF</b><span>NOT A FORECAST</span></div>
      <div class="06-bounded-what-if-together"><span>HUMAN</span><i></i><span>SAME MAP</span><i></i><span>AGENT</span></div>
    """,
    """
      .06-bounded-what-if-app { position:absolute; left:106px; top:142px; width:1708px; height:708px; transform-origin:58% 58%; }
      .06-bounded-what-if-receipt { position:absolute; z-index:4; left:138px; top:184px; padding:18px 22px; background:rgba(9,11,10,.88); border-left:3px solid #d7f85d; }
      .06-bounded-what-if-receipt b,.06-bounded-what-if-receipt span { display:block; } .06-bounded-what-if-receipt b { font-size:28px; } .06-bounded-what-if-receipt span { margin-top:4px; color:#d7f85d; font-size:12px; letter-spacing:.14em; }
      .06-bounded-what-if-rings { position:absolute; z-index:3; left:680px; top:320px; width:520px; height:520px; fill:rgba(255,112,72,.025); stroke:#ff7048; stroke-width:3; }
      .06-bounded-what-if-meaning { position:absolute; left:116px; top:315px; width:520px; }
      .06-bounded-what-if-meaning b { display:block; font-size:104px; line-height:.86; letter-spacing:-.055em; } .06-bounded-what-if-meaning span { display:inline-block; margin-top:30px; padding:13px 18px; border:1px solid rgba(255,183,92,.4); color:#ffb75c; font-size:17px; letter-spacing:.15em; }
      .06-bounded-what-if-together { position:absolute; left:560px; top:884px; display:flex; align-items:center; gap:20px; font-size:14px; letter-spacing:.15em; color:#8e9991; }
      .06-bounded-what-if-together i { width:74px; height:2px; background:#d7f85d; }
    """,
    """
      gsap.set(['.06-bounded-what-if-rings','.06-bounded-what-if-meaning','.06-bounded-what-if-together'],{opacity:0});
      tl.fromTo('.06-bounded-what-if-app',{scale:.98,opacity:0},{scale:1,opacity:1,duration:1,ease:'power3.out'},.1);
      tl.fromTo('.06-bounded-what-if-receipt',{x:-25,opacity:0},{x:0,opacity:1,duration:.75,ease:'power3.out'},.6);
      tl.to('.06-bounded-what-if-app',{scale:1.18,x:-30,y:-34,duration:4.2,ease:'power3.inOut'},4.5);
      tl.set('.06-bounded-what-if-rings',{autoAlpha:1},5.0);
      ['06-bounded-what-if-r1','06-bounded-what-if-r2','06-bounded-what-if-r3'].forEach((id,i)=>{const p=document.getElementById(id);const l=p.getTotalLength();gsap.set(p,{strokeDasharray:l,strokeDashoffset:l});tl.to(p,{strokeDashoffset:0,duration:1.6,ease:'power2.inOut'},5.1+i*.8);});
      tl.to('.06-bounded-what-if-app',{scale:.78,x:430,y:42,duration:1.5,ease:'power3.inOut'},11.4);
      tl.set('.06-bounded-what-if-rings',{autoAlpha:0},11.4);
      tl.fromTo('.06-bounded-what-if-meaning',{x:-70,opacity:0},{x:0,opacity:1,duration:1.1,ease:'power3.out'},11.8);
      tl.to('.06-bounded-what-if-app',{scale:1,x:0,y:0,duration:1.4,ease:'power3.inOut'},15.8);
      tl.set('.06-bounded-what-if-meaning',{autoAlpha:0},15.8);
      tl.fromTo('.06-bounded-what-if-together',{y:20,opacity:0},{y:0,opacity:1,duration:.9,ease:'power3.out'},16.4);
    """,
)


FRAMES["07-compare-tradeoffs"] = frame(
    "07-compare-tradeoffs",
    18,
    """
      <div class="07-compare-tradeoffs-chrome"><span class="07-compare-tradeoffs-eyebrow">REAL TOOL JOURNEY · 03</span><span class="07-compare-tradeoffs-mono">COMPARE_RESPONSE_OPTIONS</span></div>
      <div class="07-compare-tradeoffs-cards">
        <article class="07-compare-tradeoffs-card"><span>OPTION A</span><b>HOLD<br/>THE RIDGE</b><dl><dt>SETUP</dt><dd>18 MIN</dd><dt>COVERAGE</dt><dd>2 SECTORS</dd><dt>ACCESS</dt><dd class="warn">CONSTRAINED</dd></dl><i><u></u></i></article>
        <article class="07-compare-tradeoffs-card 07-compare-tradeoffs-card-accent"><span>OPTION B</span><b>PROTECT BOTH<br/>INTERFACES</b><dl><dt>SETUP</dt><dd>26 MIN</dd><dt>COVERAGE</dt><dd>4 SECTORS</dd><dt>ACCESS</dt><dd class="warn">VALIDATE LP-3</dd></dl><i><u></u></i></article>
      </div>
      <div class="07-compare-tradeoffs-app 07-compare-tradeoffs-screen"><img src="assets/05-compare-options.png" alt="Real ranked comparison workbench"/></div>
      <div class="07-compare-tradeoffs-payoff">ON SCREEN. <strong>INSPECTABLE.</strong></div>
    """,
    """
      .07-compare-tradeoffs-cards { position:absolute; left:160px; right:160px; top:155px; height:650px; display:grid; grid-template-columns:1fr 1fr; gap:1px; background:rgba(198,215,202,.2); }
      .07-compare-tradeoffs-card { padding:48px; background:#111412; }
      .07-compare-tradeoffs-card-accent { background:#d7f85d; color:#111412; }
      .07-compare-tradeoffs-card>span { font-size:13px; letter-spacing:.16em; color:#8e9991; } .07-compare-tradeoffs-card-accent>span { color:rgba(17,20,18,.6); }
      .07-compare-tradeoffs-card>b { display:block; margin-top:34px; font-size:64px; line-height:.9; letter-spacing:-.05em; }
      .07-compare-tradeoffs-card dl { display:grid; grid-template-columns:1fr auto; gap:0; margin-top:54px; border-top:1px solid rgba(198,215,202,.18); }
      .07-compare-tradeoffs-card dt,.07-compare-tradeoffs-card dd { margin:0; padding:17px 0; border-bottom:1px solid rgba(198,215,202,.12); font-size:14px; } .07-compare-tradeoffs-card dt { color:#8e9991; letter-spacing:.12em; } .07-compare-tradeoffs-card .warn { color:#ffb75c; }
      .07-compare-tradeoffs-card-accent dt { color:rgba(17,20,18,.55); } .07-compare-tradeoffs-card-accent .warn { color:#6c321f; }
      .07-compare-tradeoffs-card>i { display:block; width:100%; height:8px; margin-top:26px; background:rgba(142,153,145,.16); } .07-compare-tradeoffs-card>i u { display:block; width:76%; height:100%; background:#ffb75c; }
      .07-compare-tradeoffs-card-accent>i { background:rgba(17,20,18,.16); } .07-compare-tradeoffs-card-accent>i u { width:88%; background:#111412; }
      .07-compare-tradeoffs-app { position:absolute; left:105px; top:140px; width:1710px; height:710px; }
      .07-compare-tradeoffs-payoff { position:absolute; left:530px; top:875px; font-size:50px; letter-spacing:-.03em; color:#8e9991; } .07-compare-tradeoffs-payoff strong { color:#d7f85d; }
    """,
    """
      gsap.set(['.07-compare-tradeoffs-app','.07-compare-tradeoffs-payoff'],{opacity:0});
      tl.fromTo('.07-compare-tradeoffs-card:first-child',{x:-110,opacity:0},{x:0,opacity:1,duration:1.1,ease:'power3.out'},.1);
      tl.fromTo('.07-compare-tradeoffs-card:last-child',{x:110,opacity:0},{x:0,opacity:1,duration:1.1,ease:'power3.out'},.1);
      tl.fromTo('.07-compare-tradeoffs-card dl>*',{y:18,opacity:0},{y:0,opacity:1,duration:.45,stagger:.42,ease:'power3.out'},2.8);
      tl.fromTo('.07-compare-tradeoffs-card>i u',{scaleX:0},{scaleX:1,duration:1.6,ease:'power3.out',transformOrigin:'left center'},6.9);
      tl.to('.07-compare-tradeoffs-cards',{scale:.72,opacity:0,duration:.65,ease:'power2.in'},9.8);
      tl.fromTo('.07-compare-tradeoffs-app',{scale:1.16,opacity:0},{scale:1,opacity:1,duration:1.2,ease:'power3.out'},10.0);
      tl.fromTo('.07-compare-tradeoffs-payoff',{y:24,opacity:0},{y:0,opacity:1,duration:.8,ease:'power3.out'},14.4);
    """,
)


FRAMES["08-state-lineage"] = frame(
    "08-state-lineage",
    22,
    """
      <div class="08-state-lineage-chrome"><span class="08-state-lineage-eyebrow">STATE LINEAGE</span><span class="08-state-lineage-mono">READ → VERIFY → STAGE</span></div>
      <div class="08-state-lineage-lineage"><div class="08-state-lineage-node">READ BOARD</div><i></i><div class="08-state-lineage-version">v<span id="08-state-lineage-version-number">15</span></div><i></i><div class="08-state-lineage-node">STAGE PLAN</div></div>
      <div class="08-state-lineage-stale"><span>v14</span><b>STALE BOARD · REJECTED</b></div>
      <div class="08-state-lineage-app 08-state-lineage-screen"><img src="assets/06-staged-plan.png" alt="Real reversible plan carrying the LP-3 access constraint"/></div>
      <div class="08-state-lineage-source">LP-3 NOTE</div><div class="08-state-lineage-target">VALIDATE ACCESS</div><svg class="08-state-lineage-causal" viewBox="0 0 1920 1080"><path id="08-state-lineage-causal-path" d="M245 650 C610 720 1160 620 1600 520"/></svg>
      <div class="08-state-lineage-payoff">HUMAN INPUT <i></i> DOWNSTREAM ARTIFACT</div>
    """,
    """
      .08-state-lineage-lineage { position:absolute; left:340px; right:340px; top:160px; height:100px; display:flex; align-items:center; justify-content:center; gap:24px; }
      .08-state-lineage-node { width:250px; height:72px; display:grid; place-items:center; border:1px solid rgba(198,215,202,.22); font-size:14px; letter-spacing:.13em; }
      .08-state-lineage-lineage>i { width:90px; height:2px; background:#d7f85d; }
      .08-state-lineage-version { width:100px; height:100px; display:grid; place-items:center; border-radius:50%; border:2px solid #d7f85d; font-size:34px; font-weight:700; }
      .08-state-lineage-stale { position:absolute; left:420px; top:288px; display:flex; gap:18px; align-items:center; padding:16px 20px; border:1px solid rgba(255,183,92,.28); color:#ffb75c; background:rgba(255,183,92,.05); }
      .08-state-lineage-stale span { font-size:28px; font-weight:700; } .08-state-lineage-stale b { font-size:14px; letter-spacing:.13em; }
      .08-state-lineage-app { position:absolute; left:90px; top:360px; width:1740px; height:520px; }
      .08-state-lineage-source,.08-state-lineage-target { position:absolute; z-index:4; padding:10px 14px; background:rgba(9,11,10,.9); border:2px solid #ffb75c; color:#ffb75c; font-size:13px; letter-spacing:.12em; }
      .08-state-lineage-source { left:138px; top:680px; } .08-state-lineage-target { right:138px; top:485px; }
      .08-state-lineage-causal { position:absolute; z-index:3; inset:0; width:1920px; height:1080px; fill:none; stroke:#d7f85d; stroke-width:4; }
      .08-state-lineage-payoff { position:absolute; left:520px; top:905px; display:flex; gap:20px; align-items:center; font-size:15px; letter-spacing:.15em; } .08-state-lineage-payoff i { width:130px; height:2px; background:#d7f85d; }
    """,
    """
      const causal=document.getElementById('08-state-lineage-causal-path'); const cl=causal.getTotalLength(); gsap.set(causal,{strokeDasharray:cl,strokeDashoffset:cl});
      gsap.set(['.08-state-lineage-lineage>*','.08-state-lineage-stale','.08-state-lineage-app','.08-state-lineage-source','.08-state-lineage-target','.08-state-lineage-payoff'],{opacity:0});
      tl.fromTo('.08-state-lineage-lineage>*',{x:-28,opacity:0},{x:0,opacity:1,duration:.6,stagger:.62,ease:'power3.out'},.1);
      const digits=['?','1','5']; const vd={i:0}; const ve=document.getElementById('08-state-lineage-version-number');
      tl.to(vd,{i:digits.length-1,duration:1.2,ease:'steps(2)',onUpdate:()=>ve.textContent=digits[Math.round(vd.i)]},2.0);
      tl.fromTo('.08-state-lineage-stale',{x:-35,opacity:0},{x:0,opacity:1,duration:.8,ease:'power3.out'},5.0);
      tl.to('.08-state-lineage-stale',{x:-160,opacity:.28,duration:.6,ease:'power2.in'},8.5);
      tl.fromTo('.08-state-lineage-app',{scale:1.08,opacity:0},{scale:1,opacity:1,duration:1.1,ease:'power3.out'},9.3);
      tl.fromTo('.08-state-lineage-target',{scale:.84,opacity:0},{scale:1,opacity:1,duration:.7,ease:'power3.out'},11.7);
      tl.fromTo('.08-state-lineage-source',{scale:.84,opacity:0},{scale:1,opacity:1,duration:.7,ease:'power3.out'},15.2);
      tl.to(causal,{strokeDashoffset:0,duration:2.0,ease:'power2.inOut'},15.6);
      tl.fromTo('.08-state-lineage-payoff',{y:22,opacity:0},{y:0,opacity:1,duration:.9,ease:'power3.out'},18.8);
    """,
)


FRAMES["09-human-gate"] = frame(
    "09-human-gate",
    14,
    """
      <div class="09-human-gate-chrome"><span class="09-human-gate-eyebrow">SAFE DIVISION OF LABOR</span><span class="09-human-gate-mono">AGENT ≠ AUTHORITY</span></div>
      <div class="09-human-gate-anchor">THE AGENT CAN</div>
      <div class="09-human-gate-cycle"><span>INSPECT</span><span>ANNOTATE</span><span>SIMULATE</span><span>COMPARE</span><span>STAGE</span><span class="09-human-gate-no">APPROVE</span></div>
      <div class="09-human-gate-app 09-human-gate-screen"><img src="assets/06-staged-plan.png" alt="Staged plan with human-only approval gate"/></div>
      <div class="09-human-gate-human">HUMAN ONLY</div>
      <div class="09-human-gate-division"><span>EXPLORATION · AGENT</span><i></i><span>AUTHORITY · HUMAN</span></div>
    """,
    """
      .09-human-gate-anchor { position:absolute; z-index:3; left:150px; top:200px; font-size:68px; font-weight:700; letter-spacing:-.04em; }
      .09-human-gate-cycle { position:absolute; z-index:3; left:150px; top:300px; width:1100px; height:220px; }
      .09-human-gate-cycle span { position:absolute; inset:0; font-size:178px; line-height:1; font-weight:700; letter-spacing:-.065em; color:#d7f85d; }
      .09-human-gate-cycle .09-human-gate-no { color:#ffb75c; text-decoration:line-through; text-decoration-thickness:10px; }
      .09-human-gate-app { position:absolute; z-index:1; left:590px; top:160px; width:1250px; height:610px; }
      .09-human-gate-human { position:absolute; right:110px; top:615px; padding:15px 20px; border:2px solid #d7f85d; background:#111412; color:#d7f85d; font-size:14px; letter-spacing:.16em; }
      .09-human-gate-division { position:absolute; left:400px; top:850px; display:flex; align-items:center; gap:26px; color:#8e9991; font-size:17px; letter-spacing:.14em; } .09-human-gate-division i { width:180px; height:2px; background:#d7f85d; }
    """,
    """
      const verbs=gsap.utils.toArray('.09-human-gate-cycle span'); gsap.set(verbs,{opacity:0}); gsap.set(['.09-human-gate-app','.09-human-gate-human','.09-human-gate-division'],{opacity:0});
      tl.fromTo('.09-human-gate-anchor',{x:-60,opacity:0},{x:0,opacity:1,duration:.8,ease:'power3.out'},.1);
      verbs.slice(0,5).forEach((el,i)=>{tl.set(el,{autoAlpha:1},1.0+i*.75); if(i<4) tl.set(el,{autoAlpha:0},1.7+i*.75);});
      tl.set(verbs[4],{autoAlpha:0},4.75); tl.fromTo(verbs[5],{scale:.92,opacity:0},{scale:1,opacity:1,duration:.7,ease:'power3.out'},4.9);
      tl.fromTo('.09-human-gate-app',{y:90,opacity:0},{y:0,opacity:.92,duration:1.1,ease:'power3.out'},7.8);
      tl.fromTo('.09-human-gate-human',{scale:.82,opacity:0},{scale:1,opacity:1,duration:.7,ease:'power3.out'},9.3);
      tl.fromTo('.09-human-gate-division',{y:24,opacity:0},{y:0,opacity:1,duration:.8,ease:'power3.out'},11.1);
    """,
)


FRAMES["10-close"] = frame(
    "10-close",
    14,
    """
      <div class="10-close-app"><img src="assets/01-how-it-works.png" alt="PyroScan shared incident surface"/></div>
      <div class="10-close-proof"><span>SYNTHETIC</span><span>DETERMINISTIC</span><span>BROWSER-ONLY</span><span>OPEN SOURCE</span></div>
      <div class="10-close-boundaries"><span>NO LIVE FEED</span><span>NO DISPATCH</span><span>NO HIDDEN BACKEND</span></div>
      <div class="10-close-claim"><span>rehearse trade-offs</span><span>before they become</span><span>irreversible.</span></div>
      <div class="10-close-lockup"><img src="assets/pyroscan-mark.svg" alt="PyroScan mark"/><div><b>PYROSCAN</b><strong>Incident Twin</strong></div><p>wildfire readiness, rehearsed together.</p><a>sebastianfernandezgarcia.github.io/pyroscan-incident-twin</a></div>
    """,
    """
      .10-close-app { position:absolute; inset:0; opacity:.2; } .10-close-app::after { content:''; position:absolute; inset:0; background:rgba(9,11,10,.55); } .10-close-app img { width:100%; height:100%; object-fit:cover; }
      .10-close-proof { position:absolute; left:130px; top:205px; width:1500px; height:190px; }
      .10-close-proof span { position:absolute; inset:0; font-size:150px; line-height:1; font-weight:700; letter-spacing:-.06em; }
      .10-close-boundaries { position:absolute; left:145px; top:520px; display:grid; gap:24px; }
      .10-close-boundaries span { display:block; padding-bottom:13px; width:620px; border-bottom:1px solid rgba(255,183,92,.4); color:#ffb75c; font-size:26px; letter-spacing:.12em; }
      .10-close-claim { position:absolute; inset:0; padding:160px 125px; background:#d7f85d; color:#111412; font-size:118px; line-height:1.2; letter-spacing:-.06em; font-weight:700; opacity:0; visibility:hidden; }
      .10-close-claim span { display:block; }
      .10-close-lockup { position:absolute; inset:0; display:grid; place-content:center; text-align:center; background:#111412; }
      .10-close-lockup>img { width:96px; height:96px; margin:0 auto 28px; } .10-close-lockup div { display:flex; align-items:baseline; gap:14px; justify-content:center; } .10-close-lockup b { font-size:28px; letter-spacing:.12em; } .10-close-lockup strong { font-size:28px; font-weight:500; color:#8e9991; }
      .10-close-lockup p { margin:28px 0 0; font-size:52px; letter-spacing:-.04em; } .10-close-lockup a { margin-top:22px; color:#d7f85d; font-size:14px; letter-spacing:.08em; }
    """,
    """
      const proof=gsap.utils.toArray('.10-close-proof span'); gsap.set(proof,{opacity:0}); gsap.set(['.10-close-boundaries span','.10-close-claim','.10-close-claim span','.10-close-lockup'],{opacity:0});
      proof.forEach((el,i)=>{tl.set(el,{autoAlpha:1},.15+i*.8); if(i<proof.length-1) tl.set(el,{autoAlpha:0},.85+i*.8);});
      tl.set(proof[3],{autoAlpha:0},3.35);
      tl.fromTo('.10-close-boundaries span',{x:-40,opacity:0},{x:0,opacity:1,duration:.55,stagger:.8,ease:'power3.out'},4.0);
      tl.set('.10-close-boundaries',{autoAlpha:0},7.15); tl.set('.10-close-claim',{autoAlpha:1},7.15);
      tl.fromTo('.10-close-claim span',{y:70,opacity:0},{y:0,opacity:1,duration:.65,stagger:.55,ease:'power3.out'},7.2);
      tl.to('.10-close-claim',{scale:.82,opacity:0,duration:.7,ease:'power2.in'},10.45);
      tl.fromTo('.10-close-lockup',{scale:.92,opacity:0},{scale:1,opacity:1,duration:1.0,ease:'power3.out'},10.6);
    """,
)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for frame_id, contents in FRAMES.items():
        (OUT / f"{frame_id}.html").write_text(contents, encoding="utf-8")
    print(f"built {len(FRAMES)} frame compositions in {OUT}")


if __name__ == "__main__":
    build()
