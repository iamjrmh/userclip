# userclip.lol

The website for [userclip](https://github.com/JURMR/userclip): a landing page,
a privacy policy, and terms of service.

Static HTML and CSS with no build step, no dependencies, and no external
requests. Push it and GitHub Pages serves it.

## Why it has no dependencies

The product's entire argument is that it processes your video locally and sends
nothing anywhere. A site making that claim while loading fonts from Google, or
running an analytics script, would undercut it on the first page load. So:

- Inter is served from `/assets/inter.ttf`, not from a CDN.
- Icons are inline SVG or drawn in CSS.
- No analytics, no tag manager, no cookies, no third party anything.

## Structure

```
index.html          the landing page, served at userclip.lol
privacy/index.html  served at userclip.lol/privacy
terms/index.html    served at userclip.lol/terms
styles.css          one stylesheet for all three
assets/             the typeface and real screenshots of the app
CNAME               the custom domain, read by GitHub Pages
.nojekyll           stops Pages running Jekyll over the files
check.py            the no em dash lint, shared with the app repository
```

Pages live in directories rather than as `privacy.html`, which is what makes the
published URLs extension free.

**Asset paths are root absolute** (`/styles.css`, `/assets/...`) because a
relative path resolves against `/privacy/` on the subpages. That works because
the site is served from a domain root. If it were ever hosted under
`username.github.io/repo`, every one of those paths would need the repo prefix.

## Publishing

1. Push this folder to a GitHub repository.
2. Settings, Pages, deploy from the `main` branch, root folder.
3. Settings, Pages, Custom domain: `userclip.lol`. The `CNAME` file already
   holds it, so this should already be filled in.
4. At your registrar, point the domain at GitHub:

   | Type | Name | Value |
   |---|---|---|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `<your-username>.github.io` |

5. Wait for the DNS check to pass, then tick **Enforce HTTPS**. Certificate
   issuance takes a few minutes after the domain resolves.

## Working on it locally

```
python -m http.server 8899
```

Then open <http://127.0.0.1:8899>. Use the directory URLs (`/privacy`, not
`/privacy.html`) so what you see matches what gets published.

## House rules

**No em dashes anywhere**, matching the application. Run the lint before
pushing:

```
python check.py .
```

Copy from the app repository whenever the two disagree. The privacy policy in
particular describes real behaviour, and it is only worth anything while that
stays true: if the application's network use changes, this changes with it.
