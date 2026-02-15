"""Minimal SurrealDB connection tester for Railway debugging."""
import asyncio
import os
import sys
from surrealdb import AsyncSurreal

async def test_connection():
    """Test SurrealDB connection with env variables."""
    # Support both HTTP and WS formats
    url = os.getenv("SURREALDB_URL", "ws://localhost:8000/rpc")

    # Convert HTTP to WebSocket format if needed
    if url.startswith("http://"):
        # http://host:port -> ws://host:port/rpc
        url = url.replace("http://", "ws://")
        if not url.endswith("/rpc"):
            url = url.rstrip("/") + "/rpc"

    user = os.getenv("SURREALDB_USER", "root")
    password = os.getenv("SURREALDB_PASS", "root")
    namespace = os.getenv("SURREALDB_NAMESPACE", "open_notebook")
    database = os.getenv("SURREALDB_DATABASE", "open_notebook")

    print("=" * 60)
    print("🔍 SurrealDB Connection Test")
    print("=" * 60)
    print(f"URL:       {url}")
    print(f"User:      {user}")
    print(f"Password:  {'*' * len(password)}")
    print(f"Namespace: {namespace}")
    print(f"Database:  {database}")
    print("=" * 60)

    db = None
    try:
        print("\n🔌 Connecting to SurrealDB...")
        db = AsyncSurreal(url)
        print("✅ Connection object created!")

        print(f"\n🔐 Signing in as {user}...")
        await db.signin({"username": user, "password": password})
        print("✅ Signed in successfully!")

        print(f"\n📦 Using namespace '{namespace}' and database '{database}'...")
        await db.use(namespace, database)
        print("✅ Database selected!")

        print("\n🧪 Running test query...")
        result = await db.query("SELECT * FROM notebook LIMIT 1")
        print(f"✅ Query executed! Result: {result}")

        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ CONNECTION FAILED!")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("=" * 60)
        return 1

    finally:
        if db:
            try:
                await db.close()
                print("\n🔌 Connection closed.")
            except Exception:
                pass

if __name__ == "__main__":
    exit_code = asyncio.run(test_connection())
    sys.exit(exit_code)
