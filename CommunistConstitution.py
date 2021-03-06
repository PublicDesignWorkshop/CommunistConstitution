from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import cmudict

import curses
from curses.ascii import isdigit

import csv
import datetime

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

name = "ComConstitution"

def getFollowers():
    """
    Gets details about followers of the bot
    """

    names = []                  #Name of follower
    usernames = []              #Username of follower
    ids = []                    #User id of follower
    locations = []              #Location of follower(as listed on their profile)
    follower_count = []         #How many followers the follower has
    time_stamp = []             #Date recorded

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")


    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    follower_count.append("# of their Followers")
    time_stamp.append("Time Stamp")

    next_cursor = -1

    #Get follower list (200)
    while(next_cursor):
        get_followers = twitter.get_followers_list(screen_name=name,count=200,cursor=next_cursor)
        for follower in get_followers["users"]:
            try:
                print(follower["name"].encode("utf-8").decode("utf-8"))
                names.append(follower["name"].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't Print")
            usernames.append(follower["screen_name"].encode("utf-8").decode("utf-8"))
            ids.append(follower["id_str"])

            try:
                print(follower["location"].encode("utf-8").decode("utf-8"))
                locations.append(follower["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't Print")

            follower_count.append(follower["followers_count"])
            time_stamp.append(datestamp)
            next_cursor = get_followers["next_cursor"]

    open_csv = open("followers.csv","r",newline='')                         #Read what has already been recorded in the followers file
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))

    rows = zip(names,usernames,ids,locations,follower_count,time_stamp)     #Combine lists

    oldFollowerIDs = []                                                     #Store followers that have already been recorded in the past

    oldFollowers_csv = csv.reader(open_csv)

    for row in oldFollowers_csv:
            oldFollowerIDs.append(row[2])

    open_csv.close()

    open_csv = open("followers.csv","a", newline='')        #Append new followers to the followers file
    followers_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[2] in oldFollowerIDs):                  #if the ID isn't already in the follower list
            followers_csv.writerow(row)

    open_csv.close()

def getMentionsRetweets():
    """
    Gets details of mentions/retweets of the user
    """

    names = []                  #Name of user who retweeted/mentioned
    usernames = []              #Their username
    ids = []                    #Their user id
    locations = []              #Their location (as listed on their profile)
    tweetIDs = []               #ID of the retweet/mention
    tweets = []                 #The retweet/mention text
    time_stamp = []             #Date the retweet/mention was created

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    tweetIDs.append("Tweet ID")
    tweets.append("Tweet Text")
    time_stamp.append("Time Stamp")

    #Get mentions (200)
    mentions_timeline = twitter.get_mentions_timeline(screen_name=name,count=200)
    for mention in mentions_timeline:
        try:
            print(mention['user']['name'].encode("utf-8").decode("utf-8"))
            names.append(mention['user']['name'].encode("utf-8").decode("utf-8"))
        except:
            names.append("Can't print")
        usernames.append(mention["user"]["screen_name"].encode("utf-8").decode("utf-8"))
        ids.append(mention["user"]["id_str"])
        try:
            print(mention["user"]["location"].encode("utf-8").decode("utf-8"))
            locations.append(mention["user"]["location"].encode("utf-8").decode("utf-8"))
        except:
            locations.append("Can't Print")
        tweetIDs.append(mention["id_str"])
        try:
            print(mention['text'].encode("utf-8").decode("utf-8"))
            tweets.append(mention['text'].encode("utf-8").decode("utf-8"))
        except:
            tweets.append("Can't Print")
        time_stamp.append(mention["created_at"].encode("utf-8").decode("utf-8"))

    #Get retweets (200)
    retweetedStatuses = twitter.retweeted_of_me(count = 100)                                    #Get tweets from the user that have recently been retweeted
    for retweetedStatus in retweetedStatuses:
        statusID = retweetedStatus["id_str"]
        retweets = twitter.get_retweets(id=statusID,count=100)                                  #Get the retweets of the tweet
        for retweet in retweets:
            try:
                print(retweet['user']['name'].encode("utf-8").decode("utf-8"))
                names.append(retweet['user']['name'].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't print")
            
            usernames.append(retweet["user"]["screen_name"].encode("utf-8").decode("utf-8"))

            ids.append(retweet["user"]["id_str"])

            try:
                print(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
                locations.append(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't print")
            
            tweetIDs.append(retweet["id_str"])
            
            try:
                print(retweet['text'].encode("utf-8").decode("utf-8"))
                tweets.append(retweet['text'].encode("utf-8").decode("utf-8"))
            except:
                tweets.append("Can't print")
            
            time_stamp.append(retweet["created_at"].encode("utf-8").decode("utf-8"))


    open_csv = open("mentions_retweets.csv","r",newline='')
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))
    # print(len(names))
    rows = zip(names,usernames,ids,locations,tweetIDs, tweets,time_stamp)

    oldMentionsIDs = []                             #Record mentions/retweets that have already been recorded before

    oldMentions_csv = csv.reader(open_csv)

    for row in oldMentions_csv:
            oldMentionsIDs.append(row[4])

    open_csv.close()

    open_csv = open("mentions_retweets.csv","a", newline='') #Append new mentions/retweets to the list
    mentions_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[4] in oldMentionsIDs):          #if the ID isn't already in the mentions list
            # print(row)
            mentions_csv.writerow(row)

    open_csv.close()

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
    try:
        getFollowers()
    except:
        print("Couldn't get Followers")

    try:        
        getMentionsRetweets()
    except:
        print("Couldn't get Mentions/Retweets")

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
