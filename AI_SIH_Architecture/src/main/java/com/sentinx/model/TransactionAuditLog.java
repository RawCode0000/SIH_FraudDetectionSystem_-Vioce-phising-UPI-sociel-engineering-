package com.sentinx.model;



import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "transaction_audit_logs")
public class TransactionAuditLog {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String transactionId;
    private String userVpa;
    private String payeeVpa;
    private Double amount;

    private Integer riskScore;
    private String riskLevel;
    private String actionTaken;

    @Column(columnDefinition = "TEXT")
    private String shapReasons;

    private Boolean activeCallFlag;
    private Boolean screenShareFlag;
    private Boolean simSwapFlag;

    private LocalDateTime createdAt = LocalDateTime.now();
}