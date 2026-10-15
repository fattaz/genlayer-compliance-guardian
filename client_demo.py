# client_demo.py
# Example script to interact with deployed TaskGuard contract on GenLayer

from genlayer import GenLayerClient

# Initialize GenLayer client (update endpoint / contract address as needed)
client = GenLayerClient(rpc_url="https://studio.genlayer.com/rpc")
contract_address = "YOUR_DEPLOYED_CONTRACT_ADDRESS"

def run_remote_audit(audit_id: str, url: str, rules: str):
    print(f"Triggering on-chain compliance audit for {url}...")
    tx = client.write(
        contract_address=contract_address,
        method="run_audit",
        args=[audit_id, url, rules]
    )
    print(f"Transaction finalized! Result: {tx.result}")

def fetch_audit_summary(audit_id: str):
    details = client.read(
        contract_address=contract_address,
        method="get_audit_details",
        args=[audit_id]
    )
    print(f"Audit Details [{audit_id}]: {details}")

if __name__ == "__main__":
    # Example execution
    run_remote_audit("audit_demo_1", "https://example.com", "The page must contain a valid heading.")
    fetch_audit_summary("audit_demo_1")
