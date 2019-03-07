# -*- coding: utf-8 -*-

filename = raw_input('Input wordlist filename: ')
wordlist = open(filename).readlines()
wordlist = [x.strip().lower() for x in wordlist]

alphabet = list('abcdefghijklmnopqrstuvwxyz')

new = []
for x in wordlist:
    valid = True
    for t in x:
        if t not in alphabet:
            valid = False
            break
    if valid:
        new.append(x)
            

#Write to file
print 'Writing to file...'
for x in range(len(new)):
    new[x] += '\n'
open(filename,'w').write(''.join(new))
print 'Done!'
