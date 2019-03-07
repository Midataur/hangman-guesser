# -*- coding: utf-8 -*-
import re

filename = 'wordlist.txt'
wordlist = open(filename).readlines()
wordlist = [x.strip().lower() for x in wordlist]
og_wordlist = list(wordlist)

def get_freqs(wordlist):
    freqs = []
    for word in wordlist:
        for letter in word:
            #create entry
            found = False
            for x in range(len(freqs)):
                if freqs[x][1] == letter:
                    found = True
                    freqs[x][0] += 1
            if not found:
                freqs.append([1,letter])
    return sorted(freqs)[::-1]

#removes ineligible words
def whittle(wordlist,known,not_pool):
    wordlist = list(wordlist)
    #generate regex
    ##remove failed letters from the pool
    poss = [x if x not in not_pool else '' for x in 'abcdefghijklmnopqrstuvwxyz']
    poss = '['+''.join(poss)+']'
    query = '^'+''.join(known).replace('_',poss)+'$'
    new = []
    for x in wordlist:
        if re.match(query,x) != None:
            new.append(x)
    return new

def get_last_working(knowns,howfar,og_wordlist,not_pool):
    if abs(howfar) > len(knowns):
        return og_wordlist
    known = knowns[howfar]
    wordlist = whittle(og_wordlist,known,not_pool)
    freqs = get_freqs(wordlist)
    most_common = None
    for x in freqs:
        if x[1] not in not_pool:
            most_common = x[1]
            break
    if most_common == None:
        return get_last_working(knowns,howfar-1,og_wordlist,not_pool)
    return wordlist

true_wordlist = list(wordlist)

changed = 1
while changed > 0:
    print 'Balancing'
    perc = 1
    changed = 0
    no_dupes = []
    for x in true_wordlist:
        if x not in no_dupes:
            no_dupes.append(x)
    for pos, word in enumerate(no_dupes):
        retried = False
        while True:
            filename = 'wordlist.txt'
            wordlist = open(filename).readlines()
            wordlist = [x.strip().lower() for x in wordlist]
            og_wordlist = list(wordlist)
            tries = 0
            guesshold = 10
            won = False
            #get word template
            known = ['_' for x in range(len(word))]
            not_pool = []
            while tries < guesshold and won == False:
                #whittle down possibilites
                wordlist = whittle(wordlist,known,not_pool)
                #get lettter frequencies
                freqs = get_freqs(wordlist)
                most_common = None
                for x in freqs:
                    if x[1] not in not_pool:
                        most_common = x[1]
                        break
                #this only happens if we're dealing with a word not in the database
                if most_common == None:
                    wordlist = get_last_working(knowns,-1,og_wordlist,not_pool)
                    freqs = get_freqs(wordlist)
                    most_common = None
                    for x in freqs:
                        if x[1] not in not_pool:
                            most_common = x[1]
                            break
                #shouldn't happen that we still don't have a guess but if so concede I guess?
                if most_common == None:
                    break
                #guess
                correct = True if most_common in word else False
                if correct:
                    #slot found into known
                    places = [i for i, x in enumerate(word) if x == most_common]
                    for x in places:
                        known[x] = most_common
                        not_pool.append(most_common)
                    if '_' not in known:
                        won = True
                else:
                    tries += 1
                    not_pool.append(most_common)
            #see if computer won
            if won:
                break
            else:
                open(filename,'a').write('\n'+word)
                if not retried:
                    retried = True
                    changed += 1
        if pos >= (len(no_dupes)/100.0)*perc:
            print str(perc)+'% complete'
            perc += 1
    print '100% complete'
    print changed,'changed'
