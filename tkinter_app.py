# --- tkinter_app.py (Tkinter Frontend) ---
import tkinter as tk
from tkinter import messagebox
import requests


def predict_disease():
    symptoms = entry.get()
    symptom_list = [s.strip() for s in symptoms.split(',') if s.strip()]

    if not symptom_list:
        messagebox.showerror("Input Error", "Please enter at least one symptom.")
        return

    try:
        response = requests.post("http://127.0.0.1:5000/api/predict", json={'symptoms': symptom_list})
        data = response.json()

        if 'error' in data:
            messagebox.showerror("Error", data['error'])
        else:
            result_text = f"""
Predicted Disease: {data['predicted_disease']}
Description: {data['description']}

Precautions:
- {data['precautions'][0]}
- {data['precautions'][1]}
- {data['precautions'][2]}
- {data['precautions'][3]}

Medications: {', '.join(data['medications'])}
Diet: {', '.join(data['diet'])}
Workout: {', '.join(data['workout'])}
            """
            output.delete("1.0", tk.END)
            output.insert(tk.END, result_text)

    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect to API: {e}")


def show_about():
    about_win = tk.Toplevel(root)
    about_win.title("About")
    about_win.geometry("700x500")
    about_text = tk.Text(about_win, wrap=tk.WORD)
    about_text.insert(tk.END, """
Welcome to Medical Health Center, where health meets technology for a brighter, healthier future.

Our Vision
We envision a world where access to healthcare information is not just a luxury but a fundamental right. Our journey began with a simple yet powerful idea: to empower individuals with the knowledge and tools they need to take control of their health.

Who We Are
We are a passionate team of healthcare professionals, data scientists, and technology enthusiasts who share a common goal: to make healthcare accessible, understandable, and personalized for you.

Our Mission
Our mission is to provide you with a seamless and intuitive platform that leverages the power of artificial intelligence and machine learning to assist you in identifying potential health concerns.

How We Do It
Our platform utilizes a robust machine learning model trained on a vast dataset of symptoms and diseases. By inputting your symptoms, our system generates accurate predictions about potential illnesses.

Your Well-being, Our Priority
We provide not only accurate predictions but also comprehensive information about each disease. You'll find descriptions, recommended precautions, medications, dietary advice, and workout tips.

Join Us on this Journey
We invite you to explore our platform, engage with our educational content, and take control of your health journey.
    """)
    about_text.config(state='disabled')
    about_text.pack(expand=True, fill='both', padx=10, pady=10)


# UI setup
root = tk.Tk()
root.title("Disease Predictor")

# Menu bar
menubar = tk.Menu(root)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menubar)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Enter symptoms (comma-separated):").pack()
entry = tk.Entry(frame, width=80)
entry.pack(pady=5)

btn = tk.Button(frame, text="Predict", command=predict_disease)
btn.pack(pady=10)

output = tk.Text(frame, height=20, width=100)
output.pack()

root.mainloop()
