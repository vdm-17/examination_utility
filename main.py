from dotenv import load_dotenv
from app.files_parsing import get_questions
from app.user_choosing import choose_action, choose_output_themes, choose_output_mode
from app.output.statistics import output_estimations_stats
from app.output.questions import output_questions


def main():
    load_dotenv()
    
    questions = get_questions()
    themes = list(questions.keys())

    while True:
        action = choose_action()

        if action == 4:
            break

        if action == 3:
            print()
            output_estimations_stats()
            print()
            continue
    
        print()
        output_themes = choose_output_themes(themes)

        print()
        output_mode = choose_output_mode()

        output_questions(questions, output_themes, action, output_mode)
        print()
    
    print()
    print('Работа программы завершена.')


if __name__ == '__main__':
    main()
