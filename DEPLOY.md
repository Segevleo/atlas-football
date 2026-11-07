# ATLAS Cloudflare Pages deployment

1. Sign in to https://dash.cloudflare.com/.
2. Workers & Pages → Create application → Pages → Connect to Git.
3. Authorize GitHub, choose `Segevleo/atlas-football`, production branch `main`.
4. Framework preset: **None**. Build command: **leave empty**. Build output directory: **/** (repository root).
5. Deploy. Cloudflare will provide a unique `*.pages.dev` URL.
6. In GitHub → Actions, verify `ATLAS hourly news refresh` can run; use **Run workflow** for the first refresh.
7. GitHub → Settings → Actions → General → Workflow permissions: allow **Read and write permissions** if your repository settings otherwise prevent the bot from committing.
8. Cloudflare should rebuild on GitHub commits. Verify a successful build after the first snapshot commit.

## Accuracy and scope
The website currently contains a small **candidate** league directory, not complete global coverage. No league is marked verified. News RSS is attempted hourly; this is not a real-time match-score feed. Respect source licensing and robots/terms before adding match ingestion.
