from utils import validate_input_nums

OUTPUT_THEMES_INPUT_MESSAGE = '''\nВыберите подходящие темы для проверки знаний и введите
соответсвующие им номера через запятую в выбранном порядке (по умолчанию - все): '''
OUTPUT_THEMES_ERROR_INPUT_MESSAGE = '\nОшибка, введите корректный набор чисел через запятую в выбранном порядке: '

OUTPUT_MODES_LIST_MESSAGE = '''1. Полностью по порядку.
2. Темы и подтемы по порядку, а вопросы в подтемах случайно.
3. Темы по порядку, а подтемы и вопросы в подтемах случайно.
4. Полностью случайно.'''
OUTPUT_MODE_INPUT_MESSAGE = '''\nВыберите порядок, в котором будут выводиться вопросы, и введите
соответсвующий номер (по умолчанию - 1): '''
DEFAULT_OUTPUT_MODE = '1'


def choose_output_themes(themes: list[str] | tuple[str]):
    print('Список тем на выбор:\n')
    
    for i in range(0, len(themes)):
        print(f'{i+1}. {themes[i]}')

    output_themes_input = input(OUTPUT_THEMES_INPUT_MESSAGE)

    while True:
        if output_themes_input.strip() == '':
            return themes
        if validate_input_nums(output_themes_input, len(themes)):
            return [themes[int(i)-1] for i in output_themes_input.replace(' ', '').split(',')]
        
        output_themes_input = input(OUTPUT_THEMES_ERROR_INPUT_MESSAGE)


def choose_output_mode():
    print('\nВарианты в какой последовательности выводить вопросы на выбор:\n')
    print(OUTPUT_MODES_LIST_MESSAGE)

    output_mode_input = input(OUTPUT_MODE_INPUT_MESSAGE)

    while True:
        if output_mode_input.strip() == '':
            return DEFAULT_OUTPUT_MODE
        if output_mode_input.strip().isdigit():
            if 1 <= int(output_mode_input.strip()) <= 4:
                return output_mode_input
        
        output_mode_input = input('\nОшибка, введите корректное число: ')
