from wikiquote import random_titles
from error import InputError, AccessError, NameException, KeyError
from string import ascii_lowercase

HANGMANDRAWINGS = [
    '''
   +---+
       |
       |
       |
       |
       |
=========''',
    '''
   +---+
   |   |
       |
       |
       |
       |
=========''',
    '''
   +---+
   |   |
   O   |
       |
       |
       |
 =========''',
    '''
   +---+
   |   |
   O   |
   |   |
       |
       |
 =========''',
    '''
   +---+
   |   |
   O   |
  /|   |
       |   
       |
 =========''',
    '''
   +---+
   |   |
   O   |
  /|\  |
       |
       |
 =========''',
    '''
   +---+
   |   |
   O   |
  /|\  |
  /    |
       |
 =========''',
    '''
   +---+
   |   |
   O   |
  /|\  |
  / \  |
       |
 =========''']
 
 
WORD = ""

CURRENTSTATUS = {
   "hang_man_drawing": "",
   "wrong_word":[],
   'current_word':"",
   
}

BATSTORE = set(ascii_lowercase)
def get_hangman_store():
    global HANGMANDRAWINGS
    return HANGMANDRAWINGS

def get_current_status():
    global CURRENTSTATUS
    return CURRENTSTATUS

def get_bat_store():
    global BATSTORE
    return BATSTORE

def get_correct_word():
    global WORD
    return WORD

def make_idxs(guess,word, idxs ):
    if len(word) != len(idxs):
        raise ValueError('Word length and indices length are not the same')

    ret = ""
    i = 0
    score = False
    for letter in word:
        if word[i].lower() == guess.lower():
            score = True
        print (word[i], guess)
        if idxs[i] == True or word[i].lower() == guess.lower():
            print('Enters if statement')
            ret = ret + word[i]
            idxs[i] = True
        else:
            ret = ret + '*'
        i = i + 1
    return idxs,score


def get_display_word(word, idxs):
    """Get the word suitable for display."""
    if len(word) != len(idxs):
        raise ValueError('Word length and indices length are not the same')
    displayed_word = ''.join(
        [letter if idxs[i] else '*' for i, letter in enumerate(word)])
    return displayed_word.strip().lower()


def get_next_letter(remaining_letters, guess):
    """Get the user-inputted next letter."""
    #if len(remaining_letters) == 0:
        #raise ValueError('There are no remaining letters')
    #while True:
    next_letter = guess.lower()
    if len(next_letter) != 1:
        raise ValueError('Input is not a single character')
    elif next_letter not in ascii_lowercase:
        raise ValueError('Input is not a letter')
    elif next_letter in remaining_letters:
        raise ValueError('This has been guessed before')
    else:
        #remaining_letters.remove(next_letter)
        return next_letter


def play_hangman(guess):
    """Play a game of hangman.
    At the end of the game, returns if the player wants to retry.
    """
    # Let player specify difficulty
    print('Starting a game of Hangman...')
    status = get_current_status()
    correct_ans = get_current_status()['current_word']
    # Randomly select a word
    print('Selecting a word...')
    if status['current_word'] == "":
        print('enters if') 
        word = random_titles(max_titles=1)
        string = word[0]
        status['current_word'] = string
        correct_ans = string
        idxs = [False]*len(string)
        status['idxs'] = idxs
        status['wrong_word'] = []
        status['final'] = ""
    else:
        string = correct_ans
        idxs = status['idxs']
    print('string',string)
    print('status',get_current_status())
    # Initialize game state variables
    idxs,score = make_idxs(guess,status['current_word'], idxs )
    status['idxs'] = idxs
    #idxs = [letter not in ascii_lowercase for letter in string]
    remaining_letters = get_bat_store()
    #wrong_letters = get_wrong_word()
    hangman = get_hangman_store()
    print('idxs',idxs)
    print('this is status ------>',status)
    word_solved = False

    # Main game loop
    if len(status['wrong_word']) != 8 and not word_solved:
        # Print current game state
        print('ENTERS IF STATEMENT ')
        current_word = get_display_word(string, idxs)
        status['print_word'] = current_word
        print('Previous Guesses: {0}'.format(' '.join(status['wrong_word'])))

        # Get player's next letter guess
        next_letter = get_next_letter(status['wrong_word'], guess)

        # Check if letter guess is in word
        #if next_letter in string:
        
            # Guessed correctly
            #print('{0} is in the word!'.format(next_letter))

            # Reveal matching letters
            #for i in range(len(string)):
                #if string[i] == next_letter:
                    #idxs[i] = True
        if score == False:
            # Guessed incorrectly
            #print('{0} is NOT in the word!'.format(next_letter))
            status['hang_man_drawing'] = hangman[len(status['wrong_word'])]
            # Decrement num of attempts left and append guess to wrong guesses
            status['wrong_word'].append(next_letter)

        # Check if word is completely solved
    if False not in idxs:
        #word_solved = True
        status['final'] ='\n' + 'Congratulations! You won!' 
        status['current_word'] = ""
        return status 
    print()

    if len(status['wrong_word']) == 8:
        status['final'] ='\n' + 'Try again next time!'
        status['current_word'] = ""
        return status 
    # The game is over: reveal the word
    #if not word_solved:
    print(status)
    return status

    # Notify player of victory or defeat
    if word_solved:
        print('The word is {0}'.format(string))
        print('Congratulations! You won!')
    else:
        print('The word is {0}'.format(string))
        print('Try again next time!')

    return status
    # Ask player if he/she wants to try again
    #try_again = input('Would you like to try again? [y/n] ')
    #return try_again.lower() == 'y'



