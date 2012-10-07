import pickle
import sqlite3
import os, glob
import poster

def scanCleanDir():
    currDir = os.getcwd()
    os.chdir(currDir + "/data/clean")
    print os.getcwd()
    fileList = glob.glob("*.txt")
    """
    tokenDict = {}

    for fileName in fileList:
        f = open(fileName, 'r')
        tokens = f.readlines()
        
        docNum = int(fileName.replace('.txt', ''))
        docPos = 0
        
        for token in tokens:
            token = token.replace('\n', '')

            if token not in tokenDict:
                tokenDict[token] = {}

            if docNum not in tokenDict[token]:
                tokenDict[token][docNum] = []
                
            tokenDict[token][docNum].append(docPos)
            docPos = docPos + 1
    """
    os.chdir(currDir)
    return #tokenDict

def getWeightInDoc(positions):
    poop = 0

def makeBiggerDict(oldDict):
    #newDict = {'postings':{}, 'tiers':{'high':[], 'low':[]}}
    newDict = {}

    for token in oldDict.keys():
        newDict[token] = {'postings':{}, 'tiers':{'high': [], 'low':[]}}

        for docID in oldDict[key].keys():
            #copy the old doc ID positions into the new dictionary
            newDict[token]['postings']['docID'] = oldDict[token][docID][:]
            getWeightInDoc(newDict[token]['postings']['docID'])
            
    
        
def main():
    currentDir = os.getcwd()
    scanCleanDir()
    print currentDir
    """
    try:
        bigF = open(currentDir+"/data/bigTokensDict.p", "r")
        bigDict = pickle.load(bigF)

    except:
        try:
            f = open(currentDir+"/data/tokensDict.p", "r")
            tokens = pickle.load(f)
        except:
            print "Pickle file not found"
            tokens = scanCleanDir()
            f = open(currentDir+"/data/tokensDict.p", "w")
            pickle.dump(tokens, f)

        bigDict = makeBiggerDict(tokens)

    """
        
    

if __name__ == "__main__":
    main()
