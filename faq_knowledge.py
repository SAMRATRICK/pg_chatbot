# faq_knowledge.py

FAQ_PAIRS = [
    # 1. Basic concepts (1–10)
    {
        "id": 1,
        "patterns": ["what is pg", "what is a pg", "meaning of pg", "pg meaning"],
        "answer": "PG stands for Paying Guest. It is a type of accommodation where you stay in someone else’s house or flat, use common facilities, and pay monthly rent, sometimes including food and utilities."
    },
    {
        "id": 2,
        "patterns": ["full form of pg", "pg full form"],
        "answer": "The full form of PG is 'Paying Guest'."
    },
    {
        "id": 3,
        "patterns": ["difference between pg and hostel", "pg vs hostel", "hostel or pg which is better"],
        "answer": "A hostel usually has more beds per room, stricter rules, and is often run by institutions. A PG is more like staying in a house or flat, with fewer people per room and more flexible facilities."
    },
    {
        "id": 4,
        "patterns": ["difference between pg and flat", "pg vs flat"],
        "answer": "In a PG, facilities and rules are managed by the owner and you pay per bed or room. In a flat, you rent the entire unit, manage utilities yourself, and usually sign a rental agreement directly."
    },
    {
        "id": 5,
        "patterns": ["who can live in pg", "who can stay in pg", "can students stay in pg", "can working professional stay in pg"],
        "answer": "Both students and working professionals can stay in PGs. Some PGs are reserved only for students, some only for working people, and some allow both."
    },
    {
        "id": 6,
        "patterns": ["why choose pg", "advantages of pg", "benefits of pg"],
        "answer": "PGs are convenient for newcomers: you get furnished rooms, shared facilities, and sometimes food, without having to set up everything yourself like in a flat."
    },
    {
        "id": 7,
        "patterns": ["disadvantages of pg", "problems in pg"],
        "answer": "Disadvantages include less privacy than a flat, rules about guests and timings, shared facilities, and sometimes limited control over food and hygiene."
    },
    {
        "id": 8,
        "patterns": ["who is pg owner", "who runs pg"],
        "answer": "A PG is usually run by an individual owner or a small company that manages the property, collects rent, and enforces rules."
    },
    {
        "id": 9,
        "patterns": ["who are paying guests", "who is paying guest"],
        "answer": "Paying guests are tenants who stay in a part of someone’s house or flat, pay rent, and share facilities like kitchen, washroom, and living space."
    },
    {
        "id": 10,
        "patterns": ["is pg good for students", "pg good for working professionals"],
        "answer": "A PG can be good for both students and working professionals because it offers ready‑made accommodation, often near colleges or offices, with basic services included."
    },

    # 2. Gender, eligibility, and type of PG (11–20)
    {
        "id": 11,
        "patterns": ["pg can be for male and female", "pg for male and female both", "coed pg"],
        "answer": "PGs can be only for males, only for females, or co‑ed. It depends on the PG’s policy and local regulations."
    },
    {
        "id": 12,
        "patterns": ["ladies pg", "girls pg", "women pg"],
        "answer": "Ladies or girls PGs are accommodations reserved only for female residents, usually with specific safety and privacy rules."
    },
    {
        "id": 13,
        "patterns": ["gents pg", "boys pg", "mens pg"],
        "answer": "Gents or boys PGs are accommodations reserved only for male residents, often near colleges, coaching centres, or IT parks."
    },
    {
        "id": 14,
        "patterns": ["family pg", "can families stay in pg"],
        "answer": "Some PGs allow small families in separate rooms or units, but most PGs are designed for individuals like students and working professionals."
    },
    {
        "id": 15,
        "patterns": ["married couples pg", "couples allowed in pg"],
        "answer": "A few PGs may allow married couples, but many do not. You should check explicitly if the PG has rooms for couples."
    },
    {
        "id": 16,
        "patterns": ["age limit for pg", "minimum age for pg"],
        "answer": "There is usually no strict legal age limit, but most PGs are intended for adults (18+). Minors typically stay with guardians or in hostels."
    },
    {
        "id": 17,
        "patterns": ["can foreigners stay in pg", "foreign students pg"],
        "answer": "Yes, foreign students and professionals can stay in PGs, but they may need to provide passport, visa details, and additional verification."
    },
    {
        "id": 18,
        "patterns": ["pg for only it employees", "only working professionals allowed"],
        "answer": "Some PGs target only working professionals in specific sectors, like IT employees, to maintain a particular environment and routine."
    },
    {
        "id": 19,
        "patterns": ["pg for students only", "student only pg"],
        "answer": "Student‑only PGs are common near colleges and coaching centres, with rules and facilities designed for students’ schedules and budgets."
    },
    {
        "id": 20,
        "patterns": ["difference between girls pg and boys pg", "rules difference male female pg"],
        "answer": "Girls PGs often have stricter visitor and safety rules, while boys PGs might be slightly more flexible. Exact rules depend on the owner."
    },

    # 3. Rent, deposit, and payments (21–30)
    {
        "id": 21,
        "patterns": ["what is average pg rent", "how much is pg rent", "typical pg rent"],
        "answer": "Average PG rent varies by city and facilities. Shared rooms with basic amenities are cheaper, while single AC rooms with food cost more."
    },
    {
        "id": 22,
        "patterns": ["how is pg rent decided", "rent based on what factors"],
        "answer": "PG rent depends on location, room type (single or sharing), facilities like AC and Wi‑Fi, food inclusion, and distance from key areas."
    },
    {
        "id": 23,
        "patterns": ["security deposit", "pg deposit", "advance amount"],
        "answer": "Most PGs charge a security deposit equal to 1–2 months of rent, refundable when you leave, subject to notice period and damages."
    },
    {
        "id": 24,
        "patterns": ["is security deposit refundable", "deposit refund rules"],
        "answer": "Security deposit is usually refundable if you follow the notice period and there are no pending dues or major damages."
    },
    {
        "id": 25,
        "patterns": ["rent payment date", "due date for rent"],
        "answer": "Rent is usually due monthly, with a fixed due date (e.g., 5th of every month). Paying on time helps avoid penalties."
    },
    {
        "id": 26,
        "patterns": ["late payment fine", "late rent", "penalty for late rent"],
        "answer": "Many PGs charge a small fine if rent is paid after the due date. The exact amount and grace period should be mentioned in your agreement."
    },
    {
        "id": 27,
        "patterns": ["pg rent increase", "can landlord increase pg rent", "pg rent hike"],
        "answer": "Rent increases are usually mentioned in the agreement, often after 11 months or 1 year. The owner should inform you in advance."
    },
    {
        "id": 28,
        "patterns": ["mode of payment", "how to pay pg rent", "cash or online"],
        "answer": "PG rent can be paid via cash, bank transfer, UPI, or cheque, depending on the owner’s preference. Online payment is becoming common."
    },
    {
        "id": 29,
        "patterns": ["is electricity included in rent", "electricity charges"],
        "answer": "In some PGs, basic electricity is included in rent; in others, it is charged separately based on meter reading or fixed monthly charges."
    },
    {
        "id": 30,
        "patterns": ["is water bill included", "water charges in pg"],
        "answer": "Water charges are often included in rent, but in some cities or upscale PGs, there may be separate charges if usage is high."
    },

    # 4. Facilities & amenities (31–40)
    {
        "id": 31,
        "patterns": ["what facilities in pg", "what amenities in pg", "facilities provided"],
        "answer": "Common PG facilities include a bed, mattress, cupboard, fan, table, Wi‑Fi, shared washroom, and sometimes fridge, washing machine, and housekeeping."
    },
    {
        "id": 32,
        "patterns": ["pg with wifi", "is wifi provided", "internet facility"],
        "answer": "Many PGs provide Wi‑Fi. Ask about speed, reliability, and whether it is included in rent or charged separately."
    },
    {
        "id": 33,
        "patterns": ["ac facility", "air conditioner in pg"],
        "answer": "AC rooms are available in some PGs at higher rent or with extra electricity charges. Confirm billing rules before finalizing."
    },
    {
        "id": 34,
        "patterns": ["food facility", "are meals provided", "mess facility", "food included"],
        "answer": "Some PGs provide breakfast and dinner, sometimes lunch. Check the menu, timings, and whether food is optional or compulsory."
    },
    {
        "id": 35,
        "patterns": ["laundry facility", "washing clothes", "washing machine"],
        "answer": "Laundry may be self‑service with a washing machine, a paid laundry service, or not provided. Clarify before moving in."
    },
    {
        "id": 36,
        "patterns": ["housekeeping", "room cleaning", "who cleans room"],
        "answer": "Many PGs offer housekeeping for rooms and common areas on a fixed schedule. Ask how often cleaning is done and if it is included in rent."
    },
    {
        "id": 37,
        "patterns": ["kitchen access", "can we cook", "cooking allowed in pg"],
        "answer": "Some PGs allow limited cooking in a shared kitchen; others restrict it due to safety or gas rules. Check allowed cooking times and appliances."
    },
    {
        "id": 38,
        "patterns": ["parking facility", "two wheeler parking", "car parking in pg"],
        "answer": "Two‑wheeler parking is common; car parking may be limited or extra. Confirm whether parking is free or charged."
    },
    {
        "id": 39,
        "patterns": ["wifi speed", "internet speed", "good wifi in pg"],
        "answer": "Wi‑Fi speed differs widely. If online study or remote work is important, ask the owner to specify speed and reliability or try it once."
    },
    {
        "id": 40,
        "patterns": ["furniture in pg", "what furniture is provided"],
        "answer": "Usually PGs provide a bed with mattress, cupboard/almirah, table, and chair. Some also include curtains, mirror, and basic storage."
    },

    # 5. Rules & discipline (41–50)
    {
        "id": 41,
        "patterns": ["pg rules", "rules of pg", "house rules"],
        "answer": "Typical PG rules cover entry timings, noise control, visitor policy, cleanliness, rent payment dates, and restrictions on smoking and alcohol."
    },
    {
        "id": 42,
        "patterns": ["curfew timing", "pg curfew", "what time to come back"],
        "answer": "Many PGs have a night curfew for safety. You may need to return by a fixed time or inform the owner if you are late."
    },
    {
        "id": 43,
        "patterns": ["are guests allowed", "visitors allowed", "friends stay overnight", "can parents stay"],
        "answer": "Visitor policies vary. Some PGs allow only daytime guests, some allow parents to stay for short visits, and some do not allow overnight guests at all."
    },
    {
        "id": 44,
        "patterns": ["alcohol rules", "drink in pg", "smoke in pg", "smoking allowed"],
        "answer": "Most PGs strictly prohibit alcohol and smoking inside the premises for safety and to maintain a comfortable environment for all residents."
    },
    {
        "id": 45,
        "patterns": ["noise rules", "music in pg", "party in pg"],
        "answer": "Loud music, parties, or disturbances are usually not allowed, especially at night, to respect other residents and neighbours."
    },
    {
        "id": 46,
        "patterns": ["sharing room rules", "roommate rules"],
        "answer": "In sharedrooms, you must respect roommates’ privacy, keep your area clean, and coordinate on lights, noise, and visitors."
    },
    {
        "id": 47,
        "patterns": ["can we change room", "room change policy"],
        "answer": "Room changes are sometimes allowed based on availability and owner approval, especially if there are genuine issues like conflicts or maintenance problems."
    },
    {
        "id": 48,
        "patterns": ["can we keep pets", "pets allowed in pg"],
        "answer": "Most PGs do not allow pets due to space, hygiene, and allergy concerns. If you have a pet, always check policies in advance."
    },
    {
        "id": 49,
        "patterns": ["can we study at night", "study late night", "quiet hours"],
        "answer": "You can usually study at night inside your room, but you should maintain low noise levels so as not to disturb others."
    },
    {
        "id": 50,
        "patterns": ["kitchen timing", "mess timing"],
        "answer": "Many PGs have fixed kitchen or mess timings for breakfast, lunch, and dinner. Check if timings match your college or office schedule."
    },

    # 6. Agreement, documents & verification (51–60)
    {
        "id": 51,
        "patterns": ["is pg agreement necessary", "written agreement", "pg contract"],
        "answer": "A written PG agreement is highly recommended. It clearly states rent, deposit, rules, and notice period, helping avoid future disputes."
    },
    {
        "id": 52,
        "patterns": ["what should pg agreement contain", "contents of pg agreement"],
        "answer": "A PG agreement should mention names of parties, address, room details, rent, deposit, payment dates, facilities, rules, and notice period."
    },
    {
        "id": 53,
        "patterns": ["documents required", "id proof", "what documents to submit", "papers required"],
        "answer": "Common documents for PG include Aadhaar or other government ID, a recent photograph, sometimes college ID/offer letter, and emergency contact details."
    },
    {
        "id": 54,
        "patterns": ["police verification", "tenant verification", "is police verification mandatory"],
        "answer": "In many cities, PG owners must complete police verification of residents. You may be asked for ID and basic details for this process."
    },
    {
        "id": 55,
        "patterns": ["can we get rent receipt", "pg rent receipt"],
        "answer": "You can request rent receipts or online payment proofs. They may help for reimbursement or tax purposes, especially for salaried employees."
    },
    {
        "id": 56,
        "patterns": ["can we show pg address as proof", "address proof", "pg address proof"],
        "answer": "Some institutions accept PG address as correspondence address if you have agreement or receipts, but permanent address proof usually remains your home address."
    },
    {
        "id": 57,
        "patterns": ["legal rights of pg", "tenant rights", "rights as pg"],
        "answer": "As a paying guest, you have the right to safe living conditions and fair treatment, but your legal protection may be less than that of a long‑term tenant on a registered lease."
    },
    {
        "id": 58,
        "patterns": ["can owner enter room without permission", "privacy in pg"],
        "answer": "Owners should respect your privacy and avoid entering your room without permission except in emergencies or with prior notice for maintenance."
    },
    {
        "id": 59,
        "patterns": ["what if owner breaks agreement", "owner not following agreement"],
        "answer": "If the owner doesn’t follow the agreement, you should first try to resolve it politely. If serious, you may seek advice from local authorities or legal help."
    },
    {
        "id": 60,
        "patterns": ["can we leave pg without agreement", "no agreement pg problem"],
        "answer": "Without a written agreement, disputes become harder to resolve. It is safer to insist on at least a basic written document or clear message trail."
    },

    # 7. Notice, exit, and refund (61–70)
    {
        "id": 61,
        "patterns": ["notice period", "how many days notice", "notice period in pg"],
        "answer": "Typical PG notice period is 15–30 days. If you leave without notice, part of your deposit may be deducted."
    },
    {
        "id": 62,
        "patterns": ["how to give notice", "how to leave pg"],
        "answer": "You should inform the owner in writing (message or email) about your move‑out date, following the notice period agreed in your contract."
    },
    {
        "id": 63,
        "patterns": ["can we leave pg early", "early exit", "leave before agreement ends"],
        "answer": "You can leave early, but you may lose part of your deposit or be asked to pay rent for the notice period, depending on the agreement."
    },
    {
        "id": 64,
        "patterns": ["when will deposit be refunded", "deposit refund time"],
        "answer": "Deposits are usually refunded after final room inspection and clearing all dues, often on or after your last day in the PG."
    },
    {
        "id": 65,
        "patterns": ["reasons for deposit cut", "why deposit cut"],
        "answer": "Deposit may be reduced for unpaid rent, electricity or food dues, or major damage to property beyond normal wear and tear."
    },
    {
        "id": 66,
        "patterns": ["what if pg is not good", "can we change pg", "how to shift pg"],
        "answer": "If you are unhappy, talk to the owner first. If issues are not resolved, you can look for another PG and leave after serving the notice period."
    },
    {
        "id": 67,
        "patterns": ["can we get partial refund", "partial deposit refund"],
        "answer": "Partial refund is possible if you leave mid‑month or if some charges are adjusted. Terms should be discussed with the owner."
    },
    {
        "id": 68,
        "patterns": ["pg closing", "pg shutting down", "what if pg closes"],
        "answer": "If the owner closes the PG, they should return your deposit and any advance for unused days. You may need to find alternative accommodation."
    },
    {
        "id": 69,
        "patterns": ["how to complain about pg", "complaint against pg owner"],
        "answer": "If you face serious issues like harassment or safety risks, you can approach local authorities, helplines, or tenants’ forums, depending on your city."
    },
    {
        "id": 70,
        "patterns": ["can owner force us to leave", "eviction from pg"],
        "answer": "Owners should follow agreement terms and give reasonable notice before asking a paying guest to leave, except in extreme misconduct cases."
    },

    # 8. Safety, hygiene, and quality (71–80)
    {
        "id": 71,
        "patterns": ["is pg safe", "safety in pg", "security in pg"],
        "answer": "Safety depends on location, building security, CCTV, entry controls, and rules. Prefer PGs with verified details, reviews, and clear visitor policies."
    },
    {
        "id": 72,
        "patterns": ["cleanliness", "hygiene", "how clean is pg"],
        "answer": "Check how often rooms and bathrooms are cleaned, how garbage is handled, and whether the kitchen or mess looks hygienic."
    },
    {
        "id": 73,
        "patterns": ["fire safety", "emergency exit", "fire extinguisher in pg"],
        "answer": "Good PGs should have basic fire safety measures like extinguishers, clear exits, and no unsafe wiring. Always note emergency exits."
    },
    {
        "id": 74,
        "patterns": ["water quality", "drinking water in pg"],
        "answer": "Ask if there is RO or filtered drinking water and whether it is regularly maintained. Poor water quality can affect health."
    },
    {
        "id": 75,
        "patterns": ["pest control", "cockroaches in pg", "rats in pg"],
        "answer": "Ask how often pest control is done. Visible cockroaches, rats, or insects are signs of poor maintenance."
    },
    {
        "id": 76,
        "patterns": ["how to choose good pg", "tips for selecting pg"],
        "answer": "To choose a good PG, check location, budget, reviews, safety, cleanliness, facilities, rules, and talk to existing residents if possible."
    },
    {
        "id": 77,
        "patterns": ["should we check reviews", "online reviews of pg"],
        "answer": "Online reviews and ratings can help identify issues like food quality, safety, or behaviour of staff. Use them as a guide but also visit personally."
    },
    {
        "id": 78,
        "patterns": ["location importance", "pg near college or office"],
        "answer": "Choosing a PG near your college or office saves time and travel cost. Check distance, public transport, and neighbourhood safety."
    },
    {
        "id": 79,
        "patterns": ["what questions to ask owner", "what to ask before joining pg"],
        "answer": "Ask about rent, deposit, what is included, notice period, rules, timings, visitors, facilities, and any extra charges before you join."
    },
    {
        "id": 80,
        "patterns": ["can we negotiate pg rent", "bargain pg rent"],
        "answer": "In some cases, you can negotiate rent or get small discounts, especially for long‑term stay or if you agree to certain conditions. Be polite and reasonable."
    },
]

