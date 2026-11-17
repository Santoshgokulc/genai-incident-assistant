from dataclasses import dataclass, field , asdict
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "REPORTED": {"INVESTIGATING", "CANCELLED"},
    "INVESTIGATING": {"MITIGATED", "CANCELLED"},
    "MITIGATED": {"RESOLVED", "INVESTIGATED"},
    "RESOLVED": set(),
    "CANCELLED": set(),
}

VALID_SEVERITIES : set[str] ={
    "SEV1", "SEV2", "SEV3", "SEV4"
}
@dataclass
class IncidentReport:
    id: str
    title: str
    service: str
    severity: str
    status: str = "REPORTED"
    history: list[str] = field(default_factory=list)

    def __post_init__(self) ->None:
        if not self.history:
            self.history.append(self.status)
        if not self.severity in VALID_SEVERITIES:
            raise ValueError(f"Invalid Severity:{self.severity}")

    def transistion_to(self,new_state: str)-> None:
        allowed = ALLOWED_TRANSITIONS.get(self.status,set())
        if new_state not in allowed:
            raise ValueError(f"Invalid Transaction from{self.status} to {new_state}")
        self.status = new_state
        self.history.append(new_state)
    def to_dict(self) -> dict:
        return asdict(self)


def validate_incident_transitions(history: list[str]) -> tuple[bool, str | None]:
    # 1. Guard clause: is history empty OR does it NOT start with "REPORTED"?
    if not history or history[0] != "REPORTED":
        return (False, "Incident must start with the REPORTED")
    for i in range (len(history)-1):
        current_state = history[i]
        next_state = history[i+1]

        allowed = ALLOWED_TRANSITIONS.get(current_state,set())
        if next_state not in allowed:
            return (False, f"Invalid transition from {current_state} to {next_state}")
    
    return (True, None)
def deduplicate_incidents(incidents:list[IncidentReport]) -> list[IncidentReport]:
    seen:dict[str,IncidentReport] ={}
    for inc in incidents:
        seen[inc.id] = inc
    return list(seen.values())
if __name__ == "__main__":
    # Test 1: Empty history (should fail)
    print("Test 1 (Empty):", validate_incident_transitions([]))

    # Test 2: Starts with wrong state (should fail)
    print("Test 2 (Wrong Start):", validate_incident_transitions(["INVESTIGATING"]))

    # Test 3: Valid start (should pass)
    print("Test 3 (Valid Start):", validate_incident_transitions(["REPORTED"]))

    # Test 4: Full valid lifecycle
    print(
        "Test 4 (Valid Full):",
        validate_incident_transitions(
            ["REPORTED", "INVESTIGATING", "MITIGATED", "RESOLVED"]
        ),
    )

    # Test 5: Invalid jump (skipping steps)
    print(
        "Test 5 (Invalid Jump):",
        validate_incident_transitions(["REPORTED", "RESOLVED"]),
    )

    # Test 6: Move after terminal state
    print(
        "Test 6 (After Terminal):",
        validate_incident_transitions(["REPORTED", "CANCELLED", "INVESTIGATING"]),
    )
    inc = IncidentReport(
        id="INC-101",
        title="Payment gateway timeout",
        service="payment-service", 
        severity="SEV1", 
    ) 
    print("Incident created:", inc) 
    print("Initial status:", inc.status)
    print("Initial history:", inc.history)
    inc.transistion_to("INVESTIGATING")
    print("New status:", inc.status) 
    print("Updated history:", inc.history)

    # 2. Invalid transition: INVESTIGATING -> RESOLVED (cannot skip MITIGATED)
    try:
        inc.transistion_to("RESOLVED")
    except ValueError as e:
        print("Caught expected error:", e)
    # Test invalid severity upon creation (should raise ValueError)
        try:
            invalid_inc = IncidentReport(
                id="INC-999",
                title="Fake incident",
                service="auth-service",
                severity="CRITICAL",  # <-- Not in {"SEV1", "SEV2", "SEV3", "SEV4"}!
            )
        except ValueError as e:
            print("Caught expected severity error:", e)
    data = inc.to_dict()
    print("Exported dict:", data)
    print("Is it a dict?", type(data) is dict)
    inc1_v1 = IncidentReport("INC-1", "DB slow", "auth", "SEV2", status="REPORTED")
    inc2 = IncidentReport("INC-2", "API 500", "payment", "SEV1", status="REPORTED")
    inc1_v2 = IncidentReport("INC-1", "DB slow", "auth", "SEV2", status="INVESTIGATING") 
  
    deduped = deduplicate_incidents([inc1_v1, inc2, inc1_v2]) 
    print("Deduplicated count:", len(deduped)) # Should be 2!
    for item in deduped:
        print(" ->", item.id, item.status)

