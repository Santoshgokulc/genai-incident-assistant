# JavaScript to Python 3.12: Arrays, Objects & Functions Reference

A practical cheat sheet comparing plain JavaScript patterns directly to Python 3.12 idioms.

---

## 1. Array Iteration & Transformations

| Task | Vanilla JavaScript | Python 3.12 Idiom | Time Complexity |
| :--- | :--- | :--- | :--- |
| **Transform (`map`)** | `arr.map(x => x.name)` | `[x.name for x in arr]` | $O(n)$ |
| **Filter (`filter`)** | `arr.filter(x => x.active)` | `[x for x in arr if x.active]` | $O(n)$ |
| **Filter + Transform** | `arr.filter(x => x.active).map(x => x.name)` | `[x.name for x in arr if x.active]` | $O(n)$ *(single pass)* |
| **Find First Match** | `arr.find(x => x.id === 5)` | `next((x for x in arr if x.id == 5), None)` | $O(n)$ *(stops at first match)* |
| **Check Any Match** | `arr.some(x => x.errors > 0)` | `any(x.errors > 0 for x in arr)` | $O(n)$ *(short-circuits)* |
| **Check All Match** | `arr.every(x => x.valid)` | `all(x.valid for x in arr)` | $O(n)$ *(short-circuits)* |
| **Membership Check** | `arr.includes("target")` | `"target" in arr` *(better with set)* | $O(n)$ in list, **$O(1)$ in set** |

---

## 2. Reducing & Frequency Counting (`reduce` vs `defaultdict`)

### JavaScript: Grouping / Tallying via `reduce`
```javascript
const logs = [
  { service: "auth", status: "ERROR" },
  { service: "auth", status: "INFO" },
  { service: "payment", status: "ERROR" }
];

const counts = logs.reduce((acc, item) => {
  acc[item.service] = (acc[item.service] || 0) + 1;
  return acc;
}, {});
// Result: { auth: 2, payment: 1 }
```

### Python 3.12: Grouping via `defaultdict`
```python
from collections import defaultdict

logs = [
    {"service": "auth", "status": "ERROR"},
    {"service": "auth", "status": "INFO"},
    {"service": "payment", "status": "ERROR"},
]

counts = defaultdict(int)
for item in logs:
    counts[item["service"]] += 1
# Accessing any missing key automatically initializes to 0!
```

---

## 3. Objects & Dictionaries

| Operation | Vanilla JavaScript | Python 3.12 |
| :--- | :--- | :--- |
| **Read with fallback** | `obj[key] !== undefined ? obj[key] : "default"` | `data.get(key, "default")` |
| **Delete key** | `delete obj[key]` | `del data[key]` or `data.pop(key, None)` |
| **Get Keys** | `Object.keys(obj)` | `list(data.keys())` |
| **Get Values** | `Object.values(obj)` | `list(data.values())` |
| **Loop Key & Value** | `for (const [k, v] of Object.entries(obj))` | `for k, v in data.items():` |
| **Shallow Copy / Merge** | `const merged = { ...objA, ...objB }` | `merged = obj_a \| obj_b` (Python 3.9+) |

---

## 4. Functions & Arguments

### Rest & Spread Operators
```javascript
// JavaScript
function sendBatch(service, ...items) {
  console.log(service, items);
}
sendBatch("auth", "log1", "log2");
```
```python
# Python (*args for tuple of positional args, **kwargs for dict of keyword args)
def send_batch(service: str, *items: str) -> None:
    print(service, items)

send_batch("auth", "log1", "log2")
```

### Keyword Unpacking (Passing Object Properties)
```javascript
// JavaScript
const data = { timestamp: "10:00", level: "ERROR" };
createLog({ ...data, service: "auth" });
```
```python
# Python
data = {"timestamp": "10:00", "level": "ERROR"}
create_log(**data, service="auth")
```

---

## 5. Common Traps for JavaScript Engineers in Python

1. **Semicolons**: JavaScript lines often end with `;`. Python does not use semicolons.
2. **Iterating Strings**: In JS, `for (const x of "hello")` or `for (let i = 0; ...)` is common, but doing `for line in logs:` when `logs` is a string iterates over **every single character**! Use `logs.splitlines()` to get an array of line strings.
3. **Identity vs. Value**:
   - JS `===` checks value and type.
   - Python `==` checks value equality (`"ERROR" == "ERROR"` &rarr; `True`).
   - Python `is` checks memory identity. Use `is None` or `is not None` only.
4. **Comprehensions over `.append()`**:
   ```python
   # ❌ Non-Pythonic (imperative append loop):
   results = []
   for x in items:
       if x.valid:
           results.append(x.name)

   # ✅ Pythonic (single-pass list comprehension):
   results = [x.name for x in items if x.valid]
   ```
