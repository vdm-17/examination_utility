from typing import Literal
from app.utils import validate_input_nums

Action = Literal[1, 2, 3, 4]
OutputMode = Literal[1, 2, 3, 4]
LibraryAnswersUsingMode = Literal[1, 2]
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


def choose_action() -> Action:
    print('Доступные действия:')

    print()
    print('1-Повторение материала.')
    print('2-Экзамен.')
    print('3-Просмотр статистики.')
    print('4-Выход из программы.')

    input_message = (
        'Выберите одно из доступных действий\n'
        'и введите соответсвующий номер (по умолчанию - 1): '
    )
    
    print()
    return choose_index(4, input_message)


def choose_output_themes(themes: list[str] | tuple[str]):
    print('Список доступных тем:')

    print()
    for i in range(0, len(themes)):
        print(f'{i+1}. {themes[i]}')

    input_message = (
        'Выберите необходимые темы и введите соответствующие им номера '
        'через запятую в выбранном порядке (по умолчанию - все): '
    )

    default_indexes = list(range(1, len(themes) + 1))

    print()
    choosed_themes_indexes = choose_indexes(len(default_indexes), default_indexes, input_message)

    return [themes[i-1] for i in choosed_themes_indexes]


def choose_output_mode() -> OutputMode:
    print('Доступные варианты, в какой последовательности выводить вопросы:')

    print()
    print('1. Полностью по порядку.')
    print('2. Темы и подтемы по порядку, а вопросы в подтемах случайно.')
    print('3. Темы по порядку, а подтемы и вопросы в подтемах случайно.')
    print('4. Полностью случайно.')

    input_message = (
        'Выберите необходимый порядок, в котором будут выводиться вопросы, '
        'и введите соответсвующий номер (по умолчанию - 1): '
    )

    print()
    return choose_index(4, input_message)


def choose_library_answers_using_mode() -> LibraryAnswersUsingMode:
    print('Доступные варианты, откуда будут браться ответы на вопросы:')

    print()
    print('1. Всегда использовать ответы из библиотеки, если те имееются.')
    print('2. Всегда использовать ответы нейросети, вместо ответов из библиотеки.')

    input_message = (
        'Выберите, хотите ли вы использовать ответы на вопросы из библиотеки, '
        'и введите соответсвующий номер (по умолчанию - 1): '
    )

    print()
    return choose_index(2, input_message)


def choose_hint_output_mode(action: Action) -> HintOutputMode:
    print('Доступные действия:')

    print()
    if action == 1:
        print('1-Узнать ответ на вопрос.')
    else:
        print('1-Ввести ответ на вопрос.')
    
    print('2-Вывести подсказку.')

    input_message = 'Выберите, нужна ли вам подсказка, и введите соответсвующий номер (по умолчанию - 1): '

    print()
    return choose_index(2, input_message)


def choose_hint_size_mode() -> HintSizeMode:
    print('Доступные размеры подсказки:')

    print()
    print('1-Мелкая')
    print('2-Средняя')
    print('3-Крупная')

    input_message = 'Выберите необходимый размер подсказки и введите соответсвующий номер (по умолчанию - 1): '

    print()
    return choose_index(3, input_message)
