import pathlib
import random
from colorama import init, Fore, Back, Style
init(autoreset=True)
from argparse import ArgumentParser
from functions_guess_the_word import if_finish_to_guess , display_the_word , guess_a_letter , display_points , word_from_txt


def main_guess_the_word(path_to_file_of_words:pathlib.Path ,  number_of_words:int ,players:list):
    player = 0
    list_points = [0] * len(players)
    words_used=[]
    while(number_of_words > 0):        
        word = word_from_txt(path_to_file_of_words)
        while(word in words_used):
            word = word_from_txt(path_to_file_of_words)
        words_used.append(word)
        guessed_letters = []
        while(not if_finish_to_guess(guessed_letters , word)):
            display_the_word(word , guessed_letters)
            letter = guess_a_letter(player , guessed_letters , players)
            guessed_letters.append(letter)
            if letter in word:
                list_points[player] += 1
            if(player == len(players)-1):
                player = 0
            else:
                player += 1
        print(Fore.CYAN + f'"{word}"')
        print(Fore.YELLOW + "Congratulations! The word is guessed!")
        number_of_words -= 1
    display_points(word , players , list_points)



def arguments_from_the_cli():
    parser = ArgumentParser(description="Guess the word game")
    parser.add_argument("words_path" , help="The path to a file of words" , type=pathlib.Path)
    parser.add_argument("player_name", help="The names of the players", nargs="+")
    parser.add_argument("-l","--words_limit", type=int , help="the number of words to guess",default=None)
    args = parser.parse_args()
   
    assert args.words_path.is_file()
    if args.words_limit is not None:    
        assert args.words_limit > 0 ,"Choose at least 1 !"
    else: args.words_limit=1

    
    return args.words_path , args.words_limit , args.player_name
   
    
if __name__ == "__main__":
    
    print("\n \nWelcome to the game --Guess the word-- !")
    args = arguments_from_the_cli()
    print(args)
    words_path = args[0]
    number_of_words = args[1]
    players_name = args[2]
    main_guess_the_word(words_path , number_of_words , players_name)