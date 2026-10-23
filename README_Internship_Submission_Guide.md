# Internship Task 1: Complete Manual Test Plan & Test Case Suite - Submission Guide

**Candidate Name:** QA Intern  
**Task Number:** Task 1  
**Project:** Enterprise Web Portal Testing  
**Date of Submission:** October 2026  
**Status:** 100% Completed & Ready for Review  

---

## 1. Executive Summary & Package Contents

This submission package contains an end-to-end, enterprise-grade Manual QA documentation suite for a modern Web Portal, adhering strictly to international testing standards (**IEEE 829**). Every deliverable has been structured to meet high industry benchmarks for software quality assurance.

### Deliverables Breakdown

| Deliverable File | Format | Description |
| :--- | :---: | :--- |
| [**`Test_Plan_Document.md`**](file:///C:/Users/Sindhushree%20T%20B/.gemini/antigravity/scratch/Manual_Test_Plan_Suite/Test_Plan_Document.md) | Markdown | Comprehensive IEEE 829 Standard Master Test Plan covering Scope, Strategy, Environment Matrix, RACI, Entry/Exit criteria, and Risk Management. |
| [**`Test_Case_Suite.csv`**](file:///C:/Users/Sindhushree%20T%20B/.gemini/antigravity/scratch/Manual_Test_Plan_Suite/Test_Case_Suite.csv) | CSV (Excel Ready) | **46 Granular Test Cases** across 8 core portal modules. Formatted in UTF-8 with BOM for instant opening in Microsoft Excel, Google Sheets, Jira, or TestRail. |
| [**`Test_Case_Suite.md`**](file:///C:/Users/Sindhushree%20T%20B/.gemini/antigravity/scratch/Manual_Test_Plan_Suite/Test_Case_Suite.md) | Markdown | Human-readable Markdown tables of all 46 test cases categorized by module with execution summary dashboard. |
| [**`Requirements_Traceability_Matrix_RTM.md`**](file:///C:/Users/Sindhushree%20T%20B/.gemini/antigravity/scratch/Manual_Test_Plan_Suite/Requirements_Traceability_Matrix_RTM.md) | Markdown | 100% Bidirectional mapping from 28 Functional Requirements to Test Scenarios and Test Cases. |
| [**`Defect_Reporting_Template_and_Bug_Lifecycle.md`**](file:///C:/Users/Sindhushree%20T%20B/.gemini/antigravity/scratch/Manual_Test_Plan_Suite/Defect_Reporting_Template_and_Bug_Lifecycle.md) | Markdown | Defect Life Cycle workflow diagram, Jira-style Defect Report template, and 3 realistic sample bug reports. |

---

## 2. Tested Portal Modules & Coverage Highlights

1. **User Authentication & Authorization (10 Cases):** Valid/Invalid logins, rate limiting (brute-force defense), password masking, forgot/reset flow with token expiration, RBAC access denial, session clearance on logout.
2. **User Profile & Settings (5 Cases):** Profile info updates, avatar file format/size checks, password changes, complexity rule validation.
3. **Dashboard & Navigation (5 Cases):** KPI metric cards, responsive sidebar toggle, notifications bell counter, breadcrumbs hierarchy, date-range chart filtering.
4. **Core Entity CRUD Management (8 Cases):** Record creation with mandatory validation, character boundary limits (BVA), pagination controls, column sorting, editing, soft-delete with modal confirmation and cancellation.
5. **Search & Filter (5 Cases):** Keyword search, zero-match empty state, multi-criteria filter combinations, one-click filter reset, whitespace trimming.
6. **Data Export & Reporting (3 Cases):** Export to CSV (with comma and special character handling), PDF export formatting, disabled state handling for empty datasets.
7. **Responsive & Cross-Browser Compatibility (4 Cases):** Responsive viewport rendering (Mobile 375x812, Tablet 768x1024), parity verification across Chrome, Firefox, Edge, and Safari.
8. **Security & Edge Cases (6 Cases):** SQL injection prevention, XSS payload neutralization, Insecure Direct Object Reference (IDOR) route blocking, session inactivity timeout (15 mins), concurrent multi-browser sessions.

---

## 3. How to View & Present `Test_Case_Suite.csv` in Excel

The test case suite is provided as a production-grade CSV file:
`C:\Users\Sindhushree T B\.gemini\antigravity\scratch\Manual_Test_Plan_Suite\Test_Case_Suite.csv`

### Steps to Open in Microsoft Excel or Google Sheets:
1. **Double-click `Test_Case_Suite.csv`**: It opens natively in Microsoft Excel.
2. **Enable Text Wrapping**: Select column `E` (Test Steps) and click **Wrap Text** on the Excel ribbon to view multiline steps clearly.
3. **Freeze Header Row**: Go to **View -> Freeze Panes -> Freeze Top Row**.
4. **Auto-fit Column Widths**: Select all columns (`Ctrl + A`) and double-click any column header divider to auto-fit.
5. **Add Filters**: Select row 1 and press `Ctrl + Shift + L` to enable filtering by Module, Test Type, Severity, or Status.

---

## 4. Key QA Concepts & Interview / Viva Cheat Sheet

When discussing this task with your internship mentor, evaluation committee, or manager, be prepared to answer these core questions:

### Q1: What is the difference between a Test Plan and a Test Strategy?
* **Test Strategy:** An enterprise-level, high-level document created by QA Managers that defines overarching QA standards, test approaches, and tooling across projects. It rarely changes.
* **Test Plan:** A project-specific document created by QA Engineers/Leads that details *what* to test, *who* will test, *when* testing happens, environment requirements, schedules, and specific entry/exit criteria for that exact release.

### Q2: What test design techniques were applied in this suite?
* **Boundary Value Analysis (BVA):** Applied on input field lengths (e.g., exactly 100 characters permitted vs. 101 characters rejected in record title) and token timeouts (14 mins warning, 15 mins expiry, 16 mins token invalid).
* **Equivalence Class Partitioning (ECP):** Applied on password complexity (valid complex passwords vs. invalid weak partitions), and file upload validations (valid images: PNG/JPG < 2MB vs. invalid: .exe/.pdf or > 5MB).
* **State Transition Testing:** Verified during user session lifecycle (Unauthenticated -> Authenticated -> Idle Warning -> Expired -> Logged Out).
* **Error Guessing:** Executed for leading/trailing whitespaces in search fields, concurrent logins on two separate browsers, and direct URL manipulation (IDOR).

### Q3: What is the difference between Severity and Priority?
* **Severity:** Refers to the technical impact of the defect on system operation (Critical, Major, Medium, Low).
  * *High Severity, Low Priority:* Web portal crashes, but only when printing an obscure report that nobody uses.
* **Priority:** Refers to the business urgency of fixing the defect (P1/Blocker, P2/High, P3/Medium, P4/Low).
  * *High Priority, Low Severity:* The company logo on the public login page is misspelled or displaying an incorrect brand name. Functionality is intact, but business reputation is immediately harmed.

### Q4: Why is the Requirements Traceability Matrix (RTM) critical?
The RTM ensures **100% test coverage** by mapping every requirement from the PRD to corresponding test scenarios and test cases. It prevents missing requirements, helps determine regression scope when a requirement changes, and proves to stakeholders that the product was exhaustively tested.

### Q5: What are Entry and Exit Criteria in testing?
* **Entry Criteria:** Preconditions that must be satisfied before testing starts (e.g., Staging environment deployed, test data seeded, build verification/smoke tests passing 100%).
* **Exit Criteria:** Conditions that must be met before QA signs off for release (e.g., 100% test cases executed, >= 95% pass rate, zero Critical/High bugs open, all lower bugs documented with approved workarounds).

---

## 5. Recommended Next Steps for Phase 2
1. Import `Test_Case_Suite.csv` into Jira Xray, Zephyr Scale, or TestRail.
2. Automate Tier-1 Smoke and Critical Sanity test cases using Playwright or Cypress with TypeScript.
3. Integrate test execution into CI/CD pipelines (GitHub Actions / GitLab CI) for automated build verification on every pull request.
