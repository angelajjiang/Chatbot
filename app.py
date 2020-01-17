from flask import Flask, request
from pymessenger.bot import Bot


app = Flask(__name__)
ACCESS_TOKEN = 'ACCESS_TOKEN' #get from fb developer's app page
VERIFY_TOKEN = 'VERIFY_TOKEN' #make up a string here
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
def receive_message():
    # Before allowing people to message your bot, Facebook has implemented a verify token
    # that confirms all requests that your bot receives came from Facebook.
    # GET requests: to check our token
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token") #"hub.verify_token" is a token/variable we will make up and provide to fb
        return verify_fb_token(token_sent)
    else: #POST request: sending our bot a message sent by our user
        output = request.get_json() #output --> events --> messages
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging: #includes user's id, content
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN: #VERIFY_TOKEN our variable
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def get_message(input):


if __name__ == '__main__': 
    app.run()
