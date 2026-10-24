# TrustVault — Threat Model

## 1. Project Overview

TrustVault is a secure document-sharing application built with Python and Django. It allows users to upload documents, manage access permissions, and maintain an audit trail of document activities.

## 2. Assets to Protect

* Uploaded documents and their contents.
* User accounts and authentication credentials.
* Document ownership and sharing permissions.
* Audit events and their hash chain.
* User and document metadata.

## 3. Potential Threats

### Threat 1: Unauthorized Document Access

**Risk:** A user may attempt to access another user's private document.

**Mitigation:** Check document ownership or explicit read/edit permission before allowing access or downloads.

### Threat 2: Unauthorized Document Modification

**Risk:** A user without edit permission may attempt to change a document or its permissions.

**Mitigation:** Enforce edit authorization on the server for every modification request.

### Threat 3: Insecure Sharing Permissions

**Risk:** A document may remain accessible after its permission is revoked.

**Mitigation:** Check current permissions on every request and remove revoked grants.

### Threat 4: Malicious File Uploads

**Risk:** An attacker may upload oversized or potentially dangerous files.

**Mitigation:** Enforce file-size limits, validate uploads, and restrict access to uploaded files.

### Threat 5: Audit Log Tampering

**Risk:** Someone may attempt to alter or remove audit records.

**Mitigation:** Make audit records read-only through Django Admin and use a hash chain to detect changes to recorded events. Restrict database and server access because a hash chain alone does not prevent a privileged attacker from rewriting the entire chain.

### Threat 6: Cross-Site Request Forgery (CSRF)

**Risk:** An attacker may trick an authenticated user into submitting an unwanted request.

**Mitigation:** Use Django's CSRF middleware and CSRF tokens in forms that change data.

### Threat 7: Weak Authentication

**Risk:** Weak passwords or compromised accounts may allow unauthorized access.

**Mitigation:** Use Django authentication and password validation, protect credentials, and restrict administrative access.

## 4. Security Testing

* Test that document owners can access their documents.
* Test that authorized readers can download shared documents.
* Test that unauthorized users cannot access private documents.
* Test that readers cannot perform edit operations.
* Test that revoked permissions no longer grant access.
* Run the audit-chain verification command to check hash integrity.

## 5. Remaining Limitations

The application requires further security review before production deployment. Additional measures may include malware scanning, secure production settings, rate limiting, encrypted backups, and external storage for tamper-resistant audit records.
