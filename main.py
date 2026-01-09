from files_parsing import get_questions
from user_choosing import choose_output_themes, choose_output_mode
import random

THEME_TEXT_STYLE = '\033[31m'
SUBTHEME_TEXT_STYLE = '\033[35m'
QUESTION_TEXT_STYLE = '\033[36m'
ANSWER_TEXT_STYLE = '\033[32m'
DEFAULT_TEXT_STYLE = '\033[0m'

questions = get_questions()
themes = list(questions.keys())

output_themes = choose_output_themes(themes)
print(f'\nВы выбрали для повторения следующие темы: {'; '.join(output_themes)}.')

output_mode = choose_output_mode()
print(f'\nВы выбрали режим под номером {output_mode}.')

if output_mode == '4':
    random.shuffle(output_themes)

for theme in output_themes:
    print(f'{THEME_TEXT_STYLE}\nТема: {theme}{DEFAULT_TEXT_STYLE}')

    subthemes = list(questions[theme].keys())

    if output_mode == '4' or output_mode == '3':
        random.shuffle(subthemes)
    
    for subtheme in subthemes:
        print(f'{SUBTHEME_TEXT_STYLE}\nПодтема: {subtheme}{DEFAULT_TEXT_STYLE}')

        output_questions = questions[theme][subtheme]

        if output_mode == '4' or output_mode == '3' or output_mode == '2':
            random.shuffle(output_questions)
        
        question_num = 1

        for question, answer in output_questions:
            print(f'{QUESTION_TEXT_STYLE}\nВопрос {question_num}: {question}{DEFAULT_TEXT_STYLE}')

            if answer:
                input('\nНажмите Enter, чтобы узнать ответ на вопрос.')
                print(f'{ANSWER_TEXT_STYLE}\nОтвет: {answer}{DEFAULT_TEXT_STYLE}')
            
            input('\nНажмите Enter, чтобы перейти к следующему вопросу.')

            question_num += 1

print('\nВопросы закончились, работа программы завершена.')
