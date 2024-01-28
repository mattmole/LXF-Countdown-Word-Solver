import hashlib
import random
import itertools
from rich.prompt import Prompt
from rich.status import Status
from rich.console import Console
import sys
import time
import os
from math import floor

class Countdown:
    def __init__(self, letterNumber=9):

        self.wordDict = {}
        self.discoveredWords = []
        self.letterNumber = letterNumber
        self.generatedLetters = ""
        self.wordPrefixDict = {}

    def generateHash(self,letters):
        m = hashlib.sha256()
        m.update(letters.encode('utf-8'))
        return m.hexdigest()

    def loadFile(self, wordFile="words_alpha.txt"):
        with open(wordFile, 'r') as file:
            for line in file:
                word = line.strip()
                if len(word) <= self.letterNumber:
                    self.wordDict[self.generateHash(word)] = word
                    prefixLetters = word[0:floor(1/2*self.letterNumber)].lower()

                    prefixHash = self.generateHash(prefixLetters)
                    if prefixHash not in self.wordPrefixDict:
                        self.wordPrefixDict[prefixHash] = ""

    def genRandomLetters(self):
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        numConsonants = random.randint(4, self.letterNumber - 3)
        numVowels = self.letterNumber - numConsonants
        
        randomLetters = ""
        for i in range(0,numVowels):
            randomLetters += random.choice(vowels)
        for i in range(0,numConsonants):
            randomLetters += random.choice(consonants)
        self.generatedLetters = randomLetters
        return randomLetters

    def genLetterCombinationsAndTest(self):
        self.discoveredWords.clear()
        for i in range(2,self.letterNumber+1):
            for combination in itertools.permutations(self.generatedLetters, i):
                prefixLetters = "".join(combination[0:floor(1/2*self.letterNumber)])
                prefixHash = self.generateHash(prefixLetters)
                if prefixHash in self.wordPrefixDict:
                    constructLetters = "".join(combination)
                    self.testWord(constructLetters)

    def testWord(self,letters):
        hashedLetters = self.generateHash(letters)
        if hashedLetters in self.wordDict:
            if self.wordDict[hashedLetters] not in self.discoveredWords:
                self.discoveredWords.append(self.wordDict[hashedLetters])
            return self.wordDict[hashedLetters]
        else:
            return -1

if __name__ == "__main__":
    console = Console()
    a = Countdown()
    selectedLetters = None
    allowWordDisplay = False
    firstLoad = True

    console.print("************************************")
    console.print("Welcome to the countdown word solver")
    console.print("************************************")
    console.print()
    
    # Take the command arguments if if one is present, use this as the letter combination
    # automate the running.
    if len(sys.argv) == 2:
        console.print("Running from command line argument")
        letters = sys.argv[1].strip()
        a.generatedLetters = letters
        console.print(f"Entered Letters: {letters}")
        with Status("Generating letter combinations") as status:
            a.genLetterCombinationsAndTest()
        if len(a.discoveredWords) == 0:
            console.print("No words could be found")
        else:
            console.print("Discovered words...")
            for word in a.discoveredWords:
                console.print(f"\t{word}")
    else:
        carryOn = True
        while carryOn:
            if firstLoad == False:
                console.clear()
            firstLoad = False
            console.print("1) Enter a set of letters")
            console.print("2) Generate a random set of letters")
            if selectedLetters == None:
                console.print("[dim white]3) Find words from the set of letters[/dim white]")
            else:
                console.print("3) Find words from the set of letters")
            if allowWordDisplay:
                console.print("4) Display any found words")
            else:
                console.print("[dim white]4) Display any found words[/dim white]")
            if allowWordDisplay:
                console.print("5) Write discovered words to file")
            else:
                console.print("[dim white]5) Write discovered words to file[/dim white]")
            console.print("6) Quit")
            if selectedLetters != None:
                console.print()
                console.print(f"[yellow]Selected Letters: {selectedLetters}[/yellow]")

            response = Prompt.ask("Enter number from the list above")
            if response == "6" or response == "q" or response == "Q":
                carryOn = False
            elif response == "5":
                if allowWordDisplay == False:
                    console.print("Words have not yet been discovered")
                else:
                    if len(a.discoveredWords) == 0:
                        console.print("No words could be found")
                    else:
                        console.print("Writing words to countdownOutput.txt...")
                        with open("countdownOutput.txt","w") as outputFile:
                            for word in a.discoveredWords:
                                outputFile.write(word+os.linesep)
            elif response == "4":
                if allowWordDisplay == False:
                    console.print("Words have not yet been discovered")
                else:
                    if len(a.discoveredWords) == 0:
                        console.print("No words could be found")
                    else:
                        console.print("Discovered words...")
                        for word in a.discoveredWords:
                            console.print(f"\t{word}")
                Prompt.ask("Return to main menu")
            elif response == "3":
                if selectedLetters == None:
                    console.print("No letters have been selected")
                    Prompt.ask("Return to main menu")
                else:
                    a.loadFile()
                    startTime = time.time()
                    with Status("Discovering dictionary words") as status:
                        a.genLetterCombinationsAndTest()
                    endTime = time.time()
                    allowWordDisplay = True
                    console.print(f"Time taken to discover words: {int(endTime-startTime)}s")
                    Prompt.ask("Return to main menu")

            elif response == "2":
                numLetters = Prompt.ask("Enter number of letters")
                try:
                    intNumLetters = int(numLetters)
                    a.letterNumber = intNumLetters
                    a.genRandomLetters()
                    selectedLetters = a.generatedLetters
                except:
                    console.print("Cannot convert to an integer")
                    Prompt.ask("Return to main menu")
                allowWordDisplay = False
            elif response == "1":
                letters = Prompt.ask("Enter letters")
                letters = letters.strip()
                if len(letters) == 0:
                    console.print("No letters entered")
                    Prompt.ask("Return to main menu")
                # Check for non-alphabetical characters
                else:
                    charCounter = 0
                    for char in letters:
                        if  not((ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122)):
                            charCounter += 1
                    if charCounter >= 1:
                        console.print("String contains non alphabetical characters")
                        Prompt.ask("Return to main menu")
                    elif charCounter == 0:
                        a.generatedLetters = letters
                        a.letterNumber = len(letters)
                        selectedLetters = letters
                allowWordDisplay = False