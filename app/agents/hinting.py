from app.settings import AppSettings
from typing import Literal
from pydantic import BaseModel, Field
from agents import Agent, Runner, ModelSettings, WebSearchTool, AgentsException
from agents.model_settings import Reasoning
from agents.run import RunConfig
from openai import RateLimitError
import asyncio

HINTING_AGENT_NAME = 'Бот-подсказчик'
HINTING_AGENT_INSTRUCTIONS = (
    'Ты бот-подсказчик. Твоя задача - формулировать и составлять подсказки для правильного'
    'ответа на вопрос, загаданный пользователю. Подсказки не должны содержать сам правильный'
    'ответ на вопрос, а должны лишь направлять мысли пользователя в нужную сторону. {additional_instructions} '
    'Размер (степень) подсказки будет определяться пользователем. В ответ отправляй {output_format}.'
)

SIMPLE_HINTING_AGENT_ADDITIONAL_INSTRUCTIONS = 'Правильный ответ на вопрос будет определяться пользователем.'
SMART_HINTING_AGENT_ADDITIONAL_INSTRUCTIONS = (
    'Правильный ответ на вопрос ты должен будешь определять на основе '
    'собственных знаний, либо искать его в сети.'
)

SIMPLE_HINTING_AGENT_OUTPUT_FORMAT = 'В ответ отправляй строку подсказки длиной не более 300 символов.'
SMART_HINTING_AGENT_OUTPUT_FORMAT = 'В ответ отправляй объект с полями правильного ответа и подсказки.'

HintSize = Literal['мелкая', 'средняя', 'крупная']


class HintingAgentException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class HintingAgentRateLimitError(HintingAgentException):
    def __init__(self, message: str):
        super().__init__(message)


class SimpleHintingAgent(Agent):
    def __init__(self, app_settings: AppSettings):
        openai_model = app_settings.simple_hinting_agent.openai_model
        reasoning_effort = app_settings.simple_hinting_agent.reasoning_effort
        verbosity = app_settings.simple_hinting_agent.verbosity

        super().__init__(
            name=HINTING_AGENT_NAME, 
            instructions=HINTING_AGENT_INSTRUCTIONS.format(
                additional_instructions=SIMPLE_HINTING_AGENT_ADDITIONAL_INSTRUCTIONS,
                output_format=SIMPLE_HINTING_AGENT_OUTPUT_FORMAT
            ),
            model=openai_model,
            model_settings=ModelSettings(
                reasoning=Reasoning(effort=reasoning_effort), 
                verbosity=verbosity, 
                store=False
            ),
            output_type=str,
        )
    
    def get_hint(self, theme: str, subtheme: str, question: str, hint_size: HintSize, true_answer: str, tracing_disabled: bool) -> str:
        agent_input = f'Тема: {theme}. Подтема: {subtheme}. Вопрос: {question}. Размер подсказки: {hint_size}. Правильный ответ: {true_answer}'

        try:
            response = asyncio.run(Runner.run(self, agent_input, run_config=RunConfig(tracing_disabled=tracing_disabled)))
        except RateLimitError as e:
            raise HintingAgentRateLimitError(f'Hinting agent rate limit error: {e}') from e
        except AgentsException as e:
            raise HintingAgentException(f'Hinting agent response exception: {e}') from e
        
        return response.final_output


class SmartHintingAgentOutputSchema(BaseModel):
    true_answer: str = Field(description='Правильный ответ на предоставленный вопрос.')
    hint: str = Field(description=(
        'Текст подсказки для правильного ответа на предоставленный вопрос. '
        'Длина строки должна быть не более 300 символов.'
        )
    )


class SmartHintingAgent(Agent):
    def __init__(self, app_settings: AppSettings):
        openai_model = app_settings.simple_hinting_agent.openai_model
        reasoning_effort = app_settings.simple_hinting_agent.reasoning_effort
        verbosity = app_settings.simple_hinting_agent.verbosity

        super().__init__(
            name=HINTING_AGENT_NAME, 
            instructions=HINTING_AGENT_INSTRUCTIONS.format(
                additional_instructions = SMART_HINTING_AGENT_ADDITIONAL_INSTRUCTIONS,
                output_format=SMART_HINTING_AGENT_OUTPUT_FORMAT
            ),
            tools=[WebSearchTool()],
            model=openai_model,
            model_settings=ModelSettings(
                reasoning=Reasoning(effort=reasoning_effort), 
                verbosity=verbosity, 
                store=False
            ),
            output_type=SmartHintingAgentOutputSchema
        )
    
    def get_answer_with_hint(self, theme: str, subtheme: str, question: str, hint_size: HintSize, tracing_disabled: bool) -> SmartHintingAgentOutputSchema:
        agent_input = f'Тема: {theme}. Подтема: {subtheme}. Вопрос: {question}. Размер подсказки: {hint_size}.'

        try:
            response = asyncio.run(Runner.run(self, agent_input, run_config=RunConfig(tracing_disabled=tracing_disabled)))
        except RateLimitError as e:
            raise HintingAgentRateLimitError(f'Hinting agent rate limit error: {e}') from e
        except AgentsException as e:
            raise HintingAgentException(f'Hinting agent response exception: {e}') from e

        return response.final_output
