# Railway Quick Start - Deploy from Source

**Why from source?** The Docker image (`Dockerfile.single`) is too large for Railway to push. Deploying from source using Nixpacks creates smaller individual services that Railway can handle.

## Architecture: 4 Services

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  SurrealDB  │   │     API     │   │   Worker    │   │  Frontend   │
│  (Template) │   │  (Python)   │   │  (Python)   │   │  (Node.js)  │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

Each service is small enough for Railway (300-500MB vs 2GB+ single image).

---

## Prerequisites

- Railway account (https://railway.app)
- This repository on GitHub (fork or clone)
- OpenAI, Anthropic, or Google API key

---

## Step 1: Create Railway Project

1. Go to https://railway.app/new
2. Click "Empty Project"
3. Name it (e.g., "open-notebook")

---

## Step 2: Deploy SurrealDB

1. Click "+ New" → "Database" → "Add SurrealDB"
2. Railway will automatically create the service
3. Note: Railway generates random credentials - we'll use them later

**Alternative:** Use the Community Template:
- Search "SurrealDB" in templates
- Deploy with default settings

---

## Step 3: Deploy API Service

1. Click "+ New" → "GitHub Repo"
2. Select this repository
3. Configure:

   **Settings → General:**
   - Service name: `api`

   **Settings → Build:**
   - Build Command: (leave empty)
   - Nixpacks Config Path: `nixpacks.api.toml`
   - Watch Paths: `api/**, open_notebook/**, pyproject.toml, uv.lock, config/**`

   **Settings → Deploy:**
   - Start Command: (leave empty - uses nixpacks.api.toml)

4. **Variables** (Settings → Variables):

   ```bash
   # DATABASE - Use Railway's reference variables
   SURREAL_URL=${{SurrealDB.RAILWAY_PRIVATE_DOMAIN}}:8000/rpc
   SURREAL_USER=${{SurrealDB.SURREAL_USER}}
   SURREAL_PASSWORD=${{SurrealDB.SURREAL_PASS}}
   SURREAL_NAMESPACE=open_notebook
   SURREAL_DATABASE=open_notebook

   # AI PROVIDER (choose one - more in config/railway_config.py)
   OPENAI_API_KEY=sk-...

   # OPTIONAL: Hebrew text optimization (already in railway_config.py)
   # OPEN_NOTEBOOK_CHUNK_SIZE=1000
   # OPEN_NOTEBOOK_CHUNK_OVERLAP=150
   ```

5. Click "Deploy"

---

## Step 4: Deploy Worker Service

1. Click "+ New" → "GitHub Repo"
2. Select this repository
3. Configure:

   **Settings → General:**
   - Service name: `worker`

   **Settings → Build:**
   - Nixpacks Config Path: `nixpacks.worker.toml`
   - Watch Paths: `open_notebook/**, commands/**, pyproject.toml, uv.lock, config/**`

4. **Variables:**
   - **Copy ALL variables from API service**
   - The worker needs identical database and AI provider settings

5. Click "Deploy"

---

## Step 5: Deploy Frontend Service

1. Click "+ New" → "GitHub Repo"
2. Select this repository
3. Configure:

   **Settings → General:**
   - Service name: `frontend`

   **Settings → Build:**
   - Nixpacks Config Path: `nixpacks.frontend.toml`
   - Watch Paths: `frontend/**`

4. **Variables:**

   ```bash
   # API URLs - Use Railway service references
   INTERNAL_API_URL=http://${{api.RAILWAY_PRIVATE_DOMAIN}}:${{api.PORT}}
   API_URL=https://${{api.RAILWAY_PUBLIC_DOMAIN}}

   # Next.js config
   NODE_ENV=production
   HOSTNAME=0.0.0.0
   ```

5. Click "Deploy"

---

## Step 6: Generate Public Domains

1. **API Service:**
   - Settings → Networking → "Generate Domain"
   - Copy the URL (e.g., `api-production-abc.up.railway.app`)
   - Update Frontend's `API_URL` variable to `https://[api-domain]`

2. **Frontend Service:**
   - Settings → Networking → "Generate Domain"
   - Copy the URL - **this is your app URL**

---

## Step 7: Access Your App

Visit the frontend URL from Step 6. You should see the Open Notebook interface!

**First time setup:**
1. Settings → Configure your AI model
2. Create a notebook
3. Add sources (PDFs, web pages, etc.)

---

## Troubleshooting

### API won't start - "Database connection failed"

**Check:**
1. SurrealDB service is running (green)
2. `SURREAL_URL` format: `ws://[service-name].railway.internal:8000/rpc`
3. Credentials match SurrealDB service

**Fix:** In API variables, update to:
```bash
SURREAL_URL=ws://${{SurrealDB.RAILWAY_PRIVATE_DOMAIN}}:8000/rpc
```

### Frontend can't reach API

**Check:**
1. API has public domain generated
2. Frontend's `API_URL` matches API's public domain
3. Frontend's `INTERNAL_API_URL` uses private networking

### Build fails - "uv: command not found"

**Fix:** The Nixpacks config should install uv. Check:
- `nixpacks.api.toml` or `nixpacks.worker.toml` exists
- Build → Nixpacks Config Path is set correctly

### Worker not processing jobs

**Check:**
1. Worker has **same variables** as API (database + AI keys)
2. Worker logs show "Connected to database"

---

## Cost Estimate

Railway Hobby Plan ($5/month):
- 4 services × ~500MB RAM each = ~2GB total
- ~10-20 GB data transfer/month
- Stays within Hobby limits for small-medium usage

**Optimization tips:**
- Use Groq (free tier) for cheaper inference
- Use cheaper embedding models (text-embedding-3-small)
- Monitor usage in Railway dashboard

---

## What's in `config/railway_config.py`?

The API automatically loads default values from this file:
- Database connection defaults
- Hebrew text optimization (smaller chunks)
- Timeout settings
- AI provider placeholders

**Railway environment variables override these defaults**, so you can:
1. Deploy quickly with hardcoded values (edit the file)
2. OR set everything via Railway variables (recommended for production)

---

## Next Steps

- **Add more AI providers:** See `.env.example` for all options
- **Enable password protection:** Set `OPEN_NOTEBOOK_PASSWORD` variable
- **Custom domain:** Railway Settings → Networking → Custom Domain
- **Monitoring:** Railway automatically provides logs and metrics

---

## Need Help?

- **Railway fails to build?** Check service logs in Railway dashboard
- **Database issues?** Verify SurrealDB service is running and credentials match
- **General questions?** See full guide: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- **Discord:** https://discord.gg/37XJPXfz2w

---

**Last Updated:** February 2025
**Tested on:** Railway Hobby Plan
