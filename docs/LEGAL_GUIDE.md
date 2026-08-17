# Legal Considerations Guide — EcoInfraMind AI

## 1. Scope

This document provides high-level guidance on legal and regulatory considerations relevant to deploying an AI-assisted engineering tool in African infrastructure contexts. It is not legal advice. Users should consult qualified legal professionals in their jurisdiction before deployment.

## 2. Engineering Liability

### 2.1 Professional Responsibility
- AI-generated outputs do not replace professional engineering judgment.
- The system is a reference and calculation aid; final design decisions must be reviewed and approved by a licensed professional engineer.
- In many African jurisdictions, engineering designs, reports, and EIAs must bear the seal/signature of a registered engineer (e.g., COREN in Nigeria, ERSB in Ghana).

### 2.2 Standard of Care
- Engineers using AI tools remain fully responsible for the accuracy and adequacy of their work.
- Reliance on AI-generated calculations does not reduce the standard of care owed to clients and the public.
- Users should independently verify all critical calculations against established standards and codes.

### 2.3 Disclaimer Requirements
The application includes a prominent disclaimer that:
- Outputs are for reference and educational purposes only.
- The AI may produce incorrect or incomplete information.
- Professional verification is required before using outputs in real projects.
- The tool is not certified or approved by any engineering regulatory body.

## 3. Intellectual Property

### 3.1 Knowledge Base Content
- Source documents in `knowledge/` are either:
  - Public domain documents (government standards, open-access publications)
  - Original content created by the development team
  - Content used with explicit permission from the copyright holder
- Users must ensure uploaded documents do not infringe third-party copyrights.

### 3.2 User-Generated Content
- Conversations and uploaded documents remain on the local machine (100% offline).
- No user data is transmitted to external servers.
- Users retain full ownership of their content.

### 3.3 Model Licensing
- Qwen2.5-3B is released under Apache 2.0 license. Attribution is required in derivative works.
- all-MiniLM-L6-v2 (sentence-transformers) is released under Apache 2.0 license.
- All other dependencies (FastAPI, ChromaDB, llama-cpp-python) are MIT or Apache 2.0 licensed.

## 4. Data Privacy and Protection

### 4.1 Local-Only Operation
- The system operates entirely offline after installation.
- No data leaves the user's machine.
- No analytics, telemetry, or usage data is collected.
- Compliant with offline-only data protection requirements.

### 4.2 Sensitive Data
- Users should not input personally identifiable information (PII) unless necessary.
- The system does not encrypt stored conversations; users handling sensitive project data should:
  - Use full-disk encryption (BitLocker, VeraCrypt)
  - Clear the ChromaDB database after each project session (via `/api/v1/knowledge/clear`)
  - Consider running the application from an encrypted volume

### 4.3 Regulatory Compliance
- For projects subject to GDPR, POPIA (South Africa), or similar data protection laws:
  - The fully offline architecture supports compliance by design
  - No data transfer, processing, or storage outside the user's control
  - Users must implement their own access controls and encryption measures

## 5. Regulatory Considerations by Region

### 5.1 Nigeria
- COREN Act (Cap C12 LFN 2004): Engineering designs must be by registered engineers
- NITDA Data Protection Regulation: Applies to processing of personal data
- AI-generated engineering outputs require COREN-registered engineer review

### 5.2 Ghana
- Engineering Council Act, 1993 (PNDCL 312): Professional registration required
- Data Protection Act, 2012 (Act 843): Data protection requirements
- Local content requirements for infrastructure projects

### 5.3 Kenya
- Engineers Registration Act (Cap 530): Registration required
- Data Protection Act, 2019: Comprehensive data protection framework
- National construction authority approvals may be needed

### 5.4 South Africa
- Engineering Profession Act, 2000: ECSA registration required
- POPIA (Protection of Personal Information Act): Strict data protection
- AI advisory tools subject to professional practice guidelines

### 5.5 East African Community (EAC)
- EAC engineers must be registered with respective national bodies
- Cross-border projects may require multiple registrations
- Data protection laws vary by member state

## 6. Ethical Use Guidelines

- Do not use AI-generated designs for critical life-safety structures without full independent verification.
- Disclose use of AI tools to clients and regulatory bodies when required.
- The system is a productivity tool, not a substitute for engineering education or experience.
- Users should critically evaluate all outputs, especially unexpected or borderline results.
- Misuse for generating false documentation or bypassing regulatory requirements is prohibited.

## 7. Competition Compliance (ADTC 2026)

- The system uses llama.cpp only for model inference, as required by competition rules.
- No cloud APIs, no external model services, no internet dependency.
- All models are locally hosted GGUF files.
- Code is open-source and auditable for compliance verification.

## 8. Open Source License

EcoInfraMind AI is provided for educational and reference purposes. See LICENSE file for terms. No warranty or liability is provided for engineering or legal use.
