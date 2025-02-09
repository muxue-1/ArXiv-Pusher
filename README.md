# ArXiv Pusher

Daily push AI-summarized ArXiv paper to your mailbox.

## Setup

Create `config.py` in the root directory. Example as belows.

```py
CONFIG = {
    # ArXiv Settings
    "arxiv_categories": ["cs.AI", "cs.SY"],
    "days_lookback": 5,

    # AI Settings
    "api_key": "sk-012345789ABCDEF",
    "base_url": "https://api.openai.com/v1",
    "model": "gpt-4"
}
```
