from wordle_engine import WordleEngine


def main():
    game = WordleEngine("wordlist.txt", debug_mode=True)
    game.start()


if __name__ == '__main__':
    main()
