from app.files_parsing import QuestionsType
from app.examiner_agents import (
    ESTIMATIONS_STATISTICS_DIRNAME,
    Estimation, 
    GeneralEstimation,
    ExaminerAgent, 
    ExaminerAgentException,
    ExaminerAgentRateLimitError
)
from app.utils import calc_general_estimation_num, choose_estimation_text_style, save_user_data
from typing import Literal
import random
import time

THEME_TEXT_STYLE = '\033[31m'
SUBTHEME_TEXT_STYLE = '\033[35m'
QUESTION_TEXT_STYLE = '\033[36m'
ANSWER_TEXT_STYLE = '\033[32m'
DEFAULT_TEXT_STYLE = '\033[0m'


def output_questions(
        questions: QuestionsType, 
        output_themes: list[str],
        work_mode: Literal['1', '2'], 
        output_mode: Literal['1', '2', '3', '4']
    ):
    if work_mode == '2':
        examiner_agent = ExaminerAgent()
        estimations: list[Estimation] = []

    if output_mode == '4':
        output_themes = output_themes[:]
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

            for question, true_answer in output_questions:
                print(f'{QUESTION_TEXT_STYLE}\nВопрос {question_num}: {question}{DEFAULT_TEXT_STYLE}')

                if work_mode == '2':
                    user_answer = input('\nВведите ваш ответ на вопрос: ')

                    while user_answer.strip() == '':
                        user_answer = input('\nОшибка, введите ваш ответ на вопрос: ')
                    
                    is_rate_limit_error_message_printed = False

                    while True:
                        try:
                            estimation = examiner_agent.get_estimation(theme, subtheme, question, user_answer, true_answer)
                        except ExaminerAgentRateLimitError as e:
                            if not is_rate_limit_error_message_printed:
                                print('\nОшибка, API OpenAI не справляется с текущей частотой запросов.')
                                print('\nПодождите немного, через минуту запрос повторится.')

                                is_rate_limit_error_message_printed = True
                            
                            time.sleep(60)
                        except ExaminerAgentException as e:
                            if true_answer:
                                print('\nОшибка, агент не смог ответить на указанный вопрос.')
                            else:
                                print('\nОшибка, агент не смог сравнить ваш ответ на указанный вопрос с правильным ответом.')
                    
                            print('\nУказанный вопрос не будет учитываться при итоговой оценке.')

                            break
                        else:
                            estimations.append(estimation)

                            estimation_text_style = choose_estimation_text_style(estimation.num)

                            print(
                                f'{ANSWER_TEXT_STYLE}\nПравильный ответ: {estimation.true_answer}'
                                f'\n\n{estimation_text_style}Оценка: {estimation.num}{DEFAULT_TEXT_STYLE}'
                                f'\n\nПояснение: {estimation.explanation}'
                            )

                            break
                else:
                    if true_answer:
                        input('\nНажмите Enter, чтобы узнать ответ на вопрос.')
                        print(f'{ANSWER_TEXT_STYLE}\nПравильный ответ: {true_answer}{DEFAULT_TEXT_STYLE}')
            
                input('\nНажмите Enter, чтобы перейти к следующему вопросу.')

                question_num += 1

            if work_mode == '2':
                questions_estimations_nums = [e.num for e in estimations if e.obj_type == 'question']

                subtheme_general_estimation_num = calc_general_estimation_num(questions_estimations_nums)
                subtheme_general_estimation = GeneralEstimation('subtheme', subtheme_general_estimation_num, obj_name=subtheme)

                estimations.append(subtheme_general_estimation)

                estimation_text_style = choose_estimation_text_style(subtheme_general_estimation_num)

                print(f'{estimation_text_style}\nИтоговая оценка в подтеме "{subtheme}" темы "{theme}": {subtheme_general_estimation_num}{DEFAULT_TEXT_STYLE}')

        if work_mode == '2':
            subthemes_estimations_nums = [e.num for e in estimations if e.obj_type == 'subtheme']

            theme_general_estimation_num = calc_general_estimation_num(subthemes_estimations_nums)
            theme_general_estimation = GeneralEstimation('theme', theme_general_estimation_num, obj_name=theme)

            estimations.append(theme_general_estimation)

            estimation_text_style = choose_estimation_text_style(theme_general_estimation_num)

            print(f'{estimation_text_style}\nИтоговая оценка в теме "{theme}": {subtheme_general_estimation_num}{DEFAULT_TEXT_STYLE}')

    if work_mode == '2':
        themes_estimations_nums = [e.num for e in estimations if e.obj_type == 'theme']

        general_estimation_num = calc_general_estimation_num(themes_estimations_nums)
        general_estimation = GeneralEstimation('all', general_estimation_num)

        estimations.append(general_estimation)

        estimation_text_style = choose_estimation_text_style(general_estimation_num)
    
        print(f'{estimation_text_style}\nИтоговая оценка: {general_estimation_num}{DEFAULT_TEXT_STYLE}')

        now = time.strftime('%Y%m%d%H%M%S')
        save_user_data(ESTIMATIONS_STATISTICS_DIRNAME, f'{now}.data', estimations)
