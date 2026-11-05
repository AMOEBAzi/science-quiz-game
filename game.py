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
        JSON 파일에서 데이터 불러오기 (시작 시 자동 호출)

        우선순위:
        1. state.json 파일 존재 여부 확인
        2. JSON 형식 검증 (JSONDecodeError 캐치)
        3. 필드 완전성 검증 (KeyError 캐치)
        4. 손상 시 기본 데이터(10개 퀴즈)로 자동 복구

        예외 처리:
        - FileNotFoundError: 첫 실행 시 기본값 사용
        - JSONDecodeError: 파일 손상 시 기본값으로 복구
        - KeyError: 필드 누락 시 기본값으로 복구
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

        저장 시점:
        - 최고 점수 갱신 시 (play_quiz 내부)
        - 퀴즈 추가 시 (add_quiz 내부)
        - 프로그램 종료 시 (run 메인 루프)
        - Ctrl+C, EOFError 처리 시 (안전한 종료)

        저장 형식:
        - UTF-8 인코딩 (한글 지원)
        - 들여쓰기 2칸 (가독성)
        - ensure_ascii=False (한글 직접 표현)

        예외 처리:
        - IOError: 파일 쓰기 오류 시 사용자에게 알림
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
        메뉴 선택 입력받기 - 사용자 입력 검증

        입력 검증 규칙:
        1. 빈 입력 감지: strip() 후 길이 확인
        2. 숫자 검증: int() 변환 시도 (ValueError 캐치)
        3. 범위 확인: 1-5 사이만 허용

        오류 메시지:
        - "⚠️  입력을 해주세요." - 빈 입력
        - "⚠️  숫자를 입력하세요." - 비숫자 입력
        - "⚠️  1-5 사이의 숫자를 입력하세요." - 범위 초과

        특수 처리:
        - 공백 제거 (strip) - 앞뒤 공백 처리
        - 무한 루프 - 올바른 입력까지 반복 요청

        Returns:
            int: 1-5 사이의 유효한 선택 번호
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
        퀴즈 풀기 기능: 모든 퀴즈를 순서대로 출제하고 점수 계산

        실행 흐름:
        1. 등록된 퀴즈 개수 확인
        2. 각 퀴즈를 Quiz.display()로 출력
        3. 사용자 입력 수집 및 검증 (1-4 범위, 숫자 확인)
        4. Quiz.check_answer()로 정답 판정
        5. 점수 계산 및 최고 점수 갱신 시 저장

        입력 검증:
        - 빈 입력 감지 (strip() 후 확인)
        - 비숫자 입력 처리 (ValueError 캐치)
        - 범위 초과 감지 (1-4 범위)

        특수 처리:
        - 최고 점수 갱신 시에만 save_data() 호출 (성능 최적화)
        - 미실행 시 저장하지 않음 (의도하지 않은 점수 기록 방지)
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
        새로운 퀴즈 추가 기능

        입력 단계:
        1. 문제 입력: 빈 입력 검증
        2. 선택지 4개 입력: 각 선택지마다 빈 입력 검증
        3. 정답 번호: get_menu_choice()와 동일한 입력 검증 (1-4)

        특수 처리:
        - 선택지 4개 모두 필수 입력 (하나라도 비어있으면 중단)
        - 정답은 1-4 범위만 허용 (무한 루프로 재입력 유도)
        - 모든 입력 수집 후 Quiz 객체 생성 및 append
        - 추가 완료 후 즉시 save_data() 호출 (영속성 보장)

        예외 처리:
        - 입력 중단 시 return (함수 종료)
        - 정상 완료 시 저장 및 완료 메시지 출력
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
