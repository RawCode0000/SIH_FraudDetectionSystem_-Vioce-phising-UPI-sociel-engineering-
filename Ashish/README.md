# 🛡️ SentinX — AI Developer Module

> **Smart India Hackathon (SIH) 2026**
> Data Engineering · Synthetic Audio · Text Preprocessing · API Testing

---

## 📋 Overview

This is the **AI Developer / Data Engineering** module of the **SentinX** project — a real-time UPI fraud detection system that identifies coerced ("digital arrest") transactions.

### What this module provides

| Deliverable | File | Purpose |
|---|---|---|
| Synthetic Dataset | `data_generator.py` | Generates 2 000 realistic UPI transaction records (80 % normal, 20 % fraud) |
| Mock Vishing Audio | `audio_generator.py` | Creates sample scam/normal `.mp3` files for Whisper testing |
| Text Preprocessor | `text_preprocessor.py` | Cleans transcripts & extracts phone country codes |
| API Scenario Tester | `test_scenarios.py` | Sends 4 pre-built risk scenarios to the backend and validates responses |

### My role in SentinX

```
┌───────────────────────────────────────────────────────┐
│                    SentinX Architecture               │
├───────────┬───────────┬───────────────┬───────────────┤
│ Frontend  │ Backend   │ ML / Risk     │ AI Developer  │ ◄── THIS MODULE
│ (React)   │ (Spring/  │ Engine        │ (Data Eng.)   │
│           │  FastAPI) │               │               │
└───────────┴───────────┴───────────────┴───────────────┘
```

---

## 📁 Project Structure

```
sentinx_ai_developer/
│
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .gitignore
│
├── config.py                  # Centralized configuration
├── data_generator.py          # Synthetic transaction dataset creator
├── audio_generator.py         # Mock vishing audio generator
├── text_preprocessor.py       # Text cleaning & country-code extraction
├── test_scenarios.py          # Automated API scenario tester
│
├── synthetic_transactions.csv # Generated dataset (2 000 records)
│
├── sample_audios/             # Generated mock audio files
│   ├── digital_arrest_sample.mp3
│   ├── customs_narcotics_sample.mp3
│   └── normal_conversation_sample.mp3
│
├── tests/                     # Unit tests (pytest)
│   ├── test_data_generator.py
│   ├── test_text_preprocessor.py
│   └── test_api_payloads.py
│
└── docs/
    └── integration.md         # Integration guide for teammates
```

---

## 🚀 Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the synthetic dataset

```bash
python data_generator.py
```

Output:
```
SentinX Synthetic Dataset Generator
--------------------------------------
Total records : 2000
Normal records: 1600
Fraud records : 400
Fraud ratio   : 20.00%

Dataset validation: PASSED

Saved to: synthetic_transactions.csv
```

### 5. Generate mock vishing audio

> ⚠️ **Internet connection required** — gTTS uses Google's TTS API.

```bash
python audio_generator.py
```

Output:
```
SentinX Mock Vishing Audio Generator
-------------------------------------

Creating digital_arrest_sample.mp3...
  Created successfully.

Creating customs_narcotics_sample.mp3...
  Created successfully.

Creating normal_conversation_sample.mp3...
  Created successfully.

All sample audio files generated in 'sample_audios/'.
```

### 6. Run unit tests

```bash
python -m pytest tests/ -v
```

### 7. Run API scenario tests

> The backend must be running for this step. If it isn't, you'll get a clear error message.

```bash
python test_scenarios.py
```

---

## ⚙️ Configuration

All settings are centralized in `config.py` and can be overridden via **environment variables**:

| Setting | Env Variable | Default |
|---|---|---|
| Dataset size | `SENTINX_DATASET_SIZE` | `2000` |
| Random seed | `SENTINX_RANDOM_SEED` | `42` |
| CSV output path | `SENTINX_DATASET_OUTPUT` | `synthetic_transactions.csv` |
| Audio output dir | `SENTINX_AUDIO_DIR` | `sample_audios` |
| API URL | `SENTINX_API_URL` | `http://localhost:8000/api/v1/infer-risk` |
| API timeout (sec) | `SENTINX_API_TIMEOUT` | `10` |

### Switching between FastAPI and Spring Boot

```bash
# FastAPI (default)
set SENTINX_API_URL=http://localhost:8000/api/v1/infer-risk

# Spring Boot
set SENTINX_API_URL=http://localhost:8080/api/v1/transaction/evaluate
```

---

## 📊 Dataset Columns

| Column | Type | Description |
|---|---|---|
| `amount` | float | Transaction amount in ₹ |
| `is_active_call` | 0/1 | Whether a phone call was active during the transaction |
| `is_foreign_call` | 0/1 | Whether the call originated from a foreign number (+855, +95) |
| `is_screen_sharing` | 0/1 | Whether screen sharing was active |
| `is_sim_changed_24h` | 0/1 | Whether the SIM was changed in the last 24 hours |
| `nlp_coercion_score` | float (0–1) | NLP-derived coercion score from the call transcript |
| `is_fraud` | 0/1 | Label — 0 = normal, 1 = fraud/coerced |

---

## 🔌 API Payload Format

The scenario tester sends POST requests with this JSON shape:

```json
{
  "amount": 450.0,
  "isActiveCall": false,
  "callerCountryCode": "+91",
  "isScreenSharing": false,
  "isSimChanged24h": false,
  "transcript": "Transferring money for lunch groceries."
}
```

### Expected response

The tester supports **both** response formats:

**FastAPI style:**
```json
{
  "aiRiskScore": 25,
  "shapFactors": ["amount_low", "no_active_call"]
}
```

**Spring Boot style:**
```json
{
  "risk_score": 25,
  "shap_reasons": ["amount_low", "no_active_call"]
}
```

---

## 🛠 Text Preprocessor Usage

```python
from text_preprocessor import TextPreprocessor

tp = TextPreprocessor()

# Clean a vishing transcript
cleaned = tp.clean_text("This is CBI!!! You are under Digital Arrest.")
# → "this is cbi you are under digital arrest"

# Extract country code from a phone string
code = tp.extract_country_code("+855-9876543")
# → "+855"

# No country code found → defaults to "+91"
code = tp.extract_country_code("9876543210")
# → "+91"
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'gtts'` | Run `pip install -r requirements.txt` |
| `audio_generator.py` fails | Check your internet connection (gTTS needs it) |
| `test_scenarios.py` shows Connection Error | Start the backend server first |
| Wrong API URL | Set `SENTINX_API_URL` environment variable |
| Dataset validation fails | Check `config.py` for correct parameters |

---

## 📦 Integration

See **[docs/integration.md](docs/integration.md)** for detailed instructions on how each teammate should integrate with this module.

---

## 📝 Technology Stack

- **Python 3.10+**
- **pandas** — DataFrame operations & CSV export
- **numpy** — Random distributions for synthetic data
- **gTTS** — Google Text-to-Speech for mock audio
- **requests** — HTTP client for API testing
- **pytest** — Unit testing framework

---

## 🔒 Security & Privacy

- All data is **100% synthetic** — no real personal information
- No real banking details, phone numbers, or credentials
- No API keys or secrets are committed
- `.env` files are excluded via `.gitignore`

---

## 📄 License

Internal project for SIH 2026. Not for public distribution.
