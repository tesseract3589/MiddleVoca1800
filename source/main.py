import tkinter as tk
import random
import re
import os
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()
root.title("단어 암기 프로그램")
root.geometry("800x600")

# 현재 출제된 문제의 정답 저장하는 리스트
current_answers = []

# 출력 영역
text_area = ScrolledText(
    root,
    width=70,
    height=20,
    font=("맑은 고딕", 11)
)

text_area.pack(fill="both", expand=True, padx=10, pady=10)

def load_word_list(voca_num):
    # __file__ 속성이 없을 경우(실행 환경에 따라)를 대비한 예외 처리
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        current_dir = os.getcwd()
    project_dir = os.path.dirname(current_dir)

    filename = os.path.join(
        project_dir,
        "data",
        f"voca{voca_num}.txt"
    )

    words = []

    # 먼저 파일이 존재하는지 확인
    if not os.path.exists(filename):
        raise FileNotFoundError(f"voca{voca_num}.txt 파일을 찾을 수 없습니다.\n경로: {filename}")

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            m = re.match(r"(\d+)\s+(\S+)\s+(.+)", line)

            if m:
                num = int(m.group(1))
                word = m.group(2)
                meaning = m.group(3)

                words.append({
                    "num": num,
                    "word": word,
                    "meaning": meaning
                })

    return words


def make_test(mode):
    global current_answers  # 정답 저장을 위한 전역 변수 사용 선언
    try:
        voca_num = int(entry_voca.get())
        count = int(entry_count.get())

        words = load_word_list(voca_num)

        if count > len(words):
            count = len(words)

        selected = random.sample(words, count)

        text_area.delete("1.0", tk.END)

        title = (
            "[뜻 보고 단어 쓰기]\n\n"
            if mode == "meaning_to_word"
            else "[단어 보고 뜻 쓰기]\n\n"
        )

        text_area.insert(tk.END, title)

        # 새로운 문제를 만들 때마다 이전 정답 기록을 초기화
        current_answers = []

        for idx, item in enumerate(selected, start=1):

            if mode == "meaning_to_word":
                question = item["meaning"] # 문제는 '뜻'
                answer = item["word"]  # 정답은 '단어'

            else:
                question = item["word"] # 문제는 '단어'
                answer = item["meaning"]  # 정답은 '뜻'

            text_area.insert(
                tk.END,
                f"{idx}. {question}\n\n"
            )

            # 정답 공개를 위해 번호와 정답을 리스트에 저장
            current_answers.append(f"{idx}번 정답: {answer}")

    except Exception as e:
        messagebox.showerror("오류", str(e))

def show_word_list():
    try:
        voca_num = int(entry_voca.get())

        words = load_word_list(voca_num)

        text_area.delete("1.0", tk.END)

        text_area.insert(
            tk.END,
            f"[단어장 {voca_num} 전체 목록]\n\n"
        )

        for item in words:
            text_area.insert(
                tk.END,
                f'{item["num"]}. {item["word"]} : {item["meaning"]}\n'
            )

    except Exception as e:
        messagebox.showerror("오류", str(e))

# 정답 확인 버튼을 눌렀을 때 실행될 함수
def show_answers():
    if not current_answers:
        messagebox.showwarning(
            "경고", "출제된 문제가 없습니다. 먼저 문제를 만들어주세요."
        )
        return

    # 기존 문제 내용 아래에 구분선을 긋고 정답을 이어서 출력
    text_area.insert(
        tk.END, "\n" + "=" * 40 + "\n\n   [ 정답 확인 ]   \n\n" + "=" * 40 + "\n\n"
    )

    for ans in current_answers:
        text_area.insert(tk.END, f"{ans}\n")

    # 정답 출력 후 스크롤을 맨 아래로 이동
    text_area.see(tk.END)


# --- UI 레이아웃 설정 ---

# 단어장 번호

tk.Label(root, text="단어장 번호").pack()

entry_voca = tk.Entry(root)
entry_voca.pack()

# 문제 수

tk.Label(root, text="문제 수").pack()

entry_count = tk.Entry(root)
entry_count.pack()

# 버튼 영역

frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

btn1 = tk.Button(
    frame_btn,
    text="뜻 → 단어",
    width=15,
    command=lambda: make_test("meaning_to_word")
)

btn1.pack(side=tk.LEFT, padx=5)

btn2 = tk.Button(
    frame_btn,
    text="단어 → 뜻",
    width=15,
    command=lambda: make_test("word_to_meaning")
)

btn2.pack(side=tk.LEFT, padx=5)

# 정답 확인 버튼
btn_answer = tk.Button(
    frame_btn, text="정답 확인", width=13, fg="blue", command=show_answers
)
btn_answer.pack(side=tk.LEFT, padx=5)

btn3 = tk.Button(
    frame_btn,
    text="전체 단어 보기",
    width=15,
    command=show_word_list
)

btn3.pack(side=tk.LEFT, padx=5)

# 창 뜨게 만드는 코드
root.mainloop()