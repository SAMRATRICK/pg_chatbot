# app.py
import uuid
from flask import Flask, request, jsonify, render_template, session
from recommender import get_recommended_pgs
from nlp_utils import (
    parse_user_message,
    detect_followup,
    resolve_followup,
)
from pg_faq import answer_general_question
from gemini_helper import ask_gemini
from session_memory import (
    get_session,
    save_session,
    push_history,
    format_history_for_gemini,
    format_last_pgs_for_gemini,
)

app = Flask(__name__)
app.secret_key = "quanta-staypoint-secret-2025"   # for Flask session cookie


# ---------------------------------------------------------------------------
# Localised static responses
# ---------------------------------------------------------------------------

def _greeting_msg(lang):
    msgs = {
        'bn': (
            "হ্যালো! আমি **Quanta**, আপনার PG বিশেষজ্ঞ। 🏠\n\n"
            "আমি আপনাকে সাহায্য করতে পারি:\n"
            "• বাজেট, WiFi, খাবার, লিঙ্গ পছন্দ অনুযায়ী PG খুঁজে দিতে\n"
            "• PG-এর নিয়ম, ডকুমেন্ট, ডিপোজিট, নোটিশ পিরিয়ড সম্পর্কে জানাতে\n\n"
            "উদাহরণ: 'Asansol-এ ৬০০০ টাকার মধ্যে WiFi সহ মেয়েদের PG দেখাও'"
        ),
        'hi': (
            "नमस्ते! मैं **Quanta** हूँ, आपका PG विशेषज्ञ। 🏠\n\n"
            "मैं आपकी मदद कर सकता हूँ:\n"
            "• बजट, WiFi, खाना, लिंग के अनुसार PG खोजने में\n"
            "• PG के नियम, दस्तावेज़, जमानत राशि और नोटिस अवधि के बारे में\n\n"
            "उदाहरण: '6000 के अंदर WiFi वाला PG बताओ'"
        ),
        'en': (
            "Hi! I'm **Quanta**, your PG expert. 🏠\n\n"
            "I can help you with:\n"
            "• Finding PGs by budget, WiFi, meals, gender preference & more\n"
            "• Answering questions about PG rules, documents, deposits & notice period\n\n"
            "Example: *'Suggest 3 PGs under ₹6000 with WiFi for girls'*"
        ),
    }
    return msgs.get(lang, msgs['en'])


def _capabilities_msg(lang):
    msgs = {
        'bn': (
            "আমি Quanta — একটি PG-বিশেষায়িত সহকারী। আমি পারি:\n\n"
            "🔍 **PG অনুসন্ধান** — বাজেট, দূরত্ব, সুবিধা অনুযায়ী PG খুঁজে দেওয়া\n"
            "📋 **PG তথ্য** — ভাড়া, রেটিং, WiFi, খাবার, যোগাযোগ নম্বর\n"
            "❓ **PG প্রশ্নোত্তর** — নিয়ম, ডকুমেন্ট, ডিপোজিট, নিরাপত্তা\n"
            "💬 **কথোপকথন মেমরি** — আগের ফলাফল মনে রেখে follow-up প্রশ্নের উত্তর দেওয়া\n\n"
            "**আমি শুধু PG বিষয়ক প্রশ্নের উত্তর দিই।**"
        ),
        'hi': (
            "मैं Quanta हूँ — एक PG-विशेष सहायक। मैं कर सकता हूँ:\n\n"
            "🔍 **PG खोज** — बजट, दूरी, सुविधाओं के अनुसार PG ढूंढना\n"
            "📋 **PG जानकारी** — किराया, रेटिंग, WiFi, खाना, संपर्क नंबर\n"
            "❓ **PG सवाल-जवाब** — नियम, दस्तावेज़, जमानत, सुरक्षा\n"
            "💬 **बातचीत मेमोरी** — पहले दिखाए PG याद रखकर follow-up का जवाब देना\n\n"
            "**मैं केवल PG से जुड़े सवालों का जवाब देता हूँ।**"
        ),
        'en': (
            "I'm Quanta — a PG-only assistant. Here's what I can do:\n\n"
            "🔍 **PG Search** — find PGs by budget, distance, amenities\n"
            "📋 **PG Details** — rent, rating, WiFi, meals, contact numbers\n"
            "❓ **PG Q&A** — rules, documents, deposits, safety, notice period\n"
            "💬 **Session memory** — I remember what I showed you and answer follow-ups\n\n"
            "**I only handle PG accommodation topics.** Ask me anything about PGs!"
        ),
    }
    return msgs.get(lang, msgs['en'])


def _off_topic_msg(lang):
    msgs = {
        'bn': (
            "দুঃখিত, এই বিষয়ে আমার কাছে কোনো তথ্য নেই। 🙏\n\n"
            "আমি শুধুমাত্র **PG আবাসন** সংক্রান্ত বিষয়ে সাহায্য করতে পারি — "
            "যেমন PG খোঁজা, ভাড়া, সুবিধা, নিয়ম বা ডকুমেন্ট সম্পর্কে।\n\n"
            "অনুগ্রহ করে PG-সংক্রান্ত কোনো প্রশ্ন জিজ্ঞেস করুন।"
        ),
        'hi': (
            "क्षमा करें, इस विषय पर मेरे पास कोई जानकारी नहीं है। 🙏\n\n"
            "मैं केवल **PG आवास** से संबंधित विषयों में सहायता कर सकता हूँ — "
            "जैसे PG खोजना, किराया, सुविधाएं, नियम या आवश्यक दस्तावेज़।\n\n"
            "कृपया PG से जुड़ा कोई प्रश्न पूछें।"
        ),
        'en': (
            "I'm sorry, I don't have information on that topic. 🙏\n\n"
            "I'm a **PG accommodation assistant** and can only help with topics related to "
            "finding PGs, rent, facilities, rules, documents, and deposits.\n\n"
            "Please feel free to ask anything about PG accommodation."
        ),
    }
    return msgs.get(lang, msgs['en'])


def _no_match_msg(lang, parsed):
    msgs = {
        'bn': (
            "আপনার চাহিদার সাথে কোনো PG ম্যাচ করেনি। 😔\n\n"
            "আপনি চাইলে:\n"
            "• বাজেট একটু বাড়িয়ে দেখতে পারেন\n"
            "• কিছু ফিল্টার সরিয়ে আবার চেষ্টা করতে পারেন\n\n"
            "উদাহরণ: 'Asansol-এ ৭০০০ টাকার মধ্যে PG দেখাও'"
        ),
        'hi': (
            "आपकी ज़रूरतों से मेल खाने वाला कोई PG नहीं मिला। 😔\n\n"
            "आप कोशिश कर सकते हैं:\n"
            "• बजट थोड़ा बढ़ाएं\n"
            "• कुछ फ़िल्टर हटाकर दोबारा खोजें\n\n"
            "उदाहरण: '7000 के अंदर PG बताओ'"
        ),
        'en': (
            "No PGs matched your requirements. 😔\n\n"
            "You could try:\n"
            "• Increasing your budget slightly\n"
            "• Removing some filters and searching again\n\n"
            "Example: *'Show PGs under ₹7000'*"
        ),
    }
    return msgs.get(lang, msgs['en'])


# ---------------------------------------------------------------------------
# Response builder helpers
# ---------------------------------------------------------------------------

def _build_pg_lines(results: list) -> str:
    lines = []
    for i, pg in enumerate(results, start=1):
        name        = pg.get("PG_Name", "PG")
        loc         = pg.get("Address", "Asansol")
        rent        = pg.get("Rent", "N/A")
        rating      = pg.get("Rating", "N/A")
        wifi        = pg.get("WiFi", "N/A")
        meals       = pg.get("Meals", "N/A")
        ac          = pg.get("AC", "N/A")
        contact     = pg.get("Contact", "Not available")
        dist        = pg.get("Distance_km", "N/A")
        verified    = pg.get("Verified", "No")
        gender_pref = pg.get("Gender_Preference", "Any")
        v_badge     = "✅" if str(verified).lower().startswith("y") else "⬜"

        lines.append(
            f"**{i}. {name}** {v_badge}\n"
            f"📍 {loc}\n"
            f"💰 ₹{rent}/month  |  ⭐ {rating}  |  📏 {dist} km from AEC\n"
            f"🔧 WiFi: {wifi}  |  🍽 Meals: {meals}  |  ❄️ AC: {ac}\n"
            f"👤 Gender: {gender_pref}  |  📞 {contact}"
        )
    return "\n\n---\n\n".join(lines)


def _rec_lead(lang, parsed):
    if lang == 'bn':
        if parsed.get("min_rating"):
            return "Asansol-এ সেরা রেটিংয়ের PG গুলো:\n\n"
        elif parsed.get("max_rent"):
            return "আপনার বাজেট ও পছন্দ অনুযায়ী Asansol-এর PG:\n\n"
        else:
            return "Asansol-এর কিছু PG অপশন:\n\n"
    elif lang == 'hi':
        if parsed.get("min_rating"):
            return "Asansol के सबसे अच्छे रेटिंग वाले PG:\n\n"
        elif parsed.get("max_rent"):
            return "आपके बजट और पसंद के अनुसार Asansol के PG:\n\n"
        else:
            return "Asansol के कुछ PG विकल्प:\n\n"
    else:
        if parsed.get("min_rating"):
            return "Here are the top-rated PGs in Asansol:\n\n"
        elif parsed.get("max_rent"):
            return "Here are PGs in Asansol matching your budget and preferences:\n\n"
        else:
            return "Here are some PG options in Asansol:\n\n"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    # Assign a persistent session ID per browser tab
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    # ── Session ID ────────────────────────────────────────────────────────────
    if 'sid' not in session:
        session['sid'] = str(uuid.uuid4())
    sid = session['sid']
    mem = get_session(sid)

    data     = request.get_json(force=True)
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"answer": "Please type a message.", "pgs": []})

    parsed = parse_user_message(user_msg)
    intent = parsed["intent"]
    lang   = parsed["lang"]

    push_history(mem, 'user', user_msg)

    def finish(answer, pgs=None):
        pgs = pgs or []
        push_history(mem, 'bot', answer[:300])
        mem['last_lang'] = lang
        save_session(sid, mem)
        return jsonify({"answer": answer, "pgs": pgs})

    # ── 1. GREETING ───────────────────────────────────────────────────────────
    if intent == "greeting":
        return finish(_greeting_msg(lang))

    # ── 2. CAPABILITIES ───────────────────────────────────────────────────────
    if intent == "ask_capabilities":
        return finish(_capabilities_msg(lang))

    # ── 3. FOLLOW-UP — checked BEFORE off-topic so phrases like
    #       "which is cheapest?" aren't rejected when session has PG results ───
    if detect_followup(user_msg, mem):
        result = resolve_followup(user_msg, mem)

        if result.get('resolved'):
            pgs = result.get('pgs', [])
            if pgs:
                mem['last_pgs'] = pgs
            return finish(result['answer'], pgs)

        if result.get('hint') == 'show_more':
            last_f = mem.get('last_filters', {})
            more = get_recommended_pgs(
                max_rent    = last_f.get('max_rent'),
                min_rating  = last_f.get('min_rating'),
                max_distance= last_f.get('max_distance'),
                gender_pref = last_f.get('gender'),
                needs_wifi  = last_f.get('needs_wifi', False),
                needs_meals = last_f.get('needs_meals', False),
                needs_ac    = last_f.get('needs_ac', False),
                top_k       = last_f.get('top_k', 3) + 3,
            )
            if more:
                mem['last_pgs'] = more
                mem['last_filters']['top_k'] = len(more)
                lead = {'bn': "আরও কিছু PG অপশন:\n\n",
                        'hi': "कुछ और PG विकल्प:\n\n",
                        'en': "Here are more PG options:\n\n"}.get(lang, "Here are more PG options:\n\n")
                return finish(lead + _build_pg_lines(more), more)
            no_more = {'bn': "দুঃখিত, আর কোনো PG পাওয়া যায়নি।",
                       'hi': "माफ़ करें, और कोई PG नहीं मिला।",
                       'en': "Sorry, no more PGs found with those filters."}.get(lang, "Sorry, no more PGs found.")
            return finish(no_more)

        # hint == 'gemini' — complex follow-up
        context = (
            f"{format_last_pgs_for_gemini(mem)}\n\n"
            f"Recent conversation:\n{format_history_for_gemini(mem)}"
        )
        ai_ans = ask_gemini(f"{context}\n\nUser follow-up question: {user_msg}", lang)
        return finish(ai_ans, mem.get('last_pgs', []))

    # ── 4. OFF-TOPIC ──────────────────────────────────────────────────────────
    if intent == "off_topic":
        return finish(_off_topic_msg(lang))

    # ── 5. GENERAL PG FAQ ─────────────────────────────────────────────────────
    if intent == "pg_faq":
        local_answer = answer_general_question(user_msg, lang)
        if local_answer == "__NOT_FOUND__":
            hist_ctx = format_history_for_gemini(mem)
            prompt = f"Recent conversation:\n{hist_ctx}\n\nUser question: {user_msg}" if hist_ctx else user_msg
            return finish(ask_gemini(prompt, lang))
        return finish(local_answer)

    # ── 6. PG RECOMMENDATION ──────────────────────────────────────────────────
    if intent == "recommend_pg":
        results = get_recommended_pgs(
            max_rent    = parsed["max_rent"],
            min_rating  = parsed["min_rating"],
            max_distance= parsed["max_distance"],
            gender_pref = parsed["gender"],
            needs_wifi  = parsed["needs_wifi"],
            needs_meals = parsed["needs_meals"],
            needs_ac    = parsed["needs_ac"],
            top_k       = parsed["top_k"],
        )

        if not results:
            return finish(_no_match_msg(lang, parsed))

        mem['last_pgs']     = results
        mem['last_filters'] = {k: parsed[k] for k in
            ['max_rent', 'min_rating', 'max_distance', 'gender',
             'needs_wifi', 'needs_meals', 'needs_ac', 'top_k']}

        return finish(_rec_lead(lang, parsed) + _build_pg_lines(results), results)

    # ── 7. FALLBACK ───────────────────────────────────────────────────────────
    hist_ctx = format_history_for_gemini(mem)
    prompt   = f"Recent conversation:\n{hist_ctx}\n\nUser message: {user_msg}" if hist_ctx else user_msg
    return finish(ask_gemini(prompt, lang))

if __name__ == "__main__":
    app.run(debug=False, port=5001, use_reloader=False)
