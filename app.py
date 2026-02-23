import streamlit as st
import pandas as pd

st.set_page_config(page_title="GreenLayer Pro", page_icon="🌿", layout="wide")

# פונקציה לטעינת נתונים
@st.cache_data(ttl=5)
def load_data():
    sheet_id = "1nS-ePc8UJFa3zAZLRlpR-PjbnpOqYhFKOK5BQcAH1uw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    data = pd.read_csv(url)
    # ניקוי רווחים מהכותרות (חשוב מאוד!)
    data.columns = data.columns.str.strip()
    return data

try:
    df = load_data()
    
    # בדיקה מה המערכת רואה - זה יעזור לך למצוא שגיאות כתיב בגיליון
    with st.expander("🛠️ בדיקת תקינות גיליון הנתונים (לחץ כאן אם יש שגיאה)"):
        st.write("העמודות שמצאתי בגיליון שלך הן:")
        st.write(list(df.columns))
        st.write("הנתונים עצמם:")
        st.write(df)

    # רשימת עמודות חובה
    required = ['צמח', 'שמש', 'השקיה', 'אזור']
    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"❌ חסרות עמודות בגיליון: {missing}")
        st.info("וודא שהכותרות בשורה 1 בגיליון הן בדיוק: צמח, שמש, השקיה, אזור")
        st.stop()

except Exception as e:
    st.error(f"שגיאה בטעינת הגיליון: {e}")
    st.stop()

# --- ממשק המשתמש ---
st.sidebar.title("GreenLayer 🌿")
region = st.sidebar.selectbox("בחר אזור", ["כל הארץ", "צפון", "מרכז", "דרום"])
sun = st.sidebar.selectbox("תנאי אור", ["שמש מלאה", "חצי צל", "צל מלא"])
water = st.sidebar.selectbox("רמת השקיה", ["נמוכה", "בינונית", "גבוהה"])

# סינון (עם ניקוי רווחים מהנתונים)
for col in required:
    df[col] = df[col].astype(str).str.strip()

mask = ((df['אזור'] == region) | (df['אזור'] == "כל הארץ")) & \
       (df['שמש'] == sun) & \
       (df['השקיה'] == water)

filtered_df = df[mask]

# --- הצגת תוצאות ---
st.title("הצמחים שנמצאו")
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.markdown(f"### {row['צמח']}")
        st.write(f"**תנאים:** {row['שמש']} | {row['השקיה']} | {row['אזור']}")
        if 'תמונה' in df.columns and pd.notnull(row['תמונה']):
            st.image(row['תמונה'], width=300)
        st.divider()
else:
    st.warning("לא נמצאו צמחים תואמים לסינון. בדוק שהמילים בגיליון כתובות בדיוק כמו בסינון.")
