"""
Railway deployment configuration - HARDCODED VALUES

Edit the values below, then deploy to Railway.
Later, move these to Railway environment variables in the dashboard.

Using setdefault() so Railway env vars will override these when set.
"""

import os

# =================================================================
# AI PROVIDER - Add your API key here
# =================================================================
# Choose ONE provider. Comment/uncomment as needed.

# OpenAI (recommended for starting)
os.environ.setdefault("OPENAI_API_KEY", "REPLACE_WITH_YOUR_OPENAI_KEY")

# Anthropic
# os.environ.setdefault("ANTHROPIC_API_KEY", "REPLACE_WITH_YOUR_KEY")

# Google Gemini (good for long documents)
# os.environ.setdefault("GOOGLE_API_KEY", "REPLACE_WITH_YOUR_KEY")

# Groq (fast, free tier available)
# os.environ.setdefault("GROQ_API_KEY", "REPLACE_WITH_YOUR_KEY")

# Ollama (requires separate deployment - see Phase 5)
# os.environ.setdefault("OLLAMA_API_BASE", "http://your-ollama-host:11434")

# =================================================================
# DATABASE - Connects to separate SurrealDB Railway service
# =================================================================
# "surrealdb" is the Railway service name - change if you named it differently
os.environ.setdefault("SURREAL_URL", "ws://surrealdb.railway.internal:8000/rpc")
os.environ.setdefault("SURREAL_USER", "root")
os.environ.setdefault("SURREAL_PASSWORD", "hebrew-medical-notebook-2024")
os.environ.setdefault("SURREAL_NAMESPACE", "open_notebook")
os.environ.setdefault("SURREAL_DATABASE", "open_notebook")

# =================================================================
# HEBREW TEXT OPTIMIZATION
# =================================================================
# Smaller chunks work better for Hebrew medical text
os.environ.setdefault("OPEN_NOTEBOOK_CHUNK_SIZE", "1000")
os.environ.setdefault("OPEN_NOTEBOOK_CHUNK_OVERLAP", "150")

# =================================================================
# TIMEOUTS - Increase for slow models or large documents
# =================================================================
os.environ.setdefault("API_CLIENT_TIMEOUT", "600")
os.environ.setdefault("ESPERANTO_LLM_TIMEOUT", "300")

# =================================================================
# OPTIONAL: Password protection
# =================================================================
# Uncomment to require password for access
# os.environ.setdefault("OPEN_NOTEBOOK_PASSWORD", "your-password-here")
