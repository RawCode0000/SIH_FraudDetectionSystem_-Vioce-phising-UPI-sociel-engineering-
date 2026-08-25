package com.sentinx.service;


import com.sentinx.dto.TransactionEvaluateRequest;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class RuleEngineService {

    public RuleResult evaluateRules(TransactionEvaluateRequest req) {
        int ruleScore = 0;
        List<String> ruleReasons = new ArrayList<>();

        // Rule 1: Hardware SIM-Swap 24-Hr Lock
        if (req.isSimChanged24h()) {
            ruleScore += 45;
            ruleReasons.add("Hardware SIM-Swap detected within mandatory 24-hour cooling window.");
        }

        // Rule 2: Remote Screen-Share Blocker
        if (req.isScreenSharing()) {
            ruleScore += 35;
            ruleReasons.add("Active remote desktop / accessibility service detected (AnyDesk/TeamViewer).");
        }

        // Rule 3: Suspicious Foreign / Unsaved Call
        List<String> foreignCodes = List.of("+855", "+95", "+1", "+44");
        if (req.isActiveCall() && foreignCodes.contains(req.getCallerCountryCode())) {
            ruleScore += 40;
            ruleReasons.add("Active foreign phone call (" + req.getCallerCountryCode() + ") in progress during transaction initiation.");
        }

        // Rule 4: Blacklisted Payee VPA
        String payee = req.getPayeeVpa() != null ? req.getPayeeVpa().toLowerCase() : "";
        if (payee.contains("scam") || payee.contains("fraud") || payee.contains("fake")) {
            ruleScore += 50;
            ruleReasons.add("Recipient VPA flagged in national fraud registry.");
        }

        return new RuleResult(ruleScore, ruleReasons);
    }

    public record RuleResult(int score, List<String> reasons) {}
}