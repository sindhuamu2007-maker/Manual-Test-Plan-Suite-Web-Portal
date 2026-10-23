# Requirements Traceability Matrix (RTM)
**Project Name:** Enterprise Web Portal  
**Document ID:** RTM-WEBPORTAL-2026-V1.0  
**Associated Test Plan:** TP-WEBPORTAL-2026-V1.0  
**QA Owner:** QA Intern  
**Date:** October 2026  
**Coverage Status:** 100% Requirements Covered  

---

## 1. Overview & Purpose
The Requirements Traceability Matrix (RTM) establishes bidirectional traceability between Business/Functional Requirements (BRD/FRD), Test Scenarios, Test Cases, and Execution Outcomes. It ensures that every specified requirement is rigorously verified and no functional gap exists before production sign-off.

---

## 2. Traceability Matrix Table

| Req ID | Requirement Description | Test Scenario ID | Test Case ID | Test Type | Execution Status | Defect ID (if any) |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **REQ-AUTH-01** | User authentication with valid email and password credentials | TS_AUTH_01 | **TC_AUTH_001** | Functional (Positive) | **PASS** | None |
| **REQ-AUTH-02** | Graceful rejection and error handling for invalid/unregistered credentials | TS_AUTH_02 | **TC_AUTH_002**<br>**TC_AUTH_003** | Functional (Negative) | **PASS**<br>**PASS** | None |
| **REQ-AUTH-03** | Brute-force protection / rate limiting after 5 consecutive failures | TS_AUTH_03 | **TC_AUTH_004** | Security | **PASS** | None |
| **REQ-AUTH-04** | Client-side mandatory input field validations on login submission | TS_AUTH_04 | **TC_AUTH_005** | Functional (Negative) | **PASS** | None |
| **REQ-AUTH-05** | UI password masking with visibility eye toggle control | TS_AUTH_05 | **TC_AUTH_006** | UI/UX | **PASS** | None |
| **REQ-AUTH-06** | Self-service forgot password email recovery flow with secure token | TS_AUTH_06 | **TC_AUTH_007** | Functional (Positive) | **PASS** | None |
| **REQ-AUTH-07** | Automated expiration of password reset link after 15 minutes | TS_AUTH_07 | **TC_AUTH_008** | Security | **PASS** | None |
| **REQ-AUTH-08** | Invalidation of user session upon logout and backward cache prevention | TS_AUTH_08 | **TC_AUTH_009** | Security | **PASS** | None |
| **REQ-AUTH-09** | Role-Based Access Control (RBAC) preventing unauthorized access | TS_AUTH_09 | **TC_AUTH_010** | Security | **PASS** | None |
| **REQ-PROF-01** | User profile data updates (names, phone, preferences) | TS_PROF_01 | **TC_PROF_001** | Functional (Positive) | **PASS** | None |
| **REQ-PROF-02** | User profile avatar image upload with format/size validation | TS_PROF_02 | **TC_PROF_002**<br>**TC_PROF_003** | Functional (Boundary) | **PASS**<br>**PASS** | None |
| **REQ-PROF-03** | Password modification requiring current password and complexity rules | TS_PROF_03 | **TC_PROF_004**<br>**TC_PROF_005** | Functional / Security | **PASS**<br>**PASS** | None |
| **REQ-DASH-01** | Dynamic KPI metric cards reflecting live database totals | TS_DASH_01 | **TC_DASH_001** | Functional (Positive) | **PASS** | None |
| **REQ-DASH-02** | Responsive sidebar navigation collapse/expand toggle | TS_DASH_02 | **TC_DASH_002** | UI/UX | **PASS** | None |
| **REQ-DASH-03** | Real-time notifications bell counter and mark as read action | TS_DASH_03 | **TC_DASH_003** | Functional (Positive) | **PASS** | None |
| **REQ-DASH-04** | Breadcrumb navigation reflecting hierarchy paths | TS_DASH_04 | **TC_DASH_004** | Functional | **PASS** | None |
| **REQ-DASH-05** | Date range filtering for dashboard charts and analytics | TS_DASH_05 | **TC_DASH_005** | Functional (Positive) | **PASS** | None |
| **REQ-CRUD-01** | Creating new entity records with mandatory & optional fields | TS_CRUD_01 | **TC_CRUD_001** | Functional (Positive) | **PASS** | None |
| **REQ-CRUD-02** | Field-level validation for mandatory inputs and length limits | TS_CRUD_02 | **TC_CRUD_002**<br>**TC_CRUD_003** | Negative / BVA | **PASS**<br>**PASS** | None |
| **REQ-CRUD-03** | Paginated tabular display with dynamic page size options | TS_CRUD_03 | **TC_CRUD_004** | Functional | **PASS** | None |
| **REQ-CRUD-04** | Multi-column ascending and descending sorting on data table | TS_CRUD_04 | **TC_CRUD_005** | Functional | **PASS** | None |
| **REQ-CRUD-05** | Updating existing entity record details and persisting changes | TS_CRUD_05 | **TC_CRUD_006** | Functional (Positive) | **PASS** | None |
| **REQ-CRUD-06** | Record deletion protected by confirmation modal with cancellation | TS_CRUD_06 | **TC_CRUD_007**<br>**TC_CRUD_008** | Functional / Negative | **PASS**<br>**PASS** | None |
| **REQ-SRCH-01** | Debounced keyword search across record title and description | TS_SRCH_01 | **TC_SRCH_001** | Functional (Positive) | **PASS** | None |
| **REQ-SRCH-02** | Empty state handling for zero-match search results | TS_SRCH_02 | **TC_SRCH_002** | UI / Negative | **PASS** | None |
| **REQ-SRCH-03** | Multi-parameter filtering with AND condition logic | TS_SRCH_03 | **TC_SRCH_003** | Functional (Positive) | **PASS** | None |
| **REQ-SRCH-04** | One-click filter reset returning to baseline default dataset | TS_SRCH_04 | **TC_SRCH_004** | Functional | **PASS** | None |
| **REQ-SRCH-05** | Automated whitespace trimming and query normalization | TS_SRCH_05 | **TC_SRCH_005** | Boundary | **PASS** | None |
| **REQ-EXPRT-01** | Exporting displayed and filtered data to CSV format | TS_EXPRT_01 | **TC_EXPRT_001** | Functional (Positive) | **PASS** | None |
| **REQ-EXPRT-02** | Exporting data grid to printable PDF format | TS_EXPRT_02 | **TC_EXPRT_002** | Functional (Positive) | **PASS** | None |
| **REQ-EXPRT-03** | Disabling export actions on empty record sets | TS_EXPRT_03 | **TC_EXPRT_003** | Edge Case | **PASS** | None |
| **REQ-RESP-01** | Responsive layout scaling across Mobile viewports (375x812) | TS_RESP_01 | **TC_RESP_001** | UI/UX | **PASS** | None |
| **REQ-RESP-02** | Responsive layout scaling across Tablet viewports (768x1024) | TS_RESP_02 | **TC_RESP_002** | UI/UX | **PASS** | None |
| **REQ-XBROW-01**| Cross-browser rendering parity (Chrome, Firefox, Edge, Safari) | TS_XBROW_01 | **TC_XBROW_003**<br>**TC_XBROW_004** | Compatibility | **PASS**<br>**PASS** | None |
| **REQ-SEC-01** | Prevention of SQL injection across all user-facing input forms | TS_SEC_01 | **TC_SEC_001** | Security | **PASS** | None |
| **REQ-SEC-02** | Prevention of Cross-Site Scripting (XSS) via HTML entity encoding | TS_SEC_02 | **TC_SEC_002** | Security | **PASS** | None |
| **REQ-SEC-03** | Protection against Insecure Direct Object References (IDOR) | TS_SEC_03 | **TC_SEC_003** | Security | **PASS** | None |
| **REQ-SEC-04** | Inactive user session auto-logout after 15 minutes of idle time | TS_SEC_04 | **TC_SEC_004** | Security | **PASS** | None |
| **REQ-SEC-05** | Single active session enforcement / concurrent login detection | TS_SEC_05 | **TC_SEC_005** | Security | **PASS** | None |
| **REQ-SEC-06** | Unauthenticated route guards preventing direct URL access | TS_SEC_06 | **TC_SEC_006** | Security | **PASS** | None |

---

## 3. Coverage Analysis Summary
* **Total Business / Functional Requirements:** 28
* **Total Test Cases Mapped:** 46
* **Requirements with 100% Test Coverage:** 28 / 28 (100%)
* **Uncovered Requirements:** 0 (0%)
* **Traceability Conclusion:** The test suite provides complete end-to-end bidirectional coverage.
