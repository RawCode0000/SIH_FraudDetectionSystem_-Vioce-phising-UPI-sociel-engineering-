package com.sentinx.controller;


import com.sentinx.dto.TransactionEvaluateRequest;
import com.sentinx.dto.TransactionEvaluateResponse;
import com.sentinx.model.TransactionAuditLog;
import com.sentinx.repository.TransactionAuditLogRepository;
import com.sentinx.service.RiskEvaluationService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1")
@CrossOrigin(origins = "*") // Allows React frontend to communicate
public class SentinXController {

    private final RiskEvaluationService riskService;
    private final TransactionAuditLogRepository auditRepo;

    public SentinXController(RiskEvaluationService riskService, TransactionAuditLogRepository auditRepo) {
        this.riskService = riskService;
        this.auditRepo = auditRepo;
    }

    // Endpoint 1: Main Risk Evaluation
    @PostMapping("/transaction/evaluate")
    public TransactionEvaluateResponse evaluateTransaction(@RequestBody TransactionEvaluateRequest request) {
        return riskService.processTransaction(request);
    }

    // Endpoint 2: Bank SOC Analyst Stream
    @GetMapping("/analyst/threat-stream")
    public List<TransactionAuditLog> getThreatStream() {
        // Uses derived query: findTop20ByOrderByCreatedAtDesc() in repository
        return auditRepo.findTop20ByOrderByCreatedAtDesc();
    }

    // Endpoint 3: 1-Click 1930 / I4C Portal Sync
    @PostMapping("/report/i4c-sync")
    public Map<String, Object> syncWithI4c(@RequestBody Map<String, String> payload) {
        // Mocking the external sync
        String ackNumber = "I4C-CFCFRMS-" + LocalDateTime.now().getYear() + "-" + (int)(Math.random() * 900000 + 100000);
        return Map.of(
                "status", "SUCCESS",
                "i4cAcknowledgmentNumber", ackNumber,
                "freezeOrderDispatched", true,
                "message", "Telemetry successfully synced with National Cybercrime 1930 Portal."
        );
    }
}