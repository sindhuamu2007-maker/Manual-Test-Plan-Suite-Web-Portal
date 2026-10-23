"""
Automated Test Suite Runner for Enterprise Web Portal
Task 1: Verification of Manual Test Cases via Automated Test Harness
Executes against app.py using Flask's Test Client (In-Process)
"""

import sys
import os
import time

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app import app, USERS, RECORDS

# Colorama / ANSI styling
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

results = []

def record_result(tc_id, module, description, passed, details=""):
    status = "PASS" if passed else "FAIL"
    color = GREEN if passed else RED
    symbol = "[PASS]" if passed else "[FAIL]"
    results.append({"id": tc_id, "module": module, "desc": description, "status": status, "details": details})
    print(f"  {color}{symbol}{RESET} {BOLD}{tc_id}{RESET}: {description} {CYAN}({details}){RESET}")

def run_tests():
    print(f"\n{BOLD}{CYAN}{'=' * 75}{RESET}")
    print(f"{BOLD}>> EXECUTING AUTOMATED TEST SUITE FOR ENTERPRISE WEB PORTAL (TASK 1){RESET}")
    print(f"{BOLD}{CYAN}{'=' * 75}{RESET}\n")

    client = app.test_client()
    start_time = time.time()

    # ----------------------------------------------------
    # Module 1: Authentication & Authorization (AUTH)
    # ----------------------------------------------------
    print(f"{BOLD}[1/5] Testing Module: Authentication & RBAC{RESET}")

    # TC_SEC_006: Direct URL access without active session
    res = client.get("/dashboard", follow_redirects=False)
    record_result("TC_SEC_006", "Security", "Direct access to /dashboard redirects to /login", 
                  res.status_code == 302 and "/login" in res.headers.get("Location", ""),
                  f"Status: {res.status_code}")

    # TC_AUTH_002: Login with unregistered email
    res = client.post("/login", data={"email": "unregistered@test.com", "password": "DummyPassword123"}, follow_redirects=True)
    record_result("TC_AUTH_002", "Auth", "Login fails gracefully on unregistered email",
                  "Invalid email or password" in res.get_data(as_text=True),
                  "Generic error alert verified")

    # TC_AUTH_003: Login with correct email, incorrect password
    res = client.post("/login", data={"email": "john.doe@example.com", "password": "WrongPassword999"}, follow_redirects=True)
    record_result("TC_AUTH_003", "Auth", "Login fails on incorrect password",
                  "Invalid email or password" in res.get_data(as_text=True),
                  "Generic error alert verified")

    # TC_SEC_001: SQL Injection resilience
    res = client.post("/login", data={"email": "' OR '1'='1' --", "password": "pass"}, follow_redirects=True)
    record_result("TC_SEC_001", "Security", "SQL Injection payload in login input sanitized",
                  "SQLi prevented" in res.get_data(as_text=True),
                  "Payload neutralized")

    # TC_AUTH_001: Valid user login
    res = client.post("/login", data={"email": "john.doe@example.com", "password": "Secure@2026!"}, follow_redirects=True)
    record_result("TC_AUTH_001", "Auth", "Successful login with valid credentials redirects to Dashboard",
                  "QA Executive Dashboard" in res.get_data(as_text=True),
                  "Dashboard rendered")

    # TC_AUTH_010: Standard user accessing Admin route (RBAC Guard)
    res = client.get("/admin", follow_redirects=False)
    record_result("TC_AUTH_010", "Security", "Standard user denied access to Admin Zone (403 Forbidden)",
                  res.status_code == 403 and "Access Denied" in res.get_data(as_text=True),
                  f"HTTP {res.status_code} Access Denied")

    # ----------------------------------------------------
    # Module 2: Dashboard & Navigation
    # ----------------------------------------------------
    print(f"\n{BOLD}[2/5] Testing Module: Dashboard & KPIs{RESET}")

    res = client.get("/dashboard")
    record_result("TC_DASH_001", "Dashboard", "Dashboard KPI metrics render dynamically",
                  "Total Records" in res.get_data(as_text=True) and "High / Critical Tasks" in res.get_data(as_text=True),
                  "KPI cards active")

    # ----------------------------------------------------
    # Module 3: Core Entity CRUD Operations
    # ----------------------------------------------------
    print(f"\n{BOLD}[3/5] Testing Module: Core Entity Management (CRUD){RESET}")

    # TC_CRUD_001 & TC_SEC_002: Create record with XSS check
    xss_title = "Automated Security Audit <script>alert(1)</script>"
    res = client.post("/records/create", data={
        "title": xss_title,
        "category": "Security",
        "priority": "Critical",
        "date": "2026-11-25"
    }, follow_redirects=True)
    page_text = res.get_data(as_text=True)
    xss_safe = "&lt;script&gt;alert(1)&lt;/script&gt;" in page_text and "<script>alert(1)</script>" not in page_text
    record_result("TC_CRUD_001", "CRUD", "Create new record successfully persisted in database",
                  "Automated Security Audit" in page_text,
                  "New row rendered")
    record_result("TC_SEC_002", "Security", "XSS payload properly HTML-encoded in record title",
                  xss_safe,
                  "Tags encoded safely")

    # TC_CRUD_007: Delete record
    res = client.post("/records/101/delete", follow_redirects=True)
    record_result("TC_CRUD_007", "CRUD", "Delete record removes item from data table",
                  "#101" not in res.get_data(as_text=True),
                  "Record #101 deleted")

    # ----------------------------------------------------
    # Module 4: Search, Filter & Export
    # ----------------------------------------------------
    print(f"\n{BOLD}[4/5] Testing Module: Search, Filter & Export{RESET}")

    # TC_SRCH_001: Search keyword matching
    res = client.get("/records?q=SOC-2")
    record_result("TC_SRCH_001", "Search", "Keyword search returns matching filtered records",
                  "SOC-2 Type II Compliance" in res.get_data(as_text=True),
                  "Matching row found")

    # TC_SRCH_002: Empty state handling
    res = client.get("/records?q=nonexistentquery999")
    record_result("TC_SRCH_002", "Search", "Empty search query displays friendly empty state illustration",
                  "No records found matching your query" in res.get_data(as_text=True),
                  "Empty state verified")

    # TC_EXPRT_001: Export CSV with UTF-8 BOM
    res = client.get("/records/export/csv")
    csv_content = res.get_data(as_text=True)
    has_bom = res.data.startswith(b"\xef\xbb\xbf")
    record_result("TC_EXPRT_001", "Export", "CSV export generates with correct headers and UTF-8 BOM",
                  "ID,Title,Category" in csv_content and has_bom,
                  "UTF-8 BOM detected")

    # ----------------------------------------------------
    # Module 5: User Profile & Session Logout
    # ----------------------------------------------------
    print(f"\n{BOLD}[5/5] Testing Module: User Profile & Session Termination{RESET}")

    # TC_PROF_001: Update profile details
    res = client.post("/profile", data={"name": "Johnathon Smith QA"}, follow_redirects=True)
    record_result("TC_PROF_001", "Profile", "Profile name update successfully updates session",
                  "Johnathon Smith QA" in res.get_data(as_text=True),
                  "Updated in session")

    # TC_AUTH_009: User Logout
    res = client.get("/logout", follow_redirects=False)
    res_follow = client.get("/dashboard", follow_redirects=False)
    record_result("TC_AUTH_009", "Auth", "Logout invalidates session and prevents dashboard access",
                  res.status_code == 302 and res_follow.status_code == 302,
                  "Session destroyed")

    # ----------------------------------------------------
    # Summary Report
    # ----------------------------------------------------
    total_time = round(time.time() - start_time, 3)
    total_count = len(results)
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = total_count - pass_count
    pass_rate = round((pass_count / total_count) * 100, 1)

    print(f"\n{BOLD}{CYAN}{'=' * 75}{RESET}")
    print(f"{BOLD}>> EXECUTION SUMMARY REPORT{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 75}{RESET}")
    print(f"  Total Test Cases Executed: {BOLD}{total_count}{RESET}")
    print(f"  Passed:                    {GREEN}{BOLD}{pass_count}{RESET}")
    print(f"  Failed:                    {RED}{BOLD}{fail_count}{RESET}")
    print(f"  Pass Rate:                 {GREEN if pass_rate >= 95 else YELLOW}{BOLD}{pass_rate}%{RESET}")
    print(f"  Execution Duration:        {total_time}s")
    print(f"{CYAN}{'=' * 75}{RESET}\n")

    return fail_count == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
