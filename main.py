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

tries = 0
guesshold = 14
won = False

#get word template
known = ['_' for x in range(int(raw_input('How long is your word?: ')))]
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
        wordlist = list(og_wordlist)
        wordlist = whittle(wordlist,['_' for x in range(len(known))],[])
        freqs = get_freqs(wordlist)
        most_common = None
        for x in freqs:
            if x[1] not in not_pool:
                most_common = x[1]
                break
    #shouldn't happen that we still don't have a guess but if so concede I guess?
    if most_common == None:
        print 'I give up. No clue.'
        break
    #guess
    print 'I have',(guesshold-tries),'tries left'
    print 'What I have so far: '+''.join(known)
    correct = True if raw_input('Is '+most_common+' in the word? (y/n): ') == 'y' else False
    if correct:
        #slot found into known
        places = raw_input('What places is it in? (type each place seperated by a space): ').split()
        for x in places:
            known[int(x)-1] = most_common
            not_pool.append(most_common)
        if '_' not in known:
            won = True
    else:
        tries += 1
        not_pool.append(most_common)

#see if computer won
if won:
    print 'I guessed it! Better luck next time.'
else:
    print 'You beat me! Congratulations!'
    open(filename,'a').write('\n'+raw_input('So I can get better at this, what was your word?: '))
