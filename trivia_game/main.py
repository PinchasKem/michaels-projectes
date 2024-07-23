import json
import random
import pathlib
from argparse import ArgumentParser


def arguments_from_the_cli():
    parser = ArgumentParser(description="Trivia game")
    parser.add_argument("qusetions_path" , help="The path to a file of qusetions" , type=pathlib.Path)
    parser.add_argument("players_names", help="The names of the players", nargs="+")
    args = parser.parse_args()
   
    assert args.qusetions_path.is_file()
    
    return args.qusetions_path , args.players_names


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def set_players(players_names):
    players = []
    for i in range(len(players_names)):
        players.append({"name": players_names[i], "score": 0})
    return players


def set_categories(data):
    view_the_categories(data)
    while True:
        user_input = input(f"Choose categories (comma-separated numbers, or press Enter for all): ")
        categories = parse_categories(user_input)
        if is_valid_categories(categories):
            return categories
        print("Invalid selection. Try again.")


def view_the_categories(data):
    print("Select one or more categories")
    for i in range(3):
        print(f"{i+1} : {data['categories'][i]["name"]} : ")


def parse_categories(input_string):
    if not input_string.strip():
        return [1, 2, 3]  
    try:
        categories = [int(num.strip()) for num in input_string.split(',')]
        return categories
    except ValueError:
        return None  
    

def is_valid_categories(categories):
    if categories is None or len(set(categories)) != len(categories):
        return False
    for cat in categories:
        if not (1 <= cat <= 3):
            return False
    return True


def set_levels():
    while True:
        user_input = input(f"Choose levels between 1-4 (comma-separated numbers, or press Enter for all): ")
        levels = parse_levels(user_input)
        if is_valid_levels(levels):
            return levels
        print("Invalid selection. Try again.")


def parse_levels(input_string):
    if not input_string.strip():
        return [1, 2, 3 ,4]  
    try:
        levels = [int(num.strip()) for num in input_string.split(',')]
        return levels
    except ValueError:
        return None  


def is_valid_levels(levels):
    if levels is None or len(set(levels)) != len(levels):
        return False
    for cat in levels:
        if not (1 <= cat <= 4):
            return False
    return True


def set_num_questions(data , categories , levels):
    max_questions = count_questions(data ,  categories , levels)
    while True:
        num_questions=int(input(f"According to the choice of category and level, the maximum number of questions is {max_questions} \nEnter the number of questions: "))
        if(num_questions < 1):
            print("Invalid selection!!")
        elif(num_questions <= max_questions):
            return num_questions


def count_questions(data, categories, levels):
    total_questions = 0
    for category_index in categories:
        category = data['categories'][category_index - 1]
        for level_index in levels:
            total_questions += len(category["difficulty_levels"][level_index - 1]['questions'])######
    return total_questions


def select_question(used_questions , categories , levels , data):
    while True:       
        question = select_question_from_data(categories , levels , data)
        if not question in used_questions:
            return question
        

def select_question_from_data(categories , levels , data):
    categorie = data["categories"][categories[random.randint(0 , len(categories)-1 ) ] -1]
    level = categorie["difficulty_levels"][levels[random.randint(0 , len(levels) -1) ] -1]
    return level["questions"][random.randint(0, len(level["questions"])-1)]


def view_question_and_get_answer(player, question):
    print(f"{player} Choose the meaning of the word: {question["word"]}")
    options = question["options"].copy()
    random.shuffle(options)
    for i in range(len(options)):
        print(f"{i+1} : {options[i][::-1]}")
    return options[answer()]

   
def answer():
    while True:
        try:
            answer = int(input("Please select a number: "))
            if(answer>4 or answer<1):
                print("Invalid selection!!")
            else:
                return answer-1
        except ValueError:
            print("Invalid selection!!")



def main(num_questions , players ,categories , levels , data):
    used_questions = []
    loop_number = num_questions
    turn = 0
    while(loop_number > 0):
        current_player = turn%len(players)
        question = select_question(used_questions , categories , levels , data)
        answer = view_question_and_get_answer(players[current_player]["name"], question)
        while(answer != question["options"][question["correct_answer"]]):
            print("The answer is not correct!")
            turn += 1
            current_player = turn%len(players)
            answer = view_question_and_get_answer(players[current_player]["name"], question)
        print("Correct answer!")
        players[current_player]["score"] += 1
        used_questions.append(question)
        loop_number -= 1
        turn += 1


def results(players):
    print("The results of the players:")
    for i in range(len(players)):
        print(f"{players[i]["name"]} : {players[i]["score"]}")
        

if __name__=="__main__":
    
    args = arguments_from_the_cli()

    data = load_data(args[0])

    players = set_players(args[1])

    categories = set_categories(data)
    
    levels = set_levels()

    num_questions = set_num_questions(data , categories , levels)

    main(num_questions , players ,categories , levels , data)

    results(players)


 