"""
Data Sets: 
https://raw.githubusercontent.com/dsojevic/profanity-list/main/src/en.json
https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/list.txt
"""

import json

def checkExceptions(word : str, profane : str, exceptions):
    for exception in exceptions:
        if exception.replace("*", profane) == word:
            return False

    return True

def isProfane(text : str, deepSearch = False):
    words = text.split(" ")
    for word in words:
        if isWordProfane(word, deepSearch=deepSearch):
            return True

    return False

def isWordProfane(word : str, deepSearch = False):
    if len(word) < 3: return False

    if deepSearch:
        profanity = json.load(open("data/profanity.json"))
        for i in profanity:
            for j in i["dictionary"]:
                id = j["id"]

                if j.__contains__("exceptions"):
                    exceptions = j["exceptions"]
                else:
                    exceptions = []

                if word == id:
                    return checkExceptions(word, id, exceptions)

                m = j["match"]
                matches = m.split("|")
                for x in matches:
                    if word == x:
                        return checkExceptions(word, x, exceptions)
    else:
        with open("data/profanity_short.txt") as f:
            for line in f.readlines():
                if word == line:
                    return True

    return False

def censor(text : str):
    words = text.split(" ")
    result = ""
    for word in words:
        result += censorWord(word) + " "

    return result

def censorWord(word : str):
    if not isWordProfane(word):
        return word

    result = ""
    for i in range(len(word)):
        result += "*"

    return result

def getSeverity(text : str):
    words = text.split(" ")
    result = 0
    size = 0
    for word in words:
        severity = getWordSeverity(word)
        if not severity == 0:
            result += severity
            size += 1

    if size == 0: return 0
    result /= size
    return result

def getWordSeverity(word : str):
    if not isWordProfane(word, deepSearch=True):
        return 0

    profanity = json.load(open("data/profanity.json"))
    for i in profanity:
        for j in i["dictionary"]:
            id = j["id"]

            if j.__contains__("exceptions"):
                exceptions = j["exceptions"]
            else:
                exceptions = []

            if word == id:
                if checkExceptions(word, id, exceptions):
                    return i["severity"]

            m = j["match"]
            matches = m.split("|")
            for x in matches:
                if word == x:
                    if checkExceptions(word, x, exceptions):
                        return i["severity"]

    return 0

def getWordCategory(word : str):
    if not isWordProfane(word, deepSearch=True):
        return "Unknown Profanity"

    profanity = json.load(open("data/profanity.json"))
    for i in profanity:
        for j in i["dictionary"]:
            id = j["id"]
            if j.__contains__("exceptions"):
                exceptions = j["exceptions"]
            else:
                exceptions = []

            if word == id:
                if checkExceptions(word, id, exceptions):
                    return i["tags"][0]

            m = j["match"]
            matches = m.split("|")
            for x in matches:
                if word == x:
                    if checkExceptions(word, x, exceptions):
                        return i["tags"][0]

    return ""
    
def getWordNotes(word : str):
    if not isWordProfane(word, deepSearch=True):
        return "Unknown Profanity"

    profanity = json.load(open("data/profanity.json"))
    for i in profanity:
        for j in i["dictionary"]:
            id = j["id"]
            if j.__contains__("exceptions"):
                exceptions = j["exceptions"]
            else:
                exceptions = []

            if word == id:
                if checkExceptions(word, id, exceptions):
                    return i["notes"]

            m = j["match"]
            matches = m.split("|")
            for x in matches:
                if word == x:
                    if checkExceptions(word, x, exceptions):
                        return i["notes"]

    return ""