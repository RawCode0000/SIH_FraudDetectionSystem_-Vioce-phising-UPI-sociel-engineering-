package com.sentinx.dto;


import lombok.Data;

@Data
public class FastApiRequest {
    private Double amount;
    private boolean isActiveCall;
    private String callerCountryCode;
    private boolean isScreenSharing;
    private boolean isSimChanged24h;
    private String transcript;
}