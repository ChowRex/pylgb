#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot module for Lark Group Bot API.

This module provides all bot implementations for sending messages to
Lark Group Bots.

Classes:
    BaseBot: Abstract base class for all bots.
    SmartBot: Bot with automatic message type detection.
    TextBot: Bot for text messages.
    PostBot: Bot for post (rich text) messages.
    ImageBot: Bot for image messages.
    InteractiveBot: Bot for interactive card messages.

Example:
    ::

        from pylgb.bot import SmartBot

        bot = SmartBot("your-key", sign_secret="your-sign-secret")
        bot.send("Hello, World!")
"""

from ._abstract import BaseBot
from ._smart import SmartBot
from .text import TextBot
from .post import PostBot
from .image import ImageBot
from .interactive import InteractiveBot

__all__ = [
    "BaseBot",
    "SmartBot",
    "TextBot",
    "PostBot",
    "ImageBot",
    "InteractiveBot",
]
