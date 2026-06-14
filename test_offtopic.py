import sys; sys.path.insert(0,'d:/pg_chatbot')
from nlp_utils import parse_user_message

tests = [
    'who is the president of india',
    'what is the capital of india',
    'who is modi',
    'tell me about cricket',
    'what is AI',
    'how are you',
    'what is 2+2',
    'who is elon musk',
    'india',
    'what is love',
    'best phone to buy',
]
for t in tests:
    p = parse_user_message(t)
    print(f"[{p['intent']:<16}][{p['lang']}] {t}")
