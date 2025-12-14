# nlp_utils.py
import re
from faq_knowledge import FAQ_PAIRS   # NEW: use your FAQ patterns


def detect_intent(text: str) -> str:
    t = text.lower().strip()

    # 1) greeting / capabilities (keep these)
    if t in ["hi", "hello", "hey", "hi there", "hello there"]:
        return "greeting"

    if "what can you do" in t or "how can you help" in t:
        return "ask_capabilities"

    # 2) recommendation keywords → recommend_pg
    rec_keywords = [
        "suggest", "recommend", "find", "show",
        "pg under", "under ", "less than", "below",
        "wifi", "wi-fi", "meals", "food", "ac", "aircon",
        "girls pg", "boys pg", "for girls", "for boys",
        "near college", "near office", "near station"
    ]
    if any(k in t for k in rec_keywords):
        return "recommend_pg"

    # also: if text mentions "pg" + a number (budget) → recommend_pg
    if "pg" in t and re.search(r"\d{3,6}", t):
        return "recommend_pg"

    # 3) FAQ patterns → pg_faq
    for pair in FAQ_PAIRS:
        for pattern in pair["patterns"]:
            if pattern in t:
                return "pg_faq"

    # 4) otherwise → fallback
    return "fallback"


def parse_user_message(text: str):
    t = text.lower().strip()
    intent = detect_intent(text)

    # default values
    max_rent = None
    top_k = 3
    gender = None
    needs_wifi = False
    needs_meals = False
    needs_ac = False
    min_rating = None
    max_distance = None

    # only extract filters if recommendation intent
    if intent == "recommend_pg":
        # budget
        m = re.search(r"(\d{3,6})", t)
        if m:
            max_rent = int(m.group(1))

        # how many PGs (top 3, best 5, etc.)
        m2 = re.search(r"\b(top|best)\s+(\d+)", t)
        if m2:
            top_k = int(m2.group(2))

        # gender
        if "girls" in t or "female" in t or "ladies" in t:
            gender = "female"
        elif "boys" in t or "male" in t or "gents" in t:
            gender = "male"

        # amenities
        needs_wifi = "wifi" in t or "internet" in t
        needs_meals = "meals" in t or "food" in t
        needs_ac = "ac" in t or "air condition" in t

        # top rated
        if any(kw in t for kw in ["top rated", "best rated", "highest rated"]):
            min_rating = 4.0

        # distance
        m3 = re.search(r"within\s+(\d+)\s*km", t)
        if m3:
            max_distance = float(m3.group(1))

    return {
        "intent": intent,
        "max_rent": max_rent,
        "top_k": top_k,
        "gender": gender,
        "needs_wifi": needs_wifi,
        "needs_meals": needs_meals,
        "needs_ac": needs_ac,
        "min_rating": min_rating,
        "max_distance": max_distance
    }
