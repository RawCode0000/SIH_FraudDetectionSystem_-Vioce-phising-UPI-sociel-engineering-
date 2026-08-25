#!/usr/bin/env python3
"""
SentinX — Automated API Scenario Tester
=========================================
Sends pre-defined test payloads to the SentinX backend and validates
the returned risk scores against expected ranges.

Configuration:
  • Set SENTINX_API_URL   env var to point to your backend
    (default: http://localhost:8000/api/v1/infer-risk)
  • Set SENTINX_API_TIMEOUT env var for request timeout in seconds
    (default: 10)

Usage:
    python test_scenarios.py

Author : AI Developer — SentinX SIH 2026
"""

from __future__ import annotations

import json
import sys
from typing import Any

import requests

from config import API_TIMEOUT, API_URL


# ──────────────────────────────────────────────────────────────
#  Test scenarios (from PDF specification)
# ──────────────────────────────────────────────────────────────

TEST_CASES: list[dict[str, Any]] = [
    {
        "name": "Scenario 1: Normal Legitimate Payment",
        "description": "Low Risk — routine payment, no suspicious signals",
        "payload": {
            "amount": 450.0,
            "isActiveCall": False,
            "callerCountryCode": "+91",
            "isScreenSharing": False,
            "isSimChanged24h": False,
            "transcript": "Transferring money for lunch groceries.",
        },
        "expected_score_range": (0, 40),
    },
    {
        "name": "Scenario 2: Active Call Only",
        "description": "Medium Risk Warning — active call during transaction",
        "payload": {
            "amount": 2500.0,
            "isActiveCall": True,
            "callerCountryCode": "+91",
            "isScreenSharing": False,
            "isSimChanged24h": False,
            "transcript": "Please send the payment quickly.",
        },
        "expected_score_range": (20, 60),
    },
    {
        "name": "Scenario 3: Severe Digital Arrest + Foreign Call",
        "description": "High Risk / Panic Pause — coercion, foreign code, screen sharing",
        "payload": {
            "amount": 48000.0,
            "isActiveCall": True,
            "callerCountryCode": "+855",
            "isScreenSharing": True,
            "isSimChanged24h": False,
            "transcript": (
                "This is CBI. You are under Digital Arrest for money laundering. "
                "Transfer 48000 immediately or police will arrest you."
            ),
        },
        "expected_score_range": (76, 100),
    },
    {
        "name": "Scenario 4: Customs Narcotics Scam + Screen Share",
        "description": "High Risk / Panic Pause — narcotics coercion, foreign code, screen share, SIM swap",
        "payload": {
            "amount": 35000.0,
            "isActiveCall": True,
            "callerCountryCode": "+95",
            "isScreenSharing": True,
            "isSimChanged24h": True,
            "transcript": (
                "Customs Mumbai Airport. A FedEx parcel sent to Cambodia "
                "containing illegal MDMA drugs was seized with your Aadhaar card. "
                "Transfer penalty deposit immediately or face arrest."
            ),
        },
        "expected_score_range": (76, 100),
    },
]


# Required keys every payload must contain
REQUIRED_PAYLOAD_KEYS: set[str] = {
    "amount",
    "isActiveCall",
    "callerCountryCode",
    "isScreenSharing",
    "isSimChanged24h",
    "transcript",
}


# ──────────────────────────────────────────────────────────────
#  Helper: extract risk score from response (supports both
#  FastAPI and Spring Boot response formats)
# ──────────────────────────────────────────────────────────────

def _extract_risk_score(data: dict[str, Any]) -> float | None:
    """Try to extract risk score from response, supporting both naming conventions.
    
    Explicitly distinguishes missing key/value from legitimate 0 score.
    """
    if not isinstance(data, dict):
        return None

    raw_score = None
    if "aiRiskScore" in data and data["aiRiskScore"] is not None:
        raw_score = data["aiRiskScore"]
    elif "risk_score" in data and data["risk_score"] is not None:
        raw_score = data["risk_score"]

    if raw_score is not None:
        try:
            return float(raw_score)
        except (ValueError, TypeError):
            return None
    return None


def _extract_shap_reasons(data: dict[str, Any]) -> list[Any]:
    """Try to extract SHAP reasons from response, supporting both naming conventions."""
    if not isinstance(data, dict):
        return []

    if "shapFactors" in data and isinstance(data["shapFactors"], list):
        return data["shapFactors"]
    if "shap_reasons" in data and isinstance(data["shap_reasons"], list):
        return data["shap_reasons"]
    return []


# ──────────────────────────────────────────────────────────────
#  Test runner
# ──────────────────────────────────────────────────────────────

def run_single_test(
    test_case: dict[str, Any],
    api_url: str = API_URL,
    timeout: int = API_TIMEOUT,
) -> dict[str, Any]:
    """Execute a single scenario test against the backend.

    Returns a result dict with keys:
      name, status ('PASS'|'FAIL'|'ERROR'), score, expected,
      shap_reasons, error_message
    """
    name = test_case["name"]
    payload = test_case["payload"]
    min_score, max_score = test_case["expected_score_range"]

    result: dict[str, Any] = {
        "name": name,
        "status": "ERROR",
        "score": None,
        "expected": f"{min_score}–{max_score}",
        "shap_reasons": [],
        "error_message": None,
    }

    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )
    except requests.exceptions.ConnectionError:
        result["error_message"] = (
            f"Connection Error:\n"
            f"The SentinX backend could not be reached.\n\n"
            f"Make sure the backend server is running at:\n"
            f"  {api_url}"
        )
        return result
    except requests.exceptions.Timeout:
        result["error_message"] = (
            f"Timeout Error:\n"
            f"The backend did not respond within {timeout} seconds.\n"
            f"  URL: {api_url}"
        )
        return result
    except requests.exceptions.RequestException as exc:
        result["error_message"] = f"Request Error: {exc}"
        return result

    # Check HTTP status
    if response.status_code != 200:
        result["error_message"] = (
            f"HTTP Error: Server returned status code {response.status_code}\n"
            f"  Response: {response.text[:500]}"
        )
        return result

    # Parse JSON
    try:
        data = response.json()
    except (json.JSONDecodeError, ValueError):
        result["error_message"] = (
            "Invalid JSON: Could not parse the server response.\n"
            f"  Raw response: {response.text[:500]}"
        )
        return result

    # Extract risk score
    score = _extract_risk_score(data)
    if score is None:
        result["error_message"] = (
            "Missing risk score: The response does not contain "
            "'aiRiskScore' or 'risk_score'.\n"
            f"  Response keys: {list(data.keys())}"
        )
        return result

    result["score"] = score
    result["shap_reasons"] = _extract_shap_reasons(data)

    # Evaluate pass/fail
    if min_score <= score <= max_score:
        result["status"] = "PASS"
    else:
        result["status"] = "FAIL"
        result["error_message"] = (
            f"Score {score} is outside expected range {min_score}–{max_score}"
        )

    return result


def run_all_tests(
    api_url: str = API_URL,
    timeout: int = API_TIMEOUT,
) -> list[dict[str, Any]]:
    """Run all test scenarios and return results."""
    return [
        run_single_test(tc, api_url=api_url, timeout=timeout)
        for tc in TEST_CASES
    ]


# ──────────────────────────────────────────────────────────────
#  Pretty-print results
# ──────────────────────────────────────────────────────────────

def print_results(results: list[dict[str, Any]]) -> None:
    """Print a formatted test report."""
    sep = "=" * 50

    print(f"\n{sep}")
    print("SentinX Automated Scenario Tests")
    print(sep)

    for r in results:
        print(f"\nRunning: {r['name']}")
        if r["status"] == "PASS":
            print(f"  Status    : PASS")
            print(f"  Risk Score: {r['score']}")
            print(f"  Expected  : {r['expected']}")
            if r["shap_reasons"]:
                print(f"  SHAP Reasons: {r['shap_reasons']}")
        elif r["status"] == "FAIL":
            print(f"  Status    : FAIL")
            print(f"  Risk Score: {r['score']}")
            print(f"  Expected  : {r['expected']}")
            if r["error_message"]:
                print(f"  Detail    : {r['error_message']}")
            if r["shap_reasons"]:
                print(f"  SHAP Reasons: {r['shap_reasons']}")
        else:
            print(f"  Status: ERROR")
            if r["error_message"]:
                print(f"  {r['error_message']}")

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    errors = sum(1 for r in results if r["status"] == "ERROR")

    print(f"\n{sep}")
    print("Test Summary")
    print(sep)
    print(f"  Passed : {passed}")
    print(f"  Failed : {failed}")
    print(f"  Errors : {errors}")
    print(sep)


# ──────────────────────────────────────────────────────────────
#  CLI entry point
# ──────────────────────────────────────────────────────────────

def main() -> int:
    """Run all scenario tests and return an exit code.

    Returns
    -------
    int
        0 if all tests pass, 1 otherwise.
    """
    print(f"Backend URL : {API_URL}")
    print(f"Timeout     : {API_TIMEOUT}s")

    results = run_all_tests()
    print_results(results)

    all_passed = all(r["status"] == "PASS" for r in results)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
