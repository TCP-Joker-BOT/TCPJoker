def run(message):
    if 'reply_to_message' in message:
        return "This user's id is {}".format(message['reply_to_message']['from']['id'])
    else:
        return "Your id is {}".format(message['from']['id'])
