package com.sentinx.service;


import com.sentinx.dto.*;
import com.sentinx.model.TransactionAuditLog;
import com.sentinx.repository.TransactionAuditLogRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.*;

@Service
public class RiskEvaluationService {

    private final RuleEngineService ruleEngine;
    private final FastApiClientService aiClient;
    private final TransactionAuditLogRepository auditRepo;

    public RiskEvaluationService(RuleEngineService ruleEngine, FastApiClientService aiClient, TransactionAuditLogRepository auditRepo) {
        this.ruleEngine = ruleEngine;
        this.aiClient = aiClient;
        this.auditRepo = auditRepo;
    }

    public TransactionEvaluateResponse processTransaction(TransactionEvaluateRequest req) {
        String transactionId = "TXN-" + UUID.randomUUID().toString().substring(0, 13);

        // 1. Layer 1: Deterministic Rules
        var ruleResult = ruleEngine.evaluateRules(req);

        // 2. Layer 2: AI Risk Inference
        FastApiRequest aiReq = new FastApiRequest();
        aiReq.setAmount(req.getAmount());
        aiReq.setActiveCall(req.isActiveCall());
        aiReq.setCallerCountryCode(req.getCallerCountryCode());
        aiReq.setScreenSharing(req.isScreenSharing());
        aiReq.setSimChanged24h(req.isSimChanged24h());
        aiReq.setTranscript(req.getCoerciveTranscriptText());

        FastApiResponse aiResponse = aiClient.inferRisk(aiReq);

        // 3. Action Mapping Logic
        int finalScore = Math.min(100, Math.max(ruleResult.score(), aiResponse.getAiRiskScore()));
        String riskLevel;
        String action;
        boolean requireQuiz = false;
        int panicPause = 0;
        boolean sosAlert = false;

        if (finalScore <= 40) {
            riskLevel = "LOW";
            action = "ALLOW";
        } else if (finalScore <= 75) {
            riskLevel = "MEDIUM";
            action = "WARN";
        } else {
            riskLevel = "HIGH";
            action = "BLOCK_AND_QUIZ";
            panicPause = 30;
            requireQuiz = true;
            sosAlert = true;
        }

        // Combine Reasons
        List<String> combinedReasons = new ArrayList<>(ruleResult.reasons());
        if (aiResponse.getShapFactors() != null) {
            combinedReasons.addAll(aiResponse.getShapFactors());
        }

        // 4. Save to Database
        TransactionAuditLog log = new TransactionAuditLog();
        log.setTransactionId(transactionId);
        log.setUserVpa(req.getUserVpa());
        log.setPayeeVpa(req.getPayeeVpa());
        log.setAmount(req.getAmount());
        log.setRiskScore(finalScore);
        log.setRiskLevel(riskLevel);
        log.setActionTaken(action);
        log.setShapReasons(String.join("; ", combinedReasons));
        log.setActiveCallFlag(req.isActiveCall());
        log.setScreenShareFlag(req.isScreenSharing());
        log.setSimSwapFlag(req.isSimChanged24h());
        auditRepo.save(log);

        // 5. Build Response
        TransactionEvaluateResponse res = new TransactionEvaluateResponse();
        res.setTransactionId(transactionId);
        res.setRiskScore(finalScore);
        res.setRiskLevel(riskLevel);
        res.setAction(action);
        res.setReasons(combinedReasons);

        Map<String, Object> interventions = new HashMap<>();
        interventions.put("panicPauseSeconds", panicPause);
        interventions.put("requireQuiz", requireQuiz);
        interventions.put("sosAlertDispatched", sosAlert);
        res.setInterventions(interventions);
        res.setTimestamp(LocalDateTime.now());

        return res;
    }
}