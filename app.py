import streamlit as st
import pandas as pd

st.set_page_config(page_title="GreenLayer Pro", page_icon="🌿", layout="wide")

# עיצוב UI מתקדם
st.markdown("""
    <style>
    .plant-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 6px solid #4CAF50;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# בסיס נתונים מורחב עם מאפיינים נוספים
data = [
    {
        "צמח": "מונסטרה דליסיוסה", 
        "שמש": "צל מלא", "השקיה": "בינונית", "אזור": "כל הארץ",
        "קושי": "קל", "חיות": "לא ידידותי",
        "תיאור": "צמח בית טרופי מרהיב. מושלם לפינות ריקות בסלון.",
        "תמונה": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400"
    },
    {
        "צמח": "לבנדר רפואי", 
        "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "צפון",
        "קושי": "קל", "חיות": "ידידותי",
        "תיאור": "פרחים סגולים ריחניים. עוזר להרגעת הבית ודחיית יתושים.",
        "תמונה": "https://images.unsplash.com/photo-1591073113125-e46713c829ed?w=400"
    }
    # כאן אפשר להוסיף עוד עשרות צמחים...
]
df = pd.DataFrame(data)

# תפריט צד משופר
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)
    st.title("GreenLayer")
    
    st.subheader("🔍 חיפוש והתאמה")
    region = st.selectbox("אזור מגורים", ["כל הארץ", "צפון", "מרכז", "דרום"])
    sun = st.selectbox("תנאי אור", ["שמש מלאה", "חצי צל", "צל מלא"])
    water = st.selectbox("תדירות השקיה", ["נמוכה", "בינונית", "גבוהה"])
    
    st.divider()
    st.subheader("📧 צור קשר לייעוץ")
    with st.form("contact_form"):
        email = st.text_input("מייל לחזרה")
        msg = st.text_area("איזה צמח חסר לך?")
        submit = st.form_submit_button("שלח בקשה")
        if submit:
            st.success("תודה! נחזור אליך בקרוב.")

# גוף האפליקציה
st.title("מצא את הירוק שלך 🌿")

filtered = df[
    ((df['אזור'] == region) | (df['אזור'] == "כל הארץ")) &
    (df['שמש'] == sun) &
    (df['השקיה'] == water)
]

if not filtered.empty:
    for _, row in filtered.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(row['תמונה'], use_container_width=True)
            with col2:
                st.markdown(f"""
                <div class="plant-card">
                    <h2>{row['צמח']}</h2>
                    <span class="badge">💪 {row['קושי']} לגידול</span>
                    <span class="badge">🐾 {row['חיות']}</span>
                    <p style="margin-top:15px;">{row['תיאור']}</p>
                    <p><b>תנאים:</b> {row['שמש']} | השקיה {row['השקיה']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"קבלת מדריך טיפול ל{row['צמח']}", key=row['צמח']):
                    st.info(f"המדריך ל{row['צמח']} יישלח למייל שהזנת בתפריט הצד.")
            st.divider()
else:
    st.warning("לא מצאנו התאמה מדויקת. אולי תרצה לראות צמחים שדורשים פחות אור?")
    if st.button("הצג את כל הקטלוג"):
        st.dataframe(df[['צמח', 'שמש', 'השקיה']])
