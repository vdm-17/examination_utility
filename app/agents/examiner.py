from os import getenv
from app.estimations import QuestionAnswerEstimation
from app.utils import get_config
from pydantic import BaseModel, Field
from agents import Agent, Runner, ModelSettings, WebSearchTool
from agents.model_settings import Reasoning
from agents.run import RunConfig
from agents.exceptions import AgentsException
from openai import RateLimitError
import asyncio

COMPARING_AGENT_INSTRUCTIONS = (
    'Ты бот-экзаменатор. Твоя задача — семантически сравнивать ответ '
    'пользователя на предоставленный вопрос с указанным правильным ответом, '
    'выставляя ответу пользователя оценку от 1 до 5 в зависимости от степени соответствия. '
    'В процессе оценки пользовательского ответа тебе запрещается искажать или подвергать сомнению '
    'указанный правильный ответ, даже если он, по твоему мнению, является ошибочным. '
    'Единица должна выставляться в случае, если пользовательский ответ находится '
    'совсем в другой плоскости относительно правильного. Двойка должна выставляться в случае, '
    'если пользовательский ответ находится в той же плоскости, что и правильный, но всё равно является неверным. '
    'Тройка должна выставляться в случае, если пользовательский ответ близок к правильному, но является очень неполным '
    'и/или плохо сформулированным. Четвёрка должна выставляться в случае, если пользовательский ответ является правильным, '
    'но немного неполным или слегка некорректно сформулированным. Пятерка должна выставляться случае, '
    'если пользовательский ответ является полностью правильным, либо имеет незначительные ошибки в формулировке '
    'и/или является совсем слегка неполным. Ты также должен предоставлять небольшое пояснение, '
    'почему ты выставил ту или иную оценку.'
)

ESTIMATING_AGENT_INSTRUCTIONS = (
    'Ты бот-экзаменатор. Твоя задача — определить на основе своих знаний '
    'либо найти в сети правильный ответ на предоставленный вопрос. Семантически сравни найденный правильный '
    'ответ с ответом пользователя, после чего выстави ответу пользователя оценку от 1 до 5 '
    'в зависимости от степени соответствия. Единица должна выставляться в случае, если пользовательский ответ '
    'находится совсем в другой плоскости относительно правильного. Двойка должна выставляться в случае, '
    'если пользовательский ответ находится в той же плоскости, что и правильный, но всё равно является неверным. '
    'Тройка должна выставляться в случае, если пользовательский ответ близок к правильному, но является очень '
    'неполным и/или плохо сформулированным. Четвёрка должна выставляться в случае, если пользовательский ответ '
    'является правильным, но немного неполным или слегка некорректно сформулированным. Пятерка должна '
    'выставляться в случае, если пользовательский ответ является полностью правильным, либо имеет незначительные '
    'ошибки в формулировке и/или является совсем слегка неполным. Ты также должен предоставлять небольшое пояснение, '
    'почему ты выставил ту или иную оценку.'
)


class ComparingAgentOutputSchema(BaseModel):
    num: int = Field(
        description='Целое число, оценивающее ответ пользователя от 1 до 5.', 
        json_schema_extra={
            'minimum': 1,
            'maximum': 5
        }
    )
    explanation: str = Field(
        description='Краткое пояснение длиной не более 300 символов, почему была выставлена соответствующая оценка.'
    )


class EstimatingAgentOutputSchema(BaseModel):
    true_answer: str = Field(
        description='Правильный, по твоему мнению, ответ на вопрос длиной не более 300 символов.', 
    )
    num: int = Field(
        description='Целое число от 1 до 5, оценивающее ответ пользователя.', 
        json_schema_extra={
            'minimum': 1,
            'maximum': 5
        }
    )
    explanation: str = Field(
        description='Краткое пояснение длиной не более 300 символов, почему была выставлена соответствующая оценка.'
    )


class ComparingAgent(Agent):
    def __init__(self, name: str):
        config = get_config()

        openai_model = config['EXAMINER_AGENTS']['COMPARING_AGENT_OPENAI_MODEL']
        reasoning_effort = config['EXAMINER_AGENTS']['COMPARING_AGENT_REASONING_EFFORT']
        verbosity = config['EXAMINER_AGENTS']['COMPARING_AGENT_VERBOSITY']

        super().__init__( 
            name=name,
            instructions=COMPARING_AGENT_INSTRUCTIONS,
            model=openai_model,
            model_settings=ModelSettings(
                reasoning=Reasoning(effort=reasoning_effort),
                verbosity=verbosity,
                store=False
            ),
            output_type=ComparingAgentOutputSchema,
        )
    
    def get_estimation(self,
            theme: str,
            subtheme: str,
            question: str, 
            user_answer: str, 
            true_answer: str, 
            tracing_disabled: bool
        ):
        response = asyncio.run(
            Runner.run(self,
                input=f'Тема: {theme}. Подтема: {subtheme}. Вопрос: {question}. Правильный ответ: {true_answer}. Ответ пользователя: {user_answer}.',
                run_config=RunConfig(tracing_disabled=tracing_disabled)
            )
        )

        output: ComparingAgentOutputSchema = response.final_output

        return QuestionAnswerEstimation(
            theme=theme, 
            subtheme=subtheme, 
            question=question,
            user_answer=user_answer,
            true_answer=true_answer,
            num=output.num,
            explanation=output.explanation
        )


class EstimatingAgent(Agent):
    def __init__(self, name: str):
        config = get_config()

        openai_model = config['EXAMINER_AGENTS']['ESTIMATING_AGENT_OPENAI_MODEL']
        reasoning_effort = config['EXAMINER_AGENTS']['ESTIMATING_AGENT_REASONING_EFFORT']
        verbosity = config['EXAMINER_AGENTS']['ESTIMATING_AGENT_VERBOSITY']

        super().__init__( 
            name=name,
            instructions=ESTIMATING_AGENT_INSTRUCTIONS,
            model=openai_model,
            model_settings=ModelSettings(reasoning=Reasoning(
                effort=reasoning_effort), 
                verbosity=verbosity,
                store=False
            ),
            output_type=EstimatingAgentOutputSchema,
            tools=[WebSearchTool()]
        )
    
    def get_estimation(self,
        theme: str,
        subtheme: str,
        question: str, 
        user_answer: str, 
        tracing_disabled: bool
    ):
        response = asyncio.run(
            Runner.run(self,
                input=f'Тема: {theme}. Подтема: {subtheme}. Вопрос: {question}. Ответ пользователя: {user_answer}.',
                run_config=RunConfig(tracing_disabled=tracing_disabled)
            )
        )

        output: EstimatingAgentOutputSchema = response.final_output
        
        return QuestionAnswerEstimation(
            theme=theme,
            subtheme=subtheme,
            question=question,
            user_answer=user_answer,
            true_answer=output.true_answer,
            num=output.num, 
            explanation=output.explanation
        )


class ExaminerAgentException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class ExaminerAgentRateLimitError(ExaminerAgentException):
    def __init__(self, message: str):
        super().__init__(message)


class ExaminerAgent:
    def __init__(self):
        self.name = 'Бот-экзаменатор.'
        self.comparing_agent = ComparingAgent(self.name)
        self.estimating_agent = EstimatingAgent(self.name)
    
    def get_estimation(self, theme: str, subtheme: str, question: str, user_answer: str, true_answer: str | None = None):
        app_env = getenv('APP_ENV')

        if app_env == 'development':
            tracing_disabled = False
        else:
            tracing_disabled = True
        
        try:
            if true_answer:
                return self.comparing_agent.get_estimation(
                    theme=theme,
                    subtheme=subtheme, 
                    question=question,
                    user_answer=user_answer,
                    true_answer=true_answer, 
                    tracing_disabled=tracing_disabled
                )
            else:
                return self.estimating_agent.get_estimation(
                    theme=theme, 
                    subtheme=subtheme, 
                    question=question, 
                    user_answer=user_answer, 
                    tracing_disabled=tracing_disabled
                )
        except RateLimitError as e:
            raise ExaminerAgentRateLimitError(f'Examiner agent rate limit error: {e}') from e
        except AgentsException as e:
            raise ExaminerAgentException(f'Examiner agent response exception: {e}') from e
