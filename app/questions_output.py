from app.files_parsing import Questions
from app.estimations import Estimation, GeneralEstimation, ESTIMATIONS_STATISTICS_DIRNAME
from app.hinting_agents import SimpleHintingAgent, SmartHintingAgent
from app.examiner_agents import ExaminerAgent, ExaminerAgentException, ExaminerAgentRateLimitError
from app.user_choosing import (
    WorkMode, 
    OutputMode,
    choose_library_answers_using_mode,
    choose_hint_output_mode,
    choose_hint_size_mode
)
from app.utils import (
    DEFAULT_TEXT_STYLE,
    calc_general_estimation_num,
    choose_estimation_text_style, 
    save_user_data
)
import random
import time

THEME_TEXT_STYLE = '\033[31m'
SUBTHEME_TEXT_STYLE = '\033[35m'
QUESTION_TEXT_STYLE = '\033[36m'
ANSWER_TEXT_STYLE = '\033[32m'


def output_questions(
        questions: Questions, 
        output_themes: list[str],
        work_mode: WorkMode, 
        output_mode: OutputMode
    ):
    if work_mode == 2:
        print()
        library_answers_using_mode = choose_library_answers_using_mode()

        simple_hinting_agent = SimpleHintingAgent()
        smart_hinting_agent = SmartHintingAgent()
        examiner_agent = ExaminerAgent()

        estimations: list[Estimation] = []

    if output_mode == 4:
        output_themes = output_themes[:]
        random.shuffle(output_themes)

    for theme in output_themes:
        print(THEME_TEXT_STYLE)
        print(f'Тема: {theme}', end='')
        print(DEFAULT_TEXT_STYLE)

        subthemes = list(questions[theme].keys())

        if output_mode == 4 or output_mode == 3:
            random.shuffle(subthemes)
    
        for subtheme in subthemes:
            print(SUBTHEME_TEXT_STYLE)
            print(f'Подтема: {subtheme}', end='')
            print(DEFAULT_TEXT_STYLE)

            output_questions = questions[theme][subtheme]

            if output_mode == 4 or output_mode == 3 or output_mode == 2:
                random.shuffle(output_questions)
        
            question_num = 1

            for question, true_answer in output_questions:
                print(QUESTION_TEXT_STYLE)
                print(f'Вопрос {question_num}: {question}', end='')
                print(DEFAULT_TEXT_STYLE)

                if work_mode == 2:
                    if library_answers_using_mode == 2:
                        true_answer = None
                    
                    print()
                    hint_output_mode = choose_hint_output_mode(work_mode)

                    if hint_output_mode == 2:
                        print()
                        hint_size_mode = choose_hint_size_mode()

                        if hint_size_mode == 1:
                            hint_size = 'мелкая'
                        elif hint_size_mode == 2:
                            hint_size = 'средняя'
                        else:
                            hint_size = 'крупная'
                    
                        if true_answer == None:
                            hinting_agent_output = smart_hinting_agent.get_answer_with_hint(theme, subtheme, question, hint_size)

                            true_answer = hinting_agent_output.true_answer
                            hint = hinting_agent_output.hint
                        else:
                            hint = simple_hinting_agent.get_hint(theme, subtheme, question, hint_size, true_answer)
                    
                        print(f'{hint_size[0].upper()}{hint_size[1:]} подсказка: {hint}')
                    
                    print()
                    user_answer = input('Введите ваш ответ на вопрос: ')

                    while user_answer.strip() == '':
                        print()
                        user_answer = input('Ошибка, введите ваш ответ на вопрос: ')
                    
                    is_rate_limit_error_message_printed = False

                    while True:
                        try:
                            question_estimation = examiner_agent.get_estimation(theme, subtheme, question, user_answer, true_answer)
                        except ExaminerAgentRateLimitError:
                            if not is_rate_limit_error_message_printed:
                                print()
                                print('Ошибка, API OpenAI не справляется с текущей частотой запросов.')

                                print()
                                print('Подождите немного, через минуту запрос повторится.')

                                is_rate_limit_error_message_printed = True
                            
                            time.sleep(60)
                        except ExaminerAgentException:
                            print()
                            if true_answer:
                                print('Ошибка, агент не смог ответить на указанный вопрос.')
                            else:
                                print('Ошибка, агент не смог сравнить ваш ответ на указанный вопрос с правильным ответом.')

                            print()
                            print('Указанный вопрос не будет учитываться при итоговой оценке.')

                            break
                        else:
                            estimations.append(question_estimation)

                            print(ANSWER_TEXT_STYLE)
                            print(f'Правильный ответ: {question_estimation.true_answer}', end='')
                            print(DEFAULT_TEXT_STYLE)

                            question_estimation_text_style = choose_estimation_text_style(question_estimation.num)

                            print(question_estimation_text_style)
                            print(f'Оценка: {question_estimation.num}', end='')
                            print(DEFAULT_TEXT_STYLE)

                            print()
                            print(f'Пояснение: {question_estimation.explanation}')

                            break
                else:
                    if true_answer:
                        print()
                        input('Нажмите Enter, чтобы узнать ответ на вопрос.')
                        
                        print(ANSWER_TEXT_STYLE)
                        print(f'Правильный ответ: {true_answer}', end='')
                        print(DEFAULT_TEXT_STYLE)

                print()
                input('Нажмите Enter, чтобы перейти к следующему вопросу.')

                question_num += 1

            if work_mode == 2:
                questions_estimations_nums = [e.num for e in estimations if e.obj_type == 'question']

                subtheme_general_estimation_num = calc_general_estimation_num(questions_estimations_nums)
                subtheme_general_estimation = GeneralEstimation('subtheme', subtheme_general_estimation_num, obj_name=subtheme)

                estimations.append(subtheme_general_estimation)

                subtheme_estimation_text_style = choose_estimation_text_style(subtheme_general_estimation_num)

                print(subtheme_estimation_text_style)
                print(f'Итоговая оценка в подтеме "{subtheme}" темы "{theme}": {subtheme_general_estimation_num}', end='')
                print(DEFAULT_TEXT_STYLE)

        if work_mode == 2:
            subthemes_estimations_nums = [e.num for e in estimations if e.obj_type == 'subtheme']

            theme_general_estimation_num = calc_general_estimation_num(subthemes_estimations_nums)
            theme_general_estimation = GeneralEstimation('theme', theme_general_estimation_num, obj_name=theme)

            estimations.append(theme_general_estimation)

            theme_estimation_text_style = choose_estimation_text_style(theme_general_estimation_num)

            print(theme_estimation_text_style)
            print(f'Итоговая оценка в теме "{theme}": {subtheme_general_estimation_num}', end='')
            print(DEFAULT_TEXT_STYLE)

    if work_mode == 2:
        themes_estimations_nums = [e.num for e in estimations if e.obj_type == 'theme']

        general_estimation_num = calc_general_estimation_num(themes_estimations_nums)
        general_estimation = GeneralEstimation('all', general_estimation_num)

        estimations.append(general_estimation)

        general_estimation_text_style = choose_estimation_text_style(general_estimation_num)

        print(general_estimation_text_style)
        print(f'Итоговая оценка: {general_estimation_num}', end='')
        print(DEFAULT_TEXT_STYLE)

        now = time.strftime('%Y%m%d%H%M%S')
        save_user_data(ESTIMATIONS_STATISTICS_DIRNAME, f'{now}.data', estimations)
