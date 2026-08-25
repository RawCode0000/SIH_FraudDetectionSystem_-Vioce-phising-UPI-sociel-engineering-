#!/usr/bin/env python3
"""
SentinX — Mock Vishing Audio Generator
========================================
Creates sample vishing / scam audio files using Google Text-to-Speech
(gTTS) so that the Whisper / speech-to-text teammate can test their
transcription pipeline without needing live phone calls.

Requirements:
  • Internet connection (gTTS calls the Google Translate TTS API)
  • gTTS installed (pip install gTTS)

Usage:
    python audio_generator.py

Generated files (inside sample_audios/):
    digital_arrest_sample.mp3
    customs_narcotics_sample.mp3
    normal_conversation_sample.mp3

Author : AI Developer — SentinX SIH 2026
"""

from __future__ import annotations

import os
import sys

from config import AUDIO_OUTPUT_DIR


# ──────────────────────────────────────────────────────────────
#  Scam / Normal scripts (from PDF specification)
# ──────────────────────────────────────────────────────────────

SCAM_SCRIPTS: dict[str, str] = {
    "digital_arrest_sample.mp3": (
        "This is Officer Sharma from Delhi Cyber Crime CBI. "
        "An illegal parcel with forged passports has been found "
        "registered in your name. You are hereby placed under "
        "Digital Arrest. You must transfer Rupees 45,000 immediately "
        "to verify your bank account, or a warrant will be issued "
        "within the next thirty minutes. Do not disconnect this call."
    ),
    "customs_narcotics_sample.mp3": (
        "This is Customs Office, Mumbai Airport. A FedEx parcel "
        "addressed to Cambodia containing illegal MDMA drugs was "
        "seized by our narcotics division. Your Aadhaar card details "
        "were found inside the parcel. You are required to pay a "
        "penalty deposit immediately to clear your name. Failure to "
        "comply will result in arrest under the Narcotics Act."
    ),
    "normal_conversation_sample.mp3": (
        "Hey Rahul, I am transferring five hundred rupees for "
        "yesterday's dinner bill. Let me know once you receive it. "
        "By the way, are we still meeting for the project discussion "
        "tomorrow evening?"
    ),
}


# ──────────────────────────────────────────────────────────────
#  Generator
# ──────────────────────────────────────────────────────────────

def create_mock_vishing_audios(output_dir: str = AUDIO_OUTPUT_DIR) -> bool:
    """Generate all mock vishing audio files.

    Parameters
    ----------
    output_dir : str
        Directory in which to save the .mp3 files.

    Returns
    -------
    bool
        True if all files were created successfully.
    """
    try:
        from gtts import gTTS  # noqa: WPS433 — intentional late import
    except ImportError:
        print(
            "ERROR: gTTS is not installed.\n"
            "Install it with:  pip install gTTS\n"
            "Note: gTTS requires an internet connection."
        )
        return False

    os.makedirs(output_dir, exist_ok=True)

    success_count = 0
    total = len(SCAM_SCRIPTS)

    for filename, text in SCAM_SCRIPTS.items():
        filepath = os.path.join(output_dir, filename)
        print(f"\nCreating {filename}...")

        try:
            tts = gTTS(text=text, lang="en", tld="co.in")
            tts.save(filepath)
            print("  Created successfully.")
            success_count += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR generating {filename}: {exc}")
            print(
                "  Hint: gTTS requires an active internet connection.\n"
                "  Make sure you are connected and try again."
            )

    return success_count == total


# ──────────────────────────────────────────────────────────────
#  CLI entry point
# ──────────────────────────────────────────────────────────────

def main() -> None:
    """Generate all sample audio files and print summary."""
    print("SentinX Mock Vishing Audio Generator")
    print("-" * 37)

    success = create_mock_vishing_audios()

    if success:
        print(f"\nAll sample audio files generated in '{AUDIO_OUTPUT_DIR}/'.")
    else:
        print("\nSome audio files could not be generated. See errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
