import pathlib
from app.examiner_agents import GeneralEstimation, QuestionAnswerEstimation, ESTIMATIONS_STATISTICS_DIRNAME
from app.user_choosing import choose_output_themes
from app.utils import PROGRAM_DATA_DIRNAME, load_user_data, calc_general_estimation_num, choose_estimation_text_style

DEFAULT_TEXT_STYLE = '\033[0m'


def output_estimations():
    stat_estimations: list[GeneralEstimation | QuestionAnswerEstimation] = []

    home_path = pathlib.Path.home()
    prog_path = home_path / PROGRAM_DATA_DIRNAME
    for path in prog_path.rglob('*'):
        if path.is_dir():
            continue
        
        user_estimations_stat_data = load_user_data(ESTIMATIONS_STATISTICS_DIRNAME, path.name)

        if user_estimations_stat_data != None:
            stat_estimations.extend(user_estimations_stat_data)
    
    if len(stat_estimations) == 0:
        print('\nНа данный момент у пользователя отсутсвует статистика оценок. Работа программы завершена.')
        return

    print('\nСтатистика оценок пользователя:')

    stat_general_estimations_nums = [e.num for e in stat_estimations if e.obj_type == 'all']
    avg_general_estimation_num = calc_general_estimation_num(stat_general_estimations_nums)
    
    estimation_text_style = choose_estimation_text_style(avg_general_estimation_num)

    print(f'{estimation_text_style}\nСредняя итоговая оценка: {avg_general_estimation_num}{DEFAULT_TEXT_STYLE}')

    print('\nВыберите список тем для вывода статистики.')

    themes = list(set([e.obj_name for e in stat_estimations if e.obj_type == 'theme']))
    output_themes = choose_output_themes(themes)

    for theme in output_themes:
        stat_theme_avg_general_estimations_nums = \
            [e.num for e in stat_estimations if e.obj_type == 'theme' and e.obj_name == theme]
        avg_theme_general_estimation_num = calc_general_estimation_num(stat_theme_avg_general_estimations_nums)

        estimation_text_style = choose_estimation_text_style(avg_theme_general_estimation_num)

        print(f'{estimation_text_style}\nСредняя итоговая оценка в теме "{theme}": {avg_theme_general_estimation_num}{DEFAULT_TEXT_STYLE}')
    
    print('\nТемы закончились, работа программы завершена.')
