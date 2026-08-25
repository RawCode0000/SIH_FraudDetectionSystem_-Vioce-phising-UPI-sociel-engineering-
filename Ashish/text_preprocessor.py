#!/usr/bin/env python3
"""
SentinX — Threat-Text Preprocessor & Normalizer
=================================================
A reusable utility for cleaning transcribed text and extracting
phone country codes from strings.

Usage (as a library):
    from text_preprocessor import TextPreprocessor

    tp = TextPreprocessor()
    cleaned = tp.clean_text("This is CBI!!! You are under Digital Arrest.")
    code    = tp.extract_country_code("+855-12345678")

Author : AI Developer — SentinX SIH 2026
"""

from __future__ import annotations

import re


class TextPreprocessor:
    """Cleans and normalizes threat / vishing text for downstream NLP."""

    # Regex: keep letters, digits, whitespace, and '+' (for country codes)
    _CLEAN_PATTERN: re.Pattern[str] = re.compile(r"[^a-zA-Z0-9\s+]")

    # Regex: match international country codes like +91, +95, +855, +1, etc.
    _COUNTRY_CODE_PATTERN: re.Pattern[str] = re.compile(r"\+(\d{1,4})")

    # Default country code when none is found (India)
    _DEFAULT_COUNTRY_CODE: str = "+91"

    # ──────────────────────────────────────────────────────────
    #  Text cleaning
    # ──────────────────────────────────────────────────────────

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize input text.

        Steps:
          1. Return empty string for falsy/None input.
          2. Convert non-string inputs to string.
          3. Remove special characters (keep alphanumeric, spaces, '+').
          4. Collapse multiple whitespace into single space.
          5. Convert to lowercase.
          6. Strip leading/trailing whitespace.

        Parameters
        ----------
        text : str
            Raw input string (e.g. a vishing transcript).

        Returns
        -------
        str
            Cleaned, lowercased text.
        """
        if text is None or text == "":
            return ""

        if not isinstance(text, str):
            text = str(text)

        cleaned = TextPreprocessor._CLEAN_PATTERN.sub(" ", text)
        return " ".join(cleaned.split()).lower()

    # ──────────────────────────────────────────────────────────
    #  Country-code extraction
    # ──────────────────────────────────────────────────────────

    @staticmethod
    def extract_country_code(phone_or_text: str) -> str:
        """Extract an international country code from a string.

        Looks for patterns like +91, +855, +95 anywhere in the input.

        Parameters
        ----------
        phone_or_text : str
            A phone number or free-form text that may contain a
            country code.

        Returns
        -------
        str
            The extracted country code (e.g. '+855'), or '+91'
            (India) if none is found.
        """
        if phone_or_text is None or phone_or_text == "":
            return TextPreprocessor._DEFAULT_COUNTRY_CODE

        if not isinstance(phone_or_text, str):
            phone_or_text = str(phone_or_text)

        match = TextPreprocessor._COUNTRY_CODE_PATTERN.search(phone_or_text)
        if match:
            return f"+{match.group(1)}"

        return TextPreprocessor._DEFAULT_COUNTRY_CODE


# ──────────────────────────────────────────────────────────────
#  Quick demo when run directly
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tp = TextPreprocessor()

    demo_texts = [
        "This is CBI!!! You are under Digital Arrest.",
        "Transfer Rs.48,000 NOW or face arrest!!!",
        "Hey, sending 500 for dinner.",
        "",
    ]

    demo_phones = [
        "+855-9876543",
        "+95 12345678",
        "+91-9999999999",
        "9876543210",
        "",
    ]

    print("SentinX Text Preprocessor — Demo")
    print("=" * 40)

    print("\n--- clean_text() ---")
    for t in demo_texts:
        print(f"  IN : {t!r}")
        print(f"  OUT: {tp.clean_text(t)!r}\n")

    print("--- extract_country_code() ---")
    for p in demo_phones:
        print(f"  IN : {p!r}")
        print(f"  OUT: {tp.extract_country_code(p)!r}\n")
