# import tkinter as tk
# from tkinter import messagebox
# import cv2
# from PIL import Image, ImageTk
# import numpy as np
# from tensorflow.keras.models import load_model
# import pyttsx3
# from tensorflow.keras.models import load_model
#
# # Load model and labels
# model = load_model('model/asl_model.h5')
# labels = np.load('labels/labels.npy')
#
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
# # Initialize Text-to-Speech engine
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)
#
# # Global sentence to build detected text
# sentence = ""
#
# # Create main window
# root = tk.Tk()
# root.title("🤟 Sign Language to Text Converter")
# root.geometry("700x550")
# root.config(bg="white")
#
# # Webcam display
# lmain = tk.Label(root)
# lmain.pack()
#
# # Label to display the sentence
# sentence_label = tk.Label(root, text="Text: ", font=("Arial", 16), bg="white", fg="black")
# sentence_label.pack(pady=10)
#
# # Initialize webcam
# cap = cv2.VideoCapture(0)
#
#
# def predict_sign(frame):
#     roi = frame[100:400, 100:400]
#     roi_resized = cv2.resize(roi, (64, 64))
#     roi_norm = roi_resized / 255.0
#     roi_input = np.expand_dims(roi_norm, axis=0)
#     prediction = model.predict(roi_input)
#     pred_class = labels[np.argmax(prediction)]
#     return pred_class
#
#
# def show_frame():
#     ret, frame = cap.read()
#     if not ret:
#         return
#
#     frame = cv2.flip(frame, 1)
#     cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)
#
#     # Get prediction
#     pred_class = predict_sign(frame)
#     root.current_char = pred_class  # This is accessed during capture
#
#     # Display predicted character on frame
#     cv2.putText(frame, f'Char: {pred_class}', (10, 70),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)
#
#     # Convert frame to Tkinter-compatible image
#     img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     img = Image.fromarray(img)
#     imgtk = ImageTk.PhotoImage(image=img)
#     lmain.imgtk = imgtk
#     lmain.configure(image=imgtk)
#     lmain.after(10, show_frame)
#
#
# def capture_char():
#     global sentence
#     char = getattr(root, "current_char", "")
#     sentence += char
#     sentence_label.config(text="Text: " + sentence)
#
#
# def reset_sentence():
#     global sentence
#     sentence = ""
#     sentence_label.config(text="Text: ")
#
#
# def speak_sentence():
#     if sentence:
#         engine.say(sentence)
#         engine.runAndWait()
#     else:
#         messagebox.showinfo("Info", "Sentence is empty!")
#
#
# def close_app():
#     cap.release()
#     root.destroy()
#
#
# # Buttons
# btn_frame = tk.Frame(root, bg="white")
# btn_frame.pack(pady=10)
#
# tk.Button(btn_frame, text="📸 Capture", font=("Arial", 12), command=capture_char).grid(row=0, column=0, padx=10)
# tk.Button(btn_frame, text="🗑️ Reset", font=("Arial", 12), command=reset_sentence).grid(row=0, column=1, padx=10)
# tk.Button(btn_frame, text="🔊 Speak", font=("Arial", 12), command=speak_sentence).grid(row=0, column=2, padx=10)
# tk.Button(btn_frame, text="🚪 Exit", font=("Arial", 12), command=close_app).grid(row=0, column=3, padx=10)
#
# # Start webcam loop
# show_frame()
# root.mainloop()


import cv2
import numpy as np
import pyttsx3
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# === Load Model and Labels ===
model = load_model('model/asl_model.h5')
labels = np.load('labels/labels.npy')

# === Initialize Text-to-Speech ===
engine = pyttsx3.init()

# === Initialize Global Sentence ===
sentence = ""


# === Predict Function ===
def predict_sign(frame):
    try:
        roi = frame[100:400, 100:400]  # Region of interest
        roi_resized = cv2.resize(roi, (64, 64))
        roi_normalized = roi_resized / 255.0
        roi_input = np.expand_dims(roi_normalized, axis=0)
        prediction = model.predict(roi_input)
        pred_class = labels[np.argmax(prediction)]
        print("✅ Predicted:", pred_class)
        return pred_class
    except Exception as e:
        print("❌ Prediction Error:", e)
        return ""


# === Capture Character ===
def capture_char():
    global sentence
    char = getattr(root, "current_char", "")
    sentence += char
    sentence_label.config(text="Text: " + sentence)


# === Speak Sentence ===
def speak_sentence():
    engine.say(sentence)
    engine.runAndWait()


# === Reset Sentence ===
def reset_sentence():
    global sentence
    sentence = ""
    sentence_label.config(text="Text: ")


# === Exit App ===
def exit_app():
    cap.release()
    root.destroy()


# === Show Webcam Frame ===
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Draw the ROI box
    cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)

    # Predict current character
    pred_char = predict_sign(frame)
    root.current_char = pred_char

    # Display frame in GUI
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


# === GUI Setup ===
root = tk.Tk()
root.title("Sign Language to Text Converter")
root.geometry("800x600")
root.resizable(False, False)

# Webcam label
lmain = Label(root)
lmain.pack()

# Sentence display
sentence_label = Label(root, text="Text: ", font=("Helvetica", 20))
sentence_label.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

Button(btn_frame, text="Capture", width=15, command=capture_char).grid(row=0, column=0, padx=10)
Button(btn_frame, text="Speak", width=15, command=speak_sentence).grid(row=0, column=1, padx=10)
Button(btn_frame, text="Reset", width=15, command=reset_sentence).grid(row=0, column=2, padx=10)
Button(btn_frame, text="Exit", width=15, command=exit_app).grid(row=0, column=3, padx=10)

# Start Webcam
cap = cv2.VideoCapture(0)
show_frame()
root.mainloop()
