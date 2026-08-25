from datetime import datetime
from typing import Dict, Any
class GuardianSOSAgent:
    def generate_sos_payload(
        self,
        user_name: str,
        guardian_phone: str,
        amount: float,
        caller_country_code: str,
        threat_type: str,
        risk_score: int
    ) -> Dict[str, Any]:
        """
        Creates automated SOS emergency dispatch payload for family members.
        """
        message = (
            f"🚨 EMERGENCY ALERT: High-risk UPI transfer of ₹{amount:,.2f} initiated by {user_name} "
            f"while on an active call ({caller_country_code}). SentinX detected {threat_type.replace('_', ' ')} coercion "
            f"(Risk Score: {risk_score}/100) and activated a 30s Panic Pause. "
            f"Please call them immediately to prevent fraud!"
        )
        return {
            "recipient": guardian_phone,
            "channel": "SMS_RELAY",
            "dispatch_timestamp": datetime.now().isoformat(),
            "alert_level": "CRITICAL",
            "message": message,
            "override_token": "SOS-TOKEN-VERIFY-9021"
        }
