Depression Severity Assessment

A Streamlit web app and Random Forest model that classifies depression severity (Normal, Mild, Moderate, Severe) from PHQ-9 style questionnaire responses, gives tailored self-care recommendations, and shows nearby mental health professionals on a map.

Disclaimer: This is a student project built for learning. It is not a medical or diagnostic tool. If you are struggling with your mental health, please speak to a qualified professional.


Features
Questionnaire: a gamified PHQ-9 style assessment with four answer options per question
Severity prediction: Normal, Mild, Moderate or Severe

Recommendations: tailored suggestions for each severity level
Professional help finder: searches for psychiatrists, clinics and hospitals in the city you enter and shows them on an interactive map (OpenStreetMap / Folium)
Tech Stack

Python, Pandas, NumPy, Scikit-learn, Streamlit, Folium, Joblib, Requests

Dataset
depression_dataset_balanced.csv: 200 rows, perfectly balanced (50 per class)
Features: 9 PHQ-9 item scores, total PHQ score, reaction time, decision-making speed, interaction consistency

Target: Depression Level (Normal, Mild, Moderate, Severe)

Method
Loaded and cleaned the dataset with Pandas (checked missing values, outliers and column names)
Split the data into training and test sets
Trained a Random Forest classifier with Scikit-learn
Evaluated with accuracy and weighted F1, and plotted results with Matplotlib
Saved the model with Joblib and served it through a Streamlit app
Results and Key Finding
Features used	5-fold CV accuracy
All 13 features (including total PHQ score)	about 99%
Total PHQ score only	100%
Without total PHQ score	about 29%
9 PHQ item scores only	about 30%


The model was saved with scikit-learn 1.8.0, so keep that version for it to load.

Project Structure
├── app.py                          # Streamlit app
├── requirements.txt                # Dependencies
├── depression_rf_model.pkl         # Trained Random Forest model
├── depression_dataset_balanced.csv # Dataset
├── train_model.ipynb               # Training and evaluation notebook
└── README.md
Author

Varun K | LinkedIn | GitHub
