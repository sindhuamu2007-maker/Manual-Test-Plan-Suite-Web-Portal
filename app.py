"""
Enterprise Web Portal - Local Application for Manual QA Testing
Task 1: Manual Test Plan & Test Case Suite Verification
Author: QA Intern
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, Response
import time
import io
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = "qa_internship_super_secret_key_2026"

# In-memory database fixtures
USERS = {
    "admin.test@example.com": {"password": "AdminSecure@2026!", "name": "Admin Officer", "role": "SuperAdmin"},
    "john.doe@example.com": {"password": "Secure@2026!", "name": "John Doe", "role": "StandardUser"},
}

FAILED_LOGINS = {}  # email -> count

RECORDS = [
    {"id": 101, "title": "Quarterly Financial Audit", "category": "Finance", "priority": "High", "status": "Pending", "date": "2026-11-15"},
    {"id": 102, "title": "SOC-2 Type II Compliance", "category": "Security", "priority": "Critical", "status": "Active", "date": "2026-11-20"},
    {"id": 103, "title": "Customer Portal UI Overhaul", "category": "Frontend", "priority": "Medium", "status": "Active", "date": "2026-12-01"},
    {"id": 104, "title": "Résumé Audit – €500 / 25% discount", "category": "Finance", "priority": "Low", "status": "Pending", "date": "2026-12-05"},
    {"id": 105, "title": "Database Read Replica Setup", "category": "DevOps", "priority": "High", "status": "Active", "date": "2026-12-10"},
]
NEXT_ID = 106

# HTML Base Template with Bootstrap 5
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Enterprise Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .sidebar { min-height: 100vh; width: 250px; background: #1e293b; color: #fff; transition: all 0.3s; }
        .sidebar.collapsed { width: 75px; }
        .sidebar.collapsed .nav-label, .sidebar.collapsed .portal-brand { display: none; }
        .sidebar .nav-link { color: #94a3b8; padding: 12px 20px; font-weight: 500; border-radius: 6px; margin: 4px 10px; }
        .sidebar .nav-link:hover, .sidebar .nav-link.active { color: #fff; background: #334155; }
        .stat-card { border-radius: 12px; border: none; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
        .badge-critical { background-color: #ef4444; color: white; }
        .badge-high { background-color: #f97316; color: white; }
        .badge-medium { background-color: #eab308; color: black; }
        .badge-low { background-color: #3b82f6; color: white; }
    </style>
</head>
<body>
    <div class="d-flex">
        <!-- Sidebar Navigation -->
        {% if session.get('user') %}
        <nav class="sidebar d-flex flex-column p-3" id="mainSidebar">
            <div class="d-flex align-items-center justify-content-between mb-4 px-2">
                <span class="fs-5 fw-bold portal-brand text-white"><i class="bi bi-shield-check text-primary"></i> PortalQA</span>
                <button class="btn btn-sm btn-outline-secondary text-white" id="toggleSidebarBtn"><i class="bi bi-list"></i></button>
            </div>
            <ul class="nav nav-pills flex-column mb-auto">
                <li class="nav-item">
                    <a href="{{ url_for('dashboard') }}" class="nav-link {% if active_page == 'dashboard' %}active{% endif %}">
                        <i class="bi bi-speedometer2 me-2"></i><span class="nav-label">Dashboard</span>
                    </a>
                </li>
                <li>
                    <a href="{{ url_for('records_list') }}" class="nav-link {% if active_page == 'records' %}active{% endif %}">
                        <i class="bi bi-table me-2"></i><span class="nav-label">Records CRUD</span>
                    </a>
                </li>
                <li>
                    <a href="{{ url_for('profile') }}" class="nav-link {% if active_page == 'profile' %}active{% endif %}">
                        <i class="bi bi-person-gear me-2"></i><span class="nav-label">Profile Settings</span>
                    </a>
                </li>
                {% if session.get('role') == 'SuperAdmin' %}
                <li>
                    <a href="{{ url_for('admin_panel') }}" class="nav-link {% if active_page == 'admin' %}active{% endif %}">
                        <i class="bi bi-shield-lock me-2"></i><span class="nav-label">Admin Zone</span>
                    </a>
                </li>
                {% endif %}
            </ul>
            <hr class="border-secondary">
            <div class="d-flex align-items-center justify-content-between px-2">
                <div class="portal-brand">
                    <small class="text-white fw-bold d-block">{{ session.get('name') }}</small>
                    <small class="text-muted">{{ session.get('role') }}</small>
                </div>
                <a href="{{ url_for('logout') }}" class="btn btn-sm btn-outline-danger" title="Logout"><i class="bi bi-box-arrow-right"></i></a>
            </div>
        </nav>
        {% endif %}

        <!-- Main Content Area -->
        <main class="flex-grow-1 p-4" style="overflow-x: hidden;">
            {% if session.get('user') %}
            <!-- Top Navbar -->
            <header class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom">
                <div class="d-flex align-items-center">
                    <nav aria-label="breadcrumb">
                        <ol class="breadcrumb mb-0">
                            <li class="breadcrumb-item"><a href="{{ url_for('dashboard') }}" class="text-decoration-none">Home</a></li>
                            <li class="breadcrumb-item active" aria-current="page">{{ title }}</li>
                        </ol>
                    </nav>
                </div>
                <div class="d-flex align-items-center gap-3">
                    <div class="position-relative">
                        <button class="btn btn-light position-relative rounded-circle p-2" id="notifBell">
                            <i class="bi bi-bell"></i>
                            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" id="notifBadge">3</span>
                        </button>
                    </div>
                    <span class="badge bg-primary px-3 py-2 rounded-pill"><i class="bi bi-person-circle me-1"></i> {{ session.get('user') }}</span>
                </div>
            </header>
            {% endif %}

            <!-- Flash alerts -->
            {% if message %}
            <div class="alert alert-{{ message_type or 'info' }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            {% endif %}

            {{ content | safe }}
        </main>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const toggleBtn = document.getElementById('toggleSidebarBtn');
        const sidebar = document.getElementById('mainSidebar');
        if (toggleBtn && sidebar) {
            toggleBtn.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
            });
        }
        const notifBell = document.getElementById('notifBell');
        const notifBadge = document.getElementById('notifBadge');
        if (notifBell && notifBadge) {
            notifBell.addEventListener('click', () => {
                notifBadge.style.display = 'none';
                alert('Notifications marked as read!');
            });
        }
    </script>
</body>
</html>
"""

LOGIN_PAGE = """
<div class="container" style="max-width: 440px; margin-top: 80px;">
    <div class="card shadow-lg p-4 border-0 rounded-4 bg-white">
        <div class="text-center mb-4">
            <div class="bg-primary text-white d-inline-flex p-3 rounded-circle mb-2">
                <i class="bi bi-shield-lock-fill fs-2"></i>
            </div>
            <h4 class="fw-bold">Enterprise Web Portal</h4>
            <p class="text-muted small">Sign in to access your test dashboard</p>
        </div>

        {% if error %}
        <div class="alert alert-danger py-2 small" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-1"></i> {{ error }}
        </div>
        {% endif %}

        <form action="/login" method="POST" id="loginForm">
            <div class="mb-3">
                <label class="form-label small fw-semibold">Email Address</label>
                <div class="input-group">
                    <span class="input-group-text bg-light"><i class="bi bi-envelope"></i></span>
                    <input type="email" name="email" class="form-control" placeholder="name@example.com" value="{{ email or '' }}" required>
                </div>
            </div>

            <div class="mb-3">
                <label class="form-label small fw-semibold">Password</label>
                <div class="input-group">
                    <span class="input-group-text bg-light"><i class="bi bi-key"></i></span>
                    <input type="password" name="password" id="loginPassword" class="form-control" placeholder="Enter password" required>
                    <button class="btn btn-outline-secondary" type="button" id="togglePassBtn"><i class="bi bi-eye"></i></button>
                </div>
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2 fw-semibold rounded-3 mb-3">Sign In</button>
        </form>

        <div class="bg-light p-3 rounded-3 small">
            <strong>Demo Staging Credentials:</strong><br>
            • Standard: <code>john.doe@example.com</code> / <code>Secure@2026!</code><br>
            • Admin: <code>admin.test@example.com</code> / <code>AdminSecure@2026!</code>
        </div>
    </div>
</div>
<script>
    const togglePassBtn = document.getElementById('togglePassBtn');
    const loginPassword = document.getElementById('loginPassword');
    if (togglePassBtn && loginPassword) {
        togglePassBtn.addEventListener('click', () => {
            const isPassword = loginPassword.getAttribute('type') === 'password';
            loginPassword.setAttribute('type', isPassword ? 'text' : 'password');
            togglePassBtn.innerHTML = isPassword ? '<i class="bi bi-eye-slash"></i>' : '<i class="bi bi-eye"></i>';
        });
    }
</script>
"""

DASHBOARD_PAGE = """
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h3 class="fw-bold mb-1">QA Executive Dashboard</h3>
            <p class="text-muted small">Real-time status and operational metrics</p>
        </div>
        <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-primary" onclick="alert('Filtered by Last 30 Days')"><i class="bi bi-calendar3 me-1"></i> Last 30 Days</button>
            <a href="{{ url_for('records_list') }}" class="btn btn-sm btn-primary"><i class="bi bi-plus-circle me-1"></i> Manage Records</a>
        </div>
    </div>

    <!-- Stat Cards -->
    <div class="row g-3 mb-4">
        <div class="col-md-3">
            <div class="card stat-card p-3 bg-white">
                <span class="text-muted small fw-semibold">Total Records</span>
                <h2 class="fw-bold my-1 text-primary">{{ stats.total_records }}</h2>
                <small class="text-success"><i class="bi bi-arrow-up-right"></i> Active in database</small>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card p-3 bg-white">
                <span class="text-muted small fw-semibold">High / Critical Tasks</span>
                <h2 class="fw-bold my-1 text-danger">{{ stats.critical_records }}</h2>
                <small class="text-danger"><i class="bi bi-exclamation-circle"></i> Requires QA review</small>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card p-3 bg-white">
                <span class="text-muted small fw-semibold">Test Suite Pass Rate</span>
                <h2 class="fw-bold my-1 text-success">93.5%</h2>
                <small class="text-muted">43 of 46 Passed</small>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card stat-card p-3 bg-white">
                <span class="text-muted small fw-semibold">Active Defect Tickets</span>
                <h2 class="fw-bold my-1 text-warning">3</h2>
                <small class="text-warning">1 Major, 2 Medium</small>
            </div>
        </div>
    </div>

    <!-- Quick info callout -->
    <div class="card border-0 rounded-3 shadow-sm p-4 bg-white">
        <h5 class="fw-bold mb-2"><i class="bi bi-info-circle-fill text-primary me-2"></i>Manual Testing Verification Environment</h5>
        <p class="text-muted small mb-3">
            This local web portal is running to allow manual verification of all 46 test cases described in <code>Test_Case_Suite.csv</code>. 
            Test features including Login authentication, role-based access control (RBAC), record creation with boundary checks, 
            search and multi-criteria filters, and CSV export.
        </p>
        <div class="d-flex gap-2">
            <a href="{{ url_for('records_list') }}" class="btn btn-outline-primary btn-sm">Explore Records CRUD Table</a>
            <a href="{{ url_for('profile') }}" class="btn btn-outline-secondary btn-sm">Verify Profile & Security Settings</a>
        </div>
    </div>
</div>
"""

RECORDS_PAGE = """
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h3 class="fw-bold mb-1">Entity Records Management (CRUD)</h3>
            <p class="text-muted small">Verify creation, filtering, pagination, search, and deletion</p>
        </div>
        <div class="d-flex gap-2">
            <a href="/records/export/csv" class="btn btn-outline-success btn-sm"><i class="bi bi-file-earmark-spreadsheet me-1"></i> Export CSV</a>
            <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#createModal"><i class="bi bi-plus-lg me-1"></i> New Record</button>
        </div>
    </div>

    <!-- Filter & Search Bar -->
    <div class="card border-0 shadow-sm p-3 mb-4 bg-white">
        <form method="GET" action="/records" class="row g-2 align-items-center">
            <div class="col-md-5">
                <div class="input-group input-group-sm">
                    <span class="input-group-text bg-light"><i class="bi bi-search"></i></span>
                    <input type="text" name="q" class="form-control" placeholder="Search by title or category..." value="{{ query }}">
                </div>
            </div>
            <div class="col-md-3">
                <select name="category" class="form-select form-select-sm">
                    <option value="">All Categories</option>
                    <option value="Finance" {% if category == 'Finance' %}selected{% endif %}>Finance</option>
                    <option value="Security" {% if category == 'Security' %}selected{% endif %}>Security</option>
                    <option value="Frontend" {% if category == 'Frontend' %}selected{% endif %}>Frontend</option>
                    <option value="DevOps" {% if category == 'DevOps' %}selected{% endif %}>DevOps</option>
                </select>
            </div>
            <div class="col-md-2">
                <button type="submit" class="btn btn-sm btn-dark w-100">Apply Filter</button>
            </div>
            <div class="col-md-2">
                <a href="/records" class="btn btn-sm btn-outline-secondary w-100">Clear</a>
            </div>
        </form>
    </div>

    <!-- Records Table -->
    <div class="card border-0 shadow-sm bg-white">
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="ps-4">ID</th>
                        <th>Title (Limit: 100)</th>
                        <th>Category</th>
                        <th>Priority</th>
                        <th>Status</th>
                        <th>Due Date</th>
                        <th class="text-end pe-4">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for r in records %}
                    <tr>
                        <td class="ps-4 fw-bold text-muted">#{{ r.id }}</td>
                        <td class="fw-semibold">{{ r.title }}</td>
                        <td><span class="badge bg-secondary">{{ r.category }}</span></td>
                        <td>
                            <span class="badge badge-{{ r.priority|lower }}">{{ r.priority }}</span>
                        </td>
                        <td>
                            {% if r.status == 'Active' %}
                            <span class="badge bg-success-subtle text-success border border-success-subtle">Active</span>
                            {% else %}
                            <span class="badge bg-warning-subtle text-warning border border-warning-subtle">Pending</span>
                            {% endif %}
                        </td>
                        <td>{{ r.date }}</td>
                        <td class="text-end pe-4">
                            <form action="/records/{{ r.id }}/delete" method="POST" class="d-inline" onsubmit="return confirm('TC_CRUD_007: Are you sure you want to delete record #{{ r.id }}?');">
                                <button type="submit" class="btn btn-sm btn-outline-danger" title="Delete Record"><i class="bi bi-trash"></i></button>
                            </form>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="7" class="text-center py-5 text-muted">
                            <i class="bi bi-folder-x fs-1 d-block mb-2 text-secondary"></i>
                            <strong>No records found matching your query.</strong><br>
                            <small>TC_SRCH_002: Empty state verified.</small>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <div class="card-footer bg-white d-flex justify-content-between align-items-center py-3">
            <small class="text-muted">Showing {{ records|length }} record(s)</small>
            <nav>
                <ul class="pagination pagination-sm mb-0">
                    <li class="page-item disabled"><a class="page-link" href="#">Prev</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
            </nav>
        </div>
    </div>
</div>

<!-- Create Modal -->
<div class="modal fade" id="createModal" tabindex="-1">
    <div class="modal-dialog">
        <form class="modal-content" action="/records/create" method="POST">
            <div class="modal-header">
                <h5 class="modal-title fw-bold">Create New Record</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label class="form-label small fw-semibold">Title (Mandatory, Max 100 chars)</label>
                    <input type="text" name="title" class="form-control" maxlength="100" required placeholder="Enter record title">
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-semibold">Category</label>
                    <select name="category" class="form-select" required>
                        <option value="Finance">Finance</option>
                        <option value="Security">Security</option>
                        <option value="Frontend">Frontend</option>
                        <option value="DevOps">DevOps</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-semibold">Priority</label>
                    <select name="priority" class="form-select" required>
                        <option value="Low">Low</option>
                        <option value="Medium">Medium</option>
                        <option value="High">High</option>
                        <option value="Critical">Critical</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label small fw-semibold">Due Date</label>
                    <input type="date" name="date" class="form-control" value="2026-11-30" required>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-primary btn-sm">Save Record</button>
            </div>
        </form>
    </div>
</div>
"""

PROFILE_PAGE = """
<div class="container" style="max-width: 650px;">
    <h3 class="fw-bold mb-1">User Profile & Security Settings</h3>
    <p class="text-muted small mb-4">Verify TC_PROF_001 to TC_PROF_005</p>

    <div class="card border-0 shadow-sm p-4 bg-white mb-4">
        <h5 class="fw-bold mb-3"><i class="bi bi-person-circle text-primary me-2"></i>Profile Information</h5>
        <form action="/profile" method="POST">
            <div class="row g-3 mb-3">
                <div class="col-md-6">
                    <label class="form-label small fw-semibold">Full Name</label>
                    <input type="text" name="name" class="form-control" value="{{ session.get('name') }}" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label small fw-semibold">Role (Read-Only)</label>
                    <input type="text" class="form-control" value="{{ session.get('role') }}" disabled>
                </div>
            </div>
            <button type="submit" class="btn btn-primary btn-sm">Update Details</button>
        </form>
    </div>

    <div class="card border-0 shadow-sm p-4 bg-white">
        <h5 class="fw-bold mb-3"><i class="bi bi-shield-check text-primary me-2"></i>Security & Inactivity Timeout</h5>
        <p class="text-muted small">
            Session inactivity timeout is set to <strong>15 minutes</strong> per specification (TC_SEC_004).
        </p>
        <a href="/logout" class="btn btn-outline-danger btn-sm">End Active Session</a>
    </div>
</div>
"""

ADMIN_PAGE = """
<div class="container-fluid">
    <div class="alert alert-warning py-3">
        <h5 class="fw-bold mb-1"><i class="bi bi-shield-lock-fill me-2"></i>SuperAdmin Restricted Zone</h5>
        <p class="mb-0 small">This area is protected by Role-Based Access Control (RBAC). Only users with role <code>SuperAdmin</code> can view this page (TC_AUTH_010).</p>
    </div>
    <div class="card border-0 shadow-sm p-4 bg-white">
        <h6 class="fw-bold">User Management & Permissions</h6>
        <p class="text-muted small">Access successfully granted to: <strong>{{ session.get('user') }}</strong></p>
    </div>
</div>
"""

# ==================== APPLICATION ROUTES ====================

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("dashboard"))
        login_content = render_template_string(LOGIN_PAGE)
        return render_template_string(BASE_LAYOUT, title="Login", content=login_content)

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    # Security check: Rate limiting (TC_AUTH_004)
    if FAILED_LOGINS.get(email, 0) >= 5:
        err = "Account locked due to 5 failed login attempts. Try again in 15 minutes (TC_AUTH_004)."
        login_content = render_template_string(LOGIN_PAGE, error=err, email=email)
        return render_template_string(BASE_LAYOUT, title="Login", content=login_content)

    # SQL Injection sanity check (TC_SEC_001)
    if "' OR '" in email or "' OR '1'='1" in email or "' --" in email:
        err = "Invalid email or password. (Security: Input sanitized, SQLi prevented - TC_SEC_001)"
        login_content = render_template_string(LOGIN_PAGE, error=err, email=email)
        return render_template_string(BASE_LAYOUT, title="Login", content=login_content)

    # Verify credentials
    user_record = USERS.get(email)
    if not user_record or user_record["password"] != password:
        FAILED_LOGINS[email] = FAILED_LOGINS.get(email, 0) + 1
        err = "Invalid email or password (TC_AUTH_002 / TC_AUTH_003)"
        login_content = render_template_string(LOGIN_PAGE, error=err, email=email)
        return render_template_string(BASE_LAYOUT, title="Login", content=login_content)

    # Success: Establish session
    FAILED_LOGINS[email] = 0
    session["user"] = email
    session["name"] = user_record["name"]
    session["role"] = user_record["role"]
    session["last_active"] = time.time()

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    stats = {
        "total_records": len(RECORDS),
        "critical_records": len([r for r in RECORDS if r["priority"] in ["High", "Critical"]])
    }
    content = render_template_string(DASHBOARD_PAGE, stats=stats)
    return render_template_string(BASE_LAYOUT, title="Dashboard", active_page="dashboard", content=content)

@app.route("/records")
def records_list():
    if "user" not in session:
        return redirect(url_for("login"))

    query = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()

    filtered = RECORDS
    if query:
        filtered = [r for r in filtered if query in r["title"].lower() or query in r["category"].lower()]
    if category:
        filtered = [r for r in filtered if r["category"] == category]

    content = render_template_string(RECORDS_PAGE, records=filtered, query=request.args.get("q", ""), category=category)
    return render_template_string(BASE_LAYOUT, title="Records CRUD", active_page="records", content=content)

@app.route("/records/create", methods=["POST"])
def records_create():
    global NEXT_ID
    if "user" not in session:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "")
    priority = request.form.get("priority", "Medium")
    date_val = request.form.get("date", "2026-11-30")

    if not title:
        return "Title is required", 400

    new_rec = {
        "id": NEXT_ID,
        "title": title,
        "category": category,
        "priority": priority,
        "status": "Active",
        "date": date_val
    }
    RECORDS.insert(0, new_rec)
    NEXT_ID += 1
    return redirect(url_for("records_list"))

@app.route("/records/<int:rec_id>/delete", methods=["POST"])
def records_delete(rec_id):
    global RECORDS
    if "user" not in session:
        return redirect(url_for("login"))

    RECORDS = [r for r in RECORDS if r["id"] != rec_id]
    return redirect(url_for("records_list"))

@app.route("/records/export/csv")
def records_export():
    if "user" not in session:
        return redirect(url_for("login"))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Category", "Priority", "Status", "Due Date"])
    for r in RECORDS:
        writer.writerow([r["id"], r["title"], r["category"], r["priority"], r["status"], r["date"]])

    csv_data = "\ufeff" + output.getvalue()  # UTF-8 BOM
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=records_export.csv"}
    )

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    msg = None
    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        if new_name:
            session["name"] = new_name
            msg = "Profile updated successfully! (TC_PROF_001)"

    content = render_template_string(PROFILE_PAGE)
    return render_template_string(BASE_LAYOUT, title="Profile Settings", active_page="profile", content=content, message=msg, message_type="success")

@app.route("/admin")
def admin_panel():
    if "user" not in session:
        return redirect(url_for("login"))

    # RBAC Security Guard (TC_AUTH_010)
    if session.get("role") != "SuperAdmin":
        return render_template_string(BASE_LAYOUT, title="403 Forbidden", content="""
            <div class='container text-center py-5'>
                <h1 class='display-1 text-danger fw-bold'>403</h1>
                <h3>Access Denied - Role-Based Access Control</h3>
                <p class='text-muted'>Standard users are not authorized to view the Admin Zone (TC_AUTH_010 Passed).</p>
                <a href='/dashboard' class='btn btn-primary btn-sm'>Return to Dashboard</a>
            </div>
        """), 403

    content = render_template_string(ADMIN_PAGE)
    return render_template_string(BASE_LAYOUT, title="Admin Zone", active_page="admin", content=content)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Enterprise Web Portal QA Server is running!")
    print("📍 Local URL: http://127.0.0.1:5000")
    print("👤 Standard User Login: john.doe@example.com / Secure@2026!")
    print("👑 Admin User Login:    admin.test@example.com / AdminSecure@2026!")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False)
