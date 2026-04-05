# Deploy Prompt — Vercel (and Netlify/Cloudflare variants)

Phase 8 of the pipeline. Runs after the SEO pass is complete and user has
approved all metrics.

---

## The Prompt

```
Deploy this site to {{deploy_target}}.

## Pre-deploy Checks

Before deploying:
1. Confirm `npm run build` (or framework equivalent) completes with no errors
2. Confirm there are no uncommitted .env files that should not be committed
   - .env should be in .gitignore
   - .env.example is safe to commit
3. Confirm Lighthouse scores from Phase 7 meet the minimum (Perf+SEO >= 90)
4. Confirm the built HTML contains the meta tags and JSON-LD from Phase 7
5. Confirm `robots.txt`, `sitemap.xml`, `llms.txt` are in the public root

## GitHub First (if deploy target uses Git)

If {{deploy_target}} is Vercel or Netlify with Git integration:

1. Initialize a git repo if not already: `git init`
2. Add .gitignore with Node/framework defaults + .env + .vercel + .netlify
3. Create initial commit: "Initial site build"
4. Ask user for the repo name (default: kebab-case of {{brand_name}})
5. Create a new GitHub repo using `gh repo create {{repo_name}} --private --source=. --push`
6. Confirm push succeeded

## Vercel Path

```
vercel --prod
```

On first run, Vercel CLI will ask for:
- Link to existing project or create new → create new
- Project name → use {{repo_name}}
- Directory → current
- Settings → auto-detect from framework

Result: a production URL (e.g., https://{{repo_name}}.vercel.app).

## Netlify Path

```
netlify deploy --prod --dir={{build_dir}}
```

Where `{{build_dir}}` is the framework's output directory:
- Next.js: `.next` (use Netlify adapter)
- Astro: `dist`
- Vanilla: `.` or `public`

On first run, Netlify CLI will ask for:
- Link to existing site or create new → create new
- Team → user's default
- Site name → use {{repo_name}}

Result: a production URL (e.g., https://{{repo_name}}.netlify.app).

## Cloudflare Pages Path

```
wrangler pages deploy {{build_dir}} --project-name={{repo_name}}
```

Authenticate first with `wrangler login` if needed.

## Post-deploy

1. Verify the live URL loads and the hero animation plays
2. Check that meta tags and JSON-LD are present in the deployed HTML
3. Submit the sitemap to Google Search Console (print the URL for the user)
4. Print the final deploy report:
   - URL: ...
   - Build time: ...
   - Deploy platform: ...
   - Next steps: add custom domain, submit to Search Console, etc.

## Custom Domain (optional)

Ask the user if they have a custom domain to connect. If yes:
- Vercel: `vercel domains add {{domain}}` + show DNS instructions
- Netlify: print the DNS instructions
- Cloudflare: domain is already in Cloudflare, just configure the Pages binding

## Safety Rules

- NEVER force push
- NEVER use --no-verify or skip hooks
- NEVER commit .env files
- ALWAYS confirm with user before creating a new repo
- ALWAYS print the URL at the end so the user can verify
```

---

## Variables

- `{{deploy_target}}` — "vercel" | "netlify" | "cloudflare" | "manual"
- `{{repo_name}}` — generated from brand name (kebab-case)
- `{{build_dir}}` — inferred from framework
- `{{domain}}` — optional custom domain
