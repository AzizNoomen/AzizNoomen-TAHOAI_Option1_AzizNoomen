# 🧠 Document Classifier App

A lightweight web app that lets users paste or upload `.txt` documents and receive a predicted label and confidence score. The classification is done using a backend model served via FastAPI.

## 📦 How to Use

1. Paste or type any text directly into the textarea  
2. Or upload a `.txt` file from your machine  
3. Click **Submit**  
4. A modal will pop up showing the predicted **label** and **confidence**

## 🚀 Run Locally with Docker Compose

git clone https://github.com/AzizNoomen/TAHOAI_Option1_AzizNoomen

shell
Copy
Edit

### 2. Change directory to the project folder

cd TAHOAI_Option1_AzizNoomen


### 3. Build and start the app using Docker Compose

docker-compose up --build


### 4. Once the app is up and running, open your browser and go to:

http://localhost:3000


## 📝 Notes

- **Real Model**: The backend uses a real machine learning model for classification, not a mock model. This model processes the input text and returns a label along with a confidence score.

## ⚠️ Limitations

- **File Upload Restriction**: The app only supports `.txt` files. Files with other extensions will be rejected.
- **Language Limitation**: The model is trained primarily for English text and may not perform well with non-English text or special characters.
- **No Support for Complex Formats**: The app only processes plain text. Non-text content (e.g., images, tables) in the uploaded file will be ignored.

