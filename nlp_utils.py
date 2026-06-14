# nlp_utils.py
import re
from faq_knowledge import FAQ_PAIRS


# ---------------------------------------------------------------------------
# Romanised Bengali vocabulary maps
# ---------------------------------------------------------------------------

# "within / under / budget" words in romanised Bengali
BN_BUDGET_WORDS = [
    'modheye', 'modhye', 'moddhe', 'maddhe', 'madhye',   # মধ্যে (within)
    'er modhye', 'er maddhe', 'er madhye',
    'takar modhye', 'takar maddhe', 'takar madhye',
    'taka te', 'takar modhe', 'taka r modhye',
    'budget e', 'budget a', 'baji',
    'sosto', 'sasto', 'shosto', 'shasto',                 # সস্তো (cheap)
    'kom daame', 'kome daame', 'kom daam',                # কম দামে (low price)
    'taka', 'takar',                                       # taka = currency
]

# "want / need / looking for" in romanised Bengali
BN_WANT_WORDS = [
    'chai', 'chaichi', 'chaicho', 'chahchi', 'chaichhi', # চাই / চাইছি
    'khujchi', 'khujchhi', 'khujche', 'khujcchi',        # খুঁজছি (searching)
    'dorkar', 'darkar', 'lagbe', 'lage', 'lagche',       # দরকার / লাগবে
    'dekhao', 'dekhabo', 'dekhi', 'dechai',              # দেখাও (show me)
    'suggest karo', 'suggest dao', 'bolun', 'bolo',
    'nite chai', 'nite chahchi', 'nite lagbe',
    'thakte chai', 'thakbo', 'thakba',                   # থাকতে চাই (want to stay)
    'uthte chai', 'utthe chai',
]

# Female in romanised Bengali
BN_FEMALE_WORDS = [
    'meyeder', 'meye der', 'meyedar', 'meyder',          # মেয়েদের
    'mohilar', 'mohila', 'nari', 'ladies',
    'girls er', 'girl der', 'girls der',
]

# Male in romanised Bengali
BN_MALE_WORDS = [
    'cheleder', 'cheler', 'chele der', 'cheleder',       # ছেলেদের
    'purush', 'purush der', 'boys er', 'gents',
]

# Amenity words in romanised Bengali
BN_WIFI_WORDS    = ['wifi ache', 'wifi thakle', 'wifi hobe', 'internet ache', 'net ache']
BN_MEALS_WORDS   = ['khabar ache', 'khabar thakle', 'khabar dey', 'khawa dey',
                    'khaowa', 'khabar', 'bhojon', 'tiffin', 'mess ache']
BN_AC_WORDS      = ['ac room', 'ac er ghor', 'ac thakle', 'ac hobe', 'ac ache']

# ---------------------------------------------------------------------------
# Romanised Hindi vocabulary maps
# ---------------------------------------------------------------------------

HI_BUDGET_WORDS = [
    # IMPORTANT: do NOT add bare 'me', 'mein', 'mei' here — they cause false
    # positives on English sentences ("tell me", "cricket", etc.).
    # These are only used as REC_KEYWORDS when combined with a number in parse_user_message.
    'ke andar', 'ke under', 'ke neeche', 'ke bheetar',
    'se kam', 'se neeche',         # से कम  (less than)
    'budget mein', 'budget me',
    'sasta', 'sasti', 'saste',     # सस्ता (cheap)
    'kam kiraya', 'kam rent',
    'rupay', 'rupaye',
]

HI_WANT_WORDS = [
    'chahiye', 'chahie', 'chahie', # चाहिए (needed/want)
    'dhundh', 'dhundna', 'dhundho',# ढूंढ
    'batao', 'bataiye', 'bataye',  # बताओ (tell)
    'dikhao', 'dikhaye', 'dikhaiye',# दिखाओ (show)
    'suggest karo', 'suggest kijiye',
    'milega', 'milegi', 'milenge', # मिलेगा (will get)
    'rehna hai', 'rehna chahta', 'rehna chahti',  # रहना है (want to stay)
    'rehne ke liye', 'rehne wala',
    'lena hai', 'lena chahta',
    'khoj', 'khojo', 'khojiye',
    'dhoondo', 'dhoondho',
    'kahan milega', 'kahan hai',
]

HI_FEMALE_WORDS = [
    'ladkiyon', 'ladki', 'ladkiyo', 'ladkion', # लड़कियों
    'mahila', 'mahilaon', 'aurat', 'auraton',
    'girls ke liye', 'girl ke liye',
]

HI_MALE_WORDS = [
    'ladkon', 'ladke', 'ladka',   # लड़कों
    'mard', 'purush', 'aadmi',
    'boys ke liye', 'gents ke liye',
]

HI_WIFI_WORDS    = ['wifi hai', 'wifi wala', 'wifi chahiye', 'internet hai',
                    'wifi milega', 'wifi ke saath', 'net chahiye']
HI_MEALS_WORDS   = ['khana hai', 'khana chahiye', 'khana wala', 'khana milega',
                    'khaana', 'khana ke saath', 'mess hai', 'bhojan']
HI_AC_WORDS      = ['ac room', 'ac wala', 'ac chahiye', 'ac milega', 'ac hai']

# ---------------------------------------------------------------------------
# Combined recommendation trigger lists
# ---------------------------------------------------------------------------

REC_KEYWORDS_EN = [
    "suggest", "recommend", "find", "show", "search",
    "pg under", "pg below", "under ", "less than", "below ",
    "wifi", "wi-fi", "meals", "food", "ac", "aircon",
    "girls pg", "boys pg", "for girls", "for boys",
    "near college", "near office", "near station",
    "best pg", "top pg", "cheap pg", "affordable pg",
    "pg with", "pg having", "pg that has",
    # rating-based queries — must be rec not faq
    "best rated", "top rated", "highest rated",
    "best pgs", "top pgs", "good pg", "best pg",
]

REC_KEYWORDS_HI = (
    HI_WANT_WORDS + HI_BUDGET_WORDS +
    HI_FEMALE_WORDS + HI_MALE_WORDS +
    HI_WIFI_WORDS + HI_MEALS_WORDS + HI_AC_WORDS +
    ["pg chahiye", "pg dhundh", "pg batao", "pg dikhao",
     "sasta pg", "kiraya", "mujhe pg", "ek pg", "koi pg",
     "sabse acha pg", "sabse accha pg", "best pg", "top pg"]
)

REC_KEYWORDS_BN = (
    BN_WANT_WORDS + BN_BUDGET_WORDS +
    BN_FEMALE_WORDS + BN_MALE_WORDS +
    BN_WIFI_WORDS + BN_MEALS_WORDS + BN_AC_WORDS +
    ["pg khujchi", "pg chai", "pg dekhao", "pg suggest",
     "ami pg", "ekta pg", "kono pg", "asansol pg",
     "bhalo pg", "best pg", "top pg", "shrestho pg"]
)

# ---------------------------------------------------------------------------
# Romanised Bengali language detection hints (expanded)
# ---------------------------------------------------------------------------

BN_LANG_HINTS = [
    # want / searching
    'khujchi', 'khujchhi', 'khujche',
    'chai', 'chaichi', 'chahchi',
    'darkar', 'dorkar', 'lagbe', 'lage',
    'thakte chai', 'thakbo', 'nite chai',
    # PG-related Bengali vocab
    'pg chai', 'pg er', 'ekta pg', 'kono pg',
    'koto taka', 'takar modhye', 'takar maddhe', 'takar madhye',
    'taka te', 'modheye', 'modhye', 'maddhe',
    'meyeder', 'meye der', 'cheleder', 'chele der',
    'wifi ache', 'khabar ache', 'khabar dey', 'khawa dey',
    'bhalo pg', 'sosto pg', 'sasto pg',
    'pg dekhao', 'pg dao', 'pg bolun',
    'asansole', 'asansoler',
    'ami ekta', 'amake', 'amader',
    'ki', 'koto',                  # short but common Bengali words
    'ache', 'achhe', 'nai', 'hobe',
]

# Romanised Hindi language detection hints (expanded)
HI_LANG_HINTS = [
    # want / searching
    'chahiye', 'chahie',
    'dhundh', 'dhundna', 'dhundho',
    'batao', 'bataiye', 'dikhao',
    'milega', 'milegi',
    'rehna hai', 'rehne ke liye',
    'mujhe', 'humein', 'mujko',
    # PG-related Hindi vocab
    'pg chahiye', 'pg dhundh', 'pg batao', 'pg dikhao',
    'kiraya', 'kiray', 'ek pg', 'koi pg',
    'wifi wala', 'wifi hai', 'khana wala', 'khana hai',
    'ladki', 'ladke', 'ladkiyon', 'ladkon',
    'mahila', 'purush',
    'sasta', 'sasti', 'saste',
    'ke andar', 'se kam', 'budget mein',
    'hai kya', 'kya hai', 'kaise',
]

# ---------------------------------------------------------------------------
# Follow-up / context-aware intent patterns
# ---------------------------------------------------------------------------

# These only trigger a "followup" intent when the session already has PG results

FOLLOWUP_PATTERNS = [
    # ── Filter on existing results ──────────────────────────────────────────
    # English
    r'\bwhich (one|ones)\b',
    r'\bwhich pg\b',
    r'\bthe (first|second|third|1st|2nd|3rd)\b',
    r'\bhas (ac|wifi|meals|food)\b',
    r'\bwith (ac|wifi|meals|food)\b',
    r'\bhave (ac|wifi|meals|food)\b',
    r'\bshow (only|me) (the )?(ac|wifi|meals|verified)\b',
    r'\bfilter\b',
    r'\bnarrow\b',
    r'\bfrom (these|those|them|above)\b',
    r'\bamong (these|those|them)\b',
    r'\bout of (these|those)\b',
    r'\b(cheaper|cheapest|affordable)\b',
    r'\b(better|best) (rated|rating|one)\b',
    r'\bclosest\b',
    r'\bnearest\b',
    r'\bverified (one|only|pg)\b',
    r'\b(sort|rank|order) by\b',

    # ── Ask about a specific result ─────────────────────────────────────────
    r'\b(contact|phone|number|call) (of |for )?(the )?(first|second|third|1st|2nd|3rd|last)?\b',
    r'\b(address|location) (of |for )?(the )?(first|second|third|1st|2nd|3rd|last)?\b',
    r'\bmore (detail|info|about)\b',
    r'\btell me more\b',
    r'\bmore about\b',
    r'\bwhat about\b',

    # ── "Show more" ─────────────────────────────────────────────────────────
    r'\bshow more\b',
    r'\bmore pg\b',
    r'\bmore options\b',
    r'\bany (other|more)\b',
    r'\bsomething else\b',

    # ── Pronoun references ───────────────────────────────────────────────────
    r'\b(it|this one|that one|this pg|that pg)\b',
    r'\bof them\b',
    r'\btheir\b',

    # ── Hindi follow-ups ─────────────────────────────────────────────────────
    r'(inme|unme|in sab me|in mein)\s*(se|koi|konsa)',
    r'konsa (accha|better|sasta)',
    r'(pehla|doosra|teesra|pahla)\s*(wala|pg)',
    r'(contact|phone|number)\s*(do|dena|batao)',
    r'aur\s*(dikhao|batao|option)',
    r'(ac|wifi|khana)\s*(wala|hai kya|wale)',
    r'(in|inka|inka)\s*(address|contact)',

    # ── Bengali follow-ups ───────────────────────────────────────────────────
    r'(etar|itar|egular|tar|tader)\s*(contact|phone|number|address)',
    r'(prothomta|dwitiyota|tritiyota)',   # first, second, third
    r'(ar|aro)\s*(dekhao|option|pg)',
    r'(ekhane|ei gulo|eider)\s*(moddhe|modhye|theke)',
    r'(ac|wifi|khabar)\s*(ache|thakle|hobe)\s*erom',
    r'(kon|konta)\s*(ta|gulo)\s*(valo|bhalo|sosta)',
    r'(sob|shob)\s*(gulo|er)',
    r'sabcheye\s*(sosta|bhalo|kache|valo)',   # সবচেয়ে সস্তা/ভালো/কাছে
    r'konta\s*(sosta|valo|bhalo|kache)',
]

# Ordinal helpers (used in follow-up response builder)
ORDINALS = {
    '1': 0, 'first': 0, '1st': 0, 'pehla': 0, 'pahla': 0, 'prothomta': 0,
    '2': 1, 'second': 1, '2nd': 1, 'doosra': 1, 'dwitiyota': 1,
    '3': 2, 'third': 2, '3rd': 2, 'teesra': 2, 'tritiyota': 2,
    'last': -1,
}


def detect_followup(text: str, session: dict) -> bool:
    """
    Returns True if the message looks like a follow-up on previously shown PGs.
    Only fires when the session actually has PG results.
    """
    if not session.get('last_pgs'):
        return False
    t = text.lower().strip()
    for pattern in FOLLOWUP_PATTERNS:
        if re.search(pattern, t):
            return True
    return False


def resolve_followup(text: str, session: dict) -> dict:
    """
    Try to resolve a follow-up locally (without Gemini) for simple cases.
    Returns dict with keys: 'resolved' (bool), 'answer' (str), 'pgs' (list).
    If unresolved, caller should use Gemini with session context injected.
    """
    t = text.lower().strip()
    pgs = session.get('last_pgs', [])
    lang = session.get('last_lang', 'en')

    # ── "Show more" / "more options" ────────────────────────────────────────
    more_patterns = [
        r'\bshow more\b', r'\bmore pg\b', r'\bmore options\b',
        r'\bany (other|more)\b', r'\bsomething else\b',
        r'aur\s*(dikhao|batao|option)', r'(ar|aro)\s*(dekhao|option|pg)',
    ]
    for p in more_patterns:
        if re.search(p, t):
            return {'resolved': False, 'pgs': pgs,
                    'hint': 'show_more'}   # caller handles via recommender

    # ── Filter: which ones have AC / WiFi / Meals ────────────────────────────
    filter_map = {
        'wifi':  lambda pg: pg.get('WiFi', 'No').lower() == 'yes',
        'meals': lambda pg: pg.get('Meals', 'No').lower() == 'yes',
        'food':  lambda pg: pg.get('Meals', 'No').lower() == 'yes',
    }
    # AC needs word-boundary check to avoid matching "contact", "place", etc.
    if re.search(r'\bac\b', t):
        filter_map['ac'] = lambda pg: pg.get('AC', 'No').lower() == 'yes'

    for amenity, fn in filter_map.items():
        if amenity in t:
            filtered = [pg for pg in pgs if fn(pg)]
            if filtered:
                names = [pg['PG_Name'] for pg in filtered]
                return {
                    'resolved': True,
                    'pgs': filtered,
                    'answer': _filter_answer(amenity, names, lang),
                }
            else:
                return {
                    'resolved': True,
                    'pgs': [],
                    'answer': _none_have_answer(amenity, lang),
                }

    # ── Cheapest ─────────────────────────────────────────────────────────────
    if re.search(r'\b(cheapest|cheapest one|sasta|sosto|saste|kom daam|sabcheye sosta|sab theke sosta|konta sosta)\b', t):
        pg = min(pgs, key=lambda p: p.get('Rent', 99999))
        return {
            'resolved': True,
            'pgs': [pg],
            'answer': _single_pg_answer(pg, 'cheapest', lang),
        }

    # ── Best rated ────────────────────────────────────────────────────────────
    if re.search(r'\b(best rated|highest rated|best rating|konsa accha|bhalo rated)\b', t):
        pg = max(pgs, key=lambda p: float(p.get('Rating', 0)))
        return {
            'resolved': True,
            'pgs': [pg],
            'answer': _single_pg_answer(pg, 'best_rated', lang),
        }

    # ── Closest / nearest ────────────────────────────────────────────────────
    if re.search(r'\b(closest|nearest|kache|sabse paas)\b', t):
        pg = min(pgs, key=lambda p: float(p.get('Distance_km', 99)))
        return {
            'resolved': True,
            'pgs': [pg],
            'answer': _single_pg_answer(pg, 'closest', lang),
        }

    # ── Verified only ────────────────────────────────────────────────────────
    if re.search(r'\bverified\b', t):
        verified = [pg for pg in pgs if str(pg.get('Verified', 'No')).lower().startswith('y')]
        if verified:
            names = [pg['PG_Name'] for pg in verified]
            return {
                'resolved': True,
                'pgs': verified,
                'answer': _filter_answer('verified', names, lang),
            }

    # ── Contact / address of Nth result ─────────────────────────────────────
    for word, idx in ORDINALS.items():
        if word in t and 0 <= idx < len(pgs):
            pg = pgs[idx]
            if any(k in t for k in ['contact', 'phone', 'number', 'call']):
                return {
                    'resolved': True,
                    'pgs': [pg],
                    'answer': _contact_answer(pg, lang),
                }
            if any(k in t for k in ['address', 'location', 'where']):
                return {
                    'resolved': True,
                    'pgs': [pg],
                    'answer': _address_answer(pg, lang),
                }

    # Could not resolve locally → let Gemini handle with context
    return {'resolved': False, 'pgs': pgs, 'hint': 'gemini'}


# ── Local follow-up response builders ───────────────────────────────────────

def _filter_answer(amenity: str, names: list, lang: str) -> str:
    name_str = ', '.join(f'**{n}**' for n in names)
    labels = {
        'ac':       {'en': 'AC', 'hi': 'AC', 'bn': 'AC'},
        'wifi':     {'en': 'WiFi', 'hi': 'WiFi', 'bn': 'WiFi'},
        'meals':    {'en': 'meals', 'hi': 'खाना', 'bn': 'খাবার'},
        'food':     {'en': 'meals', 'hi': 'खाना', 'bn': 'খাবার'},
        'verified': {'en': 'verified', 'hi': 'verified', 'bn': 'verified'},
    }
    label = labels.get(amenity, {}).get(lang, amenity.upper())
    msgs = {
        'en': f"From the PGs I showed, these have **{label}**: {name_str}",
        'hi': f"जो PG मैंने दिखाए, उनमें **{label}** वाले हैं: {name_str}",
        'bn': f"আমি যে PG গুলো দেখিয়েছিলাম, তার মধ্যে **{label}** আছে এমন: {name_str}",
    }
    return msgs.get(lang, msgs['en'])


def _none_have_answer(amenity: str, lang: str) -> str:
    msgs = {
        'en': f"None of the PGs I showed have **{amenity.upper()}**. Want me to search again with that filter?",
        'hi': f"जो PG मैंने दिखाए उनमें से किसी के पास **{amenity.upper()}** नहीं है। क्या मैं उस फ़िल्टर के साथ दोबारा खोजूं?",
        'bn': f"আমি যে PG গুলো দেখিয়েছিলাম তাদের কোনোটিতে **{amenity.upper()}** নেই। আবার সেই ফিল্টার দিয়ে খুঁজবো?",
    }
    return msgs.get(lang, msgs['en'])


def _single_pg_answer(pg: dict, reason: str, lang: str) -> str:
    name = pg.get('PG_Name', 'This PG')
    rent = pg.get('Rent', 'N/A')
    rating = pg.get('Rating', 'N/A')
    dist = pg.get('Distance_km', 'N/A')
    contact = pg.get('Contact', 'N/A')

    labels = {
        'cheapest':   {'en': 'cheapest', 'hi': 'सबसे सस्ता', 'bn': 'সবচেয়ে সস্তা'},
        'best_rated': {'en': 'best rated', 'hi': 'सबसे अच्छी रेटिंग वाला', 'bn': 'সেরা রেটিংয়ের'},
        'closest':    {'en': 'closest to AEC', 'hi': 'AEC के सबसे करीब', 'bn': 'AEC-এর সবচেয়ে কাছের'},
    }
    label = labels.get(reason, {}).get(lang, reason)

    msgs = {
        'en': (f"The **{label}** among those is **{name}**.\n"
               f"💰 ₹{rent}/month  |  ⭐ {rating}  |  📏 {dist} km  |  📞 {contact}"),
        'hi': (f"उनमें **{label}** PG है **{name}**।\n"
               f"💰 ₹{rent}/माह  |  ⭐ {rating}  |  📏 {dist} km  |  📞 {contact}"),
        'bn': (f"সেগুলোর মধ্যে **{label}** PG হলো **{name}**।\n"
               f"💰 ₹{rent}/মাস  |  ⭐ {rating}  |  📏 {dist} km  |  📞 {contact}"),
    }
    return msgs.get(lang, msgs['en'])


def _contact_answer(pg: dict, lang: str) -> str:
    name = pg.get('PG_Name', 'This PG')
    contact = pg.get('Contact', 'N/A')
    owner = pg.get('Owner', 'N/A')
    msgs = {
        'en': f"Contact for **{name}**: 📞 **{contact}** (Owner: {owner})",
        'hi': f"**{name}** का संपर्क: 📞 **{contact}** (मालिक: {owner})",
        'bn': f"**{name}**-এর যোগাযোগ: 📞 **{contact}** (মালিক: {owner})",
    }
    return msgs.get(lang, msgs['en'])


def _address_answer(pg: dict, lang: str) -> str:
    name = pg.get('PG_Name', 'This PG')
    addr = pg.get('Address', 'N/A')
    dist = pg.get('Distance_km', 'N/A')
    msgs = {
        'en': f"**{name}** is located at: 📍 {addr} ({dist} km from AEC)",
        'hi': f"**{name}** का पता: 📍 {addr} (AEC से {dist} km)",
        'bn': f"**{name}**-এর ঠিকানা: 📍 {addr} (AEC থেকে {dist} km)",
    }
    return msgs.get(lang, msgs['en'])


# ---------------------------------------------------------------------------
# Off-topic patterns — anything clearly NOT PG-related
# Kept broad so general knowledge questions are caught and politely declined.
# ---------------------------------------------------------------------------

OFF_TOPIC_PATTERNS = [
    # People / politics / geography
    r'\bpresident\b', r'\bprime minister\b', r'\bminister\b',
    r'\bpolitics\b', r'\belection\b', r'\bgovernment\b',
    r'\bwho is\b', r'\bwho was\b', r'\bwho are\b',
    r'\bcapital of\b', r'\bcountry\b', r'\bstate of\b',
    r'\bhistory of\b', r'\bfamous person\b',
    # Weather / nature
    r'\bweather\b', r'\btemperature\b', r'\bforecast\b',
    r'\bearthquake\b', r'\bcyclone\b', r'\bflood\b',
    # Sports
    r'\bcricket\b', r'\bfootball\b', r'\bipl\b', r'\btennis\b',
    r'\bscore\b', r'\bmatch\b', r'\btournament\b',
    # Entertainment
    r'\bjoke\b', r'\bjokes\b', r'\bfunny\b',
    r'\bmovie\b', r'\bfilm\b', r'\bactor\b', r'\bactress\b',
    r'\bsong\b', r'\bmusic\b', r'\bgana\b', r'\balbum\b',
    r'\bnetflix\b', r'\bweb series\b',
    # Food recipes (non-PG)
    r'\brecipe\b', r'\bhow to cook\b', r'\bcooking\b',
    r'\bingredients\b',
    # Science / general knowledge
    r'\bwhat is gravity\b', r'\bwhat is electricity\b',
    r'\bwho invented\b', r'\bwhen was\b', r'\bwhere is\b',
    r'\bscience\b', r'\bphysics\b', r'\bchemistry\b', r'\bbiology\b',
    r'\bplanet\b', r'\buniverse\b', r'\bspace\b',
    # Math / coding
    r'\bmath\b', r'\bcalculate\b', r'\bequation\b', r'\bformula\b',
    r'\bcode\b', r'\bprogramming\b', r'\bpython code\b', r'\bjava code\b',
    r'\bwrite a program\b', r'\balgorithm\b',
    # Health / medical
    r'\bdisease\b', r'\bmedicine\b', r'\bsymptoms\b', r'\bdoctor\b',
    r'\bhospital\b', r'\btreatment\b', r'\bcure\b',
    # Finance (non-PG)
    r'\bstock\b', r'\bshare market\b', r'\bcrypto\b', r'\bbitcoin\b',
    r'\binvestment\b', r'\bmutual fund\b',
    # Shopping / tech
    r'\bbest phone\b', r'\bbest laptop\b', r'\bbuy online\b',
    r'\bamazon\b', r'\bflipkart\b',
    # Miscellaneous
    r'\bhow to lose weight\b', r'\bfitness\b', r'\byoga\b',
    r'\blove\b', r'\brelationship\b', r'\bmarriage\b',
    r'\bnews\b', r'\bbreaking news\b',
]

# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

def detect_language(text: str) -> str:
    """
    Returns 'bn' (Bengali), 'hi' (Hindi), or 'en' (English/default).
    Priority: Unicode script > romanised Bengali > romanised Hindi > English.
    """
    # Bengali Unicode block U+0980–U+09FF
    if re.search(r'[\u0980-\u09FF]', text):
        return 'bn'
    # Devanagari (Hindi) Unicode block U+0900–U+097F
    if re.search(r'[\u0900-\u097F]', text):
        return 'hi'

    t = text.lower()

    # Count romanised Bengali hints
    bn_score = sum(1 for h in BN_LANG_HINTS if h in t)
    # Count romanised Hindi hints
    hi_score = sum(1 for h in HI_LANG_HINTS if h in t)

    if bn_score == 0 and hi_score == 0:
        return 'en'

    # Return whichever has more matches; Bengali wins ties (common in this project area)
    return 'bn' if bn_score >= hi_score else 'hi'


# ---------------------------------------------------------------------------
# Intent detection
# ---------------------------------------------------------------------------

def detect_intent(text: str) -> str:
    t = text.lower().strip()
    lang = detect_language(text)

    # ── 1. Pure greeting ────────────────────────────────────────────────────
    pure_greets = {
        'en': ['hi', 'hello', 'hey', 'hi there', 'hello there', 'good morning',
               'good evening', 'good afternoon', 'namaste', 'namaskar', 'helo'],
        'hi': ['hi', 'hello', 'namaste', 'namaskar', 'pranam', 'shukriya'],
        'bn': ['hi', 'hello', 'namaskar', 'nomoshkar', 'namasthe'],
    }
    for greet in pure_greets.get(lang, pure_greets['en']):
        if t == greet:
            return 'greeting'

    # ── 2. Capabilities ─────────────────────────────────────────────────────
    cap_patterns = [
        'what can you do', 'how can you help', 'what do you do',
        'tumi ki korte paro', 'tumi ki jano', 'tumi ki koro',
        'kya kar sakte ho', 'kya jaante ho', 'aap kya karte ho',
        'help karo', 'help chahiye',
    ]
    if any(p in t for p in cap_patterns):
        return 'ask_capabilities'

    # ── 3. Off-topic ─────────────────────────────────────────────────────────
    for pattern in OFF_TOPIC_PATTERNS:
        if re.search(pattern, t):
            return 'off_topic'

    # ── 4. PG relevance check ────────────────────────────────────────────────
    pg_hints = [
        # English
        'pg', 'paying guest', 'hostel', 'room', 'rent', 'accommodation',
        'lodge', 'mess', 'wifi', 'meals', 'deposit', 'notice', 'document',
        'asansol', 'kanyapur', 'aec', 'college', 'stay',
        # Hindi
        'kiraya', 'kamra', 'ghar', 'tikna',
        # Bengali romanised
        'bari', 'ghor', 'bhara', 'taka', 'takar',
        # Bengali unicode
        '\u09aa\u09bf\u099c\u09bf',            # পিজি
        '\u09ad\u09be\u09dc\u09be',            # ভাড়া
        '\u09b9\u09cb\u09b8\u09cd\u099f\u09c7\u09b2',  # হোস্টেল
        '\u09a5\u09be\u0995\u09be',            # থাকা
        '\u09b8\u09c1\u09ac\u09bf\u09a7\u09be',# সুবিধা
        '\u09a1\u09bf\u09aa\u09cb\u099c\u09bf\u099f',  # ডিপোজিট
    ]
    has_pg_hint = any(h in t for h in pg_hints)

    # ── 5. Recommendation intent ─────────────────────────────────────────────
    all_rec_kw = REC_KEYWORDS_EN + REC_KEYWORDS_HI + REC_KEYWORDS_BN
    if any(k in t for k in all_rec_kw):
        return 'recommend_pg'

    # "pg" + number → recommendation
    if 'pg' in t and re.search(r'\d{3,6}', t):
        return 'recommend_pg'

    # number + budget/rent word (any language) — ONLY with clear budget context
    budget_triggers = [
        'rent', 'kiraya', 'bhara', 'taka', 'budget',
        'modheye', 'modhye', 'maddhe',
        # NOTE: bare 'mein'/'mei' removed — too broad, causes false positives
    ]
    if re.search(r'\d{3,6}', t) and any(w in t for w in budget_triggers):
        return 'recommend_pg'

    # number + 'mein'/'mei'/'me' ONLY when 'pg' is also present
    if re.search(r'\d{3,6}', t) and any(w in t for w in ['mein', 'mei', 'me']) and 'pg' in t:
        return 'recommend_pg'
    # ── 6. FAQ intent ────────────────────────────────────────────────────────
    for pair in FAQ_PAIRS:
        for pattern in pair['patterns']:
            if pattern in t:
                return 'pg_faq'

    # ── 7. Any PG hint → let Gemini answer as PG question ────────────────────
    if has_pg_hint:
        return 'pg_faq'

    # ── 8. Nothing PG-related → off_topic ────────────────────────────────────
    # Short or long — if there's no PG hint and no matching pattern, decline politely.
    return 'off_topic'


# ---------------------------------------------------------------------------
# Full message parser (extracts filters for recommendation intent)
# ---------------------------------------------------------------------------

def parse_user_message(text: str) -> dict:
    t = text.lower().strip()
    intent  = detect_intent(text)
    lang    = detect_language(text)

    max_rent     = None
    top_k        = 3
    gender       = None
    needs_wifi   = False
    needs_meals  = False
    needs_ac     = False
    min_rating   = None
    max_distance = None

    if intent == 'recommend_pg':

        # ── Budget extraction ─────────────────────────────────────────────
        # Handles: ₹6000, 6000 taka, 6000 mein, 6000 takar modhye, Rs 6000, etc.
        m = re.search(r'[₹\$]?\s*(\d{3,6})', t)
        if m:
            max_rent = int(m.group(1))

        # ── How many PGs ──────────────────────────────────────────────────
        # "top 3", "best 5", "show 4", "dikhao 3", "dekhao 5"
        m2 = re.search(r'\b(?:top|best|show|dikhao|dekhao|suggest)\s+(\d+)', t)
        if m2:
            top_k = int(m2.group(1))

        # ── Gender ────────────────────────────────────────────────────────
        all_female = (
            ['girls', 'female', 'ladies', 'women'] +
            BN_FEMALE_WORDS + HI_FEMALE_WORDS
        )
        all_male = (
            ['boys', 'male', 'gents', 'men'] +
            BN_MALE_WORDS + HI_MALE_WORDS
        )
        if any(k in t for k in all_female):
            gender = 'female'
        elif any(k in t for k in all_male):
            gender = 'male'

        # ── Amenities ─────────────────────────────────────────────────────
        wifi_triggers  = ['wifi', 'wi-fi', 'internet', 'net'] + BN_WIFI_WORDS  + HI_WIFI_WORDS
        meal_triggers  = ['meals', 'food', 'mess', 'bhojan']  + BN_MEALS_WORDS + HI_MEALS_WORDS
        ac_triggers    = [' ac ', ' ac,', ' ac.', 'air condition', 'a/c',
                          '(ac)', 'ac room', 'ac wala', 'ac hai', 'ac ache',
                          'ac chahiye', 'ac thakle', 'ac hobe'] + BN_AC_WORDS + HI_AC_WORDS

        needs_wifi  = any(k in t for k in wifi_triggers)
        needs_meals = any(k in t for k in meal_triggers)
        # Use word-boundary safe check for 'ac' to avoid matching 'ache', 'ace', etc.
        needs_ac    = bool(re.search(r'\bac\b', t)) or any(k in t for k in ac_triggers)

        # ── Top-rated ─────────────────────────────────────────────────────
        top_rated_kw = [
            'top rated', 'best rated', 'highest rated',
            'sabse acha', 'sabse accha', 'sabse badhiya',    # Hindi
            'best er', 'bhalo pg', 'shrestho',               # Bengali romanised
        ]
        if any(kw in t for kw in top_rated_kw):
            min_rating = 4.0

        # ── Distance ──────────────────────────────────────────────────────
        m3 = re.search(r'within\s+(\d+)\s*km', t)
        if m3:
            max_distance = float(m3.group(1))

    return {
        'intent':      intent,
        'lang':        lang,
        'max_rent':    max_rent,
        'top_k':       top_k,
        'gender':      gender,
        'needs_wifi':  needs_wifi,
        'needs_meals': needs_meals,
        'needs_ac':    needs_ac,
        'min_rating':  min_rating,
        'max_distance':max_distance,
    }
