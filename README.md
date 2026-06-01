# pylgb

[![Python versions](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Lark(A.K.A Feishu) Group Bot Python API - A simple and easy-to-use library for sending messages to Lark group bots.

## Features

- 🤖 **Smart Bot** - Automatic message type detection
- 📝 **Multiple Message Types** - Text, Post, Image, Interactive Card
- 🔒 **Signature Support** - HMAC-SHA256 signature verification
- ✅ **Type Hints** - Full type annotation support
- 📦 **Minimal Dependencies** - Only requires requests

## Installation

```bash
pip install pylgb
```

## Quick Start

### 1. Get Webhook URL and Sign Key

1. Add a custom bot in your Lark group
2. Copy the webhook URL or just the key (UUID format)
3. If signature verification is needed, copy the signing key

### 2. Send Messages

```python
from pylgb import SmartBot

# Without signature
bot = SmartBot("your-webhook-key")

# With signature
bot = SmartBot("your-webhook-key", sign_secret="your-sign-secret")

# Send text message
bot.send("Hello, World!")

# Send text with @mentions
bot.send("Important!", mentioned_list=["ou_xxxx", "@all"])
```

## Usage Guide

### Text Message

```python
from pylgb import TextBot

# Without signature
bot = TextBot("your-key")

# With signature
bot = TextBot("your-key", sign_secret="your-sign-secret")
bot.send("Text message", mentioned_list=["ou_xxxx"])
```

### Post (Rich Text) Message

```python
from pylgb import PostBot

content = [
    [{"tag": "text", "text": "Project Weekly Report"}],
    [{"tag": "text", "text": "Progress: 80%"}]
]

bot = PostBot("your-key", sign_secret="your-sign-secret")
bot.send("Weekly Report", content)
```

### Interactive Card

```python
from pylgb import InteractiveBot

card = {
    "header": {"title": {"tag": "plain_text", "content": "Notification"}},
    "elements": [{"tag": "div", "text": {"tag": "plain_text", "content": "Deployed successfully"}}]
}

bot = InteractiveBot("your-key", sign_secret="your-sign-secret")
bot.send(card)
```

### Using SmartBot Auto-Detection

```python
from pylgb import SmartBot

bot = SmartBot("your-key", sign_secret="your-sign-secret")

# Text
bot.send("Text message")

# Image
bot.send({"image_key": "img_xxxx"})

# Card
bot.send({"card": {"header": {...}, "elements": [...]}})
```

## Project Structure

```
pylgb/
├── src/pylgb/
│   ├── __init__.py       # Entry module
│   ├── _constants.py     # Constants
│   └── bot/
│       ├── __init__.py
│       ├── _abstract.py  # BaseBot class (with signature)
│       ├── _smart.py     # SmartBot
│       ├── text.py       # TextBot
│       ├── post.py       # PostBot
│       ├── image.py      # ImageBot
│       └── interactive.py # InteractiveBot
├── pyproject.toml
├── LICENSE
└── README.md
```

## Development

```bash
# Install dev dependencies
pip install -e ".[test]"

# Run tests
pytest --cov=pylgb -v
```

## References

- [Lark Open Platform - Custom Bot](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)
- [pywgb](https://github.com/ChowRex/pywgb) - Wecom Group Bot API

## License

MIT License
