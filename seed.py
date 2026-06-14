# -*- coding: utf-8 -*-
"""ONE-TIME local seeder. Reads manifest.json + media_data.json and writes the full
set of editable content/*.json files. Run locally once; not used by Netlify.
After this, build.py renders the site purely from content/*.json."""
import json, os, re
from urllib.parse import urlparse

HERE=os.path.dirname(os.path.abspath(__file__))
SRC=r"C:\Users\ganap\Downloads\mi_build"
CONTENT=os.path.join(HERE,"content"); os.makedirs(CONTENT,exist_ok=True)
recs=json.load(open(os.path.join(SRC,"manifest.json"),encoding="utf-8"))
media=json.load(open(os.path.join(SRC,"media_data.json"),encoding="utf-8"))
by_file={r["file"]:r for r in recs}
icons=[r for r in recs if r["px_w"]==512 and r["px_h"]==512 and r["url"]]
def on(n): return [r for r in recs if n in r["rslides"] and r not in icons]
def Ap(f): return "/assets/"+f
def url_of(f): return by_file[f]["url"]
G1=[r["file"] for r in on(3)]; G2=[r["file"] for r in on(4)]
G4=[r["file"] for r in on(5)]; G3=[r["file"] for r in on(6)]
COVER="img_00.jpg"
ports=[r["file"] for r in recs if r["aspect"] and r["aspect"]<0.95 and r["file"]!=COVER]
STORY_IMG=ports[0] if ports else "img_01.jpg"

DOMLABEL={"youtube.com":"Watch on YouTube","youtu.be":"Watch on YouTube","twitter.com":"Post on X / Twitter",
 "x.com":"Post on X / Twitter","facebook.com":"Facebook feature","instagram.com":"Instagram post",
 "issuu.com":"Read on Issuu","podcasts.apple.com":"Listen · Apple Podcasts"}
def title_from(url):
    p=urlparse(url); dom=p.netloc.replace("www.","")
    if dom in DOMLABEL: return DOMLABEL[dom]
    if p.path.lower().endswith((".jpg",".jpeg",".png",".pdf")): return "Press clipping"
    segs=[s for s in p.path.split("/") if s]
    if not segs: return dom
    slug=re.sub(r"\.(html?|cms|vpf|php|aspx)$","",segs[-1]); slug=re.sub(r"[?#].*$","",slug)
    slug=re.sub(r"-?\d{4,}.*$","",slug).replace("-"," ").replace("_"," ").replace("%20"," ").strip()
    slug=re.sub(r"\s+"," ",slug)
    return dom if (len(slug)<4 or slug.isdigit()) else slug[:1].upper()+slug[1:]
def clean_outlet(s):
    s=s.replace("�","'").replace("�","'").strip()
    return " ".join(w if (w.isupper() and len(w)>3) else w.title() for w in s.split()) if s.isupper() else s.title()

PM_TWEET="https://x.com/narendramodi/status/1236524595081097216?s=20"
UN_LINK="https://www.unwomen.org/en/news/stories/2017/6/from-where-i-stand--malvika-iyer"

site={"title":"Dr. Malvika Iyer — Speaker · Activist · Changemaker",
 "description":"Dr. Malvika Iyer — bomb-blast survivor, disability-rights activist, Doctorate in Social Work and internationally acclaimed motivational speaker.",
 "brand_first":"Dr. Malvika ","brand_last":"Iyer",
 "nav":[{"label":"Story","href":"#story","cta":False},{"label":"Honours","href":"#honours","cta":False},
        {"label":"Speaking","href":"#speaking","cta":False},{"label":"Watch","href":"#watch","cta":False},
        {"label":"Media","href":"#media","cta":False},{"label":"Books","href":"#books","cta":False},
        {"label":"Connect","href":"#connect","cta":True}],
 "footer_html":"© Dr. <b>Malvika Iyer</b> · Speaker · Activist · Changemaker · <b>malvikaiyer.com</b>"}

hero={"eyebrow":"Speaker · Activist · Changemaker","name":"Dr. Malvika Iyer",
 "sub_pre":"Disability-Rights Activist · Doctorate in Social Work · ","sub_bold":"Motivational Speaker",
 "btn1_label":"Book / Connect","btn1_href":"#connect","btn2_label":"Watch her talks","btn2_href":"#watch",
 "ribbon":"Bomb-blast survivor at 13 — now a national-award-winning global voice.","photo":Ap(COVER)}

stats={"items":[{"num":"15+","label":"Countries"},{"num":"300+","label":"Features"},
 {"num":"100M+","label":"Views"},{"num":"8+","label":"Years Speaking"},{"num":"97%","label":"Class-10 Topper"}]}

about={"eyebrow":"The Story","heading":"From survivor to global voice",
 "paragraphs":[
  "At just 13, Malvika survived a devastating bomb blast — losing both hands and suffering severe leg damage, nerve paralysis and loss of sensation. Bedridden for two years, she refused the label of victim, rebuilt body and spirit, and with three months of preparation topped her Class 10 board exams at 97%.",
  "Today she is a leading voice of the global inclusion movement: an award-winning disability-rights activist, a Doctorate in Social Work and an internationally acclaimed motivational speaker — also a TEDx speaker, corporate trainer, MC and inclusive-fashion model. With 8+ years of speaking, she advocates for disability rights, gender equality, mental health, child rights, universal design and accessibility."],
 "credentials":["Disability-Rights Activist","Doctorate in Social Work","Nari Shakti Puraskar Awardee",
  "International Motivational Speaker","TEDx Speaker","Corporate Trainer","Accessible-Fashion Model","MC / Host",
  "WEF Global Shaper","Advisory Board · India Inclusion Foundation"],
 "education":[{"degree":"Ph.D. in Social Work","place":"Madras School of Social Work"},
  {"degree":"M.Phil., Social Work","place":"Madras School of Social Work"},
  {"degree":"Master's in Social Work","place":"Delhi School of Social Work"},
  {"degree":"B.A. Economics","place":"St. Stephen's College, Delhi"},
  {"degree":"UGC–NET","place":"Junior Research Fellowship & Lectureship eligibility"}],
 "roles_html":"<b>Global roles:</b> Global Shaper at the World Economic Forum's Global Shapers Community · Advisory Board, India Inclusion Foundation · featured among <b>100 Change Agents &amp; Newsmakers of the Decade</b>."}

honours={"eyebrow":"Defining Moments","heading":"Honours that made history",
 "items":[{"title":"Nari Shakti Puraskar","description":"India's highest civilian honour for women's empowerment, conferred by the President of India.","link":""},
  {"title":"Address at the United Nations, NY","description":"A motivational keynote at UN Headquarters that drew a standing ovation.","link":UN_LINK},
  {"title":"Honoured by Dr. A. P. J. Abdul Kalam","description":"Personally recognised by the late President of India.","link":""},
  {"title":"Took over the PM's social media","description":"Chosen as a Woman Achiever to take over the Prime Minister's accounts on Women's Day.","link":PM_TWEET},
  {"title":"Chair, WEF – India Economic Summit","description":"Co-chaired alongside Union Cabinet Ministers and global business leaders.","link":""},
  {"title":"Invited speaker at The World Bank","description":"Addressed the International Day of Persons with Disabilities.","link":""},
  {"title":"Showstopper, Fashion Week Chennai","description":"Championing inclusive fashion on the runway.","link":""}],
 "gallery":[Ap(f) for f in G1]}

awards={"eyebrow":"Awards & Recognition","heading":"Celebrated across the world",
 "lead":"National and international honours for women's empowerment, disability advocacy and social impact — across more than 15 countries.",
 "items":[{"name":"Women in the World – Emerging Leaders","org":"First-ever recipient · The New York Times"},
  {"name":"Outstanding Disability Advocacy Award","org":"Presented by Gautam Adani, Adani Group"},
  {"name":"Diversity Impact 50 Award","org":"Detroit, USA"},
  {"name":"Global Inspiration & Social Impact","org":"Zero Women Honours"},
  {"name":"The She-Age Award","org":"The Hindustan Times"},
  {"name":"Young Achiever Award","org":"NAPSW, India"},
  {"name":"Spirit of Resilience – Sabal Changemaker","org":"Tata Steel Foundation"},
  {"name":"“The Conquistador”","org":"Crimson Women Champions of Change"},
  {"name":"Inspiring Young Changemaker Award","org":"CSR Journal Excellence Awards"}],
 "gallery":[Ap(f) for f in G2]}

speaking={"eyebrow":"Speaking & Global Reach","heading":"On stages in 15+ countries",
 "topics":[{"name":t} for t in ["Resilience","Breaking Barriers","Growth Mindset","Positive Self-Talk","Body Positivity",
  "Overcoming Adversity","Inclusion","Gender Equality","Mental Health","Child Rights","Universal Design","Accessibility"]],
 "regions":[
  {"name":"North America","wide":False,"organisations":"United Nations HQ · World Bank · Ford Motor Company · Austin Inclusion Summit (Applied Materials) · Pacific Northwest National Laboratory (US Dept. of Energy) · Boston Scientific · Phillips 66 · Bentley Systems · Zscaler · Marvell Semiconductor · Macy's · Reliability First · Paramount Software · Inner Science Institute · WE Canada"},
  {"name":"S-E, East & West Asia","wide":False,"organisations":"Tsangs Group (Hong Kong) · ICAI (Abu Dhabi, Bahrain, Doha, Muscat) · Indian Business & Professional Council (Dubai) · Critical River · Transworld · Global Leader Series for Non-Profits (Singapore) · Regional Dialogue on Accessible Elections (Indonesia) · Indian School Al Wadi Al Kabir (Muscat) · GEMS NM School (Dubai)"},
  {"name":"Europe & Africa","wide":False,"organisations":"Unilever (UK) · The Royal Marsden NHS Foundation Trust (UK) · Reckitt Benckiser (Netherlands) · CIVICUS World Assembly (South Africa) · Sustainable Valley Festival (Norway) · Quantum Way Summit (France) · Africa Women Innovation & Entrepreneurship Forum"},
  {"name":"Conferences & Forums","wide":False,"organisations":"World Economic Forum India Economic Summit · Youth Assembly, NYU · UN India & NITI Aayog Women Entrepreneurship Program · IEEE WIE International Leadership Summit · The New Indian Express ThinkEdu Conclave · TEDxIIMKozhikode · TEDxYouthChennai · Mathrubhumi International Festival of Letters · South India's Iconic Women Summit"},
  {"name":"South Asia (India)","wide":True,"organisations":"Microsoft · IBM · Shell · General Electric · Citi · PayPal · Atlassian · ByteDance · Volvo · John Deere · Bosch · Nokia · Morgan Stanley · Tesco · Diageo · Novo Nordisk · Target · Capgemini · Freshworks · Societe Generale · AXA · HPE Aruba · General Mills · Sandvik · Technicolor · Flex · CGI · VFS Global · Aristocrat · Suez · Amagi · Avantor · Aptiv · Indian Oil · Aditya Birla Capital · Bharat Electricals · United Breweries · J K Cements · SBI Insurance · CII · NASSCOM · Myntra · Gujarat Fluorochemicals · Valtech · Celegence · Mann+Hummel · CloudiX · IIRIS · Neewee Analytics · Harnessio R&D · Inflobox · Ask Circle · Construction Specialists · Unifeeder · PMI Chennai · Gerson Lehrman Group · RTI International · Mahindra University · Amrita Vishwa Vidyapeetham · The Shri Ram Schools · The Emerald Heights International School · Learning Matters"}],
 "gallery":[Ap(f) for f in G4]}

vids=[("VTViAugjjRg","TEDxIIMKozhikode","The only disability in life is a bad attitude"),
 ("9el_A5O9ZQI","TEDxYouth@Chennai","Inclusion starts from within"),
 ("-6kvVaiknpA","World Economic Forum","A bilateral amputee offers a lesson on resilience"),
 ("TB7wM8wwT1Q","DD India","In conversation: speaker & disability-rights activist"),
 ("ZqB7sGHqGUw","Govt. of India","PM Narendra Modi calls her a 'Phenomenal Woman'"),
 ("UkCWSds5fKY","Economic Times","Rise With India — a story to take inspiration from")]
videos={"eyebrow":"Watch","heading":"Talks, keynotes & conversations",
 "lead":"From TED stages to the United Nations and the World Economic Forum.",
 "items":[{"youtube_id":v,"source":s,"title":t,"url":"","thumb":""} for v,s,t in vids]
  +[{"youtube_id":"","source":"United Nations · CSW61","title":"Closing session — Launch of CEDAW for Youth",
     "url":"http://webtv.un.org/watch/closing-session-launch-of-cedaw-for-youth-youth-forum-csw-61/5356414875001",
     "thumb":"https://img.youtube.com/vi/-6kvVaiknpA/hqdefault.jpg"}]}

mediasec={"eyebrow":"In the Media","heading":"300+ features & 100M+ views",
 "lead":"Featured worldwide — from the United Nations and The Hindu to NDTV, Femina and Republic. Tap any clipping to read the original.",
 "items":[{"image":Ap(f),"url":url_of(f)} for f in G3]}

outlets=[]
for sec,items in media.items():
    lk=[]
    for it in items:
        t=it["title"]
        if not t or t in ("(link)","(intro)"): t=title_from(it["url"])
        lk.append({"title":t,"url":it["url"]})
    outlets.append({"name":clean_outlet(sec),"links":lk})
press={"eyebrow":"Complete Press Archive","heading":"As featured in",
 "lead":"Every story from the original site, grouped by outlet — across global & regional press, television, books and magazines.",
 "outlets":outlets}

books={"eyebrow":"Books & the MAI Graphic Novel","heading":"Her story, in print",
 "mai_title":"“MAI” — the graphic novel",
 "mai_desc":"Artist Sriram's graphic novel retells Malvika's journey from the blast to the global stage — a story of grit, reinvention and unstoppable spirit.",
 "mai_links":[{"label":"Read the story — Scroll","url":"https://scroll.in/article/885884/at-13-years-old-malvika-iyer-lost-both-her-hands-in-an-accident-a-graphic-novel-tells-her-story"},
  {"label":"The News Minute","url":"https://www.thenewsminute.com/article/srirams-graphic-novel-mai-tells-story-bomb-blast-survivor-88175"},
  {"label":"Why you need to read MAI — EdexLive","url":"https://www.edexlive.com/beinspired/2018/sep/01/why-you-need-to-read-graphic-novel-mai-to-really-understand-malvika-iyers-story-3854.html"}],
 "items":[{"title":"Girl Power: Indian Women Who Broke the Rules","note":"Featured profile","url":"https://www.amazon.in/Girl-Power-Indian-Women-Broke/dp/9352759869"},
  {"title":"GIFTED: Inspiring Stories of People with Disabilities","note":"National bestseller","url":"https://www.amazon.com/Gifted-Inspiring-Stories-People-Disabilities/dp/8184005458"},
  {"title":"Women of Pure Wonder","note":"Vodafone Foundation","url":"https://www.amazon.in/Women-Pure-Wonder-Vision-Victory/dp/9351941639"}]}

blog={"eyebrow":"Watch & Learn","heading":"Lessons from the blog",
 "lead":"Short, practical talks where Malvika turns her experience into tools you can use.",
 "items":[{"youtube_id":"0KoGXxaicdQ","title":"Fixed Mindset vs Growth Mindset"},
  {"youtube_id":"66zn092rcGc","title":"How to become & stay motivated"},
  {"youtube_id":"LkwTWk7laJQ","title":"How to accept oneself"}]}

testimonials={"eyebrow":"What people say","heading":"Testimonials","items":[]}

connect={"eyebrow":"Let's Connect","heading":"Bring this story to your stage",
 "lead":"For keynotes, panels, workshops and collaborations — reach out across any channel.",
 "form_email":"drmalvikaiyer@gmail.com",
 "social":[{"label":"Website","url":"https://malvikaiyer.com/","icon":Ap("img_46.png")},
  {"label":"Instagram","url":"https://www.instagram.com/malvika.iyer/","icon":Ap("img_47.png")},
  {"label":"LinkedIn","url":"https://www.linkedin.com/in/drmalvikaiyer/","icon":Ap("img_48.png")},
  {"label":"X / Twitter","url":"https://x.com/malvikaiyer","icon":Ap("img_49.png")},
  {"label":"Google","url":"https://share.google/ptlNX6ZUBbarv43xF","icon":Ap("img_50.png")},
  {"label":"Email","url":"mailto:drmalvikaiyer@gmail.com","icon":Ap("img_51.png")}]}

ALL={"site":site,"hero":hero,"stats":stats,"about":about,"honours":honours,"awards":awards,
 "speaking":speaking,"videos":videos,"media":mediasec,"press":press,"books":books,
 "blog":blog,"testimonials":testimonials,"connect":connect}
for name,obj in ALL.items():
    json.dump(obj,open(os.path.join(CONTENT,name+".json"),"w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("Seeded",len(ALL),"content files into",CONTENT)
