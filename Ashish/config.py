"""
SentinX AI Developer Module — Configuration
=============================================
Centralized configuration for dataset generation, audio output,
API testing, and other module-wide settings.

All values use sensible defaults from the SentinX SIH 2026
specification and can be overridden via environment variables
where noted.
"""

import os


# ─────────────────────────────────────────────
# Dataset Generation
# ─────────────────────────────────────────────
DATASET_NUM_SAMPLES: int = int(os.getenv("SENTINX_DATASET_SIZE", "2000"))
DATASET_RANDOM_SEED: int = int(os.getenv("SENTINX_RANDOM_SEED", "42"))
DATASET_OUTPUT_FILE: str = os.getenv(
    "SENTINX_DATASET_OUTPUT", "synthetic_transactions.csv"
)

# Normal / Fraud split ratio
NORMAL_RATIO: float = 0.80  # 80% normal
FRAUD_RATIO: float = 0.20   # 20% fraud

# Amount distribution parameters (gamma for normal, uniform for fraud)
NORMAL_GAMMA_SHAPE: float = 2.5
NORMAL_GAMMA_SCALE: float = 1200.0
FRAUD_AMOUNT_MIN: float = 25_000.0
FRAUD_AMOUNT_MAX: float = 90_000.0

# NLP coercion score ranges
NORMAL_NLP_MIN: float = 0.0
NORMAL_NLP_MAX: float = 0.20
FRAUD_NLP_MIN: float = 0.75
FRAUD_NLP_MAX: float = 0.99

# Country codes referenced in the specification
COUNTRY_CODE_INDIA: str = "+91"
COUNTRY_CODES_FOREIGN: list[str] = ["+855", "+95"]

# ─────────────────────────────────────────────
# Audio Generation
# ─────────────────────────────────────────────
AUDIO_OUTPUT_DIR: str = os.getenv("SENTINX_AUDIO_DIR", "sample_audios")

# ─────────────────────────────────────────────
# API Scenario Testing
# ─────────────────────────────────────────────
API_URL: str = os.getenv(
    "SENTINX_API_URL",
    "http://localhost:8000/api/v1/infer-risk",
)
API_TIMEOUT: int = int(os.getenv("SENTINX_API_TIMEOUT", "10"))

# ─────────────────────────────────────────────
# Dataset Column Names
# ─────────────────────────────────────────────
COL_AMOUNT: str = "amount"
COL_ACTIVE_CALL: str = "is_active_call"
COL_FOREIGN_CALL: str = "is_foreign_call"
COL_SCREEN_SHARING: str = "is_screen_sharing"
COL_SIM_CHANGED: str = "is_sim_changed_24h"
COL_NLP_SCORE: str = "nlp_coercion_score"
COL_FRAUD: str = "is_fraud"

DATASET_COLUMNS: list[str] = [
    COL_AMOUNT,
    COL_ACTIVE_CALL,
    COL_FOREIGN_CALL,
    COL_SCREEN_SHARING,
    COL_SIM_CHANGED,
    COL_NLP_SCORE,
    COL_FRAUD,
]
