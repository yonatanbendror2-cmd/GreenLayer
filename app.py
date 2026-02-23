import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="GreenLayer Pro", page_icon="🌿", layout="wide")

# עיצוב UI/UX באמצעות CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9f8; }
    .plant-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-right: 8px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    .badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
        margin-left: 10px;
        display: inline-block;
    }
    h2 { color: #1b5e20; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# פונקציה לטעינת נתונים מהגיליון שלך
@st.cache_data(ttl=60) # מעדכן את הנתונים כל דקה
def load_data():
    sheet_id = "1nS-ePc8UJFa3zAZLRlpR-PjbnpOqYhFKOK5BQcAH1uw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    data = pd.read_csv(url)
    return data

# טעינת הנתונים
try:
    df = load_data()
except Exception as e:
    st.error("שגיאה בחיבור לנתונים. וודא שהגיליון מוגדר כציבורי ושכותרות העמודות נכונות.")
    st.stop()

# --- תפריט צד (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)
    st.title("GreenLayer")
    st.subheader("סינון חכם")
    
    region = st.selectbox("אזור מגורים", ["כל הארץ", "צפון", "מרכז", "דרום"])
    sun = st.selectbox("תנאי אור", ["שמש מלאה", "חצי צל", "צל מלא"])
    water = st.selectbox("רמת השקיה", ["נמוכה", "בינונית", "גבוהה"])
    
    st.divider()
    st.write("### צור קשר לייעוץ")
    with st.form("contact"):
        email = st.text_input("אימייל")
        msg = st.text_area("הודעה")
        if st.form_submit_button("שלח"):
            st.success("הבקשה נשלחה!")

# --- גוף האפליקציה ---
st.title("🌿 GreenLayer")
st.markdown("#### המדריך האישי שלך להתאמת צמחייה בישראל")

# לוגיקת סינון
mask = ((df['אזור'] == region) | (df['אזור'] == "כל הארץ")) & \
       (df['שמש'] == sun) & \
       (df['השקיה'] == water)

filtered_df = df[mask]

st.write(f"מצאנו **{len(filtered_df)}** צמחים שמתאימים בדיוק עבורך:")

if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2.5])
            with col1:
                # הצגת תמונה עם פינות מעוגלות
                st.image(row['תמונה'], use_container_width=True)
            with col2:
                st.markdown(f"""
                <div class="plant-card">
                    <h2>{row['צמח']}</h2>
                    <div>
                        <span class="badge">💪 {row['קושי']} לגידול</span>
                        <span class="badge">🐾 {row['חיות']}</span>
                    </div>
                    <p style="margin-top:15px; font-size: 16px;">{row['תיאור']}</p>
                    <p><b>תנאי גידול:</b> {row['שמש']} | השקיה {row['השקיה']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"קבלת מדריך טיפול ל{row['צמח']}", key=f"btn_{index}"):
                    st.toast(f"המדריך ל{row['צמח']} בדרך אליך!", icon="🌱")
            st.divider()
else:
    st.info("לא נמצאו צמחים תואמים בדיוק. נסה לשנות את אחד הפילטרים.")
