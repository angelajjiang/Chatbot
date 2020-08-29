import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk import Tree

app = Flask(__name__)
ACCESS_TOKEN = 
VERIFY_TOKEN = 
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message(message):
    location = get_continuous_chunks(message, 'GPE')
    category = get_category(message)
    return query_location(location, category)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

def query_location(location, categories):
    FB_URL = "https://graph.facebook.com/search?type=place"
    FB_PARAMS = {'categories' : str(categories), 'fields' : ['name,checkins,overall_star_rating,location,price_range'], 'q': location, 'access_token': ACCESS_TOKEN}
    res = requests.get(url = FB_URL, params = FB_PARAMS)
    all_locations = res.json()['data']
    attractions_with_rating = [a for a in all_locations if 'overall_star_rating' in a]
    return str(attractions_with_rating[0]['name'])

def get_continuous_chunks(text, label):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == label:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk

ARTS_ENTERTAINMENT = ("theater", "studio", "show", "musical", "movie", "concert")
EDUCATION = ("school", "college", "university", "learn", "class", "teach", "tutor")
FITNESS_RECREATION = ("gym", "sports", "courts", "fields", "arena", "stadium", "fitness", "recreation", "pool", "swim")
FOOD_BEVERAGE = ("food", "beverage", "eat", "drink", "bar", "restaurants", "food", "dinner", "lunch")
HOTEL_LODGING = ("stay", "hotel", "lodging", "airbnb", "sleep", "bed", "motel", "hostel")
MEDICAL_HEALTH = ("hospital", "doctor", "emergency", "medical")
SHOPPING_RETAIL = ("mall", "shop", "stores", "shopping", "outlet")
TRAVEL_TRANSPORTATION = ("airport", "train", "bus", "car", "subway", "metro", "taxi", "bike", "rent", "boat", "walk", "ferry")

def get_category(sentence):
    for word in sentence.split():
        if word.lower() in ARTS_ENTERTAINMENT:
            return 'ARTS_ENTERTAINMENT'
        elif word.lower() in EDUCATION:
            return 'EDUCATION'
        elif word.lower() in FITNESS_RECREATION:
            return 'FITNESS_RECREATION'
        elif word.lower() in FOOD_BEVERAGE:
            return 'FOOD_BEVERAGE'
        elif word.lower() in HOTEL_LODGING:
            return 'HOTEL_LODGING'
        elif word.lower() in MEDICAL_HEALTH:
            return 'MEDICAL_HEALTH'
        elif word.lower() in SHOPPING_RETAIL:
            return 'SHOPPING_RETAIL'
        elif word.lower() in TRAVEL_TRANSPORTATION:
            return 'TRAVEL_TRANSPORTATION'

if __name__ == "__main__":
    app.run()
