class Estimation:
    def __init__(self, obj_type: str, num: int, explanation: str | None = None, obj_name: str | None = None):
        self.obj_type = obj_type
        self.num = num
        self.explanation = explanation
        self.obj_name = obj_name


class QuestionAnswerEstimation(Estimation):
    def __init__(self, 
        theme: str,
        subtheme: str,
        question: str,
        user_answer: str,
        true_answer: str,
        num: int,
        explanation: str | None = None
    ):
        super().__init__('question', num, explanation)
        
        self.theme = theme
        self.subtheme = subtheme
        self.question = question
        self.user_answer = user_answer
        self.true_answer = true_answer


class GeneralEstimation(Estimation):
    def __init__(self, obj_type: str, num: int, obj_name: str | None = None):
        super().__init__(obj_type, num, obj_name=obj_name)
