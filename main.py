from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from orchestrator import SentinXAgenticOrchestrator

app = FastAPI(title="SentinX Agentic Intervention Engine")
orchestrator = SentinXAgenticOrchestrator()

class TransactionPayload(BaseModel):
    transaction_id: str
    user_name: str
    user_vpa: str
    payee_vpa: str
    amount: float
    ml_risk_score: int
    nlp_score: float
    shap_reasons: List[str]
    is_screen_sharing: bool
    is_active_call: bool
    caller_country_code: str
    transcript: str

@app.post("/api/v1/evaluate-risk")
def evaluate_risk(payload: TransactionPayload):
    result = orchestrator.process_transaction(
        transaction_id=payload.transaction_id,
        user_name=payload.user_name,
        user_vpa=payload.user_vpa,
        payee_vpa=payload.payee_vpa,
        amount=payload.amount,
        ml_risk_score=payload.ml_risk_score,
        nlp_score=payload.nlp_score,
        shap_reasons=payload.shap_reasons,
        is_screen_sharing=payload.is_screen_sharing,
        is_active_call=payload.is_active_call,
        caller_country_code=payload.caller_country_code,
        transcript=payload.transcript
    )
    return result
@app.get("/")
def read_root():
    return {"status": "SentinX API active", "docs": "/docs"}