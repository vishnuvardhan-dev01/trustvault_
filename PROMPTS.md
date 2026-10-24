# TrustVault — AI Prompt and Development Log

This document records AI assistance used during TrustVault development. Entries should reflect the actual development process and be updated when additional AI assistance is used.

## Entry 1 — Django Project Setup

**Date:** 2026-10-19

**Prompt:** Guide me through creating a Django document-sharing project in VS Code, including the virtual environment and initial setup.

**Purpose:** Set up the project structure and development environment.

**Result:** Used step-by-step instructions to configure the Django project.

## Entry 2 — Authentication and Templates

**Date:** 2026-10-19

**Prompt:** Help me implement signup, login, logout, and a dashboard in Django.

**Purpose:** Provide a basic interface for authenticated users.

**Result:** Developed the authentication pages and dashboard. Tested the application during development.

## Entry 3 — Document Permissions

**Date:** 2026-10-20

**Prompt:** Help me enforce document ownership and read/edit permissions in Django so unauthorized users cannot access private documents.

**Purpose:** Protect documents and enforce access control.

**Result:** Added permission-checking logic and tests for authorized and unauthorized access.

## Entry 4 — Audit Hash Chain

**Date:** 2026-10-21

**Prompt:** Help me implement a tamper-evident audit hash chain using SHA-256, previous-event hashes, and event hashes.

**Purpose:** Detect changes to recorded audit events.

**Result:** Implemented audit-chain initialization and verification commands. The verification command reported success for the existing events after initialization.

**Limitation:** Rebuilding the chain establishes hashes for current records; it does not prove that historical records were never modified.

## Entry 5 — Django Admin Audit Log

**Date:** 2026-10-23

**Prompt:** Register documents, document grants, and audit events in Django Admin. Make audit events read-only and provide useful search and filtering options.

**Purpose:** Allow administrators to inspect document records and audit activity.

**Result:** Registered the three models in Django Admin and configured audit events as read-only.

## Lessons Learned

* Django class methods and attributes require correct indentation.
* Access checks must be enforced on the server, not only hidden in the interface.
* Automated tests help verify permission rules.
* Hash-chain verification checks integrity against the stored hashes but is not a substitute for independently protected audit storage.
* AI-generated code must be reviewed, tested, and corrected before use.
