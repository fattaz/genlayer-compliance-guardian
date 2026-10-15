# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class TaskGuard(gl.Contract):
    """
    TaskGuard: Autonomous Web Policy & Compliance Guardian.
    Monitors live web pages and evaluates them against compliance rules using GenLayer AI consensus,
    delivering multi-metric status, risk severity, and confidence tiers with auto-sanitization.
    """

    total_audits: u256
    audit_target: TreeMap[str, str]
    audit_rules: TreeMap[str, str]
    audit_status: TreeMap[str, str]     # COMPLIANT | VIOLATION
    audit_severity: TreeMap[str, str]   # NONE | WARNING | CRITICAL
    audit_confidence: TreeMap[str, str] # HIGH | MEDIUM | LOW

    def __init__(self):
        self.total_audits = u256(0)

    @gl.public.write
    def run_audit(self, audit_id: str, target_url: str, compliance_rules: str) -> str:
        """
        Fetches live webpage data, audits it against compliance rules via LLM consensus,
        and records structured multi-metric risk ratings on-chain.
        """
        # Auto-sanitize URL if markdown link format like [text](url) was pasted
        clean_url = target_url.strip()
        if "](" in clean_url:
            clean_url = clean_url.split("](")[-1].rstrip(")")
        clean_url = clean_url.strip()

        if len(clean_url) < 5 or not clean_url.startswith("http"):
            _raise(ValueError("Invalid target URL provided. Must start with http:// or https://"))
        if len(compliance_rules.strip()) < 5:
            _raise(ValueError("Compliance rules description is too short"))

        # Non-deterministic block: runs web scraping and structured token evaluation
        def evaluate_compliance() -> str:
            page_text = gl.nondet.web.render(clean_url, mode="text")
            snippet = page_text[:2000].strip()

            prompt = f"""
            You are an expert corporate compliance auditor.
            Determine whether the provided Web Content satisfies or violates the Compliance Rules.

            Compliance Rules:
            "{compliance_rules}"

            Web Content Snippet:
            ---
            {snippet}
            ---

            Instructions:
            You must output EXACTLY three fields separated by a pipe character (|) in this exact order:
            STATUS | SEVERITY | CONFIDENCE

            Where:
            - STATUS must be either COMPLIANT or VIOLATION
            - SEVERITY must be either NONE, WARNING, or CRITICAL
            - CONFIDENCE must be either HIGH, MEDIUM, or LOW

            Output ONLY the pipe-separated values. No extra text, no markdown formatting.
            """

            response = gl.nondet.exec_prompt(prompt).strip()
            return response

        # Strict equivalence across validators on the standardized token string
        consensus_raw = gl.eq_principle.strict_eq(evaluate_compliance)
        
        # Safely parse the pipe-separated consensus string on-chain
        parts = [p.strip() for p in consensus_raw.split("|")]
        status = parts[0] if len(parts) > 0 and parts[0] in ["COMPLIANT", "VIOLATION"] else "VIOLATION"
        severity = parts[1] if len(parts) > 1 and parts[1] in ["NONE", "WARNING", "CRITICAL"] else "WARNING"
        confidence = parts[2] if len(parts) > 2 and parts[2] in ["HIGH", "MEDIUM", "LOW"] else "MEDIUM"

        # Record structured contract state
        self.audit_target[audit_id] = clean_url
        self.audit_rules[audit_id] = compliance_rules
        self.audit_status[audit_id] = status
        self.audit_severity[audit_id] = severity
        self.audit_confidence[audit_id] = confidence
        self.total_audits = self.total_audits + u256(1)

        return f"AUDIT_SUCCESS: {status} | Risk: {severity} | Confidence: {confidence}"

    @gl.public.view
    def get_audit_status(self, audit_id: str) -> str:
        """Retrieves the compliance status (COMPLIANT or VIOLATION)."""
        return self.audit_status.get(audit_id, "AUDIT_NOT_FOUND")

    @gl.public.view
    def get_audit_severity(self, audit_id: str) -> str:
        """Retrieves the risk severity level (NONE, WARNING, CRITICAL)."""
        return self.audit_severity.get(audit_id, "AUDIT_NOT_FOUND")

    @gl.public.view
    def get_audit_confidence(self, audit_id: str) -> str:
        """Retrieves the AI consensus confidence tier (HIGH, MEDIUM, LOW)."""
        return self.audit_confidence.get(audit_id, "AUDIT_NOT_FOUND")

    @gl.public.view
    def get_audit_details(self, audit_id: str) -> str:
        """Retrieves a comprehensive summary of all audit metrics in a single call."""
        status = self.audit_status.get(audit_id, "AUDIT_NOT_FOUND")
        if status == "AUDIT_NOT_FOUND":
            return "AUDIT_NOT_FOUND"
        target = self.audit_target.get(audit_id, "")
        severity = self.audit_severity.get(audit_id, "")
        confidence = self.audit_confidence.get(audit_id, "")
        return f"Target: {target} | Status: {status} | Severity: {severity} | Confidence: {confidence}"

    @gl.public.view
    def get_total_audits(self) -> u256:
        """Returns total audits processed on-chain."""
        return self.total_audits
