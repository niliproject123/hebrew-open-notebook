# SurrealDB Connection Test

Minimal service to test SurrealDB connectivity on Railway.

## Environment Variables

Set these in Railway (script auto-converts HTTP to WebSocket):

```bash
SURREALDB_URL=http://surrealdb.railway.internal:8000
SURREALDB_USER=root
SURREALDB_PASS=hebrew-medical-notebook-2024
SURREALDB_NAMESPACE=open_notebook
SURREALDB_DATABASE=open_notebook
```

**Note:** Script automatically converts `http://host:8000` → `ws://host/rpc:8000`

## Deploy to Railway

1. Create a new service in Railway
2. Connect to GitHub → Branch: `claude/railway-deployment-setup-DPtdQ`
3. Set **Root Directory**: `connection-test`
4. Add environment variables above
5. Deploy and check logs!

## Experiment with URLs

If connection fails, try these URL formats in Railway env vars:

**HTTP (auto-converted):**
- `http://surrealdb.railway.internal:8000`
- `http://surrealdb:8000`

**WebSocket (native):**
- `ws://surrealdb.railway.internal/rpc:8000`
- `ws://surrealdb/rpc:8000`

The script will show exactly which URL it's trying to connect to!
