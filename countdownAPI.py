from typing import Union
from fastapi import FastAPI
from countdown import Countdown

a = Countdown()
app = FastAPI()

@app.get("/set/{letters}")
def setWord(letters):
    numLetters = len(letters)
    charCounter = 0
    for char in letters:
        if not((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122)):
            charCounter += 1
    if numLetters < 7:
        return {"error": "Number must be above 7"}
    else:
        if charCounter >= 1:
            return {"error": "String contains non alphabetical characters"}
        elif charCounter == 0:
            a.generatedLetters = letters
            a.letterNumber = numLetters
            return {"numLetters": numLetters, "generatedLetters": letters}

@app.get("/generate/{numLetters}")
def generateWord(numLetters):
    numLettersInt = 0
    try:
        numLettersInt = int(numLetters)
    except:
        return {"error":"Argument must be an integer"}
    else:
        if numLettersInt < 7:
            return {"error": "Number must be above 7"}
        elif numLettersInt >= 7:
            a.letterNumber = numLettersInt
            a.genRandomLetters()
            a.letterNumber = numLettersInt
            return {"numLetters": numLetters, "generatedLetters": a.generatedLetters}

@app.get("/findAndDisplay/")
def findAndDisplay():
    a.loadFile()
    a.genLetterCombinationsAndTest()
    return {"numWords": len(a.discoveredWords), "words": a.discoveredWords}