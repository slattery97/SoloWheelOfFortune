################################################################################
# Author: Ryan Slattery
# Date: 4/24/20
# This program allows the user to play a solo version of the game 
# Wheel of Fortune
################################################################################

#import packages
import random as r
import math

# MAIN
#open file
with open('phrases.txt') as phraseList:
    #assign phrases to a list
    phrases = phraseList.readlines()
    for i in range(len(phrases)):
        phrases[i] = phrases[i].strip('\n')

    #get random phrase 1
    phrase = r.choice(phrases)

    # initialize round cash
    roundCash = [0,0,0,0]

    # initialize round number 1
    roundNumber = 0

    #get hidden phrase
    phraseHid = str('')
    for i in range(len(phrase)):
        if phrase[i] == str(' '):
            phraseHid += str(' ')
        elif phrase[i] == str("'"):
            phraseHid += str("'")
        elif phrase[i] == str('-'):
            phraseHid += str('-')
        elif phrase[i] == str('&'):
            phraseHid += str('&')
        else:
            phraseHid += str('_')

    #get consonants and vowels list
    consList = str('BCDFGHJKLMNPQRSTVWXYZ')
    vowsList = str('AEIOU')
    
    #initialize list of used letters
    usedCons = []
    usedVows = []

    #SPIN WHEEL
    def spin(roundCash, phraseHid, usedCons, consList, roundNumber):
        #get list of spaces
        spaces = [500,500,500,500,500,550,600,600,600,600,650,650,650,700,700,
                  700,800,900,2500,str('BANKRUPT'),str('BANKRUPT')]
        #get random space
        space = r.choice(spaces)
        #player gets bankrupt space
        if space == str('BANKRUPT'):
            print('The wheel landed on BANKRUPT.')
            print('You lost $' + str(roundCash[0]) + '!')
            roundCash[0] = 0
            return roundCash, phraseHid, usedCons, consList, roundNumber
        #player get a cash space
        else:
            print(str('The wheel landed on $')+str(space)+str('.'))
            consChoice = input('Pick a consonant: ')
            
        #check for correct input
        while ((consChoice == str('a')) or (consChoice == str('A')) or
            (consChoice == str('e')) or (consChoice == str('E')) or
            (consChoice == str('i')) or (consChoice == str('I')) or
            (consChoice == str('o')) or (consChoice == str('O')) or
            (consChoice == str('u')) or (consChoice == str('U'))):
                print('Vowels must be purchased.')
                consChoice = input('Pick a consonant: ')

        while len(consChoice) != 1:
            print('Please enter exactly one character.')
            consChoice = input('Pick a consonant: ')

        while consChoice in usedCons == True:
            print(str('The letter ')+str(consChoice).capitalize()
                  +str(' has already been used.'))
            consChoice = input('Pick a consonant: ')
        
        
        #check for occurances of consonant
        phraseHidNew = phraseHid
        # counter variable to count number of consonant matches in phrase
        consMatches = 0
        for i in range(len(phrase)):
            if (consChoice == phrase[i]) or (consChoice.capitalize() == phrase[i]): 
                consMatches += 1
                phraseHidNew = str(phraseHidNew[: i]  + consChoice.capitalize() +
                                   phraseHidNew[i + 1 :])
        #if no occurances, print message
        if phraseHidNew == phraseHid:
            print(str("I'm sorry, there are no ")+str(consChoice).capitalize()
                      +str("'s."), sep='')
            print(' ')
            return roundCash, phraseHidNew, usedCons, consList, roundNumber
        else:
            cashEarned = int(consMatches) * int(space)
            print('There is ' + str(consMatches) + ' ' + str(consChoice)
                  + ', which earns you $' + str(cashEarned) + '.')
            roundCash[roundNumber] += cashEarned
            # append consonant to list of used consonants
            usedCons.append(consChoice)
            # remove used consonant from available consonants string
            for i in range(len(consList)):
                if (consChoice == consList[i]) or (consChoice.capitalize() == consList[i]): 
                    consList = str(consList[: i]  + ' ' +
                                   consList[i + 1 :])
            return roundCash, phraseHidNew, usedCons, consList, roundNumber

    #BUY A VOWEL
    def buyVowel(roundCash, phraseHid, usedVows, vowsList, roundNumber):
        #get vowel choice
        vowsChoice = input('Pick a vowel: ')
        
        #check for correct input
        allConsonants = ['B','b','C','c','D','d','F','f','G','g','H','h','J','j','K','k',
                         'L','l','M','m','N','n','P','p','Q','q','R','r','S','s','T','t',
                         'V','v','W','w','X','x','Y','y','Z','z']
        while vowsChoice in allConsonants:
            print('Consonants cannot be purchased.')
            vowsChoice = input('Pick a vowel: ')

        while len(vowsChoice) != 1:
            print('Please enter exactly one character.')
            vowsChoice = input('Pick a vowel: ')

        while vowsChoice in usedVows == True:
            print(str('The letter ')+str(vowsChoice).capitalize()
                  +str(' has already been purchased.'))
            vowsChoice = input('Pick a vowel: ')
        
        #check for occurances of consonant
        phraseHidNew = phraseHid
        
        # counter variable to count number of vowel matches in phrase
        consMatches = 0
        for i in range(len(phrase)):
            if (vowsChoice == phrase[i]) or (vowsChoice.capitalize() == phrase[i]): 
                consMatches += 1
                phraseHidNew = str(phraseHidNew[: i]  + vowsChoice.capitalize() +
                                   phraseHidNew[i + 1 :])
        #if no occurances, print message
        if phraseHidNew == phraseHid:
            print(str("I'm sorry, there are no ")+str(vowsChoice).capitalize()
                      +str("'s."), sep='')
            print(' ')
            return roundCash, phraseHidNew, usedVows, vowsList, roundNumber
        else:
            print('There are ' + str(consMatches) + ' ' + str(vowsChoice) + "'s")
            roundCash[roundNumber] += int(-250)
            # append vowel to list of used vowels
            usedVows.append(vowsChoice)
            # remove used vowel from available vowels string
            for i in range(len(vowsList)):
                if (vowsChoice == vowsList[i]) or (vowsChoice.capitalize() == vowsList[i]): 
                    vowsList = str(vowsList[: i]  + ' ' +
                                   vowsList[i + 1 :])
            return roundCash, phraseHidNew, usedVows, vowsList, roundNumber

    # SOLVE THE PUZZLE
    def SolvePuzzle(roundCash, phraseHid, usedVows, vowsList, roundNumber):
        #get solution input
        playerSolution = str(input('Enter solution: '))

        #if solution is correct, display message and add reward to round cash
        if playerSolution.capitalize() == phrase.capitalize():
            print('\nYou solved the puzzle! Heres $1000')
            roundCash[roundNumber] += 1000
            roundNumber += 1
            return roundCash, phraseHid, usedVows, vowsList, roundNumber
        else:
            print('\nIncorrect! I award you no points')
            roundNumber += 1
            return roundCash, phraseHid, usedVows, vowsList, roundNumber
        
        
        
    #TURN
    def getTurn1(roundCash,phraseHid,consList,vowsList,usedCons,usedVows,roundNumber):
        #print display
        print(':::::::::::::::::::::::::::::::::::::::::: ROUND ',roundNumber+1,' of 4 ::')
        cent = int((56-len(phrase))/2-1)
        print(str('::')+str(' ')*cent+phraseHid+str(' ')*cent+str('::'))
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
        print(str('::  ')+consList+str('   ::   ')+vowsList
              +str('   ::          $')+str(roundCash[roundNumber])+str(' ::'))
        print('::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n')


        #get turn selection
        print('What would you like to do?')
        print('  1 - Spin the wheel')
        print('  2 - Buy a vowel')
        print('  3 - Solve the puzzle')
        print('  4 - Quit the game\n')
        sel = input('Enter the number of your choice: ')

        # validate selection input
        while (sel in ['1','2','3','4']) == 0:
            print('Please select a number 1-4')
            sel = input('Enter the number of your choice: ')

        if sel == str(1):
            roundCash, phraseHid, usedCons, consList, roundNumber = spin(roundCash, phraseHid, usedCons, consList, roundNumber)
            return roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber
        elif sel == str(2):
            #check if they have enough money to but a vowel
            if roundCash[roundNumber] < 250:
                print("You don't have enough money to buy a vowel. Please select something else. \n")
                return roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber
            else:
                roundCash, phraseHid, usedVows, vowsList, roundNumber = buyVowel(roundCash, phraseHid, usedVows, vowsList, roundNumber)
                return roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber
        elif sel == str(3):
            roundCash, phraseHid, usedCons, consList, roundNumber = SolvePuzzle(roundCash, phraseHid, usedCons, consList, roundNumber)
            return roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber
        elif sel == str(4):
            roundNumber = 5
            return roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber

    
    # player makes turn selections until puzzle is solved either correctly or incorrectly, at which point
    # the round number is increased by 1
    
    while roundNumber == 0:
        roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber = getTurn1(roundCash,phraseHid,consList,vowsList,usedCons,usedVows,roundNumber)
    print('\nYour cash for the round is: $',roundCash[roundNumber-1])
    print('Your total cash is: $',sum(roundCash),'\n')

    # reset consonants and vowels list
    consList = str('BCDFGHJKLMNPQRSTVWXYZ')
    vowsList = str('AEIOU')
    
    # reset list of used letters
    usedCons = []
    usedVows = []

    # get random phrase 2
    phrase = r.choice(phrases)

    #get hidden phrase
    phraseHid = str('')
    for i in range(len(phrase)):
        if phrase[i] == str(' '):
            phraseHid += str(' ')
        elif phrase[i] == str("'"):
            phraseHid += str("'")
        elif phrase[i] == str('-'):
            phraseHid += str('-')
        elif phrase[i] == str('&'):
            phraseHid += str('&')
        else:
            phraseHid += str('_')

    while roundNumber == 1:
        roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber = getTurn1(roundCash,phraseHid,consList,vowsList,usedCons,usedVows,roundNumber)
    print('\nYour cash for the round is: $',roundCash[roundNumber-1])
    print('Your total cash is: $',sum(roundCash),'\n')

    # reset consonants and vowels list
    consList = str('BCDFGHJKLMNPQRSTVWXYZ')
    vowsList = str('AEIOU')
    
    # reset list of used letters
    usedCons = []
    usedVows = []

    # get random phrase 2
    phrase = r.choice(phrases)

    #get hidden phrase
    phraseHid = str('')
    for i in range(len(phrase)):
        if phrase[i] == str(' '):
            phraseHid += str(' ')
        elif phrase[i] == str("'"):
            phraseHid += str("'")
        elif phrase[i] == str('-'):
            phraseHid += str('-')
        elif phrase[i] == str('&'):
            phraseHid += str('&')
        else:
            phraseHid += str('_')

    while roundNumber == 2:
        roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber = getTurn1(roundCash,phraseHid,consList,vowsList,usedCons,usedVows,roundNumber)
    print('\nYour cash for the round is: $',roundCash[roundNumber-1])
    print('Your total cash is: $',sum(roundCash),'\n')

    # reset consonants and vowels list
    consList = str('BCDFGHJKLMNPQRSTVWXYZ')
    vowsList = str('AEIOU')
    
    # reset list of used letters
    usedCons = []
    usedVows = []

    # get random phrase 2
    phrase = r.choice(phrases)

    #get hidden phrase
    phraseHid = str('')
    for i in range(len(phrase)):
        if phrase[i] == str(' '):
            phraseHid += str(' ')
        elif phrase[i] == str("'"):
            phraseHid += str("'")
        elif phrase[i] == str('-'):
            phraseHid += str('-')
        elif phrase[i] == str('&'):
            phraseHid += str('&')
        else:
            phraseHid += str('_')

    while roundNumber == 3:
        roundCash, phraseHid, usedCons, consList, usedVows, vowsList, roundNumber = getTurn1(roundCash,phraseHid,consList,vowsList,usedCons,usedVows,roundNumber)
    print('\nYour cash for the round is: $',roundCash[roundNumber-1])
    print('Your total cash is: $',sum(roundCash),'\n')
    print('You won $', sum(roundCash),'!')
    print('Thanks for playing!\n')
    highScore1 = 5100
    highScore2 = 2000
    highScore3 = 1000
    highScore1User = 'Ryan'
    highScore2User = 'Ryan'
    highScore3User = 'Ryan'

    # if new score is higher than any top scores update scoreboard
    if sum(roundCash) > highScore1:
        highScore3 = highScore2
        highScore2 = highScore1
        highScore1 = sum(roundCash)
        highScore1User = input('New High Score! Please enter your name: ')
    elif sum(roundCash) > highScore2:
        highScore3 = highScore2
        highScore2 = sum(roundCash)
        highScore2User = input('New High Score! Please enter your name: ')
    elif sum(roundCash) > highScore3:
        highScore3 = sum(roundCash)
        highScore3User = input('New High Score! Please enter your name: ')
    print('::       HIGH SCORES       ::')
    print('::                         ::')
    print(':::::::::::::::::::::::::::::')
    print('::                         ::')
    print('::  1. ',highScore1User,': $',highScore1,'::')
    print('::  2. ',highScore2User,': $',highScore2,'::')
    print('::  3. ',highScore3User,': $',highScore3,'::')
    print('::                         ::')
    print(':::::::::::::::::::::::::::::')




 
    
        
            
            
    
