@echo off
cd /d C:\Users\ville\gestion_enquetes
call .\env\Scripts\activate.bat
start streamlit run app.py
