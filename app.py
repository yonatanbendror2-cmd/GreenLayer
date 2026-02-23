import streamlit as st
import pandas as pd

# הגדרת דף (כותרת בלשונית הדפדפן)
st.set_page_config(page_title="GreenLayer - מצא את הצמח שלך", page_icon="🌱")

# ---------- בסיס נתונים משופר בעברית ----------
data = [
    {"צמח": "תפוח עץ", "שמש": "שמש מלאה", "השקיה": "בינונית", "אזור": "צפון"},
    {"צמח": "סוקולנט", "שמש": "חצי צל", "השקיה": "נמוכה", "אזור": "כל הארץ"},
    {"צמח": "לבנדר", "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "מרכז"},
    {"צמח": "דפנה", "שמש": "שמש מלאה", "השקיה": "בינונית", "אזור": "דרום"},
    {"צמח": "שרך", "שמש": "צל מלא", "השקיה": "גבוהה", "אזור": "מרכז"},
]

df = pd.DataFrame(data)

# ---------- עיצוב הממשק ----------
st.title("🌱 GreenLayer MVP")
st.markdown("### המערכת החכמה להתאמת צמחייה לבית ולגינה")

# יצירת עמודות לממשק נקי יותר
col1, col2, col3 = st.columns(3)

with col1:
    region = st.selectbox("אזור מגורים", ["צפון", "מרכז", "דרום", "כל הארץ"])
with col2:
    sun = st.selectbox("תנאי אור", ["שמש מלאה", "חצי צל", "צל מלא"])
with col3:
    water = st.selectbox("רמת השקיה", ["נמוכה", "בינונית", "גבוהה"])

# ---------- לוגיקת הסינון ----------
# סינון לפי אזור (כולל "כל הארץ")
mask = ((df['אזור'] == region) | (df['אזור'] == "כל הארץ")) & \
       (df['שמש'] == sun) & \
       (df['השקיה'] == water)

filtered_df = df[mask]

# ---------- הצגת תוצאות ----------
st.divider()

if not filtered_df.empty:
    st.success(f"מצאנו {len(filtered_df)} צמחים שמתאימים לך!")
    # הצגת הטבלה ללא אינדקס (מספר שורה)
    st.table(filtered_df[["צמח", "שמש", "השקיה", "אזור"]])
else:
    st.warning("לא נמצאו צמחים תואמים בדיוק. נסה לשנות את הבחירה.")
    if st.button("הראה לי את כל הצמחים"):
        st.table(df)
