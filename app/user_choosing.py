from typing import Literal
from app.utils import validate_input_nums

WorkMode = Literal[1, 2, 3]
OutputMode = Literal[1, 2, 3, 4]
HintOutputMode = Literal[1, 2]
HintSizeMode = Literal[1, 2, 3]


def choose_index(indexes_len: int, input_message: str):
    index_input = input(input_message)

    while True:
        if index_input.strip() == '':
            return 1
        if index_input.strip().isdigit():
            if 1 <= int(index_input.strip()) <= indexes_len:
                return int(index_input)
        
        print()
        index_input = input('Ошибка, введите корректное число: ')


def choose_indexes(indexes_len: int, default_indexes: list[int], input_message: str):
    indexes_input = input(input_message)

    while True:
        if indexes_input.strip() == '':
            return default_indexes
        if validate_input_nums(indexes_input, indexes_len):
            return [int(i) for i in indexes_input.replace(' ', '').split(',')]
        
        print()
        indexes_input = input('Ошибка, введите корректный набор чисел через запятую в выбранном порядке: ')


def choose_work_mode() -> WorkMode:
    print('Список доступных режимов работы программы:')

    print()
    print('1-Повторение материала.')
    print('2-Экзамен.')
    print('3-Просмотр статистики.')

    input_message = (
        'Выберите один из доступных режимов работы программы\n'
        'и введите соответсвующий номер (по умолчанию - 1): '
    )
    
    print()
    return choose_index(3, input_message)


def choose_output_themes(themes: list[str] | tuple[str]):
    print('Список тем на выбор:')

    print()
    for i in range(0, len(themes)):
        print(f'{i+1}. {themes[i]}')

    input_message = (
        'Выберите подходящие темы и введите\n'
        'соответсвующие им номера через запятую в выбранном порядке (по умолчанию - все): '
    )

    default_indexes = list(range(1, len(themes) + 1))

    print()
    choosed_themes_indexes = choose_indexes(len(default_indexes), default_indexes, input_message)

    return [themes[i-1] for i in choosed_themes_indexes]


def choose_output_mode() -> OutputMode:
    print('Варианты в какой последовательности выводить вопросы на выбор:')

    print()
    print('1. Полностью по порядку.')
    print('2. Темы и подтемы по порядку, а вопросы в подтемах случайно.')
    print('3. Темы по порядку, а подтемы и вопросы в подтемах случайно.')
    print('4. Полностью случайно.')

    input_message = (
        'Выберите порядок, в котором будут выводиться вопросы, и введите'
        'соответсвующий номер (по умолчанию - 1): '
    )

    print()
    return choose_index(4, input_message)


def choose_hint_output_mode(work_mode: WorkMode) -> HintOutputMode:
    print('Варианты на выбор:')

    print()
    if work_mode == 1:
        print('1-Узнать ответ на вопрос.')
    else:
        print('1-Ввести ответ на вопрос.')
    
    print('2-Вывести подсказку.')

    input_message = 'Выберите нужна ли вам подсказка и введите соответсвующий номер (по умолчанию - 1): '

    print()
    return choose_index(2, input_message)


def choose_hint_size_mode() -> HintSizeMode:
    print('Варианты размера подсказки на выбор:')

    print()
    print('1-Мелкая')
    print('2-Средняя')
    print('3-Крупная')

    input_message = 'Выберите нужный размер подсказки и введите соответсвующий номер (по умолчанию - 1): '

    print()
    return choose_index(3, input_message)
