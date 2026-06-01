#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive card message bot implementation.

This module provides the :class:`InteractiveBot` class for sending interactive
card messages to Lark Group Bots. Interactive cards support rich layouts,
buttons, and other interactive elements.

Example:
    ::

        from pylgb import InteractiveBot

        card = {
            "header": {"title": {"tag": "plain_text", "content": "Notification"}},
            "elements": [
                {"tag": "div", "text": {"tag": "plain_text", "content": "Success!"}}
            ]
        }

        bot = InteractiveBot("your-webhook-key")
        bot.send(card)
"""

from typing import Dict

from ._abstract import BaseBot


class InteractiveBot(BaseBot):
    """
    Interactive card message bot for Lark Group.

    Sends interactive card messages with rich layouts and interactive elements.

    Args:
        webhook (Optional[str]): Webhook key (UUID format) or full webhook URL.
            If not provided, reads from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable.
        sign_secret (Optional[str]): Signing secret for signature generation.
            If not provided, reads from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable.

    Example:
        ::

            from pylgb import InteractiveBot

            card = {
                "header": {"title": {"tag": "plain_text", "content": "Notification"}},
                "elements": [
                    {"tag": "div", "text": {"tag": "plain_text", "content": "Success!"}}
                ]
            }

            bot = InteractiveBot("your-key")
            bot.send(card)

        With environment variables::

            # .env: LARK_WEBHOOK=your-key
            bot = InteractiveBot()

    See Also:
        :class:`TextBot`: For text messages.
        :class:`SmartBot`: For automatic type detection.
    """

    def send(self, card: Dict) -> Dict:
        """
        Send an interactive card message.

        Args:
            card (Dict): The card content dictionary.

        Returns:
            Dict: Response from the Lark API.

        Example:
            ::

                card = {
                    "header": {"title": {"tag": "plain_text", "content": "T"}},
                    "elements": [{"tag": "div", "text": {"tag": "plain_text"}}]
                }
                bot.send(card)
        """
        data = {"msg_type": "interactive", "card": card}
        return self._send(data)
