# pg_faq.py
from faq_knowledge import FAQ_PAIRS


def answer_general_question(text: str, lang: str = 'en') -> str:
    """
    Match user text against FAQ patterns.
    Returns the answer string or the NOT_FOUND sentinel.
    """
    t = text.lower().strip()

    # Greetings handled upstream, but keep as safety net
    if t in ['hi', 'hello', 'hey', 'hi there', 'hello there',
             'namaste', 'namaskar', 'nomoshkar']:
        return _greeting(lang)

    # Match FAQ patterns
    for pair in FAQ_PAIRS:
        for pattern in pair['patterns']:
            if pattern in t:
                return pair['answer']

    # Sentinel — caller should escalate to Gemini
    return "__NOT_FOUND__"


def _greeting(lang: str) -> str:
    msgs = {
        'bn': (
            "হ্যালো! আমি Quanta, আপনার PG সহকারী। 😊\n"
            "আমি আপনাকে Asansol-এ PG খুঁজে পেতে এবং PG সংক্রান্ত যেকোনো প্রশ্নের উত্তর দিতে পারি।\n"
            "আপনি কীভাবে সাহায্য চান?"
        ),
        'hi': (
            "नमस्ते! मैं Quanta हूँ, आपका PG सहायक। 😊\n"
            "मैं Asansol में PG खोजने और PG से जुड़े किसी भी सवाल का जवाब देने में मदद कर सकता हूँ।\n"
            "आप कैसे मदद चाहते हैं?"
        ),
        'en': (
            "Hi! I'm Quanta, your PG assistant. 😊\n"
            "I can help you find PGs in Asansol and answer any PG-related questions.\n"
            "How can I help you today?"
        ),
    }
    return msgs.get(lang, msgs['en'])
