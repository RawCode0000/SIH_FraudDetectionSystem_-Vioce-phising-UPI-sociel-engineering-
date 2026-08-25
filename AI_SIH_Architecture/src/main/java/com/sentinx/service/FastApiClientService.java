package com.sentinx.service;


import com.sentinx.dto.FastApiRequest;
import com.sentinx.dto.FastApiResponse;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class FastApiClientService {

    private final WebClient webClient;

    public FastApiClientService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl("http://localhost:8000").build();
    }

    public FastApiResponse inferRisk(FastApiRequest request) {
        try {
            return webClient.post()
                    .uri("/api/v1/infer-risk")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(FastApiResponse.class)
                    .block(); // Synchronous block for simplicity in evaluating
        } catch (Exception e) {
            // Fallback gracefully if AI is down
            FastApiResponse fallback = new FastApiResponse();
            fallback.setAiRiskScore(0);
            fallback.setAnomalyFlag(false);
            fallback.setShapFactors(List.of("AI Service Unavailable"));
            return fallback;
        }
    }
}