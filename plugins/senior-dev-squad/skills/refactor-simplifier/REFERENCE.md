# Refactor Simplifier — Worked Example

This example shows one messy function simplified in three atomic steps.
Tests are green after every step. No behavior changes — only structure.

---

## The Starting Code

```python
# user_service.py

class UserProcessor:
    """Processes user data for registration or profile update."""

    def processUserData(self, d, isNew):
        # validate
        if d.get("email") and "@" in d["email"] and "." in d["email"].split("@")[-1]:
            validEmail = True
        else:
            validEmail = False

        if isNew:
            if validEmail:
                u = User(
                    email=d["email"],
                    name=d.get("name") or "Unknown",
                    role=d.get("role") if d.get("role") in ["admin", "editor", "viewer"] else "viewer",
                )
                db.session.add(u)
                db.session.commit()
                return {"ok": True, "msg": "created", "id": u.id}
            else:
                return {"ok": False, "msg": "bad email"}
        else:
            if validEmail:
                u = db.session.query(User).filter_by(email=d["email"]).first()
                if u:
                    u.name = d.get("name") or u.name
                    u.role = d.get("role") if d.get("role") in ["admin", "editor", "viewer"] else u.role
                    db.session.commit()
                    return {"ok": True, "msg": "updated", "id": u.id}
                else:
                    return {"ok": False, "msg": "not found"}
            else:
                return {"ok": False, "msg": "bad email"}
```

**What's wrong:**

| Problem | Location |
|---------|----------|
| Boolean parameter `isNew` splits the function into two unrelated paths | signature |
| Inline email validation repeated (will be repeated again next caller) | lines 6–10 |
| `d`, `u`, `validEmail` — opaque names | throughout |
| Role allow-list duplicated in both branches | lines 16, 24 |
| Single class wrapping two static-ish functions — adds nothing | `UserProcessor` |

---

## Step 1 — Replace the Boolean Flag with Two Named Functions

**Rule applied:** #10 (boolean parameters → separate functions)

Commit message: `refactor: split processUserData boolean flag into register_user / update_user`

```python
# user_service.py

def register_user(data, isNew):          # isNew removed in next line
    ...

# WRONG — just renaming the flag does nothing. Instead:

def register_user(data):
    if data.get("email") and "@" in data["email"] and "." in data["email"].split("@")[-1]:
        validEmail = True
    else:
        validEmail = False

    if validEmail:
        u = User(
            email=data["email"],
            name=data.get("name") or "Unknown",
            role=data.get("role") if data.get("role") in ["admin", "editor", "viewer"] else "viewer",
        )
        db.session.add(u)
        db.session.commit()
        return {"ok": True, "msg": "created", "id": u.id}
    else:
        return {"ok": False, "msg": "bad email"}


def update_user(data):
    if data.get("email") and "@" in data["email"] and "." in data["email"].split("@")[-1]:
        validEmail = True
    else:
        validEmail = False

    if validEmail:
        user = db.session.query(User).filter_by(email=data["email"]).first()
        if user:
            user.name = data.get("name") or user.name
            user.role = data.get("role") if data.get("role") in ["admin", "editor", "viewer"] else user.role
            db.session.commit()
            return {"ok": True, "msg": "updated", "id": user.id}
        else:
            return {"ok": False, "msg": "not found"}
    else:
        return {"ok": False, "msg": "bad email"}
```

**Run tests. Green? Commit.**

Names are now explicit. The `UserProcessor` wrapper class is gone — it held no state and added no value (rule #6). The duplication is now visible because both functions sit side by side. That's fine: making duplication visible is the point of this step.

---

## Step 2 — Extract the Duplicated Validation

**Rule applied:** #5 (duplication 3+ occurrences → extract function; here 2 occurrences with a third caller already planned)
**Rule applied:** #2 (opaque names → descriptive)

Commit message: `refactor: extract validate_email, name ALLOWED_ROLES constant`

```python
# user_service.py

ALLOWED_ROLES = {"admin", "editor", "viewer"}


def _is_valid_email(email):
    """Return True when email has an @ and a dot after it."""
    if not email:
        return False
    parts = email.split("@")
    return len(parts) == 2 and "." in parts[1]


def register_user(data):
    if not _is_valid_email(data.get("email")):
        return {"ok": False, "msg": "bad email"}

    role = data.get("role") if data.get("role") in ALLOWED_ROLES else "viewer"
    new_user = User(
        email=data["email"],
        name=data.get("name") or "Unknown",
        role=role,
    )
    db.session.add(new_user)
    db.session.commit()
    return {"ok": True, "msg": "created", "id": new_user.id}


def update_user(data):
    if not _is_valid_email(data.get("email")):
        return {"ok": False, "msg": "bad email"}

    existing_user = db.session.query(User).filter_by(email=data["email"]).first()
    if not existing_user:
        return {"ok": False, "msg": "not found"}

    existing_user.name = data.get("name") or existing_user.name
    existing_user.role = data.get("role") if data.get("role") in ALLOWED_ROLES else existing_user.role
    db.session.commit()
    return {"ok": True, "msg": "updated", "id": existing_user.id}
```

**Run tests. Green? Commit.**

Changes in this step only:
- Validation logic lives in one place (`_is_valid_email`). Fix it once; both callers benefit.
- `ALLOWED_ROLES` is a named constant — no more magic strings repeated twice.
- `validEmail` bool variable gone — guard clause exits early instead (rule #7).
- `u` renamed to `new_user` / `existing_user` — self-documenting (rule #2).

---

## Step 3 — Delete the Single-Implementation Abstraction

In the original codebase there was also this:

```python
# processors/base.py
class DataProcessor(ABC):
    @abstractmethod
    def process(self, data): ...

# processors/user_processor.py
class UserProcessor(DataProcessor):
    def process(self, data):
        return processUserData(data, True)   # always True — update path never used
```

`DataProcessor` has exactly one implementation. No second implementation exists or is planned. The abstraction adds a file, an import, and a mental indirection — nothing else.

**Rule applied:** #6 (single-implementation interface → remove abstraction)

Commit message: `refactor: delete DataProcessor ABC, inline UserProcessor into user_service`

Delete `processors/base.py` and `processors/user_processor.py`. Update the one call site:

```python
# Before (call site)
processor = UserProcessor()
result = processor.process(payload)

# After (call site)
result = register_user(payload)
```

**Run tests. Green? Commit.**

---

## Final State

```python
# user_service.py

ALLOWED_ROLES = {"admin", "editor", "viewer"}


def _is_valid_email(email):
    if not email:
        return False
    parts = email.split("@")
    return len(parts) == 2 and "." in parts[1]


def register_user(data):
    if not _is_valid_email(data.get("email")):
        return {"ok": False, "msg": "bad email"}
    role = data.get("role") if data.get("role") in ALLOWED_ROLES else "viewer"
    new_user = User(email=data["email"], name=data.get("name") or "Unknown", role=role)
    db.session.add(new_user)
    db.session.commit()
    return {"ok": True, "msg": "created", "id": new_user.id}


def update_user(data):
    if not _is_valid_email(data.get("email")):
        return {"ok": False, "msg": "bad email"}
    existing_user = db.session.query(User).filter_by(email=data["email"]).first()
    if not existing_user:
        return {"ok": False, "msg": "not found"}
    existing_user.name = data.get("name") or existing_user.name
    existing_user.role = data.get("role") if data.get("role") in ALLOWED_ROLES else existing_user.role
    db.session.commit()
    return {"ok": True, "msg": "updated", "id": existing_user.id}
```

**What changed (structure only — zero behavior change):**

| Before | After |
|--------|-------|
| 1 function with boolean flag | 2 named functions |
| Email validation inline ×2 | `_is_valid_email` ×1 |
| Role allow-list strings ×2 | `ALLOWED_ROLES` constant ×1 |
| `DataProcessor` ABC + `UserProcessor` class | Deleted — 2 files gone |
| Opaque names `d`, `u`, `validEmail` | `data`, `new_user`, guard clause |
| Cyclomatic complexity: 8 | Cyclomatic complexity: 4 |
| 3 commits needed | 3 commits, each independently reviewable |

No comments added. No new abstractions. No behavior changed.
