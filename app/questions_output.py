from app.files_parsing import QuestionsType
from app.examiner_agents import GeneralEstimation, QuestionAnswerEstimation, ExaminerAgent, ExaminerAgentException
from app.utils import calc_general_estimation_num
from typing import Literal
import random

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
        themes_estimations: list[GeneralEstimation] = []

    if output_mode == '4':
        output_themes = output_themes[:]
        random.shuffle(output_themes)

    for theme in output_themes:
        print(f'{THEME_TEXT_STYLE}\nТема: {theme}{DEFAULT_TEXT_STYLE}')

        subthemes = list(questions[theme].keys())

        if work_mode == '2':
            subthemes_estimations: list[GeneralEstimation] = []

        if output_mode == '4' or output_mode == '3':
            random.shuffle(subthemes)
    
        for subtheme in subthemes:
            print(f'{SUBTHEME_TEXT_STYLE}\nПодтема: {subtheme}{DEFAULT_TEXT_STYLE}')

            output_questions = questions[theme][subtheme]

            if work_mode == '2':
                questions_estimations: list[QuestionAnswerEstimation] = []

            if output_mode == '4' or output_mode == '3' or output_mode == '2':
                random.shuffle(output_questions)
        
            question_num = 1

            for question, true_answer in output_questions:
                print(f'{QUESTION_TEXT_STYLE}\nВопрос {question_num}: {question}{DEFAULT_TEXT_STYLE}')

                if work_mode == '2':
                    user_answer = input('\nВведите ваш ответ на вопрос: ')

                    while user_answer.strip() == '':
                        user_answer = input('\nОшибка, введите ваш ответ на вопрос: ')
                    try:
                        estimation = examiner_agent.get_estimation(theme, subtheme, question, user_answer, true_answer)
                    except ExaminerAgentException as e:
                        if true_answer:
                            print('\nОшибка, агент не смог ответить на указанный вопрос.')
                        else:
                            print('\nОшибка, агент не смог сравнить ваш ответ на указанный вопрос с правильным ответом.')
                    
                        print('\nУказанный вопрос не будет учитываться при итоговой оценке.')
                    else:
                        questions_estimations.append(estimation)

                        print(f'{ANSWER_TEXT_STYLE}\nПравильный ответ: {estimation.true_answer}\
                            \n\n{DEFAULT_TEXT_STYLE}Оценка: {estimation.num}\
                            \n\nПояснение: {estimation.explanation}')
                else:
                    if true_answer:
                        input('\nНажмите Enter, чтобы узнать ответ на вопрос.')
                        print(f'{ANSWER_TEXT_STYLE}\nПравильный ответ: {true_answer}{DEFAULT_TEXT_STYLE}')
            
                input('\nНажмите Enter, чтобы перейти к следующему вопросу.')

                question_num += 1

            if work_mode == '2':
                questions_estimations_nums = [e.num for e in questions_estimations]

                subtheme_general_estimation_num = calc_general_estimation_num(questions_estimations_nums)
                subtheme_general_estimation = GeneralEstimation(subtheme_general_estimation_num)

                subthemes_estimations.append(subtheme_general_estimation)

                print(f'\nИтоговая оценка в подтеме "{subtheme}" темы "{theme}": {subtheme_general_estimation_num}')

        if work_mode == '2':
            subthemes_estimations_nums = [e.num for e in subthemes_estimations]

            theme_general_estimation_num = calc_general_estimation_num(subthemes_estimations_nums)
            theme_general_estimation = GeneralEstimation(theme_general_estimation_num)

            themes_estimations.append(theme_general_estimation)

            print(f'\nИтоговая оценка в теме "{theme}": {subtheme_general_estimation_num}')

    if work_mode == '2':
        themes_estimations_nums = [e.num for e in themes_estimations]
        general_estimation_num = calc_general_estimation_num(themes_estimations_nums)
    
        print(f'\nИтоговая оценка: {general_estimation_num}')
