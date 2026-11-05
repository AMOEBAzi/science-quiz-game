"""
main.py: 과학 퀴즈 게임 메인 프로그램
"""

from game import QuizGame


def main():
    """
    프로그램 시작점
    """
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
