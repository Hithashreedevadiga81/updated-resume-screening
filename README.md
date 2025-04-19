 
# 🤖 Resume Screening Application

Resume Screening App is an intelligent web-based application that automates the process of analyzing and classifying resumes into relevant job categories using machine learning. Built with Python, scikit-learn, and Streamlit, this app allows users to upload a resume (in .txt or .pdf format), processes the text using NLP techniques, and predicts the most suitable job domain using a trained SVC model.

* The goal is to reduce manual effort in resume sorting and speed up hiring pipelines by providing quick and accurate job-role predictions.

## 💡 Key Highlights:
- Built on real-world resume dataset with labeled job categories
- Uses TF-IDF vectorization for text feature extraction
- Trained and evaluated using 3 ML models:
    * Support Vector Classifier (SVC) – 99% accuracy ✅
    * Random Forest
    * K-Nearest Neighbors
- Final model (clf.pkl) is deployed in the app
- Minimal, interactive UI with Streamlit

---

## 🚀 Features
- Upload `.txt` or `.pdf` resumes
- Predicts job domain using ML (SVC, RandomForest, KNN)
- Clean interface built with **Streamlit**

---

## 🧠 ML Models Used
| Model                  | Accuracy |
|-----------------------|----------|
| **SVC (Used in App)**  | ~99%     |
| Random Forest         | ~95–97%  |
| KNeighbors Classifier | ~85–90%  |

---

## 📁 Key Files
- `app.py` – Streamlit web app
- `clf.pkl` – Final trained SVC model
- `tfidf.pkl` – TF-IDF vectorizer
- `encoder.pkl` – Label encoder
- `Resume_Screening_with_Python.ipynb` – Training notebook
- `UpdatedResumeDataSet.csv` – Resume dataset

---

## 📚 Dataset
[updated-resume-dataset](https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset)
Contains 2200+ labeled resumes and their corresponding job categories.
Used for training and evaluation of ML models.

---

## 🧠 How It Works
- Resume is uploaded by the user.
- Text is extracted and cleaned.
- TF-IDF vectorization is applied.
- Model predicts the most relevant job category.
- Result is shown in the web interface.

---

## 📦 Requirements
Python 3.7+
streamlit
scikit-learn
pandas
numpy
(See requirements.txt for exact versions.)

---

## ⚙️ Run Locally
<pre> ```bash 
pip install -r requirements.txt
streamlit run app.py
</pre>

---

## 🎥 Demo
https://videos.dyntube.com/videos/NJM9hGqdEGBPVjg3wc6dQ 
![image](https://github.com/user-attachments/assets/7d364623-0236-4ada-a572-464fee0db9dc)

---

 ## 📄 License
MIT License – free to use, modify, and share

---

## 👨‍💻 Author
Hithashree
Feel free to connect with me 


