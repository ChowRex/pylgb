#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post (rich text) message bot implementation.

This module provides the :class:`PostBot` class for sending rich text messages
to Lark Group Bots. Post messages support formatted content with text styling,
links, and @mentions.

Example:
    Basic post message::

        from pylgb import PostBot

        content = [
            [{"tag": "text", "text": "Hello "}],
            [{"tag": "a", "text": "Link", "href": "https://example.com"}]
        ]

        bot = PostBot("your-webhook-key")
        bot.send("Title", content)
"""

from typing import List

from ._abstract import BaseBot


class PostBot(BaseBot):
    """
    Post (rich text) message bot for Lark Group.

    Sends rich text messages with formatted content including text styling,
    links, and @mentions.

    Args:
        webhook (Optional[str]): Webhook key (UUID format) or full webhook URL.
            If not provided, reads from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable.
        sign_secret (Optional[str]): Signing secret for signature generation.
            If not provided, reads from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable.

    Example:
        ::

            from pylgb import PostBot

            content = [
                [{"tag": "text", "text": "Hello, "}],
                [{"tag": "a", "text": "Click here", "href": "https://example.com"}]
            ]

            bot = PostBot("your-key")
            bot.send("Announcement", content)

        With environment variables::

            # .env: LARK_WEBHOOK=your-key
            bot = PostBot()

    Note:
        Content is a list of paragraphs, where each paragraph is a list of
        content elements. Each element is a dict with a ``"tag"`` field.

    See Also:
        :class:`TextBot`: For simple text messages.
        :class:`SmartBot`: For automatic type detection.
    """

    def send(self, title: str, content: List[List[dict]]) -> dict:
        """
        Send a post (rich text) message.

        Args:
            title (str): The title of the post message.
            content (List[List[dict]]): The content of the post. A list of
                paragraphs, where each paragraph is a list of content elements.

        Returns:
            dict: Response from the Lark API.

        Example:
            ::

                content = [
                    [{"tag": "text", "text": "Hello, "}],
                    [{"tag": "a", "text": "Link", "href": "https://example.com"}]
                ]
                bot.send("Title", content)
        """
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        return self._send(data)
