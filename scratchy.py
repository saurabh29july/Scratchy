import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
from flask import Flask
from flask import request
import requests
app = Flask(__name__)
import requests
import json
from datetime import datetime


#CISCO Spark Bot Details
botEmail = ""
accessToken = ""
room_id = ""

#CISCO Spark API Details
host = "https://api.ciscospark.com/v1/"
headers = {"Authorization": "Bearer %s" % accessToken,"Content-Type": "application/json"}

#Server Details
server = "localhost"
port = 4000

#Corpus created to answer questions
corpus = ""

@app.route('/', methods=['POST'])
def chat():
    messageId = request.json.get('data').get('id')
    messageDetails = requests.get(host+"messages/"+messageId, headers=headers)
    inspectQuestion(messageDetails)
    return ""

def inspectQuestion(question):
    questionAsked = question.json().get('text')
    questioner = question.json().get('personEmail')

    print ('(' + questioner + ') says: ' + questionAsked)
    answer = ""

    if questioner != botEmail:

        if "#help" in questionAsked:
            answer = helpText()

        if "#note" in questionAsked:
            answer = addAnswer(questionAsked)

        if "#del" in questionAsked:            
            answer = delete(questionAsked)

        if "#list" in questionAsked:            
            answer = list(questionAsked)

        if answer == "":
            answer = findAnswer(questionAsked)

        sendMessage(answer, questioner)
        return answer

def list(questionAsked):
    answer = ""
    listIndex = questionAsked.index('#list')
    listText = questionAsked[listIndex+5:].strip()
    if listText == "":
        for converstation in corpus["conversations"]:
            answer = answer + converstation["question"] + " | " + converstation["answer"] + "\n"

    if listText != "":
        for converstation in corpus["conversations"]:
            if listText in converstation["question"].lower():
                answer = answer + converstation["question"] + " | " + converstation["answer"] + "\n"
    
    if answer == "":
        answer = "Nopes, nothing with me!"

    return answer


def addAnswer(questionAsked):
    questionIndex = questionAsked.index('#note')
    answerIndex = questionAsked.index('|')
    questionText = questionAsked[questionIndex+5:answerIndex].strip()
    answerText = questionAsked[answerIndex+1:].strip()
    
    converstation = {}
    converstation["question"] = questionText
    converstation["answer"] = answerText

    corpus["conversations"].append(converstation)
        
    with open('corpus.json', 'w') as outfile:
        json.dump(corpus, outfile, indent=2) 

    return "Got it!"   

def delete(questionAsked):
    questionIndex = questionAsked.index('#del')
    questionText = questionAsked[questionIndex+4:].strip()

    count = 0;
    for converstation in corpus["conversations"]:
        if converstation["question"].lower() in questionText.lower():
            corpus["conversations"].remove(converstation)
            count += 1
            
    with open('corpus.json', 'w') as outfile:
        json.dump(corpus, outfile, indent=2)
    
    if count == 0:
        return "Oops! Did not find anything with that tag.."
    if count == 1:
        return "Deleted 1 note"
    if count > 1:
        return "Done! Deleted " + str(count) + " notes"


def findAnswer(questionAsked):
    answer = ""
    count = 0
    tagsAnswer = ""
    for converstation in corpus["conversations"]:
        tags = converstation["question"].lower().split(",")
        for tag in tags:
            if tag in questionAsked.lower():
                count += 1
                answer = answer + converstation["answer"] + "\n"
    
    if count >= 6:
        answer = "I know too much about it, be more specific maybe?" 

    return answer

#A function to send the message by particular email of the receiver
def sendMessage(message,  toPersonEmail):
    if toPersonEmail != "":
        if message == "":
            message = 'Lolz.. cannot help with that! Maybe #help?'
        payload = {"roomId": room_id, "text": message}
        response = requests.request("POST","https://api.ciscospark.com/v1/messages/", data=json.dumps(payload),  headers=headers)
        return response.status_code

def helpText():
    answer = """ 
    ------------------------------------------------------------------    
    **Hi! I'm Scratchy, your scratchpad for cheatsheets, notes etc etc.**

    @gene Hi - Talk to me!
    
    #help - See this again!
    #note <tag(s)> | <note>  - Note it down with , seperated tag(s)
    #del <tag> - Delete notes with tag
    #list - List all or #list <tag> notes

    -------------------------------------------------------------------
    Like me to do something? Ping sakuagar@cisco.com (!= bot)
    -------------------------------------------------------------------
            """

    return answer

if __name__ == "__main__":

    #Load existing corpus
    with open('corpus.json') as f:
        corpus = json.load(f)

    #Start the app    
    app.run(host=server,port=port,debug=True)

    

