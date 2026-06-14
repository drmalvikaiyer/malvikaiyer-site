# -*- coding: utf-8 -*-
"""Site generator. Reads content/*.json (edited via the /admin visual editor) and
writes index.html. Pure standard library — runs locally and on Netlify
(build command: python3 build.py). No third-party packages required."""
import json, os, html, hashlib, re
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
CSS_V = hashlib.md5(open(os.path.join(HERE, "styles.css"), "rb").read()).hexdigest()[:8]
e = html.escape
def load(name): return json.load(open(os.path.join(CONTENT, name + ".json"), encoding="utf-8"))

site=load("site"); hero=load("hero"); stats=load("stats"); about=load("about")
honours=load("honours"); awards=load("awards"); speaking=load("speaking"); videos=load("videos")
mediasec=load("media"); press=load("press"); books=load("books"); blog=load("blog")
howto=load("howto"); interviews=load("interviews")
testi=load("testimonials"); connect=load("connect"); carousel=load("carousel"); onstage=load("onstage")

def attr(s): return e(s or "", quote=True)

# ---------- section builders ----------
def nav_html():
    items=[]
    for n in site["nav"]:
        cls=' class="cta"' if n.get("cta") else ""
        items.append(f'<a{cls} href="{attr(n["href"])}">{e(n["label"])}</a>')
    return "".join(items)

def stats_html():
    return "".join(f'<div class="stat"><div class="num" data-target="{attr(s["num"])}">{e(s["num"])}</div>'
                   f'<div class="lbl">{e(s["label"])}</div></div>' for s in stats["items"])

def creds_html(): return "".join(f'<span class="tag">{e(c)}</span>' for c in about["credentials"])
def edu_html():
    return "".join(f'<div class="item"><b>{e(x["degree"])}</b><span>{e(x["place"])}</span></div>'
                   for x in about["education"])
def paras_html(): return "".join(f"<p>{e(p)}</p>" for p in about["paragraphs"])

# small gold star accent for honours (sits before the title)
HSTAR=('<svg class="hstar" viewBox="0 0 24 24" aria-hidden="true">'
       '<path d="M12 2.4l2.6 6.6 7.1.4-5.5 4.5 1.8 6.9L12 17.4 6 21.2l1.8-6.9L2.3 9.8l7.1-.4z"/></svg>')

def honour_cards():
    out=[]
    for i,h in enumerate(honours["items"]):
        more=(f'<a class="more" href="{attr(h["link"])}" target="_blank" rel="noopener">Read more ↗</a>'
              if h.get("link") else "")
        phcls="ph contain" if h.get("contain") else "ph"
        ph=(f'<img class="{phcls}" src="{attr(h["image"])}" alt="{attr(h["title"])}" loading="lazy">'
            if h.get("image") else '<div class="ph ph-empty"></div>')
        out.append(f'<div class="card c{i%4}" style="--d:{i}">{ph}'
                   f'<div class="body"><h3>{HSTAR}{e(h["title"])}</h3><p>{e(h["description"])}</p>{more}</div></div>')
    return "\n".join(out)

def gallery_port(imgs):
    return "\n".join(f'<figure><img src="{attr(g)}" alt="Dr. Malvika Iyer" loading="lazy"></figure>' for g in imgs)

def award_cards():
    out=[]
    for i,a in enumerate(awards["items"]):
        ph=(f'<img class="ph" src="{attr(a["image"])}" alt="{attr(a["name"])}" loading="lazy">'
            if a.get("image") else '<div class="ph ph-empty"></div>')
        out.append(f'<div class="award" style="--d:{i}">{ph}<div class="body"><h3>{e(a["name"])}</h3>'
                   f'<p>{e(a.get("org",""))}</p></div></div>')
    return "\n".join(out)

def topics_html():
    return "".join(f'<span class="pill">{e(t["name"])}</span>' for t in speaking["topics"])
def regions_html():
    out=[]; i=0
    for r in speaking["regions"]:
        cls="wide r1" if r.get("wide") else f"r{(i%4)+1}"
        if not r.get("wide"): i+=1
        out.append(f'<div class="region {cls}"><h3>{e(r["name"])}</h3>'
                   f'<p>{e(r["organisations"])}</p></div>')
    return "\n".join(out)

def vcard(href,thumb,src,title):
    return (f'<a class="vcard" href="{attr(href)}" target="_blank" rel="noopener">'
            f'<span class="vthumb" style="background-image:url(\'{attr(thumb)}\')"><span class="play"></span></span>'
            f'<span class="vmeta"><span class="src">{e(src)}</span><h3>{e(title)}</h3></span></a>')
def videos_html():
    out=[]
    for v in videos["items"]:
        vid=v.get("youtube_id","")
        href=v.get("url") or (f"https://www.youtube.com/watch?v={vid}" if vid else "#")
        thumb=v.get("thumb") or (f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else "")
        out.append(vcard(href,thumb,v.get("source",""),v.get("title","")))
    return "\n".join(out)
def blog_html():
    out=[]
    for b in blog["items"]:
        vid=b.get("youtube_id","")
        thumb=b.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        out.append(vcard(f"https://www.youtube.com/watch?v={vid}",
                         thumb,"Watch & Learn",b.get("title","")))
    return "\n".join(out)

def howto_html():
    out=[]
    for b in howto["items"]:
        vid=b.get("youtube_id","")
        thumb=b.get("thumb") or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        out.append(vcard(f"https://www.youtube.com/watch?v={vid}",
                         thumb,howto.get("eyebrow",""),b.get("title","")))
    return "\n".join(out)

def interviews_html():
    return "\n".join(vcard(v.get("url","#"), v.get("image",""), interviews.get("eyebrow","Watch"), v.get("title",""))
                     for v in interviews.get("items", []))

def media_html():
    return "\n".join(f'<a href="{attr(m["url"])}" target="_blank" rel="noopener">'
                     f'<img src="{attr(m["image"])}" alt="Media feature on Dr. Malvika Iyer" loading="lazy"></a>'
                     for m in mediasec["items"])

def archive_html():
    out=[]
    for o in press["outlets"]:
        lis="".join(f'<li><a href="{attr(l["url"])}" target="_blank" rel="noopener">{e(l["title"])}</a></li>'
                    for l in o["links"])
        out.append(f'<div class="outlet"><h4>{e(o["name"])}</h4><ul>{lis}</ul></div>')
    return "\n".join(out)
n_press=sum(len(o["links"]) for o in press["outlets"])

_GENERIC = {"watch on youtube", "post on x / twitter", "facebook feature", "instagram post",
            "read on issuu", "listen · apple podcasts", "press clipping"}
def _dom(url):
    try: return urlparse(url).netloc.replace("www.", "")
    except Exception: return ""
def _mtitle(title, url, dom):
    t = (title or "").strip(); tl = t.lower()
    if t and tl not in _GENERIC and len(t) >= 6 and not ("." in t and " " not in t):
        return t
    u = (url or "").lower()
    if "youtube.com" in dom or "youtu.be" in dom: return "Watch the video"
    if "twitter.com" in dom or "x.com" in dom: return "View the post"
    if "facebook.com" in dom: return "View on Facebook"
    if "instagram.com" in dom: return "View on Instagram"
    if "issuu.com" in dom: return "Read the magazine"
    if "podcasts.apple" in dom: return "Listen to the podcast"
    if u.endswith((".jpg", ".jpeg", ".png", ".pdf")): return "View the feature"
    return "Read the story"
def media_cards():
    out = []
    for o in press["outlets"]:
        for l in o["links"]:
            dom = _dom(l["url"]); main = _mtitle(l.get("title"), l["url"], dom)
            logo = "https://www.google.com/s2/favicons?domain=%s&sz=64" % dom
            out.append(f'<a class="mcard" href="{attr(l["url"])}" target="_blank" rel="noopener">'
                       f'<img class="mlogo" src="{logo}" alt="" loading="lazy" onerror="this.remove()">'
                       f'<span class="minfo"><span class="mt">{e(main)}</span>'
                       f'<span class="md">{e(dom)} · Read more ↗</span></span></a>')
    return "\n".join(out)
def media_clip_cards():
    out = []
    for m in mediasec["items"]:
        dom = _dom(m["url"]); logo = "https://www.google.com/s2/favicons?domain=%s&sz=64" % dom
        out.append(f'<a class="mclip-card" href="{attr(m["url"])}" target="_blank" rel="noopener">'
                   f'<img class="mclip" src="{attr(m["image"])}" alt="{attr(m.get("title",""))}" loading="lazy">'
                   f'<span class="mfoot"><img class="mlogo" src="{logo}" alt="" loading="lazy" onerror="this.remove()">'
                   f'<span class="minfo"><span class="mt">{e(m.get("title",""))}</span>'
                   f'<span class="md">Read more ↗</span></span></span></a>')
    return "\n".join(out)

def books_html():
    return "\n".join(f'<div class="book"><h4>{e(b["title"])}</h4><span>{e(b.get("note",""))}</span>'
                     + (f'<br><a href="{attr(b["url"])}" target="_blank" rel="noopener">View ↗</a>' if b.get("url") else "")
                     + '</div>' for b in books["items"])
def mai_links_html():
    out=[]
    for m in books["mai_links"]:
        dom=_dom(m["url"]); logo="https://www.google.com/s2/favicons?domain=%s&sz=64" % dom
        out.append(f'<a class="mlink" href="{attr(m["url"])}" target="_blank" rel="noopener">'
                   f'<img class="mlink-ico" src="{logo}" alt="" loading="lazy" onerror="this.remove()">'
                   f'<span>{e(m["label"])}</span><span class="mlink-go">↗</span></a>')
    return "\n".join(out)

def onstage_cards(imgs):
    return "".join(f'<div class="ocard"><img src="{attr(im)}" alt="Dr. Malvika Iyer on stage" loading="lazy"></div>'
                   for im in imgs)

def onstage_rows():
    imgs=onstage.get("images", [])
    mid=(len(imgs)+1)//2            # split into two rows (~10 each)
    a,b=imgs[:mid], imgs[mid:]
    r1=onstage_cards(a); r2=onstage_cards(b)
    # duration scaled to card count; row 2 (reverse) eased a touch slower
    # because opposite-direction motion reads as faster to the eye
    d1=len(a)*4; d2=round(len(b)*4.5)
    return (f'<div class="marquee"><div class="track" style="animation-duration:{d1}s">{r1}{r1}</div></div>'
            f'<div class="marquee"><div class="track rev" style="animation-duration:{d2}s">{r2}{r2}</div></div>')

def carousel_html():
    imgs=carousel.get("images") or [hero.get("photo","")]
    return "".join(f'<img class="{"active" if i==0 else ""}" src="{attr(im)}" '
                   f'alt="Dr. Malvika Iyer" loading="{"eager" if i==0 else "lazy"}">'
                   for i,im in enumerate(imgs))

def social_html():
    return "\n".join(f'<a href="{attr(s["url"])}" target="_blank" rel="noopener">'
                     f'<span class="ic"><img src="{attr(s["icon"])}" alt="{attr(s["label"])}"></span>{e(s["label"])}</a>'
                     for s in connect["social"])

def testimonials_html():
    out=[]
    for t in testi["items"]:
        role=f'<span>{e(t["role"])}</span>' if t.get("role") else ""
        out.append(f'<figure class="tcard"><blockquote>{e(t["quote"])}</blockquote>'
                   f'<figcaption><b>{e(t["author"])}</b>{role}</figcaption></figure>')
    return "\n".join(out)
test_hidden = "" if testi["items"] else " is-hidden"
roles_p = ('<p class="roles" style="margin-top:18px">%s</p>' % about["roles_html"]) if about.get("roles_html") else ""
edu_note_html = ('<div class="edu-note"><span class="en-label">Continuing Education</span><p>%s</p></div>' % e(about["edu_note"])) if about.get("edu_note") else ""
speak_gal = ('<div class="gal g-port">%s</div>' % gallery_port(speaking["gallery"])) if speaking.get("gallery") else ""

FRONT_JS = """<script>
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  // ---- count-up stats ----
  function up(el){
    var t=el.getAttribute('data-target')||el.textContent;
    var m=t.match(/^(\\D*)(\\d[\\d,.]*)(.*)$/); if(!m){return;}
    var pre=m[1], raw=m[2].replace(/,/g,''), suf=m[3], target=parseFloat(raw), dur=1500, s=null;
    function step(ts){ if(!s){s=ts;} var p=Math.min((ts-s)/dur,1);
      el.textContent=pre+Math.round(target*(1-Math.pow(1-p,3)))+suf;
      if(p<1){requestAnimationFrame(step);} else {el.textContent=pre+raw+suf;} }
    requestAnimationFrame(step);
  }
  var nums=[].slice.call(document.querySelectorAll('#stats-row .num'));
  nums.forEach(function(el){ el.textContent=(el.getAttribute('data-target')||'').replace(/\\d[\\d,.]*/,'0'); });
  var row=document.getElementById('stats-row');
  if('IntersectionObserver' in window && row){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){nums.forEach(up);io.disconnect();}});},{threshold:0.3});
    io.observe(row);
  } else { nums.forEach(up); }
  // ---- hero photo carousel ----
  var carEl=document.getElementById('hero-carousel');
  var imgs=[].slice.call(document.querySelectorAll('#hero-carousel img'));
  if(imgs.length>1){
    var ci=0, gap=parseInt(carEl&&carEl.getAttribute('data-interval'),10)||3000;
    setInterval(function(){ imgs[ci].classList.remove('active'); ci=(ci+1)%imgs.length; imgs[ci].classList.add('active'); }, gap);
  }
  // ---- instant jump to Connect (skip slow smooth-scroll over a long page) ----
  [].slice.call(document.querySelectorAll('a[href="#connect"]')).forEach(function(a){
    a.addEventListener('click', function(ev){
      var t=document.getElementById('connect');
      if(t){ ev.preventDefault(); t.scrollIntoView({behavior:'auto',block:'start'}); history.replaceState(null,'','#connect'); }
    });
  });
  // ---- one-line video carousels ----
  [].slice.call(document.querySelectorAll('.vcarousel')).forEach(function(car){
    var track=car.querySelector('.vtrack');
    var prev=car.querySelector('.vnav.prev'), next=car.querySelector('.vnav.next');
    if(!track||!prev||!next){return;}
    function step(){ var card=track.querySelector('.vcard'); var w=card?card.getBoundingClientRect().width:200;
      var g=parseFloat(getComputedStyle(track).columnGap||getComputedStyle(track).gap||'24')||24;
      return Math.max(track.clientWidth*0.9, w+g); }
    function maxScroll(){ return track.scrollWidth-track.clientWidth; }
    function update(){ var m=maxScroll()-1; var fits=maxScroll()<=1;
      prev.disabled = fits || track.scrollLeft<=0;
      next.disabled = fits || track.scrollLeft>=m; }
    // timer-based tween (reliable even where rAF/native smooth-scroll is throttled)
    function glide(to){ to=Math.max(0,Math.min(to,maxScroll()));
      if(reduce){ track.scrollLeft=to; update(); return; }
      var start=track.scrollLeft, chg=to-start, steps=20, i=0;
      (function tick(){ i++; var p=i/steps;
        track.scrollLeft=start+chg*(1-Math.pow(1-p,3));
        if(i<steps){ setTimeout(tick,16); } else { track.scrollLeft=to; update(); } })(); }
    prev.addEventListener('click',function(){ glide(track.scrollLeft-step()); });
    next.addEventListener('click',function(){ glide(track.scrollLeft+step()); });
    track.addEventListener('scroll',update,{passive:true});
    window.addEventListener('resize',update);
    update();
  });
  // ---- scroll reveal ----
  if('IntersectionObserver' in window && !reduce){
    var tg=[].slice.call(document.querySelectorAll('.section .wrap'));
    tg.forEach(function(el){ el.classList.add('js-reveal'); });
    var ro=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');ro.unobserve(en.target);}});},{threshold:0.08});
    tg.forEach(function(el){ ro.observe(el); });
  }
  // ---- staggered card cascade (honours + awards) ----
  if('IntersectionObserver' in window && !reduce){
    var grids=[].slice.call(document.querySelectorAll('.cards, .awards-grid'));
    grids.forEach(function(g){ g.classList.add('stagger'); });
    var so=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');so.unobserve(en.target);}});},{threshold:0.12});
    grids.forEach(function(g){ so.observe(g); });
  }
  // offset anchor jumps so section headings aren't hidden under the sticky nav (esp. taller mobile nav)
  var navEl=document.querySelector('.nav');
  if(navEl){
    var setSP=function(){ document.documentElement.style.scrollPaddingTop=Math.max(navEl.offsetHeight-62,0)+'px'; };
    setSP(); window.addEventListener('resize', setSP); window.addEventListener('load', setSP);
  }
  // nav brand: hide while hero name is in view, fade in once it scrolls behind the nav
  var heroName=document.querySelector('.hero h1');
  if(navEl && heroName){
    var updBrand=function(){
      var navH=navEl.offsetHeight;
      navEl.classList.toggle('at-top', heroName.getBoundingClientRect().bottom > navH + 4);
    };
    updBrand();
    window.addEventListener('scroll', updBrand, {passive:true});
    window.addEventListener('resize', updBrand);
  }
})();
</script>"""

IDENTITY = ('<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>\n'
 '<script>if(window.netlifyIdentity){window.netlifyIdentity.on("init",function(u){'
 'if(!u){window.netlifyIdentity.on("login",function(){document.location.href="/admin/";});}});}</script>')

HTML = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(site["title"])}</title>
<meta name="description" content="{attr(site["description"])}">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/favicon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://malvikaiyer.com/">
<meta property="og:site_name" content="Dr. Malvika Iyer">
<meta property="og:title" content="{attr(site["title"])}">
<meta property="og:description" content="{attr(site["description"])}">
<meta property="og:image" content="https://malvikaiyer.com/assets/og-cover.jpg">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="1260">
<meta property="og:image:alt" content="Dr. Malvika Iyer — Motivational Speaker, Activist and Changemaker">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(site["title"])}">
<meta name="twitter:description" content="{attr(site["description"])}">
<meta name="twitter:image" content="https://malvikaiyer.com/assets/og-cover.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={CSS_V}">
</head><body>

<header class="nav"><div class="wrap">
  <a class="brand" href="#top">{e(site["brand_first"])}<span>{e(site["brand_last"])}</span></a>
  <nav>{nav_html()}</nav>
</div></header>

<section class="hero" id="top"><div class="wrap">
  <div>
    <span class="eyebrow">{e(hero["eyebrow"])}</span>
    <h1>{e(hero["name"])}</h1>
    <p class="sub">{e(hero["sub_pre"])}<b>{e(hero["sub_bold"])}</b></p>
    <div class="btnrow">
      <a class="btn btn-primary" href="{attr(hero["btn1_href"])}">{e(hero["btn1_label"])}</a>
      <a class="btn btn-ghost" href="{attr(hero["btn2_href"])}">{e(hero["btn2_label"])}</a>
    </div>
    <div class="ribbon">{e(hero["ribbon"])}</div>
  </div>
  <div class="hero-photo"><span class="blob"></span><span class="ring"></span>
    <div class="carousel" id="hero-carousel" data-interval="{carousel.get('interval',3000)}">{carousel_html()}</div>
  </div>
</div></section>

<section class="stats"><div class="wrap"><div class="row" id="stats-row">{stats_html()}</div></div></section>

<section class="section about" id="story"><div class="wrap">
  <div>
    <span class="eyebrow">{e(about["eyebrow"])}</span>
    <h2>{e(about["heading"])}</h2>
    {paras_html()}
    <div class="creds">{creds_html()}</div>
    {roles_p}
  </div>
  <div class="edu"><h3>Education &amp; Qualifications</h3>{edu_html()}{edu_note_html}</div>
</div></section>

<section class="section" id="honours" style="background:var(--bg2)"><div class="wrap">
  <div class="center">
  <span class="eyebrow">{e(honours["eyebrow"])}</span>
  <h2>{e(honours["heading"])}</h2>
  {('<p class="lead">'+e(honours["lead"])+'</p>') if honours.get("lead") else ''}
  </div>
  <div class="cards">{honour_cards()}</div>
</div></section>

<section class="section" id="awards"><div class="wrap center">
  <span class="eyebrow">{e(awards["eyebrow"])}</span>
  <h2>{e(awards["heading"])}</h2>
  <p class="lead">{e(awards["lead"])}</p>
  <div class="awards-spot">{award_cards()}</div>
</div></section>

<section class="section onstage" id="onstage" style="background:var(--bg2)"><div class="wrap center">
  <span class="eyebrow">{e(onstage["eyebrow"])}</span>
  <h2>{e(onstage["heading"])}</h2>
  <p class="lead">{e(onstage["lead"])}</p>
</div><div class="marquee-wrap">{onstage_rows()}</div></section>

<section class="section" id="speaking"><div class="wrap center">
  <span class="eyebrow">{e(speaking["eyebrow"])}</span>
  <h2>{e(speaking["heading"])}</h2>
  <div class="pills">{topics_html()}</div>
  <div class="regions" style="text-align:left">{regions_html()}</div>
  {speak_gal}
</div></section>

<section class="section" id="media" style="background:var(--bg2)"><div class="wrap center">
  <span class="eyebrow">{e(mediasec["eyebrow"])}</span>
  <h2>{e(mediasec["heading"])}</h2>
  <p class="lead">{e(mediasec["lead"])}</p>
  <div class="mediagrid">{media_clip_cards()}</div>
</div></section>

<section class="section" id="interviews"><div class="wrap center">
  <span class="eyebrow">{e(interviews["eyebrow"])}</span>
  <h2>{e(interviews["heading"])}</h2>
  <p class="lead">{e(interviews["lead"])}</p>
  <div class="videos">{interviews_html()}</div>
</div></section>

<section class="section" id="learn" style="background:var(--bg2)"><div class="wrap center">
  <span class="eyebrow">{e(blog["eyebrow"])}</span>
  <h2>{e(blog["heading"])}</h2>
  <p class="lead">{e(blog["lead"])}</p>
  <div class="vcarousel">
    <button class="vnav prev" type="button" aria-label="Previous">‹</button>
    <div class="videos portrait vtrack">{blog_html()}</div>
    <button class="vnav next" type="button" aria-label="Next">›</button>
  </div>
</div></section>

<section class="section" id="howto"><div class="wrap center">
  <span class="eyebrow">{e(howto["eyebrow"])}</span>
  <h2>{e(howto["heading"])}</h2>
  <p class="lead">{e(howto["lead"])}</p>
  <div class="vcarousel">
    <button class="vnav prev" type="button" aria-label="Previous">‹</button>
    <div class="videos portrait vtrack">{howto_html()}</div>
    <button class="vnav next" type="button" aria-label="Next">›</button>
  </div>
</div></section>

<section class="section{test_hidden}" id="testimonials"><div class="wrap center">
  <span class="eyebrow">{e(testi["eyebrow"])}</span>
  <h2>{e(testi["heading"])}</h2>
  <div class="tgrid">{testimonials_html()}</div>
</div></section>

<section class="section" id="books" style="background:var(--bg2)"><div class="wrap">
  <div class="center">
  <span class="eyebrow">{e(books["eyebrow"])}</span>
  <h2>{e(books["heading"])}</h2>
  </div>
  <div class="mai">
    <div class="cover"><img src="/assets/mai_cover.jpg" alt="MAI — a graphic novel by Sriram Jagannathan"></div>
    <div><h3>{e(books["mai_title"])}</h3><p>{e(books["mai_desc"])}</p>
      <div class="links">{mai_links_html()}</div></div>
  </div>
  {('<div class="books">'+books_html()+'</div>') if books["items"] else ''}
</div></section>

<section class="section connect" id="connect"><div class="wrap">
  <span class="eyebrow">{e(connect["eyebrow"])}</span>
  <h2>{e(connect["heading"])}</h2>
  <p class="lead">{e(connect["lead"])}</p>
  <div class="social">{social_html()}</div>
  <form class="form-card" name="enquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="enquiry">
    <p class="is-hidden"><label>Leave this empty: <input name="bot-field"></label></p>
    <label for="f-name">Name</label>
    <input id="f-name" name="Name" type="text" placeholder="Your name" required>
    <label for="f-email">Email</label>
    <input id="f-email" name="Email" type="email" placeholder="you@example.com" required>
    <label for="f-msg">Message</label>
    <textarea id="f-msg" name="Message" placeholder="Tell us about your event, date and audience…"></textarea>
    <button class="btn btn-primary" type="submit">Send enquiry</button>
    <a class="btn btn-ghost is-hidden" id="kit" href="assets/speaker-kit.pdf" download style="margin-top:12px;width:100%;justify-content:center">Download speaker kit (PDF)</a>
  </form>
</div></section>

<footer>{site["footer_html"]}</footer>
{FRONT_JS}
{IDENTITY}
</body></html>'''

def _ver(m):
    path = m.group(2); fp = os.path.join(HERE, path.lstrip("/"))
    if os.path.exists(fp):
        h = hashlib.md5(open(fp, "rb").read()).hexdigest()[:8]
        return '%s="%s?v=%s"' % (m.group(1), path, h)
    return m.group(0)
HTML = re.sub(r'(src|href)="(/assets/[^"?]+)"', _ver, HTML)

open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(HTML)
print("Built index.html |", n_press, "press links |", len(mediasec["items"]), "media tiles |",
      len(awards["items"]), "awards |", len(testi["items"]), "testimonials")
