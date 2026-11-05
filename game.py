"""
QuizGame 클래스: 퀴즈 게임 전체를 관리하는 클래스
"""

import json
import os
from quiz import Quiz
from quiz_data import get_additional_quizzes


class QuizGame:
    """
    퀴즈 게임 전체를 관리하는 클래스

    속성:
        quizzes (list): Quiz 객체 리스트
        best_score (int): 최고 점수
        data_file (str): 데이터 저장 파일 경로
    """

    def __init__(self, data_file="state.json"):
        """
        QuizGame 객체 초기화

        Args:
            data_file (str): 데이터 저장 파일 경로 (기본값: state.json)
        """
        self.data_file = data_file
        self.quizzes = []
        self.best_score = 0

        # 저장된 데이터 불러오기
        self.load_data()

    def load_data(self):
        """
        JSON 파일에서 데이터 불러오기
        파일이 없거나 손상되었으면 기본 데이터로 초기화
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 퀴즈 데이터 로드
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]

                # 최고 점수 로드
                self.best_score = data.get("best_score", 0)

                if self.quizzes:
                    print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)\n")

            except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
                print(f"⚠️  데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.\n")
                self.quizzes = self._get_default_quizzes()
                self.best_score = 0
        else:
            # 첫 실행: 기본 데이터 사용
            self.quizzes = self._get_default_quizzes()
            self.best_score = 0

    def save_data(self):
        """
        현재 퀴즈와 점수를 JSON 파일에 저장
        """
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score
            }

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except IOError as e:
            print(f"❌ 파일 저장 중 오류가 발생했습니다: {e}")

    def _get_default_quizzes(self):
        """
        기본 과학 퀴즈 10개 반환 (기본 5개 + 추가 5개)

        Returns:
            list: 기본 Quiz 객체 리스트
        """
        default_quizzes = [
            Quiz(
                "태양이 주로 구성된 원소는?",
                ["산소", "수소", "헬륨", "질소"],
                2
            ),
            Quiz(
                "인간의 뇌는 몸 무게의 약 몇 %를 차지할까?",
                ["5%", "10%", "2%", "15%"],
                3
            ),
            Quiz(
                "DNA의 이중나선 구조를 발견한 과학자는?",
                ["다윈", "뉴턴", "왓슨과 크릭", "파스퇴르"],
                3
            ),
            Quiz(
                "빛의 속도는 초당 약 몇 km일까?",
                ["3만 km", "30만 km", "300만 km", "3백만 km"],
                2
            ),
            Quiz(
                "화석 연료 중 가장 오래된 것은?",
                ["석유", "석탄", "천연가스", "갈탄"],
                2
            ),
        ]

        # 추가 퀴즈 통합
        default_quizzes.extend(get_additional_quizzes())

        return default_quizzes

    def display_menu(self):
        """
        메인 메뉴 출력
        """
        print("\n" + "=" * 50)
        print("        🎯 나만의 과학 퀴즈 게임 🎯")
        print("=" * 50)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 50)

    def get_menu_choice(self):
        """
        메뉴 선택 입력받기

        Returns:
            int: 선택한 메뉴 번호 (1-5)
        """
        while True:
            try:
                choice = input("\n선택: ").strip()

                if not choice:
                    print("⚠️  입력을 해주세요.")
                    continue

                choice = int(choice)

                if 1 <= choice <= 5:
                    return choice
                else:
                    print("⚠️  1-5 사이의 숫자를 입력하세요.")

            except ValueError:
                print("⚠️  숫자를 입력하세요.")

    def play_quiz(self):
        """
        퀴즈 풀기 기능
        """
        if not self.quizzes:
            print("❌ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)\n")

        correct_count = 0
        total_count = len(self.quizzes)

        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display(i)

            while True:
                try:
                    answer_str = input("\n정답 입력 (1-4): ").strip()

                    if not answer_str:
                        print("⚠️  정답을 입력하세요.")
                        continue

                    answer = int(answer_str)

                    if 1 <= answer <= 4:
                        break
                    else:
                        print("⚠️  1-4 사이의 숫자를 입력하세요.")

                except ValueError:
                    print("⚠️  숫자를 입력하세요.")

            # 정답 확인
            if quiz.check_answer(answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer}번)")

        # 결과 계산
        score = int((correct_count / total_count) * 100)

        print("\n" + "=" * 50)
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        # 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
            self.save_data()

        print("=" * 50)

    def add_quiz(self):
        """
        새로운 퀴즈 추가
        """
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        # 문제 입력
        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("⚠️  문제를 입력하세요.")
            return

        # 선택지 입력
        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if not choice:
                print(f"⚠️  선택지 {i}를 입력하세요.")
                return
            choices.append(choice)

        # 정답 입력
        while True:
            try:
                answer_str = input("정답 번호 (1-4): ").strip()

                if not answer_str:
                    print("⚠️  정답을 입력하세요.")
                    continue

                answer = int(answer_str)

                if 1 <= answer <= 4:
                    break
                else:
                    print("⚠️  1-4 사이의 숫자를 입력하세요.")

            except ValueError:
                print("⚠️  숫자를 입력하세요.")

        # 퀴즈 추가
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        print("\n✅ 퀴즈가 추가되었습니다!")
        self.save_data()

    def show_quizzes(self):
        """
        등록된 퀴즈 목록 출력
        """
        if not self.quizzes:
            print("\n❌ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 50)

        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")

        print("-" * 50)

    def show_score(self):
        """
        최고 점수 출력
        """
        print("\n🏆 최고 점수:", end=" ")

        if self.best_score == 0:
            print("아직 풀지 않았습니다.")
        else:
            total = len(self.quizzes)
            correct = int((self.best_score / 100) * total)
            print(f"{self.best_score}점 ({total}문제 중 {correct}문제 정답)")

    def run(self):
        """
        게임 메인 루프
        """
        while True:
            try:
                self.display_menu()
                choice = self.get_menu_choice()

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("\n👋 게임을 종료합니다. 안녕!")
                    self.save_data()
                    break

            except KeyboardInterrupt:
                print("\n\n⚠️  프로그램이 중단되었습니다.")
                self.save_data()
                break
            except EOFError:
                print("\n\n⚠️  입력 스트림이 종료되었습니다.")
                self.save_data()
                break
