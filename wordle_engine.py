import random
from colorama import Fore


class WordleEngine:
    def __init__(self, wordlist_location, debug_mode=False):
        self._debug_mode = debug_mode
        self._user_input = None
        self._wordlist = None
        self._wordlist_location = wordlist_location
        self._winning_word = None

        self._ping_for_input = True
        self._ping_text = "Enter your guess: "

        self._exact_match_color = Fore.GREEN
        self._near_match_color = Fore.YELLOW
        self._no_match_color = Fore.RED

        self._commands = {
            "quit": self.quit,
            "new": self._obtain_new_word
        }

    def start(self):
        if self._debug_mode:
            print(f"{Fore.RED}[DEBUG MODE ENABLED]{Fore.RESET}")

        self._build_word_list()
        self._obtain_new_word()
        self._begin_user_input_loop()

    def quit(self):
        print("Quitting Wordle...")
        self._ping_for_input = False

    def _build_word_list(self):
        with open(self._wordlist_location, "r") as f:
            # Read in all words from wordlist file, ignore empty lines and any upper-case.
            self._wordlist = [line.lower() for line in f.read().splitlines() if line]

    def _obtain_new_word(self):
        self._winning_word = random.choice(self._wordlist)

        if self._debug_mode:
            print(f"{Fore.RED}WINNING WORD: {Fore.LIGHTGREEN_EX}{self._winning_word}{Fore.RESET}\n")

    def _user_issued_command(self):
        command = False

        # Issue a wrap for failed key request from self._commands
        try:
            command = self._commands.get(self._user_input)
            if command:
                command()
        except AttributeError:
            pass

        return command

    def _begin_user_input_loop(self):
        while self._ping_for_input:
            self._user_input = input(self._ping_text).strip().lower()

            # Run command if user input matches
            if self._user_issued_command():
                continue

            # Verification and display
            if self._check_guess():
                print(f"{Fore.GREEN}Good Job! The word was {Fore.CYAN}{self._winning_word}{Fore.RESET}.")
                print(f"{Fore.GREEN}Generating new word...{Fore.RESET}")
                self._obtain_new_word()
            else:
                self._display_result()

    def _check_guess(self):
        guess_result = self._check_correct_position()
        self._check_incorrect_position(guess_result)
        self._guess_result = guess_result
        return self._user_input == self._winning_word

    def _check_correct_position(self):
        guess_result = []
        self._winning_word_list = list(self._winning_word)

        # Only mark exact matches on first pass
        for i, letter in enumerate(self._user_input):
            if letter == self._winning_word[i]:
                guess_result.append(self._colorize_text(letter, self._exact_match_color))
                self._mark_as_used(i)
            else:
                guess_result.append(letter)

        return guess_result

    def _check_incorrect_position(self, guess_result):
        for i, letter in enumerate(self._user_input):
            if guess_result[i] != letter:
                continue

            if letter in self._winning_word_list:
                guess_result[i] = self._colorize_text(letter, self._near_match_color)
                self._winning_word_list[self._winning_word_list.index(letter)] = None
            else:
                guess_result[i] = self._colorize_text(letter, self._no_match_color)

    def _mark_as_used(self, index):
        self._winning_word_list[index] = None

    def _colorize_text(self, text, color):
        return f"{color}{text}{Fore.RESET}"

    def _display_result(self):
        print("".join(self._guess_result))
