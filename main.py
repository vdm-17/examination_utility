import configparser
import pathlib
import random
import re

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')

LIBRARY_DIR_PATH = config['DEFAULT']['LIBRARY_DIR_PATH']
SEARCHABLE_QUESTIONS_BLOCKS_HEADINGS_TEXT = \
    tuple(config['DEFAULT']['SEARCHABLE_QUESTIONS_BLOCKS_HEADINGS_TEXT'].split('\n'))
SYMBOLS_CONTAINING_ANSWERS = config['DEFAULT']['SYMBOLS_CONTAINING_ANSWERS']


def validate_input_numbers(s: str, x: int) -> bool:
    pattern = re.compile(r'^\s*\d+(?:\s*,\s*\d+)*\s*$')
    if not pattern.fullmatch(s):
        return False
    try:
        nums = [int(n.strip()) for n in s.split(",")]
    except ValueError:
        return False
    return all(1 <= n <= x for n in nums)


questions = {}

for path in pathlib.Path(LIBRARY_DIR_PATH).rglob('*'):
    if not path.name.endswith('.md'):
        continue
    
    current_theme = path.name.replace('.md', '')
    current_subtheme = 'Главные'
    is_questions_block_finded = False

    file = path.open('r', encoding='utf-8')

    for line in file.readlines():
        line_title_level = 0

        for char in line:
            if char == '#':
                line_title_level += 1
            else:
                break

        if not is_questions_block_finded:
            for title_text in SEARCHABLE_QUESTIONS_BLOCKS_HEADINGS_TEXT:
                if line.startswith('# {}'.format(title_text)):
                    is_questions_block_finded = True
                    questions_block_title_level = line_title_level
                    break
            continue
            
        if line_title_level > 0 and line_title_level <= questions_block_title_level:
            break

        if line_title_level == questions_block_title_level + 1:
            current_subtheme = line[line_title_level+1:].replace('\n', '')
            continue
            
        if line[0].isdigit() or line[0] == '•':
            answer_start_index = line.find(SYMBOLS_CONTAINING_ANSWERS)
            if answer_start_index == -1:
                question = line.replace('\n', '')
                answer = None
            else:
                question = line[:answer_start_index]
                answer = line[answer_start_index:].replace(SYMBOLS_CONTAINING_ANSWERS, '').replace('\n', '')
            if current_theme not in questions:
                questions[current_theme] = {}
            if current_subtheme not in questions[current_theme]:
                questions[current_theme][current_subtheme] = []
            questions[current_theme][current_subtheme].append((question, answer))
    
    file.close()

print('Список тем на выбор:\n')
i = 1
themes = []
for key in questions.keys():
    themes.append(key)
    print('{}. {}'.format(i, key))
    i += 1

output_themes_input = input(
'''\nВыберите подходящие темы для проверки знаний и введите
соответсвующие им номера через запятую в выбранном порядке: '''
)

while True:
    if validate_input_numbers(output_themes_input, len(themes)):
        break
    output_themes_input = input('\nОшибка, введите корректный набор чисел через запятую в выбранном порядке: ')

output_themes_indexes = output_themes_input.replace(' ', '').split(',')
output_themes = []
for index in output_themes_indexes:
    output_themes.append(themes[int(index)-1])

print('\nВы выбрали для повторения следующие темы: {}.'.format('; '.join(output_themes)))

print('\nВарианты в какой последовательности выводить вопросы на выбор:\n')
print(
'''1. Полностью по порядку.
2. Темы и подтемы по порядку, а вопросы в подтемах случайно.
3. Темы по порядку, а подтемы и вопросы в подтемах случайно.
4. Полностью случайно.'''
)

output_mode_input = input(
'''\nВыберите порядок, в котором будут выводиться вопросы, и введите
соответсвующий номер (по умолчанию - 1): '''
)

while True:
    if output_mode_input.strip() == '':
        break
    if output_mode_input.strip().isdigit():
        if 1 <= int(output_mode_input.strip()) <= 4:
            break
    output_mode_input = input('\nОшибка, введите корректное число: ')

if output_mode_input == '':
    output_mode = '1'
else:
    output_mode = output_mode_input.strip()

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
