import pathlib
import random
from colorama import init, Fore, Back, Style
init(autoreset=True)

def display_the_word(word , guessed_letters):
    for letter in word:
        if letter in guessed_letters:
            print(Fore.YELLOW + letter , end=" ")
        else:
            print(Fore.GREEN + "_" , end=" ")
    print()

def is_corect_letter(letter , guessed_letters):
    if not letter.isalpha() and letter != " ":
        print("Enter only a letter!!")
        return False
    elif len(letter) != 1:
        print("Enter one letter!!")
        return False
    elif letter in guessed_letters:
        print("This letter is guessed!!")
        return False
    else:
        return True

def guess_a_letter(player , guessed_letters , players):
    letter = input(f"{players[player]} enter a letter :")
    while(not is_corect_letter(letter , guessed_letters)):
        letter = input(f"{players[player]} try agian :")
    return letter

def if_finish_to_guess(guessed_letters, word):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True

def display_points(word , players , points):
    for i in range(len(players)):
        print(Fore.BLUE + f'{players[i]} :' , end="")
        print(Fore.GREEN +  f' {points[i]}')


def word_from_txt(path_to_file_of_words:pathlib.Path):
    split_words = (path_to_file_of_words.read_text()).splitlines()
    return split_words[random.randint(0,len(split_words) - 1)]
