# --- Creates GUI for the Search Engine --- 

import tkinter as tk

from inverted_index import Inverted_index
from rankings.tf_idf import Tf_idf
from rankings.vector_space import Vector_space
from rankings.bm25 import BM25

class Gui():

    _ranking: Tf_idf

    _input_box: tk.Entry

    _output_box: tk.Text

    _current_ranking_label: tk.Label

    def __init__(self, ranking: Tf_idf) -> None:
        
        self._ranking = ranking

    def set_ranking(self, ranking: Tf_idf) -> None:

        self._ranking = ranking

    def set_input_box(self, input_box: tk.Entry) -> None:

        self._input_box = input_box

    def set_output_box(self, output_box: tk.Text) -> None:

        self._output_box = output_box

    def set_current_ranking_label(self, label: tk.Label) -> None:

        self._current_ranking_label = label

    def update_output(self, output_string: str) -> None:

        self._output_box.delete("1.0", tk.END)

        self._output_box.insert("1.0", output_string)

    def update_current_ranking_label(self, label_string: str) -> None:

        self._current_ranking_label.config(text=label_string)
    
    def use_tf_idf_ranking(self) -> None:

        self.set_ranking(Tf_idf(self._ranking.get_index()))

        self.update_output("Now using TF-IDF Ranking!")

        self.update_current_ranking_label("Current Ranking: TF-IDF")

    def use_vector_space_ranking(self) -> None:

        self.set_ranking(Vector_space(self._ranking.get_index()))

        self.update_output("Now using Vector Space Ranking! (Extension of TF-IDF)")

        self.update_current_ranking_label("Current Ranking: Vector Space")

    def use_bm25_ranking(self) -> None:

        self.set_ranking(BM25(self._ranking.get_index()))

        self.update_output("Now using BM25 Ranking! (Extension of TF-IDF)")

        self.update_current_ranking_label("Current Ranking: BM25")

    def run(self) -> None:

        root: tk.Tk = tk.Tk()

        SCREEN_WIDTH: int = root.winfo_screenwidth()
        SCREEN_HEIGHT: int = root.winfo_screenheight()

        LARGE_FONT: tuple = ("Arial", 16, "bold")
        SMALL_FONT: tuple = ("Arial", 10, "italic")
    
        root.title("Search Engine Project")
        root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')

        input_label: tk.Label = tk.Label(root, text="Enter Query:", font=LARGE_FONT)
        input_label.place(relx=0.5, rely=0.1, anchor="center")

        input_box: tk.Entry = tk.Entry(root, width=int(SCREEN_WIDTH*0.05))
        input_box.place(relx=0.5, rely=0.15, anchor="center")

        self.set_input_box(input_box)

        output_label: tk.Label = tk.Label(root, text="Query Result:", font=LARGE_FONT)
        output_label.place(relx = 0.5, rely = 0.35, anchor="center")

        output_box: tk.Text = tk.Text(root)
        output_box.place(relx = 0.5, rely = 0.4, anchor="n")

        self.set_output_box(output_box)

        current_ranking_label: tk.Label = tk.Label(root, text="Current Ranking: TF-IDF", font = SMALL_FONT)
        current_ranking_label.place(relx=0.75, rely=0.3, anchor="center")

        self.set_current_ranking_label(current_ranking_label)

        input_button: tk.Button = tk.Button(root, text="Run Query", command=lambda: self.update_output(self._ranking.process_query(self._input_box.get())))
        input_button.place(relx=0.5, rely=0.2, anchor="center")

        tf_idf_ranking_button: tk.Button = tk.Button(root, text="Use TF-IDF Ranking", command=lambda: self.use_tf_idf_ranking())
        tf_idf_ranking_button.place(relx=0.75, rely=0.15, anchor="center")

        vector_space_ranking_button: tk.Button = tk.Button(root, text="Use Vector Space Ranking", command=lambda: self.use_vector_space_ranking())
        vector_space_ranking_button.place(relx=0.75, rely=0.2, anchor="center")

        bm25_ranking_button: tk.Button = tk.Button(root, text="Use BM25 Ranking", command=lambda: self.use_bm25_ranking())
        bm25_ranking_button.place(relx=0.75, rely=0.25, anchor="center")

        root.mainloop()

# --- Testing ---

def test_gui():

    texts: list = []

    with open("test_data/_ai790XSyjDGrcj7og9LdvGCsBC_SXvb.html", encoding = "utf-8") as f:

        texts.append(f.read())
    
    with open("test_data/_avN5V1KDCAtN5Sh4Tm4YsuNzaHVTx8w.html", encoding = "utf-8") as f:

        texts.append(f.read())

    with open("test_data/_bua93nkRXBBWiJ8ulRPXASuK0xbcL8l.html", encoding = "utf-8") as f:

        texts.append(f.read())

    docs: dict = {"Luxor 3": texts[0], "Final Fantasy Tactics A2": texts[1], "Super Paper Mario": texts[2]}

    index: Inverted_index = Inverted_index()
    index.create(docs)

    ranking: Tf_idf = Tf_idf(index)

    gui: Gui = Gui(ranking)
    gui.run()

if __name__ == "__main__":

    test_gui()