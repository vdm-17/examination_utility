from dotenv import load_dotenv
from app.files_parsing import get_questions
from app.user_choosing import choose_work_mode, choose_output_themes, choose_output_mode
from app.statistics_output import output_estimations_stats
from app.questions_output import output_questions


def main():
    load_dotenv()
    
    questions = get_questions()
    themes = list(questions.keys())

    while True:
        work_mode = choose_work_mode()

        if work_mode == 4:
            break

        print()
        print(f'Вы выбрали режим работы под номером {work_mode}.')

        if work_mode == 3:
            print()
            output_estimations_stats()
            print()
            continue
    
        print()
        output_themes = choose_output_themes(themes)

        print()
        print(f'Вы выбрали для повторения следующие темы: {'; '.join(output_themes)}.')

        print()
        output_mode = choose_output_mode()

        print()
        print(f'Вы выбрали режим вывода под номером {output_mode}.')

        output_questions(questions, output_themes, work_mode, output_mode)
        print()
    
    print()
    print('Работа программы завершена.')


if __name__ == '__main__':
    main()
