import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="GreenLayer Live", page_icon="🌿", layout="wide")

# פונקציה למשיכת נתונים מהגיליון שלך
def load_data():
    # הלינק לגיליון שלך בפורמט CSV (מבוסס על ה-ID ששלחת)
    sheet_id = "1nS-ePc8UJFa3zAZLRlpR-PjbnpOqYhFKOK5BQcAH1uw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

# טעינת הנתונים
try:
    df = load_data()
except Exception as e:
    st.error("לא הצלחנו למשוך נתונים מהגיליון. וודא שהוא מכיל נתונים ושהוא מוגדר כציבורי.")
    st.stop()

# --- כאן ממשיך כל הקוד של ה-UI (הסינון, הכרטיסיות והתפריט) ---
# (השתמש בקוד הקודם שנתתי לך, רק במקום 'df = pd.DataFrame(data)' השתמש ב-df שנוצר כאן)
