# session_memory.py
"""
In-memory per-session store for the chatbot.

Each session tracks:
  - last_pgs      : list of PG dicts from the most recent recommendation
  - last_filters  : the parsed filters used in that recommendation
  - last_lang     : detected language of the last message
  - history       : list of (role, text) pairs  — last N turns
  - last_active   : timestamp of last activity  — for expiry

Sessions expire after SESSION_TTL_MINUTES of inactivity.
The store is cleaned lazily on each write.
"""

import time
import threading
from typing import Optional

SESSION_TTL_SECONDS = 30 * 60   # 30 minutes idle → expire
MAX_HISTORY_TURNS   = 10        # keep last 10 user+bot exchanges
MAX_SESSIONS        = 500       # cap to avoid unbounded growth

_store: dict = {}               # session_id → dict
_lock = threading.Lock()


# ── Public API ──────────────────────────────────────────────────────────────

def get_session(session_id: str) -> dict:
    """Return the session dict, creating it if it doesn't exist."""
    with _lock:
        _evict_expired()
        if session_id not in _store:
            _store[session_id] = _new_session()
        return _store[session_id]


def save_session(session_id: str, session: dict) -> None:
    """Persist updated session back to the store and refresh timestamp."""
    with _lock:
        session['last_active'] = time.time()
        _store[session_id] = session


def push_history(session: dict, role: str, text: str) -> None:
    """
    Append a turn to the session history.
    role: 'user' or 'bot'
    Trims to MAX_HISTORY_TURNS pairs (2 * MAX turns entries).
    """
    session['history'].append({'role': role, 'text': text})
    max_entries = MAX_HISTORY_TURNS * 2
    if len(session['history']) > max_entries:
        session['history'] = session['history'][-max_entries:]


def format_history_for_gemini(session: dict) -> str:
    """
    Build a compact conversation history string to inject into Gemini prompts.
    Returns empty string if no history.
    """
    history = session.get('history', [])
    if not history:
        return ''
    lines = []
    for turn in history[-8:]:   # last 4 pairs max
        prefix = 'User' if turn['role'] == 'user' else 'Quanta'
        lines.append(f"{prefix}: {turn['text'][:200]}")
    return '\n'.join(lines)


def format_last_pgs_for_gemini(session: dict) -> str:
    """
    Summarise the last shown PGs into a compact string for Gemini context.
    """
    pgs = session.get('last_pgs', [])
    if not pgs:
        return ''
    lines = ['Recently shown PGs:']
    for i, pg in enumerate(pgs, 1):
        lines.append(
            f"  {i}. {pg.get('PG_Name','?')} | "
            f"₹{pg.get('Rent','?')}/mo | "
            f"Rating:{pg.get('Rating','?')} | "
            f"WiFi:{pg.get('WiFi','?')} | "
            f"Meals:{pg.get('Meals','?')} | "
            f"AC:{pg.get('AC','?')} | "
            f"Gender:{pg.get('Gender_Preference','?')} | "
            f"Contact:{pg.get('Contact','?')} | "
            f"Dist:{pg.get('Distance_km','?')}km | "
            f"Addr:{pg.get('Address','?')}"
        )
    return '\n'.join(lines)


# ── Private helpers ─────────────────────────────────────────────────────────

def _new_session() -> dict:
    return {
        'last_pgs':     [],
        'last_filters': {},
        'last_lang':    'en',
        'history':      [],
        'last_active':  time.time(),
    }


def _evict_expired() -> None:
    """Remove sessions that have been idle longer than SESSION_TTL_SECONDS."""
    now = time.time()
    expired = [sid for sid, s in _store.items()
               if now - s.get('last_active', 0) > SESSION_TTL_SECONDS]
    for sid in expired:
        del _store[sid]

    # Hard cap — remove oldest if too many
    if len(_store) > MAX_SESSIONS:
        oldest = sorted(_store.items(), key=lambda x: x[1]['last_active'])
        for sid, _ in oldest[:len(_store) - MAX_SESSIONS]:
            del _store[sid]
