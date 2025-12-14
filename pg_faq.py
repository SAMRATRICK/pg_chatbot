from faq_knowledge import FAQ_PAIRS

def answer_general_question(text: str) -> str:
    t = text.lower().strip()

    # greetings
    if t in ["hi", "hello", "hey", "hi there", "hello there"]:
        return (
            "Hi! I’m your PG assistant. I can answer general PG questions and "
            "also suggest PGs from the database based on your budget and needs.\n"
            "How can I help you today?"
        )

    # match FAQ patterns
    for pair in FAQ_PAIRS:
        for pattern in pair["patterns"]:
            if pattern in t:
                return pair["answer"]

    # fallback
    return (
        "I’m not sure about that specific question, but I can answer questions like:\n"
        "- What is PG / full form of PG\n"
        "- PG rules, curfew, visitors\n"
        "- Documents and deposit\n"
        "Or you can ask me to suggest PGs from the database."
    )
