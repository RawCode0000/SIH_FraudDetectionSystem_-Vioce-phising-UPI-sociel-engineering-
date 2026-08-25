package com.sentinx.dto;


import lombok.Data;

@Data
public class TransactionEvaluateRequest {
    private String userVpa;
    private String payeeVpa;
    private Double amount;
    private boolean isActiveCall;
    private String callerCountryCode;
    private boolean isScreenSharing;
    private boolean isSimChanged24h;
    private String coerciveTranscriptText;
    private String deviceFingerprint;
}