#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for pylgb bot module."""

import hashlib
import hmac
from unittest.mock import MagicMock, patch

import pytest

from pylgb import SmartBot, TextBot, PostBot, ImageBot, InteractiveBot


class TestTextBot:
    """Tests for TextBot."""

    def test_init_with_key(self):
        """Test initialization with webhook key."""
        bot = TextBot("test-key")
        assert bot.webhook == "https://open.feishu.cn/open-apis/bot/v2/hook/test-key"

    def test_init_with_url(self):
        """Test initialization with full URL."""
        url = "https://open.feishu.cn/open-apis/bot/v2/hook/test-key"
        bot = TextBot(url)
        assert bot.webhook == url

    def test_send_text(self):
        """Test sending text message."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = TextBot("test-key")
            result = bot.send("Hello")
            assert result["StatusCode"] == 0
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "text"
            assert call_kwargs["json"]["content"]["text"] == "Hello"

    def test_send_text_with_mentions(self):
        """Test sending text with mentions."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = TextBot("test-key")
            bot.send("Hello", mentioned_list=["ou_xxx", "@all"])
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["content"]["mentioned_list"] == [
                "ou_xxx",
                "@all",
            ]

    def test_send_with_sign_secret(self):
        """Test sending message with sign_secret."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = TextBot("test-key", sign_secret="sign-secret")
            bot.send("Hello")
            call_kwargs = mock_post.call_args.kwargs
            assert "timestamp" in call_kwargs["json"]
            assert "sign" in call_kwargs["json"]


class TestPostBot:
    """Tests for PostBot."""

    def test_send_post(self):
        """Test sending post message."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = PostBot("test-key")
            content = [[{"tag": "text", "text": "Hello"}]]
            result = bot.send("Title", content)
            assert result["StatusCode"] == 0
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "post"
            assert call_kwargs["json"]["content"]["post"]["zh_cn"]["title"] == "Title"


class TestImageBot:
    """Tests for ImageBot."""

    def test_send_image(self):
        """Test sending image message."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = ImageBot("test-key")
            result = bot.send("img_xxxx")
            assert result["StatusCode"] == 0
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "image"
            assert call_kwargs["json"]["content"]["image_key"] == "img_xxxx"


class TestInteractiveBot:
    """Tests for InteractiveBot."""

    def test_send_card(self):
        """Test sending interactive card."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = InteractiveBot("test-key")
            card = {"header": {"title": {"tag": "plain_text", "content": "Title"}}}
            result = bot.send(card)
            assert result["StatusCode"] == 0
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "interactive"


class TestSmartBot:
    """Tests for SmartBot."""

    def test_init(self):
        """Test SmartBot initialization."""
        bot = SmartBot("test-key")
        assert bot.text is not None
        assert bot.post is not None
        assert bot.image is not None
        assert bot.interactive is not None

    def test_send_text(self):
        """Test SmartBot sending text."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = SmartBot("test-key")
            bot.send("Hello")
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "text"

    def test_send_image(self):
        """Test SmartBot sending image."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = SmartBot("test-key")
            bot.send({"image_key": "img_xxxx"})
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "image"

    def test_send_card(self):
        """Test SmartBot sending card."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = SmartBot("test-key")
            bot.send({"card": {"header": {}}})
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "interactive"

    def test_send_post(self):
        """Test SmartBot sending post."""
        with patch("pylgb.bot._abstract.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = SmartBot("test-key")
            bot.send(
                {"title": "Title", "content": [[{"tag": "text", "text": "Hello"}]]}
            )
            call_kwargs = mock_post.call_args.kwargs
            assert call_kwargs["json"]["msg_type"] == "post"

    def test_send_unsupported(self):
        """Test SmartBot with unsupported message type."""
        bot = SmartBot("test-key")
        with pytest.raises(ValueError, match="Unsupported message type"):
            bot.send({"unknown": "type"})


class TestSignature:
    """Tests for signature generation."""

    def test_gen_sign(self, monkeypatch):
        """Test signature generation."""
        # Clear env variables first
        monkeypatch.delenv("LARK_SIGN_SECRET", raising=False)
        monkeypatch.delenv("FEISHU_SIGN_SECRET", raising=False)

        bot = TextBot("test-key", sign_secret="sign-secret")
        timestamp = "1234567890"
        sign = bot._gen_sign(timestamp)

        # Verify signature manually using Lark's algorithm:
        # string_to_sign = timestamp + "\n" + secret is the HMAC key
        # Sign an empty string, then Base64 encode
        from base64 import b64encode

        string_to_sign = f"{timestamp}\nsign-secret"
        expected = b64encode(
            hmac.new(
                string_to_sign.encode("utf-8"),
                b"",  # Empty bytes
                digestmod=hashlib.sha256,
            ).digest()
        ).decode("utf-8")

        assert sign == expected

    def test_gen_sign_none(self, monkeypatch):
        """Test signature generation without sign secret."""
        monkeypatch.delenv("LARK_SIGN_SECRET", raising=False)
        monkeypatch.delenv("FEISHU_SIGN_SECRET", raising=False)
        bot = TextBot("test-key", sign_secret=None)
        sign = bot._gen_sign("1234567890")
        assert sign == ""


class TestConstants:
    """Tests for constants."""

    def test_webhook_url(self):
        """Test webhook URL constant."""
        from pylgb._constants import WEBHOOK_URL

        assert WEBHOOK_URL == "https://open.feishu.cn/open-apis/bot/v2/hook/"

    def test_get_env_webhook(self, monkeypatch):
        """Test get_env_webhook function."""
        from pylgb._constants import get_env_webhook

        monkeypatch.delenv("LARK_WEBHOOK", raising=False)
        monkeypatch.delenv("FEISHU_WEBHOOK", raising=False)
        assert get_env_webhook() is None

        monkeypatch.setenv("LARK_WEBHOOK", "lark-key")
        assert get_env_webhook() == "lark-key"

        monkeypatch.delenv("LARK_WEBHOOK")
        monkeypatch.setenv("FEISHU_WEBHOOK", "feishu-key")
        assert get_env_webhook() == "feishu-key"

    def test_get_env_sign_secret(self, monkeypatch):
        """Test get_env_sign_secret function."""
        from pylgb._constants import get_env_sign_secret

        monkeypatch.delenv("LARK_SIGN_SECRET", raising=False)
        monkeypatch.delenv("FEISHU_SIGN_SECRET", raising=False)
        assert get_env_sign_secret() is None

        monkeypatch.setenv("LARK_SIGN_SECRET", "lark-secret")
        assert get_env_sign_secret() == "lark-secret"

    def test_bot_with_env_webhook(self, monkeypatch):
        """Test bot initialization with environment variable."""
        monkeypatch.setenv("LARK_WEBHOOK", "env-webhook-key")

        with patch("requests.post") as mock_post:
            mock_post.return_value = MagicMock(json=lambda: {"StatusCode": 0})
            bot = TextBot()
            bot.send("Hello")
            assert "env-webhook-key" in bot.webhook


class TestEnvVariableSupport:
    """Tests for environment variable support."""

    def test_smartbot_with_env(self, monkeypatch):
        """Test SmartBot with environment variables."""
        monkeypatch.setenv("LARK_WEBHOOK", "env-key")
        monkeypatch.setenv("LARK_SIGN_SECRET", "env-secret")

        bot = SmartBot()
        assert "env-key" in bot.webhook
        assert bot._sign_secret == "env-secret"

    def test_bot_without_webhook_raises(self, monkeypatch):
        """Test that missing webhook raises ValueError."""
        monkeypatch.delenv("LARK_WEBHOOK", raising=False)
        monkeypatch.delenv("FEISHU_WEBHOOK", raising=False)

        with pytest.raises(ValueError, match="webhook is required"):
            TextBot()
