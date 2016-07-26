from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import cmudict

import curses
from curses.ascii import isdigit

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def tweet(tweet):
    """
    Tweets a string
    """
    twitter.update_status(status = tweet);


def getCorpus(fileLocation, fileids):
    """
    Takes in a location of files and  list of fileids and turns
    those files into corpus
    """
    docs = PlaintextCorpusReader(fileLocation, fileids)

    return docs

d = cmudict.dict()

def countSyllables(word):
    """
    Returns the amount of syllables in a word
    """
    try:
        return max([len([y for y in x if isdigit(y[-1])]) for x in d[word.lower()]])
    except:
        return None

def editDoc(docName):
    doc = open(docName, 'r')
    docList = doc.readlines()
    doc.close()

    newLines = []
    for line in docList:
        newLines.append(line.replace('\n', ''))

    doc = open(docName,'w')
    for line in newLines:
        doc.write(line)
    doc.close()

def editDoc2(docName):
    doc = open(docName, 'r')
    docList = doc.readlines()
    doc.close()

    newLines = []
    for line in docList:
        newLines.append(line.replace('\n', ' '))

    doc = open(docName,'w')
    for line in newLines:
        doc.write(line)
    doc.close()



def makeNewTweet(corpus, doc1, doc2):
    """
    Reinvents a sentence from doc1 by feeding words from doc2 into it
    """

    sentences1 = corpus.sents(doc1)                                 #List of Sentences from first document
    sentences2 = corpus.sents(doc2)                                 #List of Sentences from second document

    sent1 = sentences1[randint(0, len(sentences1)-1)]               #Random sentence from first document
    sent2 = sentences2[randint(0, len(sentences2)-1)]               #Random sentence from second document

    sents = [sent1, sent2]

    tags = []

    for sent in sents:                                              #Get parts-of-speech tags for each word in both sentences
        print('\n')
        tag = nltk.pos_tag(sent)
        tags.append(tag)
        print(tag)

    sent1Tags = []                                                  #A list of all the pos tags from first sentence
    for word in tags[0]:
        sent1Tags.append(word[1])

    # print("\n", sent1Tags)
    numEdits = 0

    nounCounter = 0             #Counters for each pos of speech and how many have already been edited
    nnsCounter = 0
    vbCounter = 0
    vbdCounter = 0
    vbnCounter = 0
    adjCounter = 0
    newSentence = sent1
    for word in tags[1]:        #for each word in the second document
        posTag = word[1]

        disregardWords = ["been", "be", "is", "am", "are", "own", "our"]    #Disregard these words, theyre not worth replacing another

        if not (word[0] in disregardWords):
            if posTag == 'NNP' or posTag == 'NN':                           #If the word is a noun
                # print(word[0])
                count = 0
                tCount = 0
                found = False
                for t in sent1Tags:                                         #iterate through the tags in the first sentence
                    if (t == 'NNP' or t == "NN") and not found:             #until another noun is found
                        if count == nounCounter:                            #If this noun hasn't been replaced yet
                            newSentence[tCount] = word[0]                   #Replace the word at this index in the first sentence with the word
                            nounCounter += 1                                #Increase the number of nouns edited
                            found = True
                            numEdits += 1                                   #Increase number of edits
                        else:                                               #Else if this noun has already been replaced
                            count += 1                                      #Say you've hit a replaced noun and move to the next

                    tCount += 1                                             #Increase the index of words being looked at
            elif posTag == "NNS":                                           #Repeat the process with all other parts of speech, like plural nouns
                count = 0
                tCount = 0
                found = False
                for t in sent1Tags:
                    if (t == 'NNS') and not found:
                        if count == nnsCounter:
                            newSentence[tCount] = word[0]
                            nnsCounter += 1
                            found = True
                            numEdits += 1
                        else:
                            count += 1

                    tCount += 1
            elif posTag == "VB":                                            #Verbs
                count = 0
                tCount = 0
                found = False
                for t in sent1Tags:
                    if (t == 'VB') and not found:
                        if count == vbCounter:
                            newSentence[tCount] = word[0]
                            vbCounter += 1
                            found = True
                            numEdits += 1
                        else:
                            count += 1

                    tCount += 1
            elif posTag == "VBD":                                            #Past tense verbs
                count = 0
                tCount = 0
                found = False
                for t in sent1Tags:
                    if (t == 'VBD') and not found:
                        if count == vbdCounter:
                            newSentence[tCount] = word[0]
                            vbdCounter += 1
                            found = True
                            numEdits += 1
                        else:
                            count += 1

                    tCount += 1
            elif posTag == "VBN":                                           #Past participle Verbs
                count = 0
                tCount = 0
                found = False
                for t in sent1Tags:
                    if (t == 'VBN') and not found:
                        if count == vbnCounter:
                            newSentence[tCount] = word[0]
                            vbnCounter += 1
                            found = True
                            numEdits += 1
                        else:
                            count += 1

                    tCount += 1
            elif posTag == "JJ":                                            #Adjectives
                count = 0
                tCount = 0
                found = False
                for t in sent1Tags:
                    if (t == 'JJ') and not found:
                        if count == adjCounter:
                            newSentence[tCount] = word[0]
                            adjCounter += 1
                            found = True
                            numEdits += 1
                        else:
                            count += 1

                    tCount += 1

    # print("\n", newSentence)



    # sentStrings = []

    # for sent in sents:

    if numEdits == 0:
        print("No changes!")
        return None

    formatSent = ""
    index = 0

    for word in newSentence:                        #Format the sentence
        if index == 0:
            formatSent = word.capitalize()
        elif word in ".,'!?-:;":
            formatSent = formatSent + word
        elif formatSent[-1:] == "'" and word == 's':
            formatSent = formatSent + word
        else:
            formatSent = formatSent + " " + word

        index += 1
    # print(formatSent)

    #   sentString.append(formatSent)
    return formatSent



def runBot():
    corpus = getCorpus('Docs', '.*')

    

    found = False

    while not found:                                            #Keep trying to find a sentence til you find one that fits
        newTweet = makeNewTweet(corpus, 'const.txt', 'comm_manifesto.txt')
        if newTweet == None:                                    #If there are no changes to sentence, try again
            found = False
        elif len(newTweet) < 140:                               #If the sentence is less than 140 characters, it's good!
            found = True
        else:                                                   #Else try to shorten it
            index = 0
            indices = []
            for character in newTweet:
                if character == "," or character == ";":       #By cutting it off at commas and semicolons
                    indices.append(index)
                index += 1

            while len(newTweet) > 140 and len(indices) > 0:         #Keep cutting the sentence until it's short enough
                newTweet = newTweet[:indices.pop(len(indices)-1)]

            if len(newTweet) < 140:
                found = True

    print(newTweet)

    if not debug:

        try:
            tweet(newTweet)
            print("I just tweeted!")
        except:
            print("Ran into a problem Tweeting!")






def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60*3)        #runs every 3 hours

# editDoc2('Docs\const.txt')
