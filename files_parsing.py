import configparser
import pathlib

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')

LIBRARY_DIR_PATH = config['DEFAULT']['LIBRARY_DIR_PATH']
SEARCHABLE_QUESTIONS_BLOCKS_HEADINGS_TEXT = \
    tuple(config['DEFAULT']['SEARCHABLE_QUESTIONS_BLOCKS_HEADINGS_TEXT'].split('\n'))
SYMBOLS_CONTAINING_ANSWERS = config['DEFAULT']['SYMBOLS_CONTAINING_ANSWERS']


def get_questions():
    questions: dict[str, dict[str, list[tuple[str]]]] = {}

    for path in pathlib.Path(LIBRARY_DIR_PATH).rglob('*'):
        if not path.name.endswith('.md'):
            continue
    
        current_theme = path.name.replace('.md', '')
        current_subtheme = 'Главные'
        is_questions_block_finded = False

        file = path.open(encoding='utf-8')

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
    
    return questions
