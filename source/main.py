import tkinter as tk
import random
import re
import os
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()
root.title("단어 암기 프로그램")
root.geometry("800x600")

# 출력 영역
text_area = ScrolledText(
    root,
    width=70,
    height=25,
    font=("맑은 고딕", 11)
)

text_area.pack(fill="both", expand=True, padx=10, pady=10)

def load_word_list(voca_num):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)

    filename = os.path.join(
        project_dir,
        "data",
        f"voca{voca_num}.txt"
    )

    words = []

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

        for idx, item in enumerate(selected, start=1):

            if mode == "meaning_to_word":
                question = item["meaning"]

            else:
                question = item["word"]

            text_area.insert(
                tk.END,
                f"{idx}. {question}\n\n"
            )

    except Exception as e:
        messagebox.showerror("오류", str(e))


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

# 창 뜨게 만드는 코드
root.mainloop()