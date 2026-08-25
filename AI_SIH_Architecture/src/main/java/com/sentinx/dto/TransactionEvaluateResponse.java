package com.sentinx.dto;


import lombok.Data;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Data
public class TransactionEvaluateResponse {
    private String transactionId;
    private int riskScore;
    private String riskLevel;
    private String action;
    private List<String> reasons;
    private Map<String, Object> interventions;
    private LocalDateTime timestamp;
}