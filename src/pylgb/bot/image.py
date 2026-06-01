#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image message bot implementation.

This module provides the :class:`ImageBot` class for sending image messages
to Lark Group Bots.

Example:
    ::

        from pylgb import ImageBot

        bot = ImageBot("your-webhook-key")
        bot.send("img_xxxx")

Note:
    The image must be uploaded to Lark first to obtain the image_key.
"""

from ._abstract import BaseBot


class ImageBot(BaseBot):
    """
    Image message bot for Lark Group.

    Sends image messages using an image key from Lark.

    Args:
        webhook (Optional[str]): Webhook key (UUID format) or full webhook URL.
            If not provided, reads from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable.
        sign_secret (Optional[str]): Signing secret for signature generation.
            If not provided, reads from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable.

    Example:
        ::

            from pylgb import ImageBot

            bot = ImageBot("your-key")
            bot.send("img_xxxx")

        With environment variables::

            # .env: LARK_WEBHOOK=your-key
            bot = ImageBot()

    Note:
        The image_key must be obtained by uploading the image to Lark first.

    See Also:
        :class:`TextBot`: For text messages.
        :class:`SmartBot`: For automatic type detection.
    """

    def send(self, image_key: str) -> dict:
        """
        Send an image message.

        Args:
            image_key (str): The image key from Lark.

        Returns:
            dict: Response from the Lark API.

        Example:
            ::

                bot.send("img_xxxx")
        """
        data = {"msg_type": "image", "content": {"image_key": image_key}}
        return self._send(data)
