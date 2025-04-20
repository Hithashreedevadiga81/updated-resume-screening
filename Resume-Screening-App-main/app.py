# you need to install all these in your terminal
# pip install streamlit
# pip install scikit-learn
# pip install python-docx
# pip install PyPDF2
import random  # make sure this is at the top of your script
import streamlit as st
import pickle
import re

# Load model and vectorizer
svc_model = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))
le = pickle.load(open('encoder.pkl', 'rb'))

def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_txt(file):
    try:
        text = file.read().decode('utf-8')
    except UnicodeDecodeError:
        text = file.read().decode('latin-1')
    return text

def handle_file_upload(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        text = extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        text = extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        text = extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
    return text

def pred(input_resume):
    cleaned_text = cleanResume(input_resume)
    vectorized_text = tfidf.transform([cleaned_text])
    vectorized_text = vectorized_text.toarray()
    predicted_proba = svc_model.predict_proba(vectorized_text)[0]
    predicted_index = predicted_proba.argmax()
    predicted_category = svc_model.classes_[predicted_index]
    confidence = predicted_proba[predicted_index] * 100
    predicted_category_name = le.inverse_transform([predicted_category])[0]
    return predicted_category_name, round(confidence, 2)

def main():
    st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <style>
        .greeting-container {
            display: flex; align-items: center; justify-content: center;
            margin-top: 40px; margin-bottom: 60px; flex-wrap: wrap;
            animation: popIn 1.8s ease-out;
        }
        @keyframes popIn {
            0% { transform: scale(0.5) translateY(-100px); opacity: 0; }
            60% { transform: scale(1.1) translateY(20px); opacity: 1; }
            100% { transform: scale(1) translateY(0); }
        }
        .greeting-gif {
            width: 300px; height: auto; border-radius: 10px;
            margin-right: 40px; animation: flipIn 2.5s ease-in-out;
        }
        @keyframes flipIn {
            0% { transform: rotateY(90deg) translateY(-100px); opacity: 0; }
            50% { transform: rotateY(45deg) translateY(20px); opacity: 0.8; }
            100% { transform: rotateY(0deg) translateY(0); opacity: 1; }
        }
        .greeting-text {
            font-size: 14px; color: #ffffff; font-family: 'Press Start 2P', cursive;
            text-align: left; line-height: 1.8; max-width: 400px;
        }
        @media (max-width: 768px) {
            .greeting-container { flex-direction: column; text-align: center; }
            .greeting-gif { margin-right: 0; margin-bottom: 20px; }
            .greeting-text { font-size: 12px; }
        }
    </style>
    <div class="greeting-container">
        <img src="https://i.pinimg.com/originals/4b/cb/1f/4bcb1fb72d1d08efa44efa5ceb712ec7.gif" class="greeting-gif">
        <div class="greeting-text">
            HELLO, HUMAN.<br><br>
            I'M <span style="color: #3399ff;">RESUMAI</span><br>
            DROP YOUR FILE AND<br>
            LET'S UNLOCK ITS POWER!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style="color: #3399ff; font-family: 'Press Start 2P', cursive; text-align: center;">
            Automatic Resume Screening
        </h1>
        <p style="text-align: center; font-size: 16px; color: #ccc;">
            Upload a resume in <b>PDF, TXT, or DOCX</b> format and get the predicted job category instantly!
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .custom-upload .stFileUploader {
                border: 2px dashed #3399ff; padding: 40px; background-color: #0f172a;
                border-radius: 15px; box-shadow: 0 0 20px #3399ff44;
            }
            .custom-upload .stFileUploader:hover {
                box-shadow: 0 0 25px #3399ffaa; background-color: #1e293b;
            }
        </style>
        <div class="custom-upload">
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(" 📄 DROP YOUR RESUME HERE", type=["pdf", "docx", "txt"])
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        try:
            resume_text = handle_file_upload(uploaded_file)
            st.success("✅ Successfully extracted the text from the uploaded resume.")

            if st.checkbox("📖 Show extracted text"):
                st.text_area("Extracted Resume Text", resume_text, height=300)

            st.subheader("")
            with st.spinner("Analyzing resume..."):
                category, match_accuracy = pred(resume_text)

            st.markdown(f"""
            <div style='padding: 30px; background-color: #001f3f; border-radius: 20px;
                        color: #ffffff; font-size: 20px; font-weight: bold;
                        text-align: center; box-shadow: 0 0 25px #3399ff55;
                        margin-top: 30px; border: 2px solid #3399ff; font-family: monospace;'
                 class="result-container">
                         <img src="https://i.pinimg.com/originals/a3/f3/12/a3f3127c2ac754cc8378a09a532e397c.gif">
                <span style="font-size: 22px; color: #3399ff;height:200px "><br> RESULT:</span><br><br>
                The AI predicts this resume best fits the category of:<br>
                <span class='result-category' style='color:	#ff073a; font-size: 32px;'> {category}</span><br><br>
                <span id="match-accuracy" style='font-size: 20px; color: #3399ff;'> Match Accuracy: {match_accuracy}%</span><br><br>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error processing the file: {str(e)}")

if __name__ == "__main__":
    main()

st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            color: #000;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        Made by Hithashree | © 2025 All rights reserved
    </div>
    """,
    unsafe_allow_html=True
)
