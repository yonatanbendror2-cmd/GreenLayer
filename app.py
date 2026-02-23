import streamlit as st
import pandas as pd

# הגדרות דף לשיפור ה-UI
st.set_page_config(
    page_title="GreenLayer | עוזר הגינון האישי שלך",
    page_icon="🌿",
    layout="wide"
)

# עיצוב CSS מותאם אישית להצגת כרטיסיות (UX/UI)
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f5;
    }
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-right: 5px solid #2e7d32;
    }
    h1 {
        color: #2e7d32;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- בסיס נתונים מורחב (סקר שוק צמחים נפוצים) ----------
data = [
    {"צמח": "לבנדר", "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "כל הארץ", "תיאור": "צמח ריחני, דוחה מזיקים ומושך דבורים.", "תמונה": "https://images.unsplash.com/photo-1591073113125-e46713c829ed?w=400"},
    {"צמח": "מונסטרה (דליסיוסה)", "שמש": "צל מלא", "השקיה": "בינונית", "אזור": "מרכז", "תיאור": "צמח בית מרשים עם עלים מחוררים.", "תמונה": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?w=400"},
    {"צמח": "רוזמרין", "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "כל הארץ", "תיאור": "חזק מאוד, מתאים לבישול ולגדר חיה.", "תמונה": "https://images.unsplash.com/photo-1594313054110-5004f5296377?w=400"},
    {"צמח": "ציפור גן עדן", "שמש": "שמש מלאה", "השקיה": "בינונית", "אזור": "דרום", "תיאור": "פריחה כתומה מרהיבה ומראה טרופי.", "תמונה": "https://images.unsplash.com/photo-1603436326446-747293021160?w=400"},
    {"צמח": "סנסיביריה (לשון החותנת)", "שמש": "צל מלא", "השקיה": "נמוכה", "אזור": "כל הארץ", "תיאור": "הצמח הכי עמיד שיש, מנקה את האוויר.", "תמונה": "https://images.unsplash.com/photo-1631553127989-5f6c69551fe0?w=400"},
    {"צמח": "זית אירופי", "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "צפון", "תיאור": "עץ קלאסי ארץ-ישראלי, דורש מינימום טיפול.", "תמונה": "https://images.unsplash.com/photo-1445296119251-8f328a7e1373?w=400"},
    {"צמח": "גרניום", "שמש": "חצי צל", "השקיה": "בינונית", "אזור": "כל הארץ", "תיאור": "פריחה צבעונית לאורך רוב השנה.", "תמונה": "https://images.unsplash.com/photo-1524179091875-bf99a9a6af57?w=400"},
    {"צמח": "לימון", "שמש": "שמש מלאה", "השקיה": "גבוהה", "אזור": "מרכז", "תיאור": "עץ פרי ריחני שמתאים גם לעציצים גדולים.", "תמונה": "https://images.unsplash.com/photo-1585059895316-16056524259b?w=400"},
    {"צמח": "סוקולנט אלוורה", "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "דרום", "תיאור": "צמח מרפא קל לגידול.", "תמונה": "https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?w=400"},
    {"צמח": "בוגונוויליה", "שמש": "שמש מלאה", "השקיה": "נמוכה", "אזור": "כל הארץ", "תיאור": "צמח מטפס עם פריחה עוצמתית בקיץ.", "תמונה": "https://images.unsplash.com/photo-1582769923195-c6e60dc1d8bc?w=400"}
]

df = pd.DataFrame(data)

# ---------- תפריט צד (UX) ----------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=100)
st.sidebar.title("סינון חכם")
st.sidebar.write("הגדר את תנאי השטח שלך:")

region = st.sidebar.selectbox("אזור בארץ", ["כל הארץ", "צפון", "מרכז", "דרום"])
sun = st.sidebar.selectbox("תנאי אור", ["שמש מלאה", "חצי צל", "צל מלא"])
water = st.sidebar.selectbox("רמת השקיה", ["נמוכה", "בינונית", "גבוהה"])

st.sidebar.divider()
st.sidebar.info("טיפ: צמחי 'שמש מלאה' צריכים לפחות 6 שעות אור ישיר ביום.")

# ---------- גוף האפליקציה ----------
st.title("🌿 GreenLayer")
st.markdown("### מצא את הצמח המושלם עבורך")

# לוגיקת סינון
filtered_df = df[
    ((df['אזור'] == region) | (df['אזור'] == "כל הארץ")) &
    (df['שמש'] == sun) &
    (df['השקיה'] == water)
]

st.write(f"הצגת {len(filtered_df)} תוצאות עבור הבחירה שלך:")

# הצגת התוצאות בעיצוב כרטיסיות (Grid)
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['תמונה'], use_container_width=True)
            with col2:
                st.markdown(f"""
                <div class="stCard">
                    <h2>{row['צמח']}</h2>
                    <p><b>תנאים:</b> {row['שמש']} | {row['השקיה']}</p>
                    <p>{row['תיאור']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.divider()
else:
    st.warning("לא מצאנו צמח שתואם בדיוק את כל הפילטרים. נסה להפחית דרישות (למשל לשנות רמת השקיה).")

# הצגת כל הצמחים אם אין תוצאות
if filtered_df.empty:
    if st.button("הצג את כל הקטלוג"):
        for index, row in df.iterrows():
             st.write(f"**{row['צמח']}**")
