# Editing your site in the browser (no code)

Your site comes with a free visual editor (Decap CMS) at **malvikaiyer.com/admin**.
You log in, change text/images, click **Publish**, and the live site updates in about a
minute. Set this up once after the site is live (see DEPLOY.md first).

---

## One-time setup (~5 minutes, in Netlify)

1. In Netlify: **Site configuration → Identity → Enable Identity.**
2. Under **Identity → Registration**, set it to **“Invite only.”**
   *(So only you can log in.)*
3. Under **Identity → Services → Git Gateway**, click **Enable Git Gateway.**
4. Go to the **Identity** tab → **Invite users** → enter your email
   (`drmalvikaiyer@gmail.com`) → **Send.**
5. Check your inbox → click **Accept the invite** → set a password.

That’s it. You won’t need to do this again.

---

## How to edit, any time

1. Go to **https://malvikaiyer.com/admin/**
2. Log in with your email + password.
3. Pick a section in the left menu. **Every part of the site is editable:**
   - **Site & Navigation** — page title, SEO description, brand name, top menu, footer.
   - **Hero (top banner)** — your name, taglines, buttons, and the main photo.
   - **Stats band** — the five numbers (15+, 300+, …).
   - **Story / About** — bio paragraphs, credential tags, education list, global roles.
   - **Honours (Defining Moments)** — the numbered honour cards + photo gallery.
   - **Awards & Recognition** — add a new award anytime (name + who gave it) + photos.
   - **Speaking (topics & engagements)** — topic pills, and engagements by region
     (open a region and add the organisation; separate names with ` · `).
   - **Watch (videos)** — featured talks. Paste just the YouTube **video ID** (the bit
     after `watch?v=` — e.g. `VTViAugjjRg`), or a full URL for non-YouTube.
   - **In the Media (clippings)** — the image tiles + their article links.
   - **Press archive (by outlet)** — every outlet and article link.
   - **Books & MAI novel** — the MAI panel and book cards.
   - **Watch & Learn (blog)** — your blog videos.
   - **Testimonials** — quotes from organisers/audiences. *(This section stays hidden
     until you add your first quote, then appears automatically.)*
   - **Connect** — intro text, the enquiry email, and your social links/icons.
4. Make your changes → click **Publish**.
5. Wait ~1 minute (the site rebuilds itself automatically), then refresh. Done.

> **Photos:** anywhere you see an image field, click it to upload a new picture —
> it's saved into the site automatically.

### Example: adding a new award
1. Go to **/admin** → **Awards & Recognition**.
2. Click **Add Award** (the **+** at the bottom of the list).
3. Type the **Award name** and **who gave it / detail** → **Publish**.
4. A minute later it appears in the "Celebrated across the world" grid. That's it —
   no code, no me.

> Adding images (e.g. in future sections): use the image button in the editor — files
> are saved into the site’s `assets` folder automatically.

---

## What you can edit yourself

**Everything** — every section, all text, all links, and all photos are in the visual
editor. When you publish a change, the site automatically rebuilds itself in about a
minute (no code, and your Google ranking and page speed stay perfect).

The only things not in the editor are the colours/layout design itself — for those,
just ask me.

---

## Adding your speaker-kit PDF (when ready)

1. Put your PDF in the `assets` folder named `speaker-kit.pdf` (upload it to GitHub the
   same way as in DEPLOY.md, or drag it into the repo’s `assets` folder on GitHub).
2. In `index.html`, find `id="kit"` and delete the words `is-hidden` from that line.
3. Commit — the **“Download speaker kit (PDF)”** button appears on the site.

*(Ask me and I’ll do this for you in seconds.)*
