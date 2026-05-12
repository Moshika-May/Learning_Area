import random

WORD_BANK = {
    "animals": ["tiger", "rabbit", "panda", "monkey"],
    "fruit": ["banana", "orange", "mango", "papaya"],
    "country": ["thailand", "japan", "brazil", "canada"],
}

MAX_WRONG = 6


def normalize_text(text):
    """Return trimmed lowercase text.

    >>> normalize_text("  Panda  ")
    'panda'
    >>> normalize_text(" FRUIT")
    'fruit'
    """
    return text.strip().lower()


def get_words_in_category(word_bank, category):
    """Return a copy of the words in the chosen category.

    >>> get_words_in_category(WORD_BANK, " fruit ")
    ['banana', 'orange', 'mango', 'papaya']
    >>> get_words_in_category(WORD_BANK, "sports")
    []
    """
    category_formal = category.strip().lower()
    empty_list = []

    if category_formal in word_bank:
        return word_bank[category_formal]
    
    else:
        return empty_list


def build_hidden_word(secret_word):
    """Build the starting hidden word list.

    >>> build_hidden_word("tiger")
    ['_', '_', '_', '_', '_']
    """
    secret_word_list_under = []
    secret_word_list = []
    for _ in secret_word:
        secret_word_list_under.append('_')
        secret_word_list.append(_)

    return secret_word_list_under


def reveal_letter(secret_word, hidden_word, guess):
    """Reveal matching letters and return the updated list with a count.

    >>> reveal_letter("banana", ["_", "_", "_", "_", "_", "_"], "a")
    (['_', 'a', '_', 'a', '_', 'a'], 3)
    >>> reveal_letter("banana", ["b", "_", "_", "_", "_", "_"], "x")
    (['b', '_', '_', '_', '_', '_'], 0)
    """

    new_hidden_word = []
    secret_word_list = []
    for word in secret_word_list:
        secret_word_list.append(word)
    new_hidden_word_list = []
    n = 0
    count = 0

    if guess in secret_word:
        # for word in secret_word:
        #     if guess == word:
        #         new_hidden_word_list.append(word)

        for sec_word in hidden_word:
            if sec_word != "_":
                new_hidden_word.append(sec_word)
                count += 1

        for word in secret_word:

            if guess == word:
                new_hidden_word.append(word)

            if guess != word:
                new_hidden_word.append("_")
            
            if count != 0:
                for _ in range(count):
                    if "_" in new_hidden_word:
                        new_hidden_word.remove("_")
                        count -= 1

        new_hidden_word_list.append(new_hidden_word)
        for guess_word in new_hidden_word:
            if guess_word == guess:
                n += 1

    else:
        new_hidden_word_list.append(hidden_word)
    new_hidden_word_list.append(n)
    new_hidden_word_tuple = tuple(new_hidden_word_list)

    return new_hidden_word_tuple


def format_hidden_word(hidden_word):
    """Format the hidden word for display.

    >>> format_hidden_word(["b", "_", "n", "_", "n", "_"])
    'b _ n _ n _'
    """
    return " ".join(hidden_word)


def build_letter_frequency(secret_word):
    """Count each letter in the secret word.

    >>> build_letter_frequency("banana")
    {'b': 1, 'a': 3, 'n': 2}
    """

    frequency = {}
    for char in secret_word:

        if char == ' ':
            continue

        if char in frequency:
            frequency[char] += 1

        else:
            frequency[char] = 1
            
    return frequency


def choose_hint(letter_frequency, used_letters):
    """Choose the best unused hint letter.

    >>> choose_hint({"b": 1, "a": 3, "n": 2}, ["b", "n"])
    'a'
    >>> choose_hint({"b": 1}, ["b"])
    ''
    """
    hint_letter = ""
    highest_frequency = -1

    for letter, freq in letter_frequency.items():
        if letter not in used_letters:
            if freq > highest_frequency:
                highest_frequency = freq
                hint_letter = letter
    
    return hint_letter


def is_game_won(hidden_word):
    """Return whether the player has revealed all letters.

    >>> is_game_won(["b", "a", "n", "a", "n", "a"])
    True
    >>> is_game_won(["b", "_", "n", "_", "n", "_"])
    False
    """

    return "_" not in hidden_word


def create_game_state(secret_word, max_wrong):
    """Create the dictionary that stores the game state.

    >>> create_game_state("banana", 6)
    {'hidden_word': ['_', '_', '_', '_', '_', '_'], 'used_letters': [], 'remaining_attempts': 6, 'letter_frequency': {'b': 1, 'a': 3, 'n': 2}, 'consecutive_wrong_guesses': 0, 'show_hint': False, 'guess': ''}
    """
    game_state = {'hidden_word': build_hidden_word(secret_word), 
                  'used_letters': [], 
                  'remaining_attempts': max_wrong, 
                  'letter_frequency': build_letter_frequency(secret_word),
                  'consecutive_wrong_guesses': 0,
                  'show_hint': False,
                  'guess': ''}
    return game_state


def should_continue_game(game_state):
    """Return whether the main game loop should continue.

    >>> should_continue_game(create_game_state("banana", 6))
    True
    >>> should_continue_game({"hidden_word": ["b", "a"], "remaining_attempts": 3})
    False
    >>> should_continue_game({"hidden_word": ["_", "_"], "remaining_attempts": 0})
    False
    """
    a_key = False
    b_key = False

    for key_dict, value_dict in game_state.items():
        if key_dict == "remaining_attempts":
            if value_dict > 0:
                b_key = True
            if value_dict == 0:
                return False
        if key_dict == "hidden_word":
            if "_" not in value_dict:
                a_key = True
        if a_key == True and b_key == True:
            return False
    return True


def display_game_state(game_state):
    """Display the current game state.

    >>> import io
    >>> from contextlib import redirect_stdout
    >>> state = create_game_state("banana", 6)
    >>> state["used_letters"] = ["x", "y"]
    >>> state["show_hint"] = True
    >>> with redirect_stdout(io.StringIO()) as buffer:
    ...     display_game_state(state)
    >>> print(buffer.getvalue(), end="")
    <BLANKLINE>
    Word: _ _ _ _ _ _
    Used letters: x, y
    Hint: a
    Remaining wrong attempts: 6
    >>> state["show_hint"]
    False
    """
    print()

    hidden_word_str = format_hidden_word(game_state["hidden_word"])
    print(f"Word: {hidden_word_str}")

    if game_state["used_letters"]:
        used_letters_str = ", ".join(game_state["used_letters"])
        print(f"Used letters: {used_letters_str}")
    else:
        print("Used letters: none")

    if game_state["show_hint"]:
        hint = choose_hint(game_state["letter_frequency"], game_state["used_letters"])
        print(f"Hint: {hint}")
        game_state["show_hint"] = False

    print(f"Remaining wrong attempts: {game_state['remaining_attempts']}")


def should_retry_guess(game_state):
    """Read and validate a guess, returning True when input must be retried.

    >>> from unittest.mock import patch
    >>> import io
    >>> from contextlib import redirect_stdout
    >>> state = create_game_state("banana", 6)
    >>> with patch("builtins.input", return_value="ab"):
    ...     with redirect_stdout(io.StringIO()) as buffer:
    ...         retry = should_retry_guess(state)
    >>> retry
    True
    >>> print(buffer.getvalue(), end="")
    Please enter exactly 1 letter.
    >>> with patch("builtins.input", return_value=" a "):
    ...     retry = should_retry_guess(state)
    >>> retry
    False
    >>> state["guess"]
    'a'
    """

    text = input("Guess a letter: ")
    norm_text = normalize_text(text)
    english = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    if len(norm_text) != 1:
        print('Please enter exactly 1 letter.')
        return True
    if norm_text not in english:
        print('Please enter an English letter only.')
        return True
    if norm_text in game_state["used_letters"]:
        print('You already guessed that letter.')
        return True
    else:
        game_state['guess'] = norm_text
        return False


def apply_guess(secret_word, game_state, guess):
    """Apply a valid guess and return the number of revealed letters.

    >>> state = create_game_state("banana", 6)
    >>> apply_guess("banana", state, "a")
    3
    >>> state["hidden_word"]
    ['_', 'a', '_', 'a', '_', 'a']
    >>> state["used_letters"]
    ['a']
    """
    game_state['used_letters'].append(guess)
    new_hidden, count = game_state['hidden_word'] = reveal_letter(secret_word, game_state['hidden_word'], guess)
    game_state['hidden_word'] = new_hidden

    return count


def display_guess_result(game_state, count):
    """Display guess feedback and update counters.

    >>> import io
    >>> from contextlib import redirect_stdout
    >>> state = create_game_state("banana", 6)
    >>> with redirect_stdout(io.StringIO()) as buffer:
    ...     display_guess_result(state, 0)
    >>> print(buffer.getvalue(), end="")
    Incorrect!
    >>> state["remaining_attempts"], state["consecutive_wrong_guesses"], state["show_hint"]
    (5, 1, False)
    >>> with redirect_stdout(io.StringIO()) as buffer:
    ...     display_guess_result(state, 0)
    >>> state["remaining_attempts"], state["consecutive_wrong_guesses"], state["show_hint"]
    (4, 2, True)
    >>> with redirect_stdout(io.StringIO()) as buffer:
    ...     display_guess_result(state, 1)
    >>> print(buffer.getvalue(), end="")
    Correct!
    >>> state["consecutive_wrong_guesses"], state["show_hint"]
    (0, False)
    """
    if count > 0:
        print('Correct!')
        game_state['consecutive_wrong_guesses'] = 0
        game_state['show_hint'] = False

    if count == 0:
        print('Incorrect!')
        game_state['remaining_attempts'] -= 1
        game_state['consecutive_wrong_guesses'] += 1
        
    if game_state['consecutive_wrong_guesses'] == 2:
        game_state['show_hint'] = True


def play_game(secret_word, max_wrong):
    """Play one game and return the final result dictionary.

    >>> from unittest.mock import patch
    >>> import io
    >>> from contextlib import redirect_stdout
    >>> with patch("builtins.input", side_effect=["x", "y", "a", "n", "b"]):
    ...     with redirect_stdout(io.StringIO()) as buffer:
    ...         result = play_game("banana", 6)
    >>> result
    {'won': True, 'secret_word': 'banana', 'remaining_attempts': 4, 'used_letters': ['x', 'y', 'a', 'n', 'b']}
    >>> "Hint: a" in buffer.getvalue()
    True
    """
    game_state = create_game_state(secret_word, max_wrong)
    
    while should_continue_game(game_state):
        display_game_state(game_state)
        while should_retry_guess(game_state):
            pass
        guess = game_state['guess']
        count = apply_guess(secret_word, game_state, guess)
        display_guess_result(game_state, count)

    won = is_game_won(game_state['hidden_word'])

    result = {'won': won, 
            'secret_word': secret_word, 
            'remaining_attempts': game_state['remaining_attempts'],
            'used_letters': game_state['used_letters']}
    
    return result


def choose_secret_word(word_bank):
    """Ask the user for a category and return one secret word.

    >>> from unittest.mock import patch
    >>> import io
    >>> from contextlib import redirect_stdout
    >>> with patch("builtins.input", return_value="fruit"), patch("random.choice", lambda words: words[0]):
    ...     with redirect_stdout(io.StringIO()) as buffer:
    ...         secret_word = choose_secret_word(WORD_BANK)
    >>> secret_word
    'banana'
    >>> "Available categories:" in buffer.getvalue()
    True
    >>> with patch("builtins.input", return_value="sports"):
    ...     with redirect_stdout(io.StringIO()) as buffer:
    ...         secret_word = choose_secret_word(WORD_BANK)
    >>> secret_word
    ''
    >>> print(buffer.getvalue(), end="")
    Available categories: animals, fruit, country
    Invalid category.
    """
    word_bank = WORD_BANK
    word_in_word_bank = []

    print('Available categories: ', sep="", end="")
    for word in word_bank.keys():
        word_in_word_bank.append(word)
    print(", ".join(word_in_word_bank))
    
    category = input('Choose a category: ')
    if category not in word_bank.keys():
        print('Invalid category.')
        return ""
    
    return random.choice(get_words_in_category(word_bank, category))

    
def display_game_result(result):
    """Display the final result summary.

    >>> import io
    >>> from contextlib import redirect_stdout
    >>> result = {"won": False, "secret_word": "banana", "remaining_attempts": 0, "used_letters": ["x", "y", "a"]}
    >>> with redirect_stdout(io.StringIO()) as buffer:
    ...     display_game_result(result)
    >>> print(buffer.getvalue(), end="")
    <BLANKLINE>
    You lost!
    The secret word was: banana
    Used letters: x, y, a
    """
    print()
    
    if result['won']:
        print('You won!')
    else:
        print('You lost!')
    print(f'The secret word was: {result['secret_word']}')
    print(f'Used letters: {", ".join(result['used_letters'])}')


def main():
    """Run the full program.

    >>> from unittest.mock import patch
    >>> import io
    >>> from contextlib import redirect_stdout
    >>> with patch("builtins.input", side_effect=["fruit", "x", "y", "a", "n", "b"]), patch("random.choice", lambda words: words[0]):
    ...     with redirect_stdout(io.StringIO()) as buffer:
    ...         main()
    >>> "You won!" in buffer.getvalue()
    True
    """
    secret_word = choose_secret_word(WORD_BANK)
    if secret_word == "":
        return None
    display_game_result(play_game(secret_word, MAX_WRONG))
    

if __name__ == "__main__":
    main()
    import doctest
    doctest.run_docstring_examples(normalize_text, globals())