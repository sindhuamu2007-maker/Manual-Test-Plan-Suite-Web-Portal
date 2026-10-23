# Complete Manual Test Case Suite for Enterprise Web Portal
**Document ID:** TCS-WEBPORTAL-2026-V1.0  
**Associated Test Plan:** TP-WEBPORTAL-2026-V1.0  
**Author:** QA Intern  
**Date:** October 2026  
**Total Test Cases:** 46  
**Execution Type:** Manual Functional, UI/UX, Security, Compatibility  

---

## Test Execution Summary Dashboard

| Module Name | Total Cases | Positive | Negative | Boundary / Security | Pass | Fail | Blocked |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Authentication & Authorization** | 10 | 3 | 3 | 4 | 9 | 1 | 0 |
| **2. User Profile & Settings** | 5 | 2 | 2 | 1 | 5 | 0 | 0 |
| **3. Dashboard & Navigation** | 5 | 4 | 0 | 1 | 5 | 0 | 0 |
| **4. Core Entity Management (CRUD)** | 8 | 4 | 2 | 2 | 7 | 1 | 0 |
| **5. Search & Filter Functionality** | 5 | 3 | 1 | 1 | 5 | 0 | 0 |
| **6. Data Export & Reporting** | 3 | 2 | 1 | 0 | 3 | 0 | 0 |
| **7. Responsive & Cross-Browser** | 4 | 3 | 0 | 1 | 4 | 0 | 0 |
| **8. Security & Edge Case Testing** | 6 | 0 | 2 | 4 | 5 | 1 | 0 |
| **TOTAL** | **46** | **21** | **11** | **14** | **43** | **3** | **0** |

*Current Execution Pass Rate: 93.5% (3 Defects Logged in Defect Tracker)*

---

## Module 1: User Authentication & Authorization (AUTH)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_AUTH_001** | Verify successful user login with valid credentials | User account is registered and active in staging DB | 1. Navigate to `/login`<br>2. Enter registered email<br>3. Enter valid password<br>4. Click 'Sign In' button | Email: `john.doe@example.com`<br>Pass: `Secure@2026!` | User is redirected to `/dashboard`; success toast displayed; session token stored securely | Successfully redirected to dashboard with greeting toast | **PASS** | Positive | Critical / P1 |
| **TC_AUTH_002** | Verify login error handling with unregistered email address | None | 1. Navigate to `/login`<br>2. Enter unregistered email<br>3. Enter dummy password<br>4. Click 'Sign In' | Email: `unregistered_99@test.com`<br>Pass: `TestPassword123` | Generic error message displayed: "Invalid email or password"; user remains on login page | Error message "Invalid email or password" displayed | **PASS** | Negative | Critical / P1 |
| **TC_AUTH_003** | Verify login error handling with incorrect password | User account exists | 1. Navigate to `/login`<br>2. Enter valid email<br>3. Enter incorrect password<br>4. Click 'Sign In' | Email: `john.doe@example.com`<br>Pass: `WrongPass999` | Error message "Invalid email or password" displayed; password field cleared | Generic error displayed; password field cleared | **PASS** | Negative | Critical / P1 |
| **TC_AUTH_004** | Verify account lockout / rate limiting after 5 failed login attempts | User account exists | 1. Navigate to `/login`<br>2. Enter valid email with incorrect password 5 consecutive times<br>3. Attempt 6th login | Email: `john.doe@example.com`<br>Pass: `WrongPass` (x5) | Account temporarily locked for 15 minutes; message: "Too many failed attempts. Try again in 15 minutes." | Account locked for 15 mins with warning alert | **PASS** | Security | Critical / P1 |
| **TC_AUTH_005** | Verify inline validation on submitting empty login form | Login page open | 1. Navigate to `/login`<br>2. Leave email and password blank<br>3. Click 'Sign In' | Blank fields | Red inline validation borders; messages: "Email is required" and "Password is required"; no request sent | Inline red text shown; no network payload sent | **PASS** | Negative | Medium / P2 |
| **TC_AUTH_006** | Verify password masking and toggle visibility eye icon | Login page open | 1. Enter password in password field<br>2. Verify characters are masked (dots)<br>3. Click eye icon<br>4. Verify plain text<br>5. Click eye icon again | Password: `SecretPassword123` | Field starts masked (`••••••`); clicking eye unmasks text; clicking again re-masks | Password toggles visibility seamlessly | **PASS** | UI/UX | Low / P3 |
| **TC_AUTH_007** | Verify forgot password email trigger for registered user | User account exists | 1. Click "Forgot Password?"<br>2. Enter registered email<br>3. Click "Send Reset Link" | Email: `john.doe@example.com` | Success message: "Password reset link sent to your email"; reset email received with token | Success alert shown; reset email delivered | **PASS** | Positive | High / P2 |
| **TC_AUTH_008** | Verify password reset link expiration after token expiry time | Reset email link generated | 1. Wait 16 minutes after generating reset link (expiry is 15 min)<br>2. Open reset URL in browser | Expired Token URL | Message: "This reset link has expired. Please request a new one"; form disabled | Error message displayed as expected | **PASS** | Security | High / P2 |
| **TC_AUTH_009** | Verify user logout and back button browser cache security | User logged into dashboard | 1. Click Profile Avatar<br>2. Click 'Logout'<br>3. Click browser 'Back' button | Active Session | User redirected to `/login`; clicking back does NOT display cached dashboard pages; requires re-login | User redirected to login; back button redirected to login | **PASS** | Security | Critical / P1 |
| **TC_AUTH_010** | Verify Role-Based Access Control (RBAC) - Standard user accessing admin page | Standard user logged in | 1. Log in as Standard User<br>2. Directly type URL: `/admin/user-management`<br>3. Hit Enter | URL: `/admin/user-management`<br>Role: Standard User | Access denied; 403 Forbidden page or redirect to `/unauthorized` with message | System displays 403 Access Denied page | **PASS** | Security | Critical / P1 |

---

## Module 2: User Profile & Account Settings (PROF)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_PROF_001** | Verify updating user profile details with valid data | User logged in on `/settings/profile` | 1. Update First Name, Last Name, and Phone Number<br>2. Click 'Save Changes' | First Name: `Jonathan`<br>Last Name: `Smith`<br>Phone: `+1-555-0199` | Toast "Profile updated successfully"; updated names reflected across header avatar | Profile updated and header reflects new name | **PASS** | Positive | High / P2 |
| **TC_PROF_002** | Verify avatar image upload with valid format and file size | Profile settings page open | 1. Click "Upload Avatar"<br>2. Select valid `.png` file (< 2MB)<br>3. Click 'Confirm' | File: `avatar_valid.png` (850 KB, 500x500px) | Image cropped/previewed properly; uploaded successfully; avatar updated in header | Avatar uploaded and saved | **PASS** | Positive | Medium / P3 |
| **TC_PROF_003** | Verify avatar image upload validation with unsupported file type | Profile settings page open | 1. Click "Upload Avatar"<br>2. Select `.exe` or `.pdf` file<br>3. Attempt upload | File: `malicious_script.exe` / `doc.pdf` | Error message: "Unsupported file format. Please upload JPG, PNG, or WEBP only."; upload blocked | Error message shown; file rejected | **PASS** | Negative / Security | High / P2 |
| **TC_PROF_004** | Verify password change error when current password is wrong | User logged in on `/settings/security` | 1. Enter incorrect current password<br>2. Enter valid new password & confirm<br>3. Click 'Update Password' | Current: `WrongCurrent123`<br>New: `NewComplexPass@2026!` | Error message: "Current password does not match"; password is not updated | Error message displayed; password remains unchanged | **PASS** | Negative | High / P2 |
| **TC_PROF_005** | Verify password change rejection on weak password complexity | Security settings page open | 1. Enter correct current password<br>2. Enter weak new password (e.g., all lowercase, < 8 chars)<br>3. Click 'Update Password' | Current: `ValidPass@2026`<br>New: `simple` | Inline validation: "Password must be at least 8 characters, contain 1 uppercase, 1 number, and 1 special symbol" | Validation error displayed; button disabled | **PASS** | Boundary / ECP | High / P2 |

---

## Module 3: Dashboard & Navigation (DASH)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_DASH_001** | Verify dynamic rendering of KPI summary metric cards | User logged in; database has active records | 1. Navigate to `/dashboard`<br>2. Check cards: Total Users, Active Orders, Revenue, Pending Tasks | Staging DB metrics | Metric values match database counts; skeleton loaders display while loading | KPI cards loaded with accurate numbers | **PASS** | Positive | High / P2 |
| **TC_DASH_002** | Verify sidebar navigation expand and collapse behavior | Dashboard loaded | 1. Click hamburger icon on sidebar<br>2. Verify sidebar collapses to icon-only mode<br>3. Click hamburger icon again | Navigation toggle | Main content area expands fluidly; tooltip appears on icon hover when collapsed; expands cleanly | Sidebar collapses and expands smoothly | **PASS** | UI/UX | Low / P3 |
| **TC_DASH_003** | Verify notification bell counter and dropdown list | User has 3 unread notifications | 1. Inspect notification bell icon<br>2. Click bell icon<br>3. Click "Mark all as read" | 3 unread notifications | Badge displays count '3'; dropdown lists notifications chronologically; count clears to 0 upon clicking mark as read | Notification badge clears to 0 upon action | **PASS** | Positive | Medium / P2 |
| **TC_DASH_004** | Verify breadcrumb navigation hierarchy links | User on deep sub-page: `/portal/projects/101/tasks` | 1. Navigate to sub-page<br>2. Click 'Projects' breadcrumb<br>3. Verify destination | Sub-page URL | Breadcrumb displays `Home > Projects > Project #101 > Tasks`; clicking 'Projects' navigates to `/portal/projects` | Breadcrumb links navigate accurately | **PASS** | Functional | Medium / P3 |
| **TC_DASH_005** | Verify dashboard date range filter updates chart data | Dashboard loaded | 1. Select date range dropdown<br>2. Choose "Last 30 Days"<br>3. Observe graph/chart reload | Date filter: "Last 30 Days" | Graph triggers async refresh with spinner; chart data points re-plot for selected 30-day window | Charts update correctly with new date range data | **PASS** | Positive | High / P2 |

---

## Module 4: Core Entity Management - CRUD Operations (CRUD)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_CRUD_001** | Verify creating a new entity record with all valid inputs | User on `/records/create` | 1. Enter Title, Category, Priority, Description, Due Date<br>2. Click 'Submit' button | Title: `Q4 Compliance Audit`<br>Category: `Finance`<br>Priority: `High`<br>Date: `2026-11-15` | Record saved in DB; toast "Record created successfully"; redirected to table list with new record visible | Record created and displayed at top of table | **PASS** | Positive | Critical / P1 |
| **TC_CRUD_002** | Verify form validation when creating entity with empty mandatory fields | User on `/records/create` | 1. Leave Title and Category empty<br>2. Click 'Submit' button | Empty fields | Form submission prevented; mandatory fields highlighted red with "Field is required" text; cursor focuses on 1st error | Validation errors shown; no record created | **PASS** | Negative | Critical / P1 |
| **TC_CRUD_003** | Verify boundary value character limit for record Title field | User on `/records/create` | 1. Enter 100 characters in Title (allowed)<br>2. Attempt entering 101st character | Title: 100 'A's vs 101 'A's | Field permits exactly 100 chars; input truncated or warning displayed; counter shows 100/100 | Field strictly stops input at 100 characters | **PASS** | BVA | Medium / P2 |
| **TC_CRUD_004** | Verify data table pagination controls and page size selector | More than 50 records exist | 1. Navigate to record list<br>2. Click 'Next' (Page 2)<br>3. Change page size dropdown from 10 to 25 | Total records: 55 | Page 2 loads records 11-20; changing page size to 25 updates table to display 25 rows and recalculates total pages to 3 | Pagination operates smoothly | **PASS** | Functional | High / P2 |
| **TC_CRUD_005** | Verify column sorting on Data Table (Ascending / Descending) | Record list loaded | 1. Click 'Created Date' column header<br>2. Observe order (Ascending)<br>3. Click column header again | Sorting column: `Created Date` | First click sorts dates Oldest -> Newest with up arrow icon; second click sorts Newest -> Oldest with down arrow icon | Sorting works as expected | **PASS** | Functional | Low / P3 |
| **TC_CRUD_006** | Verify editing an existing record and updating details | Record exists in list | 1. Click 'Edit' icon on record #101<br>2. Modify Description and Priority<br>3. Click 'Update' | Priority: Changed from `Low` to `Critical`<br>Desc: `Updated Notes` | Toast "Changes saved successfully"; table view reflects updated values immediately | Record updated in DB and UI table | **PASS** | Positive | Critical / P1 |
| **TC_CRUD_007** | Verify deleting a record with modal confirmation prompt | Record exists in list | 1. Click 'Delete' icon on record #102<br>2. Confirmation modal appears: "Are you sure?"<br>3. Click 'Confirm Delete' | Record ID: 102 | Record deleted from DB (soft-delete); toast "Record deleted"; row removed from table view | Record deleted and removed from view | **PASS** | Positive | Critical / P1 |
| **TC_CRUD_008** | Verify cancelling record deletion from confirmation modal | Record exists in list | 1. Click 'Delete' icon on record #103<br>2. Modal appears<br>3. Click 'Cancel' button or outside modal | Record ID: 103 | Modal closes immediately; record remains untouched in table; no deletion API call triggered | Modal closes; record remains intact | **PASS** | Negative | Medium / P2 |

---

## Module 5: Search & Filter Functionality (SRCH)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_SRCH_001** | Verify global keyword search returns matching records | Record list has diverse items | 1. Enter keyword in search input<br>2. Press Enter or wait for 300ms debounce | Query: `Compliance` | Only records containing "Compliance" in Title or Description are displayed; match count shown | Filtered list correctly displays 4 matching records | **PASS** | Positive | High / P2 |
| **TC_SRCH_002** | Verify empty state message when search query has no match | Record list open | 1. Enter query that matches zero records<br>2. Observe table body | Query: `xyznonexistent999` | "No records found matching your search" placeholder illustration displayed; no crash or broken table | Empty state illustration and message shown | **PASS** | Negative | Medium / P3 |
| **TC_SRCH_003** | Verify combining multiple filters (Category + Status) | Record list open | 1. Select Category filter: "Finance"<br>2. Select Status filter: "Pending"<br>3. Click 'Apply' | Category: `Finance`<br>Status: `Pending` | Table updates displaying only records that satisfy BOTH conditions simultaneously (logical AND) | Records filtered accurately by both criteria | **PASS** | Positive | High / P2 |
| **TC_SRCH_004** | Verify "Clear Filters" action resets data table to initial state | Filters actively applied | 1. Apply multiple filters<br>2. Click 'Clear All Filters' button | Active filters | Filter dropdowns reset to "All"; search bar clears; table re-fetches and displays all default records | All filters cleared; full dataset reloaded | **PASS** | Functional | Medium / P3 |
| **TC_SRCH_005** | Verify search input ignores leading/trailing whitespaces | Records exist | 1. Enter search keyword with spaces before and after<br>2. Submit search | Query: `"   Audit   "` | Whitespaces trimmed automatically; results matching "Audit" are returned without error | Query trimmed; valid records returned | **PASS** | Boundary | Low / P3 |

---

## Module 6: Data Export & Reporting (EXPRT)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_EXPRT_001** | Verify export of filtered data table to CSV format | Filtered dataset displayed (15 rows) | 1. Apply filter (Status: Active)<br>2. Click 'Export' -> Choose 'CSV'<br>3. Open downloaded file | File: `records_export_20261023.csv` | File downloads with valid header row; exactly 15 records exported; commas in text properly escaped | CSV downloads with 15 rows and correct headers | **PASS** | Positive | High / P2 |
| **TC_EXPRT_002** | Verify export of data table to PDF document | Records displayed on table | 1. Click 'Export' -> Choose 'PDF'<br>2. Open downloaded PDF | File: `report_20261023.pdf` | PDF generates cleanly; portal logo, generation timestamp, table borders, and pagination formatted properly | PDF formatted with company logo and timestamp | **PASS** | Positive | High / P2 |
| **TC_EXPRT_003** | Verify export button behavior when current table has 0 records | Zero search results displayed | 1. Filter table until 0 records found<br>2. Inspect and click 'Export' button | 0 records | Export button is either disabled or displays toast: "No records available to export" | Export button disabled with tooltip explanation | **PASS** | Edge Case | Medium / P3 |

---

## Module 7: Responsive Design & Cross-Browser Compatibility (RESP / XBROW)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_RESP_001** | Verify responsive layout on Mobile Viewport (375x812 - iPhone) | Staging portal URL | 1. Set browser viewport to 375x812<br>2. Inspect header, navigation, and dashboard | Viewport: 375x812 | Sidebar collapses into hamburger drawer; KPI cards stack vertically (1 column); no horizontal scroll bar | UI stacks neatly; hamburger menu operates smoothly | **PASS** | UI/UX | High / P2 |
| **TC_RESP_002** | Verify responsive layout on Tablet Viewport (768x1024 - iPad) | Staging portal URL | 1. Set browser viewport to 768x1024<br>2. Inspect grid layout and data table | Viewport: 768x1024 | 2-column grid layout; table enables smooth horizontal scroll for wide columns without breaking layout | Grid adapts cleanly to 2 columns | **PASS** | UI/UX | Medium / P3 |
| **TC_XBROW_003** | Verify visual and functional parity on Google Chrome vs Mozilla Firefox | Chrome v128+ & Firefox v130+ installed | 1. Execute login, record creation, and modal dialogs on Firefox<br>2. Compare rendering with Chrome | Standard test dataset | CSS styles, fonts, date pickers, button states, and APIs render identically without visual clipping | Identical rendering on Chrome and Firefox | **PASS** | Compatibility | Critical / P1 |
| **TC_XBROW_004** | Verify visual and functional parity on Microsoft Edge vs Apple Safari (macOS/WebKit) | Edge Chromium & Safari 17+ | 1. Perform navigation, form submission, and dropdowns on Safari and Edge | Standard test dataset | Form inputs, SVG icons, and drop shadows render consistently; no JavaScript errors in Safari console | Layout and interactions pass cleanly | **PASS** | Compatibility | High / P2 |

---

## Module 8: Security, Session & Edge Case Testing (SEC)

| Test Case ID | Test Scenario / Objective | Pre-conditions | Test Steps | Test Data | Expected Result | Actual Result | Status | Type | Sev / Prio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC_SEC_001** | Verify SQL Injection resilience in login and search fields | Login & Search inputs accessible | 1. In email field enter SQL payload<br>2. In search field enter SQL payload<br>3. Submit request | Payload: `' OR '1'='1' --`<br>`admin' --` | Input sanitized / parameterized; system rejects login; no database error or SQL syntax dump shown | Inputs sanitized; system rejects with generic invalid credentials | **PASS** | Security | Critical / P1 |
| **TC_SEC_002** | Verify Cross-Site Scripting (XSS) prevention in form inputs | Entity creation page | 1. In Title field, enter malicious JavaScript tag<br>2. Save record<br>3. View record details | Payload: `<script>alert('XSS_ATTACK')</script>` | Input HTML-entity encoded (`&lt;script&gt;`); string rendered as harmless text; NO JavaScript popup executes | String encoded and rendered safely as plain text | **PASS** | Security | Critical / P1 |
| **TC_SEC_003** | Verify Insecure Direct Object Reference (IDOR) prevention | User A and User B exist; User A has record #501 | 1. Log in as User B<br>2. Directly modify URL parameter to edit User A's record: `/records/501/edit`<br>3. Submit changes | URL: `/records/501/edit`<br>Logged in: User B | Server verifies ownership; returns 403 Forbidden or 404 Not Found; User B CANNOT view/edit User A's record | Access denied with 403 Forbidden alert | **PASS** | Security | Critical / P1 |
| **TC_SEC_004** | Verify session inactivity auto-logout after timeout | User logged in | 1. Leave web portal idle with no mouse/keyboard interaction for 15 minutes | Inactivity: 15 minutes | Warning modal at 14 min: "Session expiring in 60s"; at 15 min session invalidated; redirected to `/login?session=expired` | Auto-logout triggered at 15 minutes | **PASS** | Security | High / P2 |
| **TC_SEC_005** | Verify concurrent login session handling from multiple browsers | User logged in on Chrome | 1. Open new Firefox session<br>2. Log into same account<br>3. Return to Chrome and click any dashboard link | Account: `john.doe@example.com` | First session invalidated or notified: "You have been logged in from another device"; redirected to login | First session invalidated immediately upon second login | **PASS** | Security | High / P2 |
| **TC_SEC_006** | Verify direct URL access to protected pages without session | No active session (Incognito) | 1. Open new Incognito window<br>2. Directly paste protected URL: `/records/create`<br>3. Hit Enter | URL: `/records/create` | User instantly redirected to `/login?redirect=/records/create`; protected page content is NOT rendered | Redirected to login page immediately | **PASS** | Security | Critical / P1 |
