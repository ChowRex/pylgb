#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constants for Lark Group Bot API.

This module defines the constants used throughout the pylgb package.
"""

from os import getenv
from pathlib import Path
from typing import Optional

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv  # pragma: no cover
    # Load .env from current directory or project root
    env_path = Path.cwd() / ".env"  # pragma: no cover
    if env_path.exists():  # pragma: no cover
        load_dotenv(env_path, override=True)  # pragma: no cover
except ImportError:  # pragma: no cover
    pass  # pragma: no cover

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/"
"""str: The base webhook URL for Lark Group Bot API."""


def get_env_webhook() -> Optional[str]:
    """
    Get webhook key from environment variable.

    Returns:
        Optional[str]: The webhook key from LARK_WEBHOOK or FEISHU_WEBHOOK
            environment variable, or None if not set.

    Example:
        ::

            # Set in .env file:
            # LARK_WEBHOOK=your-webhook-key

            from pylgb._constants import get_env_webhook
            webhook = get_env_webhook()
    """
    return getenv("LARK_WEBHOOK") or getenv("FEISHU_WEBHOOK")


def get_env_sign_secret() -> Optional[str]:
    """
    Get sign secret from environment variable.

    Returns:
        Optional[str]: The sign secret from LARK_SIGN_SECRET or FEISHU_SIGN_SECRET
            environment variable, or None if not set.

    Example:
        ::

            # Set in .env file:
            # LARK_SIGN_SECRET=your-sign-secret

            from pylgb._constants import get_env_sign_secret
            secret = get_env_sign_secret()
    """
    return getenv("LARK_SIGN_SECRET") or getenv("FEISHU_SIGN_SECRET")
