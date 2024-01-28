from guizero import App, Text, PushButton, TextBox, ListBox
from countdown import Countdown

def enterLetters():
    generateLettersButton2.visible = False
    numLettersTextBox.visible = False
    discoveredWordsListBox.clear()
    lettersTextBox.value = ""
    lettersTextBox.visible = True
    lettersTextBox.enable()
    generateLettersButton1.disable()
    findWordsButton.disable()

    a.generatedLetters = lettersTextBox.value

def setLetters():
    a.generatedLetters = lettersTextBox.value
    a.letterNumber = len(lettersTextBox.value)
    findWordsButton.enable()
    displayWordsButton.disable()

def generateLetters1():
    enterLettersButton.disable()
    discoveredWordsListBox.clear()
    lettersTextBox.disable()
    lettersTextBox.value = ""
    numLettersTextBox.visible = True
    numLettersTextBox.enable()
    generateLettersButton2.visible = True
    displayWordsButton.disable()

def generateLetters2():
    a.letterNumber = int(numLettersTextBox.value)
    letters = a.genRandomLetters()
    lettersTextBox.visible = True
    lettersTextBox.value = letters
    findWordsButton.enable()

def findWords():
    a.loadFile()
    a.genLetterCombinationsAndTest()
    displayWordsButton.enable()
    enterLettersButton.disable()
    generateLettersButton1.disable()

def displayWords():
    discoveredWordsText.visible = True
    discoveredWordsListBox.enable()
    discoveredWordsListBox.clear()
    for word in a.discoveredWords:
        discoveredWordsListBox.append(word)
    enterLettersButton.enable()
    generateLettersButton1.enable()
    findWordsButton.disable()

a = Countdown()
app = App(title="Countdown solver", layout="grid")
welcomeText = Text(app, text="Welcome to the Countdown word solver app!", grid=[0,0,4,1])
enterLettersButton = PushButton(app, command=enterLetters, text="Enter letters", grid=[0,1])
generateLettersButton1 = PushButton(app, command=generateLetters1, text="Generate letters", grid=[1,1])
findWordsButton = PushButton(app, command=findWords, text="Find words", grid=[2,1], enabled=False)
displayWordsButton = PushButton(app, command=displayWords, text="Display words", grid=[3,1], enabled=False)
numLettersTextBox = TextBox(app, text="9", grid=[0,2,2,1], enabled=False, visible=False)
generateLettersButton2 = PushButton(app, command=generateLetters2, text="Generate", grid=[2,2,2,1], visible=False)
lettersTextBox = TextBox(app, text="", command=setLetters, width=40, grid=[0,3,4,1], enabled=False, visible=False)
discoveredWordsText = Text(app, text="Discovered words", grid=[0,4,4,1], visible=False)
discoveredWordsListBox = ListBox(app, width="fill", grid=[0,5,4,4], enabled=False, visible=True, items=[" "*40])
app.display()