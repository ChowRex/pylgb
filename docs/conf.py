#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sphinx configuration."""

project = "pylgb"
author = "ChowRex"
version = "0.1.0"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
