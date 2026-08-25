from typing import Dict, Any
class StatutoryQuizAgent:
    def __init__(self):
        # Statutory Legal Ground Truth Database (MHA / I4C / RBI Directives)
        self.legal_kb = {
            "DIGITAL_ARREST": {
                "title": "⚖️ Statutory Legal Reality Check: Digital Arrest",
                "question": "A caller claiming to be a CBI / Police / Customs officer is demanding money via UPI to avoid arrest. Is 'Digital Arrest' legally valid in India?",
                "options": [
                    {"id": "A", "text": "Yes, law enforcement agencies can issue warrants and bail over video calls.", "is_correct": False},
                    {"id": "B", "text": "No, 'Digital Arrest' does not exist in Indian Law. Police/CBI never collect money via UPI.", "is_correct": True}
                ],
                "correct_id": "B",
                "statutory_reference": "MHA / I4C Advisory: Indian Law has no provision for 'Digital Arrest'. All such calls are fraudulent extortion."
            },
            "REMOTE_ACCESS_TAKEOVER": {
                "title": "⚠️ Remote Desktop Security Verification",
                "question": "An external caller asked you to install AnyDesk/TeamViewer to 'verify' your account. What does this enable?",
                "options": [
                    {"id": "A", "text": "It provides safe remote assistance certified by the bank.", "is_correct": False},
                    {"id": "B", "text": "It allows the caller to view your screen, read OTPs, and control your device.", "is_correct": True}
                ],
                "correct_id": "B",
                "statutory_reference": "RBI Cyber Security Directive: Banks never instruct customers to install third-party screen sharing applications."
            }
        }
    def generate_quiz(self, threat_category: str = "DIGITAL_ARREST") -> Dict[str, Any]:
        return self.legal_kb.get(threat_category, self.legal_kb["DIGITAL_ARREST"])
