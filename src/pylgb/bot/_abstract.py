#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Abstract base class for bots.

This module provides the :class:`BaseBot` abstract class which serves as the
foundation for all bot implementations. It handles webhook URL construction,
signature generation, and HTTP communication with the Lark API.
"""

from abc import ABC, abstractmethod
from base64 import b64encode
from hashlib import sha256
from hmac import new
from time import time
from typing import Optional

from requests import post

from .._constants import WEBHOOK_URL, get_env_webhook, get_env_sign_secret


class BaseBot(ABC):
    """
    Abstract base class for Lark Group Bot.

    This class provides the core functionality for sending messages to Lark
    Group Bots, including webhook URL handling and HMAC-SHA256 signature
    generation for secure communication.

    Args:
        webhook (str): Webhook key (UUID format) or full webhook URL.
            If not provided, reads from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable.
        sign_secret (Optional[str]): Signing secret for signature generation.
            If not provided, reads from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable.

    Attributes:
        webhook (str): The full webhook URL.
        _sign_secret (Optional[str]): The signing secret for signature generation.

    Example:
        Subclass implementation::

            class TextBot(BaseBot):
                def send(self, text: str) -> dict:
                    return self._send({"msg_type": "text", "content": {"text": text}})

        Using environment variables::

            # .env file:
            # LARK_WEBHOOK=your-webhook-key
            # LARK_SIGN_SECRET=your-sign-secret

            bot = TextBot()  # Reads from environment

    Note:
        Subclasses must implement the :meth:`send` method.
    """

    def __init__(
        self, webhook: Optional[str] = None, sign_secret: Optional[str] = None
    ):
        # Get webhook from argument or environment
        if webhook is None:
            webhook = get_env_webhook()
        if webhook is None:
            raise ValueError(
                "webhook is required. Set LARK_WEBHOOK environment variable "
                "or pass webhook parameter."
            )

        if webhook.startswith("http"):
            self.webhook = webhook
        else:
            self.webhook = f"{WEBHOOK_URL}{webhook}"

        # Get sign_secret from argument or environment
        self._sign_secret = (
            sign_secret if sign_secret is not None else get_env_sign_secret()
        )

    def _gen_sign(self, timestamp: str) -> str:
        """
        Generate HMAC-SHA256 signature for the request.

        Args:
            timestamp (str): Unix timestamp string (seconds).

        Returns:
            str: Base64-encoded signature string, or empty string if no sign secret.

        Note:
            The signature algorithm uses ``timestamp + "\\n" + sign_secret`` as the
            HMAC key to sign an empty string, then Base64 encodes the result.
            This follows the Lark/Feishu signature specification.
        """
        if not self._sign_secret:
            return ""
        # string_to_sign is used as the HMAC key
        string_to_sign = f"{timestamp}\n{self._sign_secret}"
        # Sign an empty string using string_to_sign as the key
        hmac_code = new(
            string_to_sign.encode("utf-8"), b"", digestmod=sha256  # Empty bytes
        ).digest()
        sign = b64encode(hmac_code).decode("utf-8")
        return sign

    def _send(self, data: dict) -> dict:
        """
        Send message to Lark via HTTP POST request.

        Args:
            data (dict): The message data to send.

        Returns:
            dict: Response from the Lark API.

        Example:
            ::

                result = self._send({
                    "msg_type": "text",
                    "content": {"text": "Hello"}
                })
        """
        if self._sign_secret:
            timestamp = str(int(time()))
            sign = self._gen_sign(timestamp)
            data["timestamp"] = timestamp
            data["sign"] = sign
        resp = post(self.webhook, json=data, timeout=10)
        return resp.json()

    @abstractmethod
    def send(self, *args, **kwargs) -> dict:
        """
        Send message. Must be implemented by subclasses.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            dict: Response from the Lark API.
        """
        pass  # pragma: no cover
