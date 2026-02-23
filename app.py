import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="GreenLayer Pro", page_icon="🌿", layout="wide")

# עיצוב UI/UX
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

# פונקציה לטעינת נתונים
@st.cache_data(ttl=60)
def load_data():
    sheet_id = "1nS-ePc8UJFa3zAZLRlpR-PjbnpOqYhFKOK5BQcAH1uw"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    data = pd.read_csv(url)
    
    # ניקוי רווחים מיותרים משמות העמודות ומהנתונים עצמם (המנגנון הסלחני)
    data.columns = data.columns.str.strip()
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].str.strip()
        
    return data

try:
    df = load_data()
except Exception as e:
    st.error("שגיאה בחיבור לנתונים. וודא שהגיליון מוגדר כציבורי.")
    st.stop()

# --- תפריט צד ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)
    st.title("GreenLayer")
    
    st.subheader("סינון חכם")
    region = st.selectbox("אזור מגורים", ["כל הארץ", "צפון", "מרכז", "דרום"])
    sun = st.selectbox("תנאי אור", ["שמש מלאה", "חצי צל", "צל מלא"])
    water = st.selectbox("רמת השקיה", ["נמוכה", "בינונית", "גבוהה"])
    
    if st.button("איפוס סינונים 🔄"):
        st.rerun()

# --- גוף האפליקציה ---
st.title("🌿 GreenLayer")

# שורת חיפוש חופשי
search_query = st.text_input("חפש צמח לפי שם...", "")

# לוגיקת סינון משולבת (סינון + חיפוש)
mask = (
    ((df['אזור'] == region) | (df['אזור'] == "כל הארץ")) &
    (df['שמש'] == sun) &
    (df['השקיה'] == water)
)

# אם המשתמש כתב משהו בשורת החיפוש, נתעלם מהסינונים האחרים ונציג את הצמח הספציפי
if search_query:
    filtered_df = df[df['צמח'].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df[mask]

# הצגת תוצאות
st.markdown(f"מצאנו **{len(filtered_df)}** צמחים עבורך:")

if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 2.5])
            with col1:
                # טיפול במקרה של תמונה חסרה
                img_url = row['תמונה'] if pd.notnull(row['תמונה']) else "https://via.placeholder.com/150"
                st.image(img_url, width=250)
            with col2:
                st.markdown(f"""
                <div class="plant-card">
                    <h2>{row['צמח']}</h2>
                    <div>
                        <span class="badge">💪 {row['קושי']}</span>
                        <span class="badge">🐾 {row['חיות']}</span>
                        <span class="badge">📍 {row['אזור']}</span>
                    </div>
                    <p style="margin-top:15px; font-size: 16px;">{row['תיאור']}</p>
                    <p><b>תנאי גידול:</b> {row['שמש']} | השקיה {row['השקיה']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.divider()
else:
    st.info("לא נמצאו צמחים תואמים. נסה לשנות את הסינון או לבדוק את איות שם הצמח.")

# להצגת הטבלה הגולמית לניפוי שגיאות (תוכל למחוק את זה אחר כך)
with st.expander("צפייה בנתוני הגיליון הגולמיים"):
    st.write(df)
