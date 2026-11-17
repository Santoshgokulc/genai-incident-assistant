# Drill 2: Incident Schema Validation & State Transitions — Summary & Cheatsheet

**Date:** November 17, 2026  
**Curriculum Alignment:** Phase 0 — Environment Setup & Python Muscle Memory  
**Target File:** `drills/drill_2_schemas.py`  
**Status:** **PASSED & VERIFIED** ✅  

---

## 1. Executive Summary & Journey

### The Problem
Implement a deterministic finite state machine (FSM) to validate incident lifecycle transitions, an immutable dataclass schema (`IncidentReport`) with strict field and severity validation, safe transition mutation with audit history, JSON serialization via `asdict`, and an $O(n)$ alert deduplication algorithm.

### How We Arrived Here (The "Divide & Conquer" Progression)
1. **Logic Gate 2 (State Machine & Guard Clauses)**:
   - Defined `ALLOWED_TRANSITIONS` mapping valid lifecycle steps using $O(1)$ set lookups.
   - Built `validate_incident_transitions` to catch empty histories, invalid start states, illegal stage jumps, and transitions attempting to exit terminal states (`RESOLVED`, `CANCELLED`).
2. **Stage 1 (Data Contract & Post-Init Validation)**:
   - Defined `IncidentReport` dataclass using `field(default_factory=list)` to avoid shared mutable state traps.
   - Used `__post_init__` to validate severity against `VALID_SEVERITIES` upon object creation.
3. **Stage 2 (Safe State Transitions)**:
   - Implemented `transition_to(new_state)` method to validate jumps against the FSM and append to audit history.
4. **Stage 3 (Serialization & Deduplication)**:
   - Used `dataclasses.asdict` inside `to_dict()` for clean primitive dictionary exports.
   - Built `deduplicate_incidents` leveraging dictionary key uniqueness to preserve the latest state per incident ID in $O(n)$ time.

---

## 2. Technical Cheatsheet: JavaScript vs. Python 3.12

### 1. The State Machine & Set Lookups

| Concept | Vanilla JavaScript | Python 3.12 Idiom | Why It Matters |
| :--- | :--- | :--- | :--- |
| **Set of Values** | `new Set(["INVESTIGATING", "CANCELLED"])` | `{"INVESTIGATING", "CANCELLED"}` | Instant $O(1)$ hash lookup vs. $O(n)$ linear array scan. |
| **Empty Set** | `new Set()` | `set()` | `{}` creates an empty dict; `set()` creates an empty set. |
| **Membership Check** | `set.has("RESOLVED")` | `"RESOLVED" in set` | Canonical, readable English-like check. |

---

### 2. Dataclass Fields & Mutable Defaults

```python
from dataclasses import dataclass, field

@dataclass
class IncidentReport:
    id: str
    title: str
    service: str
    severity: str
    status: str = "REPORTED"
    history: list[str] = field(default_factory=list) # FRESH list per instance!
```

> [!WARNING]
> **The Mutable Default Argument Trap in Python**:  
> In Python, writing `history: list[str] = []` creates a **single shared list in memory across all instances**.  
> Always use `field(default_factory=list)` so each instance receives its own unique list.

---

### 3. Constructor Validation (`__post_init__`)

- In JS: Validation happens inside `constructor() { ... }`.
- In Python `@dataclass`: The constructor is generated automatically. To run code immediately after creation, implement `__post_init__(self)`:

```python
def __post_init__(self) -> None:
    if self.severity not in VALID_SEVERITIES:
        raise ValueError(f"Invalid Severity: {self.severity}")
    if not self.history:
        self.history.append(self.status)
```

---

### 4. Serialization: `dataclasses.asdict`

- **Purpose**: Converts a live Python class instance (with methods and internal references) into a plain primitive `dict` suitable for JSON encoding.
- **Syntax**:
  ```python
  from dataclasses import asdict

  def to_dict(self) -> dict:
      return asdict(self)
  ```
- **Benefit**: Deep-copies nested structures so external mutations do not affect the live instance.

---

### 5. Deduplication by Key (`seen[inc.id] = inc`)

#### How it works:
```python
def deduplicate_incidents(incidents: list[IncidentReport]) -> list[IncidentReport]:
    seen: dict[str, IncidentReport] = {}
    for inc in incidents:
        seen[inc.id] = inc       # Overwrites duplicate keys; keeps latest update
    return list(seen.values())   # Extracts only the incident objects
```

#### Comparison with JS:
```javascript
// JavaScript equivalent:
function deduplicateIncidents(incidents) {
  const seen = new Map();
  for (const inc of incidents) {
    seen.set(inc.id, inc);
  }
  return Array.from(seen.values());
}
```
- **Time Complexity**: $O(n)$ where $n$ is total incoming incidents.
- **Space Complexity**: $O(u)$ where $u$ is unique incident IDs.
