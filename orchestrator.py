from quiz_agent import StatutoryQuizAgent
from guardian_agent import GuardianSOSAgent
from i4c_incident_agent import I4CIncidentSyncAgent
class SentinXAgenticOrchestrator:
    def __init__(self):
        self.quiz_agent = StatutoryQuizAgent()
        self.guardian_agent = GuardianSOSAgent()
        self.i4c_agent = I4CIncidentSyncAgent()
    def process_transaction(
        self,
        transaction_id: str,
        user_name: str,
        user_vpa: str,
        payee_vpa: str,
        amount: float,
        ml_risk_score: int,
        nlp_score: float,
        shap_reasons: list,
        is_screen_sharing: bool,
        is_active_call: bool,
        caller_country_code: str,
        transcript: str
    ) -> dict:
        # 1. Master Risk Fusion
        final_risk_score = min(100, int(round((ml_risk_score * 0.6) + (nlp_score * 40))))
        
        # 2. Determine Action State
        if final_risk_score <= 40:
            return {
                "risk_score": final_risk_score,
                "risk_level": "LOW",
                "action": "ALLOW",
                "interventions": None,
                "shap_factors": shap_reasons
            }

        elif final_risk_score <= 75:
            return {
                "risk_score": final_risk_score,
                "risk_level": "MEDIUM",
                "action": "WARN",
                "interventions": {
                    "show_modal": True,
                    "requires_user_acknowledgment": True
                },
                "shap_factors": shap_reasons
            }

        else:
            # HIGH RISK -> Cognitive Circuit Breaker
            threat_type = "REMOTE_ACCESS_TAKEOVER" if is_screen_sharing else "DIGITAL_ARREST"
            quiz = self.quiz_agent.generate_quiz(threat_type)
            sos_payload = self.guardian_agent.generate_sos_payload(
                user_name=user_name,
                guardian_phone="+919876500000",
                amount=amount,
                caller_country_code=caller_country_code,
                threat_type=threat_type,
                risk_score=final_risk_score
            )
            i4c_report = self.i4c_agent.package_incident_report(
                transaction_id=transaction_id,
                user_vpa=user_vpa,
                payee_vpa=payee_vpa,
                amount=amount,
                risk_score=final_risk_score,
                shap_factors=shap_reasons,
                transcript_snippet=transcript
            )

            return {
                "risk_score": final_risk_score,
                "risk_level": "HIGH",
                "action": "BLOCK_AND_QUIZ",
                "interventions": {
                    "panic_pause_seconds": 30,
                    "statutory_quiz": quiz,
                    "guardian_sos_dispatched": sos_payload,
                    "i4c_sync_payload": i4c_report
                },
                "shap_factors": shap_reasons
            }

# Quick Local Verification Test:
if __name__ == "__main__":
    orchestrator = SentinXAgenticOrchestrator()
    result = orchestrator.process_transaction(
        transaction_id="TXN-908124",
        user_name="Ankit Panda",
        user_vpa="ankit@okaxis",
        payee_vpa="scam_merchant@upi",
        amount=45000.0,
        ml_risk_score=85,
        nlp_score=0.92,
        shap_reasons=["Coercive authority triggers ('CBI', 'Digital Arrest')", "Active foreign call (+855)"],
        is_screen_sharing=True,
        is_active_call=True,
        caller_country_code="+855",
        transcript="This is CBI. Transfer 45000 now."
    )
    print("Orchestration Output:\n", result)
