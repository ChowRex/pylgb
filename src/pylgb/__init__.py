#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lark(A.K.A Feishu) Group Bot Python API.

This module provides a simple and easy-to-use Python API for sending messages
to Lark (Feishu) Group Bots. It supports multiple message types including text,
post (rich text), image, and interactive cards.

Example:
    Basic usage with SmartBot::

        from pylgb import SmartBot

        bot = SmartBot("your-webhook-key")
        bot.send("Hello, World!")

    With signature verification::

        bot = SmartBot("your-webhook-key", sign_secret="your-sign-secret")
        bot.send("Hello, World!")

    Send different message types::

        # Text
        bot.send("Text message")

        # Image
        bot.send({"image_key": "img_xxxx"})

        # Interactive card
        bot.send({"card": {"header": {...}, "elements": [...]}})

:author: ChowRex
:copyright: Copyright © 2026 ChowRex. All rights reserved.
:license: MIT
"""

__author__ = "ChowRex"
__version__ = "0.0.1"

from .bot import SmartBot, TextBot, PostBot, ImageBot, InteractiveBot

__all__ = [
    "SmartBot",
    "TextBot",
    "PostBot",
    "ImageBot",
    "InteractiveBot",
]
