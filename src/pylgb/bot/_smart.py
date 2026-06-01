#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart bot with automatic message type detection.

This module provides the :class:`SmartBot` class which automatically detects
the message type and uses the appropriate bot implementation.

Example:
    ::

        from pylgb import SmartBot

        bot = SmartBot("your-webhook-key", sign_secret="your-sign-secret")

        # Text message
        bot.send("Hello, World!")

        # Image message
        bot.send({"image_key": "img_xxxx"})

        # Interactive card
        bot.send({"card": {"header": {...}, "elements": [...]}})

        # Post message
        bot.send({"title": "Title", "content": [[{"tag": "text", "text": "Hello"}]]})

    Using environment variables::

        # .env file:
        # LARK_WEBHOOK=your-webhook-key
        # LARK_SIGN_SECRET=your-sign-secret

        bot = SmartBot()  # Reads from environment
"""

from typing import Optional, Union

from ._abstract import BaseBot
from .text import TextBot
from .post import PostBot
from .image import ImageBot
from .interactive import InteractiveBot


class SmartBot(BaseBot):
    """
    Smart bot with automatic message type detection.

    Automatically detects the message type and delegates to the appropriate
    bot implementation.

    Args:
        webhook (Optional[str]): Webhook key (UUID format) or full webhook URL.
            If not provided, reads from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable.
        sign_secret (Optional[str]): Signing secret for signature generation.
            If not provided, reads from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable.

    Attributes:
        text (TextBot): Text message bot instance.
        post (PostBot): Post message bot instance.
        image (ImageBot): Image message bot instance.
        interactive (InteractiveBot): Interactive card bot instance.

    Example:
        ::

            from pylgb import SmartBot

            # With explicit parameters
            bot = SmartBot("your-key", sign_secret="your-sign-secret")

            # With environment variables
            # .env: LARK_WEBHOOK=your-key, LARK_SIGN_SECRET=your-sign-secret
            bot = SmartBot()

            # Text
            bot.send("Hello")

            # Image
            bot.send({"image_key": "img_xxxx"})

            # Card
            bot.send({"card": {"header": {...}, "elements": [...]}})

            # Post
            bot.send({"title": "Title", "content": [[{"tag": "text", "text": "Hello"}]]})

    Note:
        Message type detection rules:
            - ``str``: Text message
            - ``dict`` with ``"image_key"``: Image message
            - ``dict`` with ``"card"``: Interactive card
            - ``dict`` with ``"title"`` and ``"content"``: Post message

    See Also:
        :class:`TextBot`: For text messages.
        :class:`PostBot`: For rich text messages.
        :class:`ImageBot`: For image messages.
        :class:`InteractiveBot`: For interactive cards.
    """

    def __init__(
        self, webhook: Optional[str] = None, sign_secret: Optional[str] = None
    ):
        super().__init__(webhook, sign_secret)
        self.text = TextBot(webhook, sign_secret)
        self.post = PostBot(webhook, sign_secret)
        self.image = ImageBot(webhook, sign_secret)
        self.interactive = InteractiveBot(webhook, sign_secret)

    def send(self, message: Union[str, dict], **kwargs) -> dict:
        """
        Send a message with automatic type detection.

        Args:
            message (Union[str, dict]): The message to send. Can be:
                - ``str``: Text message
                - ``dict`` with ``"image_key"``: Image message
                - ``dict`` with ``"card"``: Interactive card
                - ``dict`` with ``"title"`` and ``"content"``: Post message
            **kwargs: Additional keyword arguments passed to the specific bot.

        Returns:
            dict: Response from the Lark API.

        Raises:
            ValueError: If the message type is not supported.

        Example:
            ::

                # Text
                bot.send("Hello")

                # Image
                bot.send({"image_key": "img_xxxx"})

                # Card
                bot.send({"card": {"header": {...}, "elements": [...]}})
        """
        if isinstance(message, str):
            return self.text.send(message, **kwargs)
        if isinstance(message, dict):
            if "image_key" in message:
                return self.image.send(message["image_key"])
            if "card" in message:
                return self.interactive.send(message["card"])
            if "title" in message and "content" in message:
                return self.post.send(message["title"], message["content"])
        raise ValueError("Unsupported message type")
