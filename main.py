from files_parsing import get_questions
from user_choosing import choose_work_mode, choose_output_themes, choose_output_mode
from questions_output import output_questions

questions = get_questions()
themes = list(questions.keys())

work_mode = choose_work_mode()
print(f'\nВы выбрали режим работы под номером {work_mode}.')

output_themes = choose_output_themes(themes)
print(f'\nВы выбрали для повторения следующие темы: {'; '.join(output_themes)}.')

output_mode = choose_output_mode()
print(f'\nВы выбрали режим вывода под номером {output_mode}.')

output_questions(questions, output_themes, work_mode, output_mode)

print('\nВопросы закончились, работа программы завершена.')
