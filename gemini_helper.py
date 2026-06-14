# gemini_helper.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# ---------------------------------------------------------------------------
# Strict PG-only system prompt (injected before every request)
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """You are Quanta, a dedicated AI assistant for the StayPoint PG (Paying Guest) platform.

YOUR STRICT RULES:
1. You ONLY answer questions related to PG (Paying Guest) accommodations, hostels, rental rooms, or student housing topics.
2. If the user asks about ANYTHING that is NOT related to PG accommodations (e.g., weather, sports, movies, coding, general knowledge, politics, health, recipes, etc.), you must politely refuse and redirect them to PG topics.
3. You serve students and working professionals looking for PGs, especially near colleges in Tier-2/Tier-3 cities like Asansol, West Bengal, India.
4. You support three languages: English, Hindi, and Bengali. Detect the language of the user's message and ALWAYS respond in the SAME language they used.
5. Be concise, warm, and helpful. Use simple language. Avoid jargon.
6. When refusing off-topic questions, be brief and friendly, then offer to help with PG topics.
7. For PG questions not in your knowledge base, use your general knowledge about Indian PG accommodations to give a helpful answer.

RESPONSE LANGUAGE RULE (CRITICAL):
- If user writes in Bengali (বাংলা or romanised Bangla), respond in Bengali.
- If user writes in Hindi (हिंदी or romanised Hindi), respond in Hindi.
- If user writes in English, respond in English.
- When responding in Bengali or Hindi, use simple, everyday language (not overly formal).

OFF-TOPIC REFUSAL TEMPLATE (adapt to detected language):
- English: "I'm only able to help with PG accommodation questions. Feel free to ask me about PG rent, facilities, rules, or finding PGs near your college!"
- Hindi: "मैं केवल PG आवास से जुड़े सवालों का जवाब दे सकता हूँ। PG किराया, सुविधाएं, नियम या कॉलेज के पास PG खोजने के बारे में पूछें!"
- Bengali: "আমি শুধুমাত্র PG আবাসন সম্পর্কিত প্রশ্নের উত্তর দিতে পারি। PG ভাড়া, সুবিধা, নিয়ম বা কলেজের কাছে PG খোঁজার বিষয়ে জিজ্ঞেস করুন!"
"""


def ask_gemini(user_message: str, lang: str = 'en') -> str:
    """
    Send a message to Gemini with the strict PG-only system context.
    lang: 'en', 'hi', or 'bn' — used to reinforce language instruction.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _no_key_msg(lang)

    lang_instruction = {
        'bn': "The user is writing in Bengali. Respond in Bengali (বাংলায় উত্তর দিন).",
        'hi': "The user is writing in Hindi. Respond in Hindi (हिंदी में जवाब दें)।",
        'en': "The user is writing in English. Respond in English.",
    }.get(lang, "Respond in the same language as the user.")

    full_prompt = f"{_SYSTEM_PROMPT}\n\n{lang_instruction}\n\nUser message: {user_message}"

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
        )
        return response.text.strip()
    except Exception as e:
        return _error_msg(lang, str(e))


def _no_key_msg(lang: str) -> str:
    msgs = {
        'bn': "দুঃখিত, AI সেবাটি এই মুহূর্তে উপলব্ধ নেই। অনুগ্রহ করে পরে চেষ্টা করুন।",
        'hi': "माफ़ करें, AI सेवा अभी उपलब्ध नहीं है। कृपया बाद में प्रयास करें।",
        'en': "Sorry, the AI service is not configured. Please contact the administrator.",
    }
    return msgs.get(lang, msgs['en'])


def _error_msg(lang: str, detail: str = '') -> str:
    msgs = {
        'bn': "দুঃখিত, AI সেবায় একটি সমস্যা হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
        'hi': "माफ़ करें, AI सेवा से संपर्क करने में समस्या हुई। कृपया पुनः प्रयास करें।",
        'en': f"Sorry, I had a problem contacting the AI service. Please try again.",
    }
    return msgs.get(lang, msgs['en'])
