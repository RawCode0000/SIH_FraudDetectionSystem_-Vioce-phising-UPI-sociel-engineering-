package com.sentinx.model;


import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String userVpa;
    private String phoneNumber;
    private String currentImsiToken;
    private LocalDateTime lastSimSwapTimestamp;
    private String deviceFingerprint;
}