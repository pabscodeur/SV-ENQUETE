Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
cd "C:\Users\ville\gestion_enquetes"
.\env\Scripts\activate
pip install streamlit-calendar
streamlit run app.py
