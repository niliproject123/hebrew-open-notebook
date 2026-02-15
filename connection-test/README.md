# SurrealDB Connection Test

Minimal service to test SurrealDB connectivity on Railway.

## Environment Variables

Set these in Railway:

```bash
SURREALDB_URL=http://surrealdb.railway.internal:8000
SURREALDB_USER=root
SURREALDB_PASS=hebrew-medical-notebook-2024
SURREALDB_NAMESPACE=open_notebook
SURREALDB_DATABASE=open_notebook
```

## Deploy to Railway

1. Create a new service in Railway
2. Point it to this `connection-test/` directory
3. Set the environment variables above
4. Check the deployment logs for connection results

## Experiment

Try different URLs to find the right connection:
- `http://surrealdb.railway.internal:8000`
- `http://surrealdb:8000`
- `ws://surrealdb.railway.internal:8000/rpc`
- Internal Railway service URL from dashboard
