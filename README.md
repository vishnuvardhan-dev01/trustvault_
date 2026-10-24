# TrustVault — Secure Document Sharing

## Overview

TrustVault is a Django-based document-sharing application designed to protect private documents through access permissions and maintain an audit trail of document activity.

## Features

* User registration and authentication.
* Document upload and dashboard.
* Document ownership and sharing permissions.
* Read and edit permission levels.
* Audit events with SHA-256 hash-chain verification.
* Django Admin interface for viewing documents, permissions, and audit events.
* Automated tests for document access control.

## Technology Stack

* Python
* Django
* SQLite
* HTML and CSS
* SHA-256 hashing

## Installation and Setup

1. Install Python.

2. Clone or download the project.

3. Open a terminal in the folder containing `manage.py`.

4. Create and activate a virtual environment.

5. Install Django:

   ```bash
   pip install django
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create an administrator account:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

9. Open `http://127.0.0.1:8000/` in your browser.

## Testing

Run the automated tests:

```bash
python manage.py test vault
```

Verify the audit hash chain:

```bash
python manage.py verify_audit_chain
```

## Admin Panel

Open `http://127.0.0.1:8000/admin/` and log in using a superuser account.

Administrators can inspect document records, sharing permissions, and read-only audit events.

## Security Notes

* Document access must be checked on the server.
* Permissions should be checked for every document request.
* Audit-chain verification helps detect changes to recorded events.
* A hash chain alone does not prevent an attacker with database access from rewriting the entire chain.
* Production deployment requires additional security configuration.

## Project Status

Automated tests and audit-chain verification have passed during development. Additional permission testing, documentation review, and deployment checks remain necessary before final submission.
