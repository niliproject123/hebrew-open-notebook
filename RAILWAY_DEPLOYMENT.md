# Railway Deployment Guide - Source Code Deployment

This guide walks you through deploying Open Notebook to Railway using source code (not Docker images).

## Architecture Overview

Open Notebook requires **4 services** on Railway:

1. **SurrealDB** - Graph database with vector search
2. **API** - FastAPI backend (Python)
3. **Worker** - Background job processor (Python)
4. **Frontend** - Next.js web application (Node.js)

## Prerequisites

- Railway account (https://railway.app)
- GitHub account with this repository
- API keys for at least one AI provider (OpenAI, Anthropic, Google, etc.)

---

## Step 1: Create a New Railway Project

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your fork/clone of this repository
4. Railway will create a project - **don't deploy yet**, we need to configure services first

---

## Step 2: Deploy SurrealDB Service

### Option A: Use Railway Template (Recommended)

1. In your Railway project, click "+ New Service"
2. Search for "SurrealDB" in templates
3. Click "Deploy" on the official SurrealDB template
4. Configure environment variables:
   - `SURREAL_USER`: `root`
   - `SURREAL_PASS`: `root` (change for production!)
   - `SURREAL_STRICT`: `false`

### Option B: Deploy from Nixpacks

1. In your Railway project, click "+ New Service"
2. Select "Empty Service"
3. Add a custom start command: `surreal start --user root --pass root memory`
4. Set nixpacks configuration to install SurrealDB

**Note**: Railway's SurrealDB template is recommended as it includes persistence.

---

## Step 3: Deploy API Service (FastAPI Backend)

1. In your Railway project, click "+ New Service"
2. Select "GitHub Repo" and choose this repository
3. Configure the service:

   **Settings → General:**
   - Service Name: `open-notebook-api`
   - Root Directory: `/` (keep at project root)

   **Settings → Deploy:**
   - Custom Start Command: (leave empty, uses nixpacks.api.toml)
   - Nixpacks Config File: `nixpacks.api.toml`
   - Watch Paths: `api/**, open_notebook/**, pyproject.toml, uv.lock`

4. **Environment Variables** (Settings → Variables):

   ```bash
   # Railway will auto-set PORT - don't override it

   # SurrealDB Connection (replace with your SurrealDB service variables)
   SURREAL_URL=ws://${{SurrealDB.RAILWAY_PRIVATE_DOMAIN}}:8000/rpc
   SURREAL_USER=root
   SURREAL_PASSWORD=root
   SURREAL_NAMESPACE=open_notebook
   SURREAL_DATABASE=open_notebook

   # API Configuration
   API_HOST=0.0.0.0
   API_RELOAD=false

   # AI Provider API Keys (add at least one)
   OPENAI_API_KEY=sk-...
   # ANTHROPIC_API_KEY=
   # GOOGLE_API_KEY=

   # Optional: Security
   # OPEN_NOTEBOOK_PASSWORD=your-secure-password
   ```

5. Deploy the service

---

## Step 4: Deploy Worker Service (Background Jobs)

1. In your Railway project, click "+ New Service"
2. Select "GitHub Repo" and choose this repository
3. Configure the service:

   **Settings → General:**
   - Service Name: `open-notebook-worker`
   - Root Directory: `/` (keep at project root)

   **Settings → Deploy:**
   - Custom Start Command: (leave empty, uses nixpacks.worker.toml)
   - Nixpacks Config File: `nixpacks.worker.toml`
   - Watch Paths: `open_notebook/**, commands/**, pyproject.toml, uv.lock`

4. **Environment Variables** (Settings → Variables):

   **Important**: The worker needs the **same environment variables as the API service**.

   Copy all environment variables from the API service, especially:
   - All `SURREAL_*` variables
   - All AI provider API keys
   - `SURREAL_COMMANDS_*` retry configuration

---

## Step 5: Deploy Frontend Service (Next.js)

1. In your Railway project, click "+ New Service"
2. Select "GitHub Repo" and choose this repository
3. Configure the service:

   **Settings → General:**
   - Service Name: `open-notebook-frontend`
   - Root Directory: `/` (keep at project root)

   **Settings → Deploy:**
   - Custom Start Command: (leave empty, uses nixpacks.frontend.toml)
   - Nixpacks Config File: `nixpacks.frontend.toml`
   - Watch Paths: `frontend/**`

4. **Environment Variables** (Settings → Variables):

   ```bash
   # Railway will auto-set PORT - don't override it

   # API Connection - use Railway's internal networking
   INTERNAL_API_URL=http://${{API.RAILWAY_PRIVATE_DOMAIN}}:${{API.PORT}}

   # Public API URL - use Railway's public domain
   API_URL=https://${{API.RAILWAY_PUBLIC_DOMAIN}}

   # Next.js Configuration
   NODE_ENV=production
   HOSTNAME=0.0.0.0
   ```

5. Deploy the service

---

## Step 6: Configure Public Domains

1. **Frontend Service:**
   - Go to Settings → Networking
   - Click "Generate Domain" to get a public URL (e.g., `open-notebook-frontend.up.railway.app`)
   - (Optional) Add custom domain

2. **API Service:**
   - Go to Settings → Networking
   - Click "Generate Domain" to get a public URL
   - Update the frontend's `API_URL` environment variable with this domain

---

## Step 7: Verify Deployment

1. Visit your frontend URL (from Step 6)
2. You should see the Open Notebook interface
3. Check the API health: `https://your-api-domain.railway.app/api/health`
4. Try creating a notebook and uploading a source

---

## Environment Variables Reference

### Required for All Services

| Variable | Description | Example |
|----------|-------------|---------|
| `SURREAL_URL` | WebSocket URL to SurrealDB | `ws://surrealdb.railway.internal:8000/rpc` |
| `SURREAL_USER` | Database user | `root` |
| `SURREAL_PASSWORD` | Database password | `root` |
| `SURREAL_NAMESPACE` | Database namespace | `open_notebook` |
| `SURREAL_DATABASE` | Database name | `open_notebook` |

### Required for API & Worker

At least one AI provider key:
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google AI API key
- `GROQ_API_KEY` - Groq API key
- `OLLAMA_API_BASE` - Ollama endpoint (if self-hosted)

Optional TTS (for podcasts):
- `ELEVENLABS_API_KEY` - ElevenLabs TTS

### Required for Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `INTERNAL_API_URL` | Internal API URL (server-side) | `http://api.railway.internal:5055` |
| `API_URL` | Public API URL (client-side) | `https://api.railway.app` |

---

## Railway Service Reference Variables

Railway provides special variables you can use:

- `${{SERVICE_NAME.RAILWAY_PRIVATE_DOMAIN}}` - Internal hostname
- `${{SERVICE_NAME.RAILWAY_PUBLIC_DOMAIN}}` - Public domain
- `${{SERVICE_NAME.PORT}}` - Assigned port

Example:
```bash
SURREAL_URL=ws://${{SurrealDB.RAILWAY_PRIVATE_DOMAIN}}:8000/rpc
INTERNAL_API_URL=http://${{API.RAILWAY_PRIVATE_DOMAIN}}:${{API.PORT}}
API_URL=https://${{API.RAILWAY_PUBLIC_DOMAIN}}
```

---

## Troubleshooting

### API Service Won't Start

**Check logs for:**
- Database connection errors → Verify `SURREAL_URL` and credentials
- Missing dependencies → Ensure `uv.lock` is committed
- Port binding errors → Let Railway set `PORT`, don't override

### Frontend Can't Connect to API

**Check:**
1. API service has a public domain generated
2. Frontend's `API_URL` matches the API's public domain
3. Frontend's `INTERNAL_API_URL` uses Railway's private networking
4. CORS is configured (should be enabled by default in `api/main.py`)

### Worker Not Processing Jobs

**Check:**
1. Worker has the same `SURREAL_*` variables as API
2. Worker has AI provider API keys
3. Worker logs show successful connection to database

### Database Connection Errors

**Check:**
1. SurrealDB service is running
2. `SURREAL_URL` uses WebSocket protocol (`ws://` not `http://`)
3. Port is correct (usually `:8000/rpc`)
4. Credentials match

---

## Production Recommendations

### Security

1. **Change default passwords:**
   ```bash
   SURREAL_USER=admin
   SURREAL_PASSWORD=<strong-random-password>
   ```

2. **Enable application password:**
   ```bash
   OPEN_NOTEBOOK_PASSWORD=<your-secure-password>
   ```

3. **Use secrets management:**
   - Store API keys in Railway's environment variables
   - Never commit `.env` files to git

### Performance

1. **Increase worker concurrency** (for faster processing):
   ```bash
   SURREAL_COMMANDS_MAX_TASKS=10
   ```

2. **Optimize API timeouts** (for slow AI providers):
   ```bash
   API_CLIENT_TIMEOUT=600
   ESPERANTO_LLM_TIMEOUT=120
   ```

### Monitoring

1. **Enable Railway metrics** in each service's Settings
2. **Set up health checks:**
   - API: `/api/health`
   - Frontend: `/` (homepage)
3. **Configure restart policies** (already set in railway.json)

---

## Scaling

### Vertical Scaling
- Upgrade Railway plan for more CPU/RAM per service
- Increase worker concurrency with more resources

### Horizontal Scaling
- Railway supports multiple replicas (Pro plan)
- Update `numReplicas` in railway.json
- **Note**: Ensure SurrealDB can handle concurrent connections

---

## Cost Optimization

1. **Start with Hobby plan** ($5/month)
2. **Monitor usage** via Railway dashboard
3. **Optimize AI costs:**
   - Use cheaper models for embeddings (text-embedding-3-small)
   - Use Groq for fast, free inference
   - Self-host Ollama for unlimited usage

---

## Support

- **Documentation**: https://open-notebook.ai
- **Discord**: https://discord.gg/37XJPXfz2w
- **GitHub Issues**: https://github.com/lfnovo/open-notebook/issues
- **Railway Docs**: https://docs.railway.app

---

## What's Different from Docker Deployment?

| Aspect | Docker Deployment | Railway Source Deployment |
|--------|-------------------|---------------------------|
| **Services** | Single container (all-in-one) | 4 separate services |
| **Database** | Bundled SurrealDB | Managed SurrealDB service |
| **Updates** | Rebuild entire image | Per-service deployments |
| **Scaling** | Vertical only | Horizontal scaling available |
| **Configuration** | supervisord.conf | Nixpacks TOML files |
| **Logs** | Combined logs | Per-service logs |

---

**Last Updated**: February 2025
**Version**: 1.6.2+
