import configparser
import re
import pathlib
import pickle

ESTIMATION_FIVE_TEXT_STYLE = '\033[32m'
ESTIMATION_FOUR_TEXT_STYLE = '\033[32m'
ESTIMATION_THREE_TEXT_STYLE = '\033[33m'
ESTIMATION_TWO_TEXT_STYLE = '\033[31m'
ESTIMATION_ONE_TEXT_STYLE = '\033[31m'

DEFAULT_TEXT_STYLE = '\033[0m'

PROGRAM_DATA_DIRNAME = '.examination_utility'


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini', 'utf-8')

    return config


def validate_input_nums(s: str, x: int) -> bool:
    pattern = re.compile(r'^\s*\d+(?:\s*,\s*\d+)*\s*$')
    if not pattern.fullmatch(s):
        return False
    try:
        nums = [int(n.strip()) for n in s.split(',')]
    except ValueError:
        return False
    return all(1 <= n <= x for n in nums)


def calc_general_estimation_num(estimations_nums: list[int]):
    return round(sum(estimations_nums) / len(estimations_nums))


def get_estimation_text_style(estimation_num: int):
    if estimation_num == 5:
        return ESTIMATION_FIVE_TEXT_STYLE
    elif estimation_num == 4:
        return ESTIMATION_FOUR_TEXT_STYLE
    elif estimation_num == 3:
        return ESTIMATION_THREE_TEXT_STYLE
    elif estimation_num == 2:
        return ESTIMATION_TWO_TEXT_STYLE
    else:
        return ESTIMATION_ONE_TEXT_STYLE


def save_user_data(dirname: str, filename: str, data):
    home_path = pathlib.Path.home()
    prog_path = home_path / PROGRAM_DATA_DIRNAME

    if not prog_path.exists():
        prog_path.mkdir()

    dir_path = prog_path / dirname

    if not dir_path.exists():
        dir_path.mkdir()
    
    file_path = dir_path / filename

    with file_path.open('wb') as f:
        pickle.dump(data, f)


def load_user_data(dirname: str, filename: str):
    home_path = pathlib.Path.home()
    prog_path = home_path / PROGRAM_DATA_DIRNAME

    dir_path = prog_path / dirname
    file_path = dir_path / filename

    if not file_path.exists():
        return None

    with file_path.open('rb') as f:
        return pickle.load(f)
