from dotenv import load_dotenv
from os import getenv
from configparser import ConfigParser


class AgentSettings:
    def __init__(self, openai_model: str, verbosity: str, reasoning_effort: str):
        self.openai_model = openai_model
        self.verbosity = verbosity
        self.reasoning_effort = reasoning_effort


class AppSettings:
    def __init__(
        self,
        app_env: str,
        openai_api_key: str,
        openai_base_url: str,
        library_dir_path: str,
        searchable_questions_blocks_headings_text: list[str],
        symbols_containing_answers: str,
        simple_hinting_agent: AgentSettings,
        smart_hinting_agent: AgentSettings,
        comparing_agent: AgentSettings,
        estimating_agent: AgentSettings
    ):
        self.app_env = app_env
        self.openai_api_key = openai_api_key
        self.openai_base_url = openai_base_url
        self.library_dir_path = library_dir_path
        self.searchable_questions_blocks_headings_text = searchable_questions_blocks_headings_text
        self.symbols_containing_answers = symbols_containing_answers
        self.simple_hinting_agent = simple_hinting_agent
        self.smart_hinting_agent = smart_hinting_agent
        self.comparing_agent = comparing_agent
        self.estimating_agent = estimating_agent


def get_app_settings():
    load_dotenv()
    app_env = getenv('app_env')
    openai_api_key = getenv('OPENAI_API_KEY')
    openai_base_url = getenv('OPENAI_BASE_URL')
    library_dir_path = getenv('LIBRARY_DIR_PATH')

    config = ConfigParser()
    config.read('config.ini', 'utf-8')

    main_config = config['DEFAULT']
    searchable_questions_blocks_headings_text = main_config['SEARCHABLE_QUESTIONS_BLOCKS_HEADINGS_TEXT'].split('\n')
    symbols_containing_answers = main_config['SYMBOLS_CONTAINING_ANSWERS']

    hinting_agents_config = config['HINTING_AGENTS']
    simple_hinting_agent_settings = AgentSettings(
        openai_model=hinting_agents_config['SIMPLE_HINTING_AGENT_OPENAI_MODEL'],
        verbosity=hinting_agents_config['SIMPLE_HINTING_AGENT_VERBOSITY'],
        reasoning_effort=hinting_agents_config['SIMPLE_HINTING_AGENT_REASONING_EFFORT']
    )
    smart_hinting_agent_settings = AgentSettings(
        openai_model=hinting_agents_config['SMART_HINTING_AGENT_OPENAI_MODEL'],
        verbosity=hinting_agents_config['SMART_HINTING_AGENT_VERBOSITY'],
        reasoning_effort=hinting_agents_config['SMART_HINTING_AGENT_REASONING_EFFORT']
    )

    examiner_agents_config = config['EXAMINER_AGENTS']
    comparing_agent_settings = AgentSettings(
        openai_model=examiner_agents_config['COMPARING_AGENT_OPENAI_MODEL'],
        verbosity=examiner_agents_config['COMPARING_AGENT_VERBOSITY'],
        reasoning_effort=examiner_agents_config['COMPARING_AGENT_REASONING_EFFORT']
    )
    estimating_agent_settings = AgentSettings(
        openai_model=examiner_agents_config['ESTIMATING_AGENT_OPENAI_MODEL'],
        verbosity=examiner_agents_config['ESTIMATING_AGENT_VERBOSITY'],
        reasoning_effort=examiner_agents_config['ESTIMATING_AGENT_REASONING_EFFORT']
    )

    return AppSettings(
        app_env=app_env,
        openai_api_key=openai_api_key,
        openai_base_url=openai_base_url,
        library_dir_path=library_dir_path,
        searchable_questions_blocks_headings_text=searchable_questions_blocks_headings_text,
        symbols_containing_answers=symbols_containing_answers,
        simple_hinting_agent=simple_hinting_agent_settings,
        smart_hinting_agent=smart_hinting_agent_settings,
        comparing_agent=comparing_agent_settings,
        estimating_agent=estimating_agent_settings
    )
