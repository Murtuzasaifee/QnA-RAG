# Hydra Configuration - Quick Reference

## 📁 File Structure (Concise!)

```
app/
├── conf/
│   └── config.yaml           # Single config file (all settings)
├── core/
│   └── config.py            # Type definitions (dataclasses)
├── utils/
│   └── config_utils.py      # Helper functions
└── examples/
    └── config_examples.py   # Usage examples
```

**Just 4 files total!** ✨

## 🚀 Quick Start

### 1. Basic Usage

```python
from app.utils.config_utils import get_settings

# Get configuration
settings = get_settings()

# Access values with dot notation
print(settings.openai.api_key)
print(settings.model.llm_model)
print(settings.document_processing.chunk_size)
```

### 2. Runtime Overrides

```python
from app.utils.config_utils import get_config

cfg = get_config(overrides=(
    "model.llm_model=gpt-4",
    "retrieval.k=10",
))
```

## 📋 Migration from Pydantic Settings

### What Changed?

Fields are now organized into logical groups:

| Old (Pydantic) | New (Hydra) |
|----------------|-------------|
| `settings.openai_api_key` | `settings.openai.api_key` |
| `settings.qdrant_url` | `settings.qdrant.url` |
| `settings.chunk_size` | `settings.document_processing.chunk_size` |
| `settings.llm_model` | `settings.model.llm_model` |
| `settings.retrieval_k` | `settings.retrieval.k` |

### What Stayed the Same?

- ✅ Environment variables (`.env` file unchanged)
- ✅ Function name: `get_settings()` still works
- ✅ Dot notation access

## 🔧 Configuration File

`app/conf/config.yaml` contains everything:

```yaml
# Application Info
app_name: "QnA RAG"
app_version: "0.1.0"

# OpenAI Configuration
openai:
  api_key: ${oc.env:OPENAI_API_KEY}

# Qdrant Configuration
qdrant:
  url: ${oc.env:QDRANT_URL}
  api_key: ${oc.env:QDRANT_API_KEY}

# Model Configuration
model:
  embedding_model: "text-embedding-3-small"
  llm_model: "gpt-4o-mini"
  llm_temperature: 0.0

# ... etc
```

## 🌍 Environment Variables

Your `.env` file stays exactly the same:

```env
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_API_KEY=...
COLLECTION_NAME=ragit_documents
```

## ✅ Testing

Run the examples to verify everything works:

```bash
uv run python -m app.examples.config_examples
```

## 💡 Key Benefits

1. **Modular**: Organized into logical groups (openai, qdrant, model, etc.)
2. **Type Safe**: Full IDE autocomplete and type checking
3. **Flexible**: Easy runtime overrides
4. **Simple**: Just 1 YAML file + 3 Python files
5. **Compatible**: Works like pydantic-settings

## 🎯 Common Patterns

### Pattern 1: Basic Access
```python
from app.utils.config_utils import get_settings

settings = get_settings()
api_key = settings.openai.api_key
```

### Pattern 2: Override at Runtime
```python
from app.utils.config_utils import get_config

cfg = get_config(overrides=("model.llm_model=gpt-4",))
```

### Pattern 3: Print Full Config
```python
from app.utils.config_utils import print_config

print_config()
```

## 🔍 Troubleshooting

**Q: Environment variable not found?**  
A: Make sure your `.env` file is in the project root

**Q: Import errors?**  
A: Ensure all `__init__.py` files exist in `app/`, `app/core/`, `app/utils/`, `app/examples/`

**Q: Want to add new config?**  
A: 
1. Add to `app/conf/config.yaml`
2. Add dataclass to `app/core/config.py`
3. Access via `settings.your_group.your_field`

---

**That's it!** You now have a clean, modular, type-safe configuration system. 🎉
