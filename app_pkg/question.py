class Question:

    def __init__(self, question_id="", question="", category="", answer=""): # type is build-in category so I changed it to category
        self.question_id = question_id
        self.category = category
        self.question = question
        self.answer = answer
        # 我在思考要不要弄个choice column/attribute还有score啥的

    def __str__(self):
        return f"Question id:{self.question_id} \nQuestion:{self.question} \nCategory:{self.category} \n" \
               f"Answer:{self.answer}"
