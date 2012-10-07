import sqlite3
import pickle
import os

from portStemmer import PorterStemmer
from makeBigDict import scanCleanDir

class Searcher:
    def __init__(self):
        self.stemmer = PorterStemmer()
        try:
            f = open(os.getcwd()+"/data/tokensDict.p", "r")
            self.tokens = pickle.load(f)
        except:
            print "Pickle file not found"
            print "Creating the Dirctionary"
            self.tokens = scanCleanDir()
            f = open(os.getcwd()+"/data/tokensDict.p", "w")
            pickle.dump(self.tokens, f)

        
    def dbQuery(self, query, args = ()):
        conn = sqlite3.connect('/Users/kristofer/comp_490/2lab/data/cache.db')
        db = conn.cursor()
        
        #args should be a tuple of the arguments in the query
        db.execute(query, args)
        
        rows = db.fetchall()
        conn.close()
        
        return rows

    def singleToken(self):
        print
        word = raw_input("Enter your one word query: ")
        token = word.lower()
        token = self.stemmer.stem(token, 0, len(token) - 1)

        try: 
            wordDict = self.tokens[token]
        except:
            print word, "does not seem to exist in our files. Please try a different word"
            print 
            return
            
        occurenceTotal = 0
        highestFreq = {'freq': 0, 'docs':[]}
        
        i = 1
        for doc in wordDict.keys():
            freq = len(wordDict[doc])
            occurenceTotal += freq

            linksQuery = """
                         SELECT webPage.linkText, item.itemName FROM (
                         SElECT itemToWebPage.webPageId, itemToWebPage.itemId
                         FROM itemToWebPage
                         WHERE webPageId = ?) AS linkItem
                         JOIN item
                         ON item.itemId = linkItem.itemId
                         JOIN webPage
                         ON webPage.webPageId = linkItem.webPageId;
                         """
            linksRow = self.dbQuery(linksQuery, (doc,))
            
            print 
            print i,"\t",linksRow[0][0]
            print "\t item: ",linksRow[0][1]
            print "\t occured ",freq,"times"
            i += 1
            
            if freq > highestFreq['freq']:
                highestFreq['freq'] = freq
                highestFreq['docs'] = [linksRow[0][0]]
                
            elif freq == highestFreq['freq']:
                highestFreq['docs'].append(doc)
            
        
        print
        print "Total occurence of", word, "is", occurenceTotal, "times"
        print "Highest frequency: ", highestFreq['freq'], " times in: ",
        for i in range(len(highestFreq['docs'])):
            if i > 0:
                print "and"
            print highestFreq['docs'][i]
        print

    def orQuery(self):
        print
        word1 = raw_input("Enter the first word of your query: ")
        word2 = raw_input("Enter the second word of your query: ")
        token1 = word1.lower()
        token1 = self.stemmer.stem(token1, 0, len(token1) - 1)
        token2 = word2.lower()
        token2 = self.stemmer.stem(token2, 0, len(token2) - 1)

        try: 
            docs = self.tokens[token1].keys()
        except:
            print word1, "does not seem to exist in our files. Please try a different word"
            print 
            return

        try: 
            docs2 = self.tokens[token2].keys()
        except:
            print word2, "does not seem to exist in our files. Please try a different word"
            print 
            return

        #Perform a logical or on the elements of both lists.
        #Storing them in keys
        for doc in docs2:
            if doc not in docs:
                docs.append(doc)

        
        occurenceTotal = 0
        i = 1
        
        highestFreq = {'freq': 0, 'docs':[]}
        for doc in docs:
            freq1 = 0
            freq2 = 0

            try:
                freq1 = len(self.tokens[token1][doc])
            except:
                None

            try:
                freq2 = len(self.tokens[token2][doc])
            except:
                None
            
            freq = freq1 + freq2
            occurenceTotal += freq
            
            linksQuery = """
                         SELECT webPage.linkText, item.itemName FROM (
                         SElECT itemToWebPage.webPageId, itemToWebPage.itemId
                         FROM itemToWebPage
                         WHERE webPageId = ?) AS linkItem
                         JOIN item
                         ON item.itemId = linkItem.itemId
                         JOIN webPage
                         ON webPage.webPageId = linkItem.webPageId;
                         """
            linksRow = self.dbQuery(linksQuery, (doc,))

            print 
            print i,"\t",linksRow[0][0]
            print "\t item: ",linksRow[0][1]
            print "\t occured ",freq,"times"
            i += 1
            
            if freq > highestFreq['freq']:
                highestFreq['freq'] = freq
                highestFreq['docs'] = [linksRow[0][0]]
                
            elif freq == highestFreq['freq']:
                highestFreq['docs'].append(doc)
        print
        print "Total occurence of", word1, "or", word2, "is", occurenceTotal, "times"
        print "Highest frequency: ", highestFreq['freq'], " times in: ",
        for i in range(len(highestFreq['docs'])):
            if i > 0:
                print "and"
            print highestFreq['docs'][i]
        print

    def andQuery(self):
        print
        word1 = raw_input("Enter the first word of your query: ")
        word2 = raw_input("Enter the second word of your query: ")
        token1 = word1.lower()
        token1 = self.stemmer.stem(token1, 0, len(token1) - 1)
        token2 = word2.lower()
        token2 = self.stemmer.stem(token2, 0, len(token2) - 1)
        
        #Get the keys from both lists
        docs = []
        try: 
            docs1 = self.tokens[token1].keys()
        except:
            print word1, "does not seem to exist in our files. Please try a different word"
            print 
            return

        try: 
            docs2 = self.tokens[token2].keys()
        except:
            print word2, "does not seem to exist in our files. Please try a different word"
            print 
            return

        #Perform a logical and on the elements of both lists.
        #Storing them in keys
        for doc in docs1:
            if doc in docs2:
                docs.append(doc)

        
        occurenceTotal = 0
        i = 1
        
        highestFreq = {'freq': 0, 'docs':[]}
        for doc in docs:
            freq1 = 0
            freq2 = 0

            try:
                freq1 = len(self.tokens[token1][doc])
            except:
                None

            try:
                freq2 = len(self.tokens[token2][doc])
            except:
                None
            
            freq = freq1 + freq2
            occurenceTotal += freq
            
            linksQuery = """
                         SELECT webPage.linkText, item.itemName FROM (
                         SElECT itemToWebPage.webPageId, itemToWebPage.itemId
                         FROM itemToWebPage
                         WHERE webPageId = ?) AS linkItem
                         JOIN item
                         ON item.itemId = linkItem.itemId
                         JOIN webPage
                         ON webPage.webPageId = linkItem.webPageId;
                         """
            linksRow = self.dbQuery(linksQuery, (doc,))

            print 
            print i,"\t",linksRow[0][0]
            print "\t item: ",linksRow[0][1]
            print "\t occured ",freq,"times"
            i += 1
            
            if freq > highestFreq['freq']:
                highestFreq['freq'] = freq
                highestFreq['docs'] = [linksRow[0][0]]
                
            elif freq == highestFreq['freq']:
                highestFreq['docs'].append(doc)
        print
        print "Total occurence of", word1, "and", word2, "is", occurenceTotal, "times"
        print "Highest frequency: ", highestFreq['freq'], " times in: ",
        for i in range(len(highestFreq['docs'])):
            if i > 0:
                print "and"
            print highestFreq['docs'][i]
        print

    def phraseQuery(self):
        print
        phrase = raw_input("Enter a two word phrase: ")

        while len(phrase.split(' ')) != 2:
            phrase = raw_input("Make sure your phrase is two words (e.g. 'hello goodbye'): ")
            
        words = phrase.split(' ')
        word1 = words[0]
        word2 = words[1]
        token1 = word1.lower()
        token1 = self.stemmer.stem(token1, 0, len(token1) - 1)
        token2 = word2.lower()
        token2 = self.stemmer.stem(token2, 0, len(token2) - 1)

        
        
        
        #Get the keys from both lists
        docs = []
        try: 
            docs1 = self.tokens[token1].keys()
        except:
            print word1, "does not seem to exist in our files. Please try a different word"
            print 
            return

        try: 
            docs2 = self.tokens[token2].keys()
        except:
            print word2, "does not seem to exist in our files. Please try a different word"
            print 
            return

        #Perform a logical and on the elements of both lists.
        #Storing them in keys
        phraseDict = {}

        #Check which documents have both words
        for doc in docs1:
            if doc in docs2:
                doc1Pos = self.tokens[token1][doc]
                doc2Pos = self.tokens[token2][doc]

                #check which documents have the phrase in the correct order
                freq = 0
                for pos1 in doc1Pos:
                    for pos2 in doc2Pos:
                        if pos2 == pos1 + 1:
                            freq += 1
                
                if freq > 0:
                    phraseDict[doc] = freq
        
        occurenceTotal = 0
        i = 1
        
        highestFreq = {'freq': 0, 'docs':[]}
        for doc in phraseDict.keys():
            
            freq = phraseDict[doc]
            occurenceTotal += freq
        
            linksQuery = """
                         SELECT webPage.linkText, item.itemName FROM (
                         SElECT itemToWebPage.webPageId, itemToWebPage.itemId
                         FROM itemToWebPage
                         WHERE webPageId = ?) AS linkItem
                         JOIN item
                         ON item.itemId = linkItem.itemId
                         JOIN webPage
                         ON webPage.webPageId = linkItem.webPageId;
                         """
            linksRow = self.dbQuery(linksQuery, (doc,))
        
            print 
            print i,"\t",linksRow[0][0]
            print "\t item: ",linksRow[0][1]
            print "\t occured ",freq,"times"
            i += 1
            
            if freq > highestFreq['freq']:
                highestFreq['freq'] = freq
                highestFreq['docs'] = [linksRow[0][0]]
                
            elif freq == highestFreq['freq']:
                highestFreq['docs'].append(doc)
        print
        print "Total occurence of",phrase, "is", occurenceTotal, "times"
        print "Highest frequency: ", highestFreq['freq'], " times in: ",
        for i in range(len(highestFreq['docs'])):
            if i > 0:
                print "and"
            print highestFreq['docs'][i]
        print


    def nearQuery(self):
        print
        word1 = raw_input("Enter the first word: ")
        word2 = raw_input("Enter the second word: ")
        distance = input ("Enter the number of positions away you want to look: ")
        
        token1 = word1.lower()
        token1 = self.stemmer.stem(token1, 0, len(token1) - 1)
        token2 = word2.lower()
        token2 = self.stemmer.stem(token2, 0, len(token2) - 1)

        
        
        
        #Get the keys from both lists
        docs = []
        try: 
            docs1 = self.tokens[token1].keys()
        except:
            print word1, "does not seem to exist in our files. Please try a different word"
            print 
            return

        try: 
            docs2 = self.tokens[token2].keys()
        except:
            print word2, "does not seem to exist in our files. Please try a different word"
            print 
            return

        #Perform a logical and on the elements of both lists.
        #Storing them in keys
        phraseDict = {}

        #Check which documents have both words
        for doc in docs1:
            if doc in docs2:
                doc1Pos = self.tokens[token1][doc]
                doc2Pos = self.tokens[token2][doc]

                #check which documents have the words within the allotted distance of each other
                freq = 0
                for pos1 in doc1Pos:
                    for pos2 in doc2Pos:
                        if (pos2 - pos1 >= 0 - distance) and (pos2 - pos1 <= distance):
                            freq += 1
                
                if freq > 0:
                    phraseDict[doc] = freq
        
        occurenceTotal = 0
        i = 1
        
        highestFreq = {'freq': 0, 'docs':[]}
        for doc in phraseDict.keys():
            
            freq = phraseDict[doc]
            occurenceTotal += freq
        
            linksQuery = """
                         SELECT webPage.linkText, item.itemName FROM (
                         SElECT itemToWebPage.webPageId, itemToWebPage.itemId
                         FROM itemToWebPage
                         WHERE webPageId = ?) AS linkItem
                         JOIN item
                         ON item.itemId = linkItem.itemId
                         JOIN webPage
                         ON webPage.webPageId = linkItem.webPageId;
                         """
            linksRow = self.dbQuery(linksQuery, (doc,))
        
            print 
            print i,"\t",linksRow[0][0]
            print "\t item: ",linksRow[0][1]
            print "\t occured ",freq,"times"
            i += 1
            
            if freq > highestFreq['freq']:
                highestFreq['freq'] = freq
                highestFreq['docs'] = [linksRow[0][0]]
                
            elif freq == highestFreq['freq']:
                highestFreq['docs'].append(doc)
        print
        print "Total occurence of",word1, "within ", distance, "positions of", word2, "was",occurenceTotal, "times"
        print "Highest frequency: ", highestFreq['freq'], " times in: ",
        for i in range(len(highestFreq['docs'])):
            if i > 0:
                print "and"
            print highestFreq['docs'][i]
        print
    
    def searchMenu(self):
        print
        print "-----------------------------------------------------------"
        print "\t       Welcome to Stensland-ipedia!"
        print "\tWhere you can search to your hearts content!"
        print "-----------------------------------------------------------"
        print 
        
        menu = True
        while menu:
            print "Choose the number corresponding to the query you would like to perform"
            print "---------------------------------------------------------------------"
            print "1.\tSingle token query."
            print "2.\tAND query."
            print "3.\tOR query."
            print "4.\t2-Token query."
            print "5.\tNear query."
            print "6.\tQuit"
            
            choice = raw_input("Enter your choice: ")
            
            if choice == '1':
                self.singleToken()
                
            elif choice == '2':
                self.andQuery()
                
            elif choice == '3':
                self.orQuery()

            elif choice == '4':
                self.phraseQuery()

            elif choice == '5':
                self.nearQuery()
                 
            elif choice == '6':
                menu = False
                print "\n"
                
            else:
                print "That is not a thing I understand."
                print 
                
        print
        print "Thank you for being my friend!"
        print 
        
def main():
    #os.chdir('/Users/kristofer/comp_490/2lab')
    print "Preparing the search engine..."
    stenslandipedia = Searcher()
    stenslandipedia.searchMenu()

if __name__ == "__main__":
    main()

