import tkinter as tk
from tkinter import messagebox
from random import shuffle


class QuizGame:
    def __init__(self, quiz_data):
        self.root = tk.Tk()
        self.root.title("Quiz Game")
        self.quiz_data = quiz_data
        self.total_questions = len(quiz_data)
        self.current_question_index = 0
        self.user_answers = []
        self.score = 0

        self.question_label = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", font=("Arial", 12), width=40, height=2, command=lambda i=i: self.choose_option(i))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="Timer: 0", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        self.play_again_button = tk.Button(self.root, text="Play Again", font=("Arial", 12), width=20, command=self.play_again)
        self.play_again_button.pack(pady=10)

        self.next_question()

        self.root.mainloop()

    def next_question(self):
        if self.current_question_index < self.total_questions:
            question, options, correct_answer = self.quiz_data[self.current_question_index]
            self.reset_options()
            self.question_label.config(text=f"Question {self.current_question_index + 1}/{self.total_questions}: {question}")
            self.start_timer()
            self.update_options(options)
            self.correct_answer = correct_answer
            self.current_question_index += 1
        else:
            self.show_result()

    def reset_options(self):
        for button in self.option_buttons:
            button.config(bg="white", state=tk.NORMAL)

    def update_options(self, options):
        options_with_indices = list(enumerate(options))
        shuffle(options_with_indices)
        for i, option in options_with_indices:
            self.option_buttons[i].config(text=option)

    def choose_option(self, option_index):
        self.stop_timer()
        self.evaluate_answer(option_index)
        self.disable_options()
        self.update_score()
        self.root.after(2000, self.next_question)

    def evaluate_answer(self, option_index):
        if option_index == self.correct_answer:
            self.option_buttons[option_index].config(bg="green")
            self.user_answers.append(1)
        else:
            self.option_buttons[option_index].config(bg="red")
            self.option_buttons[self.correct_answer].config(bg="green")
            self.user_answers.append(0)

    def disable_options(self):
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)

    def update_score(self):
        self.score = sum(self.user_answers)
        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")

    def show_result(self):
        self.stop_timer()
        messagebox.showinfo("Quiz Result", f"You scored {self.score}/{self.total_questions}!")
        self.play_again_button.config(state=tk.NORMAL)

    def start_timer(self):
        self.timer_value = 30
        self.update_timer()

    def stop_timer(self):
        self.root.after_cancel(self.timer_id)

    def update_timer(self):
        self.timer_label.config(text=f"Timer: {self.timer_value}")
        if self.timer_value > 0:
            self.timer_value -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.disable_options()
            self.root.after(2000, self.next_question)

    def play_again(self):
        self.current_question_index = 0
        self.user_answers = []
        self.score = 0
        self.reset_options()
        self.next_question()
        self.play_again_button.config(state=tk.DISABLED)


def read_quiz_data(filename):
    quiz_data = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            question, options, correct_answer = line.strip().split(";")
            options = options.split(",")
            correct_answer = int(correct_answer)
            quiz_data.append((question, options, correct_answer))
    return quiz_data


quiz_data = read_quiz_data("quiz_data.txt")
game = QuizGame(quiz_data)
