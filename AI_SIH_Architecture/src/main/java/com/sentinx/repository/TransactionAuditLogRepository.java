package com.sentinx.repository;

import com.sentinx.model.TransactionAuditLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransactionAuditLogRepository extends JpaRepository<TransactionAuditLog, Long> {

    // Spring Data JPA automatically writes the SQL query for this based on the method name!
    List<TransactionAuditLog> findTop20ByOrderByCreatedAtDesc();

}