package com.sentinx.dto;




import lombok.Data;
import java.util.List;

@Data
public class FastApiResponse {
    private int aiRiskScore;
    private boolean anomalyFlag;
    private List<String> shapFactors;
    private String threatCategory;
}