# 🛡️ TaskGuard: Autonomous Web Policy & Compliance Guardian

## 🚀 Overview
**TaskGuard** is a decentralized, autonomous regulatory and compliance monitoring DApp built on **GenLayer**. It bridges the gap between smart contracts and real-world web data by leveraging decentralized AI validator consensus (`gl.nondet.web.render`, `gl.nondet.exec_prompt`, and `gl.eq_principle.strict_eq`) to audit live web pages against plain-English compliance policies.

---

## 🔑 Key Features
- **Live Web Scraping & Auditing:** Dynamically fetches and analyzes public web pages in real time without centralized middleware.
- **Multi-Metric Risk Assessment:** Evaluates compliance across three distinct dimensions:
  1. **Status:** (`COMPLIANT` | `VIOLATION`)
  2. **Risk Severity:** (`NONE` | `WARNING` | `CRITICAL`)
  3. **Confidence Tier:** (`HIGH` | `MEDIUM` | `LOW`)
- **Deterministic Cross-Model Consensus:** Employs pipe-token normalization and strict equivalence checks (`gl.eq_principle.strict_eq`) to guarantee 100% agreement across diverse LLM validator nodes (GPT-4, Claude, Grok, Qwen).
- **Auto-Sanitization & On-Chain Storage:** Includes robust input sanitization for URLs and immutable on-chain record-keeping using optimized `TreeMap` data structures.

---

## 🏗️ Architecture & Technical Design

TaskGuard strictly adheres to GenLayer's GenVM architectural guidelines:
1. **Flat Scalar & TreeMap Storage:** Persistent state variables use primitive types and `TreeMap` structures.
2. **Encapsulated Non-Determinism:** All web rendering and LLM prompt execution are strictly encapsulated inside inner helper functions passed to equivalence principles.
3. **Standardized Tokenization:** Eliminates free-form text divergence in validator consensus by enforcing rigid categorical output tokens.

---

## 📜 Smart Contract Interface (`task_guard.py`)

### Write Methods
- `run_audit(audit_id: str, target_url: str, compliance_rules: str) -> str`: Fetches the target URL, executes multi-metric AI evaluation under consensus, and records the findings on-chain.

### View Methods
- `get_audit_status(audit_id: str) -> str`: Returns compliance status.
- `get_audit_severity(audit_id: str) -> str`: Returns risk severity level.
- `get_audit_confidence(audit_id: str) -> str`: Returns AI confidence tier.
- `get_audit_details(audit_id: str) -> str`: Returns a comprehensive summary string of all metrics.
- `get_total_audits() -> u256`: Returns total audits processed.

---

## 🧪 Testing & Deployment
1. Deploy `task_guard.py` on **GenLayer Studio**.
2. Call `run_audit` with a valid public URL and compliance rules.
3. Query results instantly using `get_audit_details`.
