#!/usr/bin/python3
'''
data structure to hold entire dictionary in to the memory in efficient manner.
here key is alphabetically sorted characters of each word
from dictionary file and value is list of words who has same key.
'''
dict = {}
#createDictionary creates dictionary data structure
def createDictionary():
    global dict
    #dict = {}
    # dictionaryPointer is pointer to dictionary text file
    try:
        dictionaryPointer = open("en_US.dic")
    except IOError:
        print("Dictionary source file does not exists")
        sys.exit()
    #line represents line in the dictionary file
    line = dictionaryPointer.readline()
    line = re.sub(r'/.*$', "", line)
    #program progress info printed on console
    print("Preprocessing dictionary.....")
    #key is key of dictionary data structure
    key = ""
    while line:
        #read dictionary line by line, declare key.
        line = line.strip()
        line = line.lower()
        #Sort each word in the dictionary.
        #It creates a list of alphabets in each word.
        #Then join each alphabet of word, store in key
        keyList = sorted(line)
        key = ''.join(keyList)
        words = []
        #dict is dictioanary data structure in which dictionary is loaded
        #If key is in dictionary, append new value to existing list
        if key in dict:
            dict[key] = dict[key] + ',' + line
        #If key is not in dictionary add key to dictionary and value to the key.
        else:
            dict[key] = line
        line = dictionaryPointer.readline()
        line = re.sub(r'/.*$', "", line)
    #len(dict)
    #print("length of dict is", len(dict))
    #Close file handler explicitely and report progress to user on console
    dictionaryPointer.close()
    print("Done")
    return dict

#spellChecker finds misspelled words in input file
def spellChecker(dict):
    #inputFilePointer is pointer to input text file
    #inputLine represents line in the input file
    inputLine = inputFilePointer.readline()
    inputLine = inputLine.strip()
    #inputWordList represents all words in input file
    inputWordList = re.findall(r"[\w']+", inputLine)
    foundFlag = False
    wordList = []
    #report progress to user on console
    print("Writing misspelled words in log file.....")
    logFilePointer.write("Detailed spell checker log: \n")
    while inputWordList:
        # For every word in inputWordList, sort word alphabetically
        for word in inputWordList:
            foundFlag == False
            word = word.strip()
            word = word.lower()
            sortedWord = sorted(word)
            sortedWord = ''.join(sortedWord)
            # Check if sortedWord is there in the dictionary key.
            if sortedWord in dict.keys():
                # If sorted word is found, check if word is present in wordList of particular key.
                if word in dict[sortedWord]:
                    foundFlag = True
                # If word not found in dictioanry, print misspelled word to log file.
                # Also print suggestions to log file.
                if word not in dict[sortedWord]:
                    # report progress to user on console
                    logFilePointer.write("Misspelled word:")
                    logFilePointer.write(''.join(word))
                    logFilePointer.write('\n')
                    logFilePointer.write("Suggested spelling:")
                    logFilePointer.write(dict[sortedWord])
                    logFilePointer.write('\n')
            # If key not found in keys of dictionary, then print no suggestion found in log file.
            else:
                logFilePointer.write("Misspelled word:")
                logFilePointer.write(''.join(word))
                logFilePointer.write('\n')
                logFilePointer.write("No suggestion found in dictionary")
                logFilePointer.write('\n')
        inputLine = inputFilePointer.readline()
        inputLine = inputLine.strip()
        #print(inputLine)

        inputWordList = re.findall(r"[\w']+", inputLine)
        #print(inputWordList)
    #report progress to user on console
    print("Done.")

#GrammarChecker finds gramatical mistakes in input file.
def grammarChecker():
    #seek specifies where the cursor is.
    #Here we want to read file from start, so seek(0) will point to start of the file
    inputFilePointer.seek(0)
    input = inputFilePointer.read()
    if input.strip() != '':
        input = re.split('\.|;|\?|!', input)
        tool = language_check.LanguageTool('en-GB')
        #report progress to the user
        print("Writing gramatical mistakes in log file.....")
        logFilePointer.write("Detailed grammar checker log:\n")
        for inputTextLine in input:
            #inputTextLine = inputTextLine.strip()
            matches = tool.check(inputTextLine)
            for match in matches:
                logFilePointer.write(str(match))
                logFilePointer.write('\n')
    #report progress to user on console
    print("Done")

if __name__ == '__main__':
    import sys
    import re
    import time
    from functools import reduce
    import itertools
    import language_check
    import os

    #Start try block to check if input is given or not
    try:
        inputFile = sys.argv[1]
    except:
        if len(sys.argv) < 2:
            print("Please provide input file. Thank you.")
            sys.exit()
    #Start try block to if given input file is present or not
    try:
        inputFilePointer = open(inputFile)
    except IOError:
        print("Sorry, cannot find input file %s" %(inputFile))
        sys.exit()
    #dict represents dictionary returned by function createDictionary
    #Call createDictionary function
    dict = createDictionary()
    #Check if output drectory present or not, if not create one.
    #Create output file with timestamp.
    #timeStr represents current timestamp with hour, minutes and seconds
    if not os.path.exists('output'):
        currentPath = os.path.dirname(os.path.abspath(__file__))
        outputDirPath = os.path.join(currentPath, 'output')
        os.makedirs(outputDirPath)
        timeStr = time.strftime('%Y%m%d-%H%M%S')
        logFilePointer = open("output/" + "output_" + timeStr + ".txt", "w+")
        print("Creating output directory")
    else:
        timeStr = time.strftime('%Y%m%d-%H%M%S')
        logFilePointer = open("output/" + "output_" + timeStr + ".txt", "w+")


    #Call spellChecker function
    spellChecker(dict)
    #Call grammarChecker function
    grammarChecker()
    print("Find log file in output directory")














