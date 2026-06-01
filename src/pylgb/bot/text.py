#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text message bot implementation.

This module provides the :class:`TextBot` class for sending plain text messages
to Lark Group Bots. It supports @mentions for specific users or all members.

Example:
    Basic text message::

        from pylgb import TextBot

        bot = TextBot("your-webhook-key")
        bot.send("Hello, World!")

    Text with mentions::

        bot.send("Important!", mentioned_list=["ou_xxxx", "@all"])

    With signature::

        bot = TextBot("your-webhook-key", sign_secret="your-sign-secret")
        bot.send("Hello, World!")
"""

from typing import Optional, List

from ._abstract import BaseBot


class TextBot(BaseBot):
    """
    Text message bot for Lark Group.

    Sends plain text messages with optional @mentions.

    Args:
        webhook (Optional[str]): Webhook key (UUID format) or full webhook URL.
            If not provided, reads from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable.
        sign_secret (Optional[str]): Signing secret for signature generation.
            If not provided, reads from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable.

    Example:
        Simple text message::

            from pylgb import TextBot

            bot = TextBot("your-key")
            bot.send("Hello, World!")

        With environment variables::

            # .env: LARK_WEBHOOK=your-key
            bot = TextBot()

        With mentions::

            bot.send("Team meeting!", mentioned_list=["ou_xxxx", "@all"])

        With signature::

            bot = TextBot("your-key", sign_secret="your-sign-secret")

    See Also:
        :class:`PostBot`: For rich text messages.
        :class:`SmartBot`: For automatic type detection.
    """

    def send(self, text: str, *, mentioned_list: Optional[List[str]] = None) -> dict:
        """
        Send a text message.

        Args:
            text (str): The text message to send.
            mentioned_list (Optional[List[str]]): List of user IDs to mention.
                Use ``"@all"`` to mention all members.

        Returns:
            dict: Response from the Lark API.

        Example:
            ::

                bot.send("Hello, World!")
                bot.send("Important!", mentioned_list=["ou_xxxx", "@all"])
        """
        content: dict = {"text": text}
        if mentioned_list:
            content["mentioned_list"] = mentioned_list
        data = {"msg_type": "text", "content": content}
        return self._send(data)
