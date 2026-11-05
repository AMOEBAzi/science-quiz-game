"""
Quiz 클래스: 개별 퀴즈를 표현하는 클래스
"""


class Quiz:
    """
    퀴즈 하나를 표현하는 클래스

    속성:
        question (str): 문제
        choices (list): 선택지 4개
        answer (int): 정답 (1-4)
    """

    def __init__(self, question, choices, answer):
        """
        Quiz 객체 초기화

        Args:
            question (str): 문제 문장
            choices (list): 4개의 선택지 [선택지1, 선택지2, 선택지3, 선택지4]
            answer (int): 정답 번호 (1-4)
        """
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, question_number):
        """
        퀴즈를 화면에 출력

        Args:
            question_number (int): 몇 번째 문제인지
        """
        print(f"\n{'-' * 50}")
        print(f"[문제 {question_number}]")
        print(f"{self.question}\n")

        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        """
        사용자의 답변이 정답인지 확인

        Args:
            user_answer (int): 사용자가 입력한 답 (1-4)

        Returns:
            bool: 정답이면 True, 오답이면 False
        """
        return user_answer == self.answer

    def to_dict(self):
        """
        Quiz 객체를 딕셔너리로 변환 (JSON 저장용)

        Returns:
            dict: {'question': 문제, 'choices': [선택지들], 'answer': 정답}
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(data):
        """
        딕셔너리에서 Quiz 객체 생성 (JSON 로드용)

        Args:
            data (dict): {'question': 문제, 'choices': [선택지들], 'answer': 정답}

        Returns:
            Quiz: 생성된 Quiz 객체
        """
        return Quiz(data["question"], data["choices"], data["answer"])
