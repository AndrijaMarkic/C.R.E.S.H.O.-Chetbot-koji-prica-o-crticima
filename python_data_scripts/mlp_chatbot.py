import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import json
import random
from keras.models import load_model
from stt_tts.stt import speech_to_text
from stt_tts.tts import female_voice, hrvatski_voice
import time
import winsound
from python_data_scripts.mlp_dub1_chatbot import chat_mlp_dub1

model = load_model('models/mlp_chatbot_model.h5')

with open("databases/My Little Pony Friendship is Magic/mlp.json", "r", encoding="utf8") as f:
    intents = json.load(f)
words = pickle.load(open('pkl_w/words_mlp.pkl','rb'))
labels = pickle.load(open('pkl_l/labels_mlp.pkl','rb'))

def bank_of_words(s,words, show_details=True):
    bag_of_words = [0 for _ in range(len(words))]
    sent_words = nltk.word_tokenize(s)
    sent_words = [lemmatizer.lemmatize(word.lower()) for word in sent_words]
    for sent in sent_words:
        for i,w in enumerate(words):
            if w == sent:
                bag_of_words[i] = 1
    return np.array(bag_of_words)

def predict_label(s, model):
    # filtering out predictions
    pred = bank_of_words(s, words,show_details=False)
    response = model.predict(np.array([pred]))[0]
    ERROR_THRESHOLD = 0.25
    final_results = [[i,r] for i,r in enumerate(response) if r>ERROR_THRESHOLD]
    final_results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in final_results:
        return_list.append({"intent": labels[r[0]], "probability": str(r[1])})
    return return_list

def Response(ints, intents_json):
    tags = ''
    response = ''
    try:
        tags = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tags):
                response = random.choice(i['responses'])
                break
    except IndexError:
        response = "Sorry I dont have data about that."
    return response
    

def chatbot_response(msg, model):
    ints = predict_label(msg, model)
    response = Response(ints, intents)
    return response

def chat_mlp():
    con2 = 0
    con3 = 0
    while True:
        inp = '' 
        if con2 == 0:
            control = input('\n Do want to use speech option? Enter "yes" or "no".\n ')
            if control.lower() == 'yes':
                con2 = 1
            elif control.lower() == 'no':
                con2 = 2

        if con2 == 1:
            if con3 == 3:
                print("\n Bot: Sorry but this conversation is over. \n")
                female_voice("Sorry but this conversation is over.")
                time.sleep(5)
                inp = 'exit'
            else:
                inp = speech_to_text()
        elif con2 == 2:
            if con3 == 3:
                print("\n Bot: Sorry but this conversation is over. \n")
                female_voice("Sorry but this conversation is over.")
                time.sleep(5)
                inp = 'exit'
            else:
                inp = input("You: ")

        if inp.lower() == 'quit' or inp.lower() == 'exit':
            print('\n back to the main menu\n ')
            female_voice('Back to the main menu')
            time.sleep(3)
            break
        elif inp.lower() == 'intro':
            winsound.PlaySound(None, winsound.SND_PURGE)
            print('\n Playing  My Little Pony G04 Theme Song from youtube.com\n ')
            female_voice('playing My Little Pony G4 Theme Song from Youtube dot com')
            time.sleep(5)
            winsound.PlaySound('intros/mlp_g04_intro.wav', winsound.SND_ASYNC)
        elif inp.lower() == 'stop':
            winsound.PlaySound(None, winsound.SND_PURGE)
            print('')
        elif inp.lower()=='dub':
            winsound.PlaySound(None, winsound.SND_PURGE)
            print('\n Odabrali ste Moj Mali Poni Hrvatska Sinkronizacija. Što želite znati o sinkronizaciji?\n ')
            hrvatski_voice('Odabrali ste Moj Mali Poni Hrvatska Sinkronizacija. Što želite znati o sinkronizaciji?')
            print(' Enter any subject from this cartoon.\n Enter "exit" to back to the conan category\n ')
            chat_mlp_dub1()
        else:
            response = chatbot_response(inp, model)
            winsound.PlaySound(None, winsound.SND_PURGE)
            if response == "Sorry I dont have data about that.":
                con3 += 1
                if con3<3:
                    print("\n BOT:" + response + '\n')
                    female_voice(response)
            else: 
                con3 = 0
                print("\n BOT:" + response + '\n')
                female_voice(response)
