from flask import Flask, request, jsonify, render_template
from recommender import get_recommended_pgs
from nlp_utils import parse_user_message
from pg_faq import answer_general_question
from gemini_helper import ask_gemini   # <-- NEW import

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")  # templates/index.html


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_msg = data.get("message", "")
    if not user_msg.strip():
        return jsonify({"answer": "Please type a question or requirement about PGs.", "pgs": []})

    parsed = parse_user_message(user_msg)
    intent = parsed["intent"]

    # 1) GREETING
    if intent == "greeting":
        return jsonify({
            "answer": (
                "Hi! I’m your PG assistant.\n"
                "I can suggest PGs based on budget, wifi, meals, gender preference, etc.,\n"
                "and answer general questions like PG rules, documents, deposits, and notice period.\n\n"
                "How can I help you today?"
            ),
            "pgs": []
        })

    # 2) CAPABILITIES
    if intent == "ask_capabilities":
        return jsonify({
            "answer": (
                "I can:\n"
                "- Suggest PGs from the database based on your requirements\n"
                "- Answer general PG questions (rules, documents, deposits, notice, safety)\n\n"
                "Example: 'Suggest 3 best PG under 6000 with wifi for girls'."
            ),
            "pgs": []
        })

    # 3) GENERAL PG FAQ: local FAQ first, then Gemini fallback
    if intent == "pg_faq":
        local_answer = answer_general_question(user_msg)

        if "I’m not sure about that specific question" in local_answer:
            # FAQ did not match → send to Gemini
            ai_ans = ask_gemini(
                "You are a helpful assistant for students looking for Paying Guest (PG) "
                "accommodation in India. Answer clearly and briefly.\n\n"
                f"User question: {user_msg}"
            )
            return jsonify({"answer": ai_ans, "pgs": []})
        else:
            # FAQ matched → use local answer
            return jsonify({"answer": local_answer, "pgs": []})

    # 4) RECOMMENDATION: dataset first
    if intent == "recommend_pg":
        results = get_recommended_pgs(
            max_rent=parsed["max_rent"],
            min_rating=parsed["min_rating"],
            max_distance=parsed["max_distance"],
            gender_pref=parsed["gender"],
            needs_wifi=parsed["needs_wifi"],
            needs_meals=parsed["needs_meals"],
            needs_ac=parsed["needs_ac"],
            top_k=parsed["top_k"]
        )

        if not results:
            # No PGs found → optionally ask Gemini to explain
            ai_ans = ask_gemini(
                "You are a PG recommendation assistant with a small local dataset.\n"
                f"The user asked: {user_msg}\n"
                "Explain politely that there is no exact match in the local list and suggest how "
                "they could relax budget, location, or facilities."
            )
            return jsonify({"answer": ai_ans, "pgs": []})

        lines = []
        for i, pg in enumerate(results, start=1):
            name = pg.get("PG_Name", "PG")
            loc = pg.get("Location", "Unknown area")
            rent = pg.get("Rent", "N/A")
            rating = pg.get("Rating", "N/A")
            wifi = pg.get("WiFi", "N/A")
            meals = pg.get("Meals", "N/A")

            line = (
                f"{i}. {name} in {loc} | Rent: ₹{rent} | Rating: {rating} | "
                f"WiFi: {wifi} | Meals: {meals}"
            )
            lines.append(line)

        if parsed["min_rating"]:
            lead = "Here are some of the top rated PG options from my database:\n"
        elif parsed["max_rent"]:
            lead = "Here are some PGs matching your budget and preferences:\n"
        else:
            lead = "Here are a few PG options for you:\n"

        answer_text = lead + "\n".join(lines)

        return jsonify({
            "answer": answer_text,
            "pgs": results
        })

    # 5) FALLBACK: anything else → Gemini
    ai_ans = ask_gemini(
        "You are a PG accommodation assistant. The following message may or may not be clear. "
        "If it is about housing, answer helpfully. Otherwise, ask briefly for their PG budget, "
        "city, and requirements.\n\n"
        f"User message: {user_msg}"
    )
    return jsonify({"answer": ai_ans, "pgs": []})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
