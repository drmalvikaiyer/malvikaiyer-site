# Going live with malvikaiyer.com — step by step

This puts your new site online **for free**, points your existing domain at it, and
lets you cancel the ₹2,832/year WordPress plan. Your domain stays at name.com.

You will need two free accounts: **GitHub** (stores the site) and **Netlify** (hosts it).
Using GitHub is what makes the visual editor work later — so please use this path.

Estimated time: ~30–40 minutes. Nothing here can break your current site until the
very last DNS step, so take your time.

---

## STEP 1 — Put the site on GitHub (stores your files)

1. Create a free account at **https://github.com** (skip if you have one).
2. Click the **+** (top right) → **New repository**.
   - Repository name: `malvikaiyer-site`
   - Keep it **Public**, click **Create repository**.
3. On the new repo page, click **“uploading an existing file”**.
4. Open the folder `C:\Users\ganap\Downloads\malvikaiyer-site`, select **everything
   inside it** (index.html, styles.css, app.js, netlify.toml, the `assets`, `admin`
   and `content` folders) and **drag it all** into the GitHub upload box. Wait for the
   files to finish (the images take a minute).
5. Click **Commit changes**.

> ✅ Your site now lives in a GitHub repository.

---

## STEP 2 — Host it on Netlify (free, instant)

1. Go to **https://app.netlify.com** → **Sign up** → choose **“Sign up with GitHub.”**
2. Click **Add new site → Import an existing project → Deploy with GitHub**.
3. Authorise Netlify, then pick the **`malvikaiyer-site`** repository.
4. The build settings fill in **automatically** (from the included `netlify.toml`):
   build command `python3 build.py`, publish directory `.`. Just leave them as shown
   and click **Deploy**. *(This build step is what lets you edit everything in the
   visual editor — Netlify re-runs it automatically each time you publish a change.)*
5. After ~1 minute you get a live preview link like `https://random-name-1234.netlify.app`.
   **Open it — your site is live on the internet.** 🎉

> Optional but recommended: Site configuration → **Change site name** to something
> like `malvika-iyer` so the temporary address is tidier.

---

## STEP 3 — Turn on the enquiry form notifications

Your contact form already works through Netlify (no code needed).
1. In Netlify: **Site configuration → Forms → Form notifications**.
2. **Add notification → Email notification** → enter `drmalvikaiyer@gmail.com`.

Now every enquiry from the site lands in your inbox automatically.

---

## STEP 4 — Connect your domain (malvikaiyer.com)

In Netlify: **Domain management → Add a domain** → type `malvikaiyer.com` → **Verify → Add**.
Netlify will then show you the DNS settings to enter at name.com. Use **one** of these:

### Option A (recommended, simplest): let Netlify manage DNS
1. Netlify will offer **“Set up Netlify DNS”** and show you **4 nameservers**, like:
   `dns1.p01.nsone.net`, `dns2.p01.nsone.net`, `dns3.p01.nsone.net`, `dns4.p01.nsone.net`
   *(yours will differ — copy the exact 4 Netlify shows you).*
2. Log in to **https://www.name.com** → **My Domains → malvikaiyer.com → Nameservers**.
3. Replace the existing nameservers with the **4 from Netlify** → **Save / Apply**.

### Option B: keep DNS at name.com (use records instead)
At name.com → **malvikaiyer.com → DNS Records**, add:
| Type  | Host (Name) | Value / Answer            |
|-------|-------------|---------------------------|
| A     | `@`         | `75.2.60.5`               |
| CNAME | `www`       | `<your-site>.netlify.app` |

*(Netlify confirms the exact A-record IP in its dashboard — use whatever it displays.)*

### Then
- DNS changes take anywhere from a few minutes to a few hours to take effect.
- Back in Netlify, once it verifies the domain, click **“Verify DNS / Provision
  certificate.”** Netlify gives you **free HTTPS** automatically.
- Visit **https://malvikaiyer.com** — it now shows your new site. 🎉

---

## STEP 5 — Cancel the WordPress plan (save ₹2,832/year)

Do this **only after** Step 4 works and https://malvikaiyer.com shows the new site.

1. Go to **https://wordpress.com** → log in.
2. **Upgrades → Plans** (or **Me → Purchases**).
3. Select your plan → **Cancel plan / Turn off auto-renew**.

Notes:
- Your **domain is at name.com, not WordPress**, so cancelling does **not** affect it.
- All your old content is already rebuilt into the new site — nothing is lost.
- If you cancelled within WordPress’s refund window you may even get money back.

---

## You’re done 🎉
- New site: free hosting on Netlify
- Domain: still name.com (~₹1,871/year — the only bill you keep)
- Saved: ₹2,832/year
- Next: set up the visual editor — see **EDITING.md**.
