from wikiquote import random_titles

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

def get_hangman_store():
    global HANGMANDRAWINGS
    return HANGMANDRAWINGS

def get_display_word(word, idxs):
    """Get the word suitable for display."""
    if len(word) != len(idxs):
        raise ValueError('Word length and indices length are not the same')
    displayed_word = ''.join(
        [letter if idxs[i] else '*' for i, letter in enumerate(word)])
    return displayed_word.strip().lower()


def get_next_letter(remaining_letters):
    """Get the user-inputted next letter."""
    if len(remaining_letters) == 0:
        raise ValueError('There are no remaining letters')
    while True:
        next_letter = input('Choose the next letter: ').lower()
        if len(next_letter) != 1:
            print('{0} is not a single character'.format(next_letter))
        elif next_letter not in ascii_lowercase:
            print('{0} is not a letter'.format(next_letter))
        elif next_letter not in remaining_letters:
            print('{0} has been guessed before'.format(next_letter))
        else:
            remaining_letters.remove(next_letter)
            return next_letter


def play_hangman():
    """Play a game of hangman.
    At the end of the game, returns if the player wants to retry.
    """
    # Let player specify difficulty
    print('Starting a game of Hangman...')
    attempts_remaining = 8
    hangman_stat = 0

    # Randomly select a word
    print('Selecting a word...')
    word = random_titles(max_titles=1)
    string = word[0]
    print()

    # Initialize game state variables
    idxs = [letter not in ascii_lowercase for letter in string]
    remaining_letters = set(ascii_lowercase)
    wrong_letters = []
    hangman = get_hangman_store()
    word_solved = False

    # Main game loop
    while attempts_remaining > 0 and not word_solved:
        # Print current game state
        print('Word: {0}'.format(get_display_word(string, idxs)))
        print('Attempts Remaining: {0}'.format(attempts_remaining))
        print('Previous Guesses: {0}'.format(' '.join(wrong_letters)))

        # Get player's next letter guess
        next_letter = get_next_letter(remaining_letters)

        # Check if letter guess is in word
        if next_letter in string:
            # Guessed correctly
            print('{0} is in the word!'.format(next_letter))

            # Reveal matching letters
            for i in range(len(string)):
                if string[i] == next_letter:
                    idxs[i] = True
        else:
            # Guessed incorrectly
            print('{0} is NOT in the word!'.format(next_letter))
            if hangman_stat != 8:
                print(hangman[hangman_stat])
            hangman_stat += 1
            # Decrement num of attempts left and append guess to wrong guesses
            attempts_remaining -= 1
            wrong_letters.append(next_letter)

        # Check if word is completely solved
        if False not in idxs:
            word_solved = True
        print()

    # The game is over: reveal the word
    print('The word is {0}'.format(string))

    # Notify player of victory or defeat
    if word_solved:
        print('Congratulations! You won!')
    else:
        print('Try again next time!')

    # Ask player if he/she wants to try again
    try_again = input('Would you like to try again? [y/n] ')
    return try_again.lower() == 'y'


if __name__ == '__main__':
    while play_hangman():
        print()