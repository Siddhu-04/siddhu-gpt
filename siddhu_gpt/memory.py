import json
from pathlib import Path
from datetime import datetime

BASE = Path.home() / ".siddhu-gpt" / "sessions"

def session_path(session_id: str) -> Path:
    BASE.mkdir(parents=True, exist_ok=True)
    return BASE / f"{session_id}.json"

def load_session(session_id: str) -> list[dict]:
    p = session_path(session_id)
    if p.exists():
        return json.loads(p.read_text())["messages"]
    return []

def save_session(session_id: str, messages: list[dict]) -> None:
    session_path(session_id).write_text(json.dumps({
        "id": session_id,
        "updated": datetime.now().isoformat(),
        "messages": messages
    }, indent=2))

def list_sessions() -> list[dict]:
    if not BASE.exists():
        return []
    sessions = []
    for f in BASE.glob("*.json"):
        data = json.loads(f.read_text())
        sessions.append({
            "id": data["id"],
            "updated": data["updated"],
            "turns": len([m for m in data["messages"] if m["role"] == "user"])
        })
    return sorted(sessions, key=lambda x: x["updated"], reverse=True)