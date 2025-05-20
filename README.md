# Sign_Language_to_Text_and_Speech_Converter

This project uses **OpenCV**, **CNN (Deep Learning)**, and **Tkinter GUI** to recognize American Sign Language (ASL) hand gestures and convert them into text, with optional speech output using **pyttsx3**.

## 🔧 Features

- Real-time webcam-based sign recognition
- Trained on ASL Alphabet dataset
- Displays recognized character in a GUI
- Builds words and speaks them using Text-to-Speech


## 🗂️ Project Structure
├── model     # Trained CNN model (asl_model.h5)

├── labels    # Labels for ASL classes

├── app.py    # Main GUI app using Tkinter

├── requirements.txt

└── README.md


## 🚀 Run Locally

1. Clone the repo:

git clone https://github.com/Aditee01/Sign_Language_to_Text_and_Speech_Converter.git

cd Sign_Language_to_Text_and_Speech_Converter

pip install -r requirements.txt

python app.py



