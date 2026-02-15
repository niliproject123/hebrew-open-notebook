"""Minimal SurrealDB connection tester for Railway debugging."""
import asyncio
import os
import sys
from surrealdb import Surreal

async def test_connection():
    """Test SurrealDB connection with env variables."""
    url = os.getenv("SURREALDB_URL", "http://localhost:8000")
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

    try:
        print("\n🔌 Connecting to SurrealDB...")
        async with Surreal(url) as db:
            print("✅ Connected successfully!")

            print(f"\n🔐 Signing in as {user}...")
            await db.signin({"user": user, "pass": password})
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

if __name__ == "__main__":
    exit_code = asyncio.run(test_connection())
    sys.exit(exit_code)
