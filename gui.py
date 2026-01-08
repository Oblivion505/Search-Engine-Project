# --- Creates GUI for the Search Engine --- 

import tkinter as tk

from inverted_index import Inverted_index
from tf_idf import Tf_idf

def update_gui(output_string: str, output_box: tk.Text) -> None:

    output_box.delete("1.0", tk.END)

    output_box.insert("1.0", output_string)

def run_gui(ranking: Tf_idf) -> None:

    root: tk.Tk = tk.Tk()

    SCREEN_WIDTH: int = root.winfo_screenwidth()
    SCREEN_HEIGHT: int = root.winfo_screenheight()

    TEXT_FONT: tuple = ("Arial", 16, "bold")
    
    root.title("Search Engine Project")
    root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')

    input_label: tk.Label = tk.Label(root, text="Enter Query:", font=TEXT_FONT)
    input_label.place(relx=0.5, rely=0.1, anchor="center")

    input_box: tk.Entry = tk.Entry(root, width=int(SCREEN_WIDTH*0.05))
    input_box.place(relx=0.5, rely=0.15, anchor="center")

    output_label: tk.Label = tk.Label(root, text="Query Result:", font=TEXT_FONT)
    output_label.place(relx = 0.5, rely = 0.35, anchor="center")

    output_box: tk.Text = tk.Text(root)
    output_box.place(relx = 0.5, rely = 0.6, anchor="center")

    input_button: tk.Button = tk.Button(root, text="Run Query", command=lambda: update_gui(ranking.process_query(input_box.get()), output_box))
    input_button.place(relx=0.5, rely=0.2, anchor="center")

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
    index.new_index(docs)

    ranking: Tf_idf = Tf_idf(index)

    run_gui(ranking)

if __name__ == "__main__":

    test_gui()