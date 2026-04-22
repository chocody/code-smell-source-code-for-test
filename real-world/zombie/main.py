import random
import sys

score = 0

ASCII_ART = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠾⠛⠉⠉⠀⠀⠀⠀⠀⠀⢀⡤⠊⠉⠉⠛⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢮⡀⠀⠀⠀⠀⠀⠀⠙⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⡡⢤⠀⠀⠀⢰⣛⣉⣉⣓⠢⣄⠀⠀⠀⠈⢉⡁⠐⠒⠒⠂⠉⠉⠉⠛⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⠁⣘⡒⠁⢀⠀⠀⠀⣀⣀⣀⣈⣹⣾⣕⠀⢠⡎⠁⡹⠀⣠⠄⠀⠀⠀⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⢀⣎⡩⠃⢠⣏⡴⠞⠛⠉⠉⠀⠀⠀⠀⠹⡏⠀⠉⠉⣠⣾⠖⠋⠉⠻⣅⠀⣠⠖⢲⠌⢻⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⡠⠔⢿⠀⢀⡟⠉⠀⠀⠀⣀⣤⣤⡀⠀⠀⠀⣿⠀⠀⠀⡼⠉⠉⠒⢦⣀⠘⠷⡛⠒⡿⣄⠈⣷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⣠⠏⠀⢸⠀⠀⠀⠀⢰⣿⣿⣿⡇⠀⠀⢀⡿⠀⠀⣸⠃⠀⠀⣀⣄⡙⢷⣄⡇⠘⠀⢸⡆⢹⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣧⠞⠁⠀⠀⢸⡆⠀⠀⠀⠸⣿⣿⡿⠃⠀⢀⣼⠃⠀⠀⣿⣆⠀⠀⣿⣿⡟⠀⠙⣧⠳⡤⠞⠀⢸⡇⠀⠀⠀⠀
⠀⢀⣠⠤⠤⢄⡀⠈⣧⢈⣧⠀⠀⢸⣿⣄⣀⣀⣠⣬⣥⠴⠶⢚⣿⠋⠀⠀⠀⢻⣿⣦⣄⠈⠁⠀⠀⣰⠟⠆⠀⠀⠀⢸⣡⠴⠖⠶⣦
⢠⠏⠀⠀⠀⢀⠈⠓⢿⡄⢳⠀⠀⠀⢳⣌⠻⠯⣤⣀⣀⣀⣴⣿⠏⢀⣶⢰⣦⠈⢿⣿⣿⣷⣀⣠⡼⠋⠀⢀⡀⠀⢀⣿⠥⢄⠀⠀⣿
⣏⠀⠀⠀⡟⢉⡽⣦⡈⢻⣼⠄⠀⠀⠀⠉⠓⠦⠤⠬⣏⣡⠾⠃⢀⣾⣿⢸⣿⣇⠈⠻⡯⠽⢯⡽⠁⠠⣴⠝⠃⢀⣾⢋⣁⠈⢀⡾⠃
⠘⠶⠲⢦⣷⠸⣤⣸⡇⠀⢻⣦⡀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠘⠛⠋⠘⠋⠋⠀⠀⠑⠚⠉⠀⠀⠀⠈⣠⣠⡾⠳⠤⣿⡀⣾⠁⠀
⠀⠀⠀⠀⠸⢧⠉⠉⠀⢀⡾⠀⠉⠻⣦⠀⠀⠀⠈⢟⡽⠄⠀⠀⢀⣀⣤⣤⣤⣄⣀⠀⠀⠀⢀⡀⠀⠀⣴⡿⠛⠻⢶⣤⣿⡿⠋⠀⠀
⠀⠀⠀⠀⠀⠙⠒⠒⠚⠋⠀⠀⠀⠀⠸⣧⠀⠀⠀⠀⠁⠀⣠⣾⡿⢿⠀⠀⢀⣮⣙⡻⣦⡈⠙⠿⠀⣸⠏⠀⠀⠀⠀⢀⣿⣇⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡆⠀⠀⠀⠀⣼⣿⣿⣇⣸⣷⣶⣾⡀⣯⣻⣿⣿⡄⠀⠀⡿⠀⠀⠀⠀⠀⢻⣾⡛⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⡇⠀⠀⠀⠀⠀⠀⠛⠟⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⡀⠀⢸⣿⣿⡟⢻⡿⠿⣇⣿⢸⠿⣿⣿⣿⡏⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠐⡇⠀⠸⣯⠉⠙⠒⣃⣀⣈⣭⣭⣤⣀⣩⡟⠁⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠃⠀⣀⣽⠷⠞⠛⠉⠉⠁⠀⣠⠤⠤⢤⣉⠙⠢⠤⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠘⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⠀⠹⠂⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠶⢦⣤⣀⣀⠀⠀⠀⠀⢀⣈⣛⣥⣤⠴⠾⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

AUTO_ANSWERS = ["1", "2", "2", "1", "1", "2", "2", "3", "1", "3"]

# ---------------------------------------------------------------------------
# Refactor Snapshot (commented as requested)
# - Data-driven questions and result buckets
# - Shared scoring helper
# - Compact loop-based main flow
# ---------------------------------------------------------------------------
# QUESTIONS = [
#     ("question text", "choices text", "best_answer", "second_answer"),
# ]
#
# RESULT_BUCKETS = [
#     (range(0, 6), "result message"),
# ]
#
# def score_for_answer(answer, best_answer, second_answer):
#     if answer == best_answer:
#         return random.randint(10, 20)
#     if answer == second_answer:
#         return random.randint(5, 10)
#     return 3
#
# def print_result(score):
#     for score_range, message in RESULT_BUCKETS:
#         if score in score_range:
#             print(message)
#             return
# ---------------------------------------------------------------------------

QUESTIONS = [
    (
        "Your house is burning down. What do you save?",
        "(1) your dog\n(2) some food cans\n(3) your clothes\n(4) your cell phone",
        "1",
        "2",
    ),
    (
        "It is night, and you will freeze to death soon. Making too much noise/light will attract the zombies. What do you do?",
        "(1) keep moving around\n(2) build a tiny fire\n(3) build a normal fire\n(4) try to wait out the night",
        "2",
        "4",
    ),
    (
        "You are cornered in a grocery store with only a knife. A horde is moving in from all sides. What do you do?",
        "(1) kill zombies to make a path\n(2) try to climb up on the wobbly shelves\n(3) shout for help\n(4) self.kill",
        "2",
        "1",
    ),
    (
        "You see a group of survivors ahead on the road. What do you do?",
        "(1) watch them for a while\n(2) ignore them\n(3) kill them and steal their stuff\n(4) try to greet them",
        "1",
        "3",
    ),
    (
        "A group of about 6 people take your stuff at gunpoint, then tell you to get in a storage container. What do you do?",
        "(1) get in the container\n(2) try to reason with them\n(3) refuse\n(4) try to fight them",
        "1",
        "4",
    ),
    (
        "You and 3 other people are down to 1 last can or food. What do you do?",
        "(1) share it\n(2) eat it\n(3) give it to them\n(4) burn it so there is no argument",
        "2",
        "1",
    ),
    (
        "You are given the choice between 4 weapons. What do you take?",
        "(1) katana\n(2) crossbow\n(3) pistol\n(4) RPG",
        "2",
        "3",
    ),
    (
        "You only have room in your pack for 1 more package of food. What do you take?",
        "(1) trail mix\n(2) crackers\n(3) oreos\n(4) raw chicken",
        "3",
        "4",
    ),
    (
        "You have some choices on where to set up camp.",
        "(1) next to the river\n(2) in the mountains\n(3) near the ocean\n(4) next to the city",
        "1",
        "2",
    ),
    (
        "Your camp, with your group of ~20 people, has been overrun by a horde. What do you do?",
        "(1) follow your friends\n(2) run\n(3) try and save the camp\n(4) get your stuff from your tent",
        "3",
        "4",
    ),
]

RESULT_BUCKETS = [
    (
        range(0, 6),
        "You would be one of the first peopple to die in the apocalypse.\n"
        "You panic at the sight of a zombie and have no survival skills, getting eaten within an hour.\n"
        "Pathetic.",
    ),
    (
        range(6, 20),
        "You would live a few hours in the apocalypse.\n"
        "As the chaos begins, you make a desperate attempt to save your stuff.\n"
        "Getting into the car, you get surrounded.\n"
        "They break open the windows and eat you.\n"
        "That must suck.",
    ),
    (
        range(21, 50),
        "You would live a few days in the apocalypse.\n"
        "As the chaos begins, you attempt to go to the emergency shelters.\n"
        "You die when they get overcrowded and overrun.\n"
        "Too bad.",
    ),
    (
        range(51, 80),
        "You would live a month in the apocalypse.\n"
        "You find a camp and manage to survive for a month, but when the camp gets overrun, you get bit.\n"
        "So close, yet so far.",
    ),
    (
        range(81, 110),
        "You would live a few months in the apocalypse.\n"
        "Your camp moves from place to place before settling at an old school building.\n"
        "After living there for a month, you accidentally shoot yourself with a crossbow while attempting to load it.\n"
        "At least you tried.",
    ),
    (
        range(111, 130),
        "You would live a few years in the apocalypse.\n"
        "Your group settles at a town in Tennessee, fortifying it so that it can withstand a horde.\n"
        "While on a run, you fall through a floor and break your leg, attracting zombies and getting eaten.\n"
        "You will be remembered.",
    ),
    (
        range(131, 1000),
        "You would live for a really long time in the apocalypse.\n"
        "Being the leader of your group, you settle at a town near the beach, where hardly any hordes pass through.\n"
        "You help build a utopia named Z-Land.\n"
        "At the age of 79, you pass away in your sleep.\n"
        "There was a statue of you built.",
    ),
]


def get_answer(index, auto_mode):
    if auto_mode:
        answer = AUTO_ANSWERS[index]
        print(f">{answer}")
        return answer
    return input(">")


def score_for_answer(answer, best_answer, second_answer):
    if answer == best_answer:
        return random.randint(10, 20)
    if answer == second_answer:
        return random.randint(5, 10)
    return 3


def print_result(score):
    for score_range, message in RESULT_BUCKETS:
        if score in score_range:
            print(message)
            return


def main():
    auto_mode = "--interactive" not in sys.argv
    score = 0

    print(ASCII_ART)
    print("Take this quiz and find out how long you would survive amongst the walking dead.")
    print("There are easy, intermediate and hard questions all mixed together.")
    print("There may be more than one correct answer.\nGood luck!")

    for index, (question, choices, best_answer, second_answer) in enumerate(QUESTIONS):
        print(question)
        print(choices)
        answer = get_answer(index, auto_mode)
        score += score_for_answer(answer, best_answer, second_answer)
        print("")

    print("The results are in!")
    print(f"You scored a {score}%")
    print_result(score)


if __name__ == "__main__":
    main()