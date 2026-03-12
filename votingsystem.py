import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os

parties = ["NOTA", "Party A", "Party B", "Party C", "Party D"]
db_path = "voting_system.db"

# SQLite Setup
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS votes")  # Remove this line in production
    cursor.execute("""
        CREATE TABLE votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT UNIQUE,
            age INTEGER,
            party TEXT
        )
    """)
    conn.commit()
    conn.close()

def has_voted(user_code):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM votes WHERE user_code = ?", (user_code,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_vote(party, user_code, age):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO votes (user_code, age, party) VALUES (?, ?, ?)", (user_code, age, party))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def get_detailed_votes():
    vote_details = {party: [] for party in parties}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, age, party FROM votes")
    for user_code, age, party in cursor.fetchall():
        if party in vote_details:
            vote_details[party].append((user_code, age))
    conn.close()
    return vote_details

def cast_vote():
    code = code_entry.get().strip()
    age_input = age_entry.get().strip()
    selected = selected_party.get()

    if not code:
        messagebox.showwarning("Error", "Enter your unique code.")
        return
    if not age_input.isdigit():
        messagebox.showwarning("Error", "Enter a valid numeric age.")
        return

    age = int(age_input)
    if age < 18:
        messagebox.showerror("Underage", "You must be 18 or older to vote.")
        return

    if not selected:
        messagebox.showwarning("Error", "Please select a party to vote for.")
        return
    if has_voted(code):
        messagebox.showerror("Duplicate", "You have already voted!")
        return
    if save_vote(selected, code, age):
        messagebox.showinfo("Success", f"Vote cast for {selected}")
        code_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        selected_party.set(None)
    else:
        messagebox.showerror("Error", "Failed to cast vote.")

def show_results():
    vote_details = get_detailed_votes()
    vote_counts = {party: len(vote_details[party]) for party in vote_details}

    max_votes = max(vote_counts.values()) if vote_counts else 0
    min_votes = min(vote_counts.values()) if vote_counts else 0

    majority = [p for p in vote_counts if vote_counts[p] == max_votes]
    minority = [p for p in vote_counts if vote_counts[p] == min_votes]

    result_window = tk.Toplevel(root)
    result_window.title("Voting Results")
    result_window.attributes("-fullscreen", True)
    result_window.configure(bg="#1f2833")

    tk.Label(result_window, text="Voting Results", font=("Helvetica", 36, "bold"),
             fg="#66fcf1", bg="#1f2833").pack(pady=40)

    for party in parties:
        color = "#45a29e" if party in majority else "#e74c3c" if party in minority else "#c5c6c7"
        tk.Label(result_window, text=f"{party}: {vote_counts[party]} vote{'s' if vote_counts[party] != 1 else ''}",
                 font=("Helvetica", 24, "bold"), fg=color, bg="#1f2833").pack(pady=10)

    summary_text = f"\nMajority: {', '.join(majority)} with {max_votes} vote(s)\n"
    summary_text += f"Minority: {', '.join(minority)} with {min_votes} vote(s)"
    tk.Label(result_window, text=summary_text, font=("Helvetica", 20),
             fg="#f1c40f", bg="#1f2833").pack(pady=30)

    tk.Button(result_window, text="Close Results", command=result_window.destroy,
              font=("Helvetica", 16), bg="#0b0c10", fg="white", padx=20, pady=10).pack(pady=20)

    result_window.bind("<Escape>", lambda e: result_window.destroy())

# GUI Setup
root = tk.Tk()
root.title("Voting System with SQLite")
root.attributes("-fullscreen", True)
root.configure(bg="#0b0c10")

# Background image setup
try:
    bg_img = Image.open("voting_bg.png")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    bg_img_resized = bg_img.resize((screen_width, screen_height), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img_resized)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Background image not loaded:", e)

frame = tk.Frame(root, bg='white', bd=6)
frame.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(frame, text="Enter Your Unique Code", bg="white", font=('Helvetica', 16)).pack(pady=10)
code_entry = tk.Entry(frame, font=('Helvetica', 16), width=30)
code_entry.pack(pady=5)

tk.Label(frame, text="Enter Your Age", bg="white", font=('Helvetica', 16)).pack(pady=10)
age_entry = tk.Entry(frame, font=('Helvetica', 16), width=30)
age_entry.pack(pady=5)

tk.Label(frame, text="Select a Party", bg="white", font=('Helvetica', 16)).pack(pady=10)
selected_party = tk.StringVar()
for party in parties:
    tk.Radiobutton(frame, text=party, variable=selected_party, value=party,
                   bg="white", font=('Helvetica', 14)).pack(anchor="w")

tk.Button(frame, text="Cast Vote", command=cast_vote, font=('Helvetica', 14),
          bg="#1abc9c", fg="white", padx=20, pady=5).pack(pady=15)

tk.Button(frame, text="Show Results", command=show_results, font=('Helvetica', 14),
          bg="#3498db", fg="white", padx=20, pady=5).pack(pady=5)
root.bind("<Escape>", lambda e: root.destroy())
init_db()
root.mainloop()
