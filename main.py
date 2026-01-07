from files_parsing import get_questions
from user_choosing import choose_output_themes, choose_output_mode
import random

questions = get_questions()
themes = list(questions.keys())

output_themes = choose_output_themes(themes)
print('\nВы выбрали для повторения следующие темы: {}.'.format('; '.join(output_themes)))

output_mode = choose_output_mode()
print('\nВы выбрали режим под номером {}.'.format(output_mode))

if output_mode == '4':
    random.shuffle(output_themes)

for theme in output_themes:
    print('{text_color}\nТема: {theme}\033[0m'.format(text_color='\033[31m', theme=theme))

    subthemes = list(questions[theme].keys())

    if output_mode == '4' or output_mode == '3':
        random.shuffle(subthemes)
    
    for subtheme in subthemes:
        print('{text_color}\nПодтема: {subtheme}\033[0m'.format(text_color='\033[35m', subtheme=subtheme))

        output_questions = questions[theme][subtheme]

        if output_mode == '4' or output_mode == '3' or output_mode == '2':
            random.shuffle(output_questions)
        
        for question, answer in output_questions:
            print('{text_color}\nВопрос: {question}\033[0m'.format(text_color='\033[36m', question=question))

            if answer:
                input('\nНажмите Enter, чтобы узнать ответ на вопрос.')
                print('{text_color}\nОтвет: {answer}\033[0m'.format(text_color='\033[32m', answer=answer))
            
            input('\nНажмите Enter, чтобы перейти к следующему вопросу.')

print('\nВопросы закончились, работа программы завершена.')
