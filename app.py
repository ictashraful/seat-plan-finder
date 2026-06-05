import streamlit as st
import pandas as pd
import re
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Seat Plan Finder | Narsingdi Government Polytechnic Institute",
    page_icon="🎓",
    layout="centered"
)

# --- CUSTOM CSS FOR SMART & PREMIUM UI ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    
    /* Input Form Label Styling */
    label {
        font-weight: 600 !important;
        color: #1e293b !important;
        font-size: 15px !important;
    }
    
    /* Premium Result Card */
    .custom-result-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        border: 2px solid #10b981;
        margin-top: 30px;
        text-align: center;
    }
    
    .seat-found-text {
        color: #1e3a8a;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    
    .student-badge {
        background-color: #3b82f6;
        color: white;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
    }
    
    .room-label {
        color: #047857;
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    .room-display-box {
        color: #059669;
        font-size: 72px;
        font-weight: 900;
        line-height: 1;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- MAPPER FOR DROPDOWNS ---
TECH_OPTIONS = {
    'Civil Technology': 'CT', 
    'Electrical Technology': 'ET',
    'Food Technology': 'FT', 
    'Refrigeration and Air Conditioning Technology': 'RAC',
    'Computer Science and Technology': 'CST'
}

SEMESTER_OPTIONS = {
    '2nd Semester': '2', 
    '3rd Semester': '3',
    '5th Semester': '5', 
    '7th Semester': '7'
}

# --- STABLE DATA PROCESSING FUNCTION ---
def load_all_seat_plans_direct(file_list):
    database = {}
    
    for file_path in file_list:
        if not os.path.exists(file_path):
            continue
            
        try:
            excel_file = pd.ExcelFile(file_path)
            for sheet_name in excel_file.sheet_names:
                room_number = sheet_name.split('-')[0].strip()
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
                
                for row_idx, row in df.iterrows():
                    for col_idx, cell_value in enumerate(row):
                        if pd.notna(cell_value):
                            cell_text = str(cell_value).strip()
                            
                            # সেলের ভেতর থেকে শুধু ৬ ডিজিটের রোলটি খুঁজে বের করা
                            roll_match = re.search(r'\d{6}', cell_text)
                            
                            if roll_match:
                                roll = roll_match.group()
                                # ডাটাবেজে রোলকে কি (Key) বানিয়ে শুধু রুম নম্বরটি সেভ রাখছি
                                database[roll] = room_number
        except Exception as e:
            st.error(f"ফাইল পড়তে সমস্যা হয়েছে: {file_path}. Error: {e}")
                            
    return database

# --- APP INTERFACE ---
st.markdown("<h2 style='text-align: center; color: #1e3a8a; margin-bottom: 0;'>নরসিংদী সরকারি পলিটেকনিক ইনস্টিটিউট</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #475569; font-weight: 500; margin-top: 5px; margin-bottom: 0;'>Narsingdi Government Polytechnic Institute</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; margin-top: 10px;'>🎓 মধ্যপর্ব পরীক্ষা ২০২৬ - ডিজিটাল সিট প্ল্যান</p>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 2px solid #3b82f6; margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# সাব-ফোল্ডারের নাম
FOLDER_NAME = "seat_plan_finder_2nd_3rd_5th_7th"

# বেস ফাইল নেম লিস্ট
BASE_FILES = [
    "seat_plan_2nd.xlsx",
    "seat_plan_3rd.xlsx",
    "seat_plan_5th.xlsx",
    "seat_plan_7th.xlsx"
]

# ক্লাউড সার্ভার এবং লোকাল এনভায়রনমেন্ট—উভয় জায়গার জন্য ডাইনামিক পাথ হ্যান্ডলিং
EXCEL_FILES = []
for f in BASE_FILES:
    sub_folder_path = os.path.join(FOLDER_NAME, f)
    if os.path.exists(sub_folder_path):
        EXCEL_FILES.append(sub_folder_path)
    elif os.path.exists(f):
        EXCEL_FILES.append(f)

if len(EXCEL_FILES) == 0:
    st.info("ℹ️ অনুগ্রহ করে আপনার ৪টি এক্সেল ফাইল প্রজেক্ট ফোল্ডারে রাখুন। ফাইলগুলোর নাম যথাক্রমে: seat_plan_2nd.xlsx, seat_plan_3rd.xlsx, seat_plan_5th.xlsx, seat_plan_7th.xlsx হতে হবে।")
else:
    # ডাটাবেজ লোড
    student_db = load_all_seat_plans_direct(EXCEL_FILES)

    # --- TWO NEW INPUT FIELDS (MANUAL SELECTION) ---
    col1, col2 = st.columns(2)
    
    with col1:
        selected_tech_label = st.selectbox("📂 আপনার টেকনোলজি সিলেক্ট করুন:", list(TECH_OPTIONS.keys()))
        tech_code = TECH_OPTIONS[selected_tech_label]
        
    with col2:
        selected_sem_label = st.selectbox("⏳ আপনার পর্ব/সেমিস্টার সিলেক্ট করুন:", list(SEMESTER_OPTIONS.keys()))
        sem_code = SEMESTER_OPTIONS[selected_sem_label]

    # --- ROLL NUMBER INPUT ---
    search_roll = st.text_input(
        "🔍 আপনার ৬ ডিজিটের বোর্ড রোল নম্বরটি লিখুন:",
        placeholder="যেমন: ৩৪০২৪১",
        max_chars=10
    ).strip()

    # --- SMART & PROFESSIONAL RESULT DISPLAY ---
    if search_roll:
        if student_db and search_roll in student_db:
            room_no = student_db[search_roll]
            
            # আপনার রিকোয়েস্ট করা ফরম্যাট অনুযায়ী ডায়নামিক কম্বিনেশন (যেমন: 2FT 340241)
            formatted_student = f"{sem_code}{tech_code} {search_roll}"
            
            st.markdown(f"""
            <div class="custom-result-card">
                <div class="seat-found-text">Seat Found for "{formatted_student}"</div>
                <div class="student-badge">{selected_tech_label} • {selected_sem_label}</div>
                <div class="room-box">
                    <div class="room-label">ROOM NUMBER</div>
                    <div class="room-display-box">{room_no}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ দুঃখিত! এই রোল নম্বরটি কোনো পর্বের সিট প্ল্যানেই খুঁজে পাওয়া যায়নি। অনুগ্রহ করে সঠিক তথ্য দিয়ে আবার চেষ্টা করুন।")

# নোটিশ সেকশন
st.markdown("""
<br>
<div style="background-color: #fff7ed; padding: 15px; border-radius: 10px; border: 1px solid #ffedd5;">
    <p style="margin: 0; color: #c2410c; font-weight: 600; font-size: 14px;">⚠️ পরীক্ষার্থীদের জন্য নির্দেশনাবলী:</p>
    <ul style="margin: 5px 0 0 0; color: #9a3412; font-size: 13px;">
        <li>পরীক্ষা শুরুর অন্তত ১৫ মিনিট আগে অবশ্যই নির্দিষ্ট কক্ষে আসন গ্রহণ করতে হবে।</li>
        <li>পরীক্ষাকক্ষে মোবাইল ফোন বা যেকোনো ধরনের ইলেকট্রনিক ডিভাইস আনা সম্পূর্ণ নিষিদ্ধ।</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align: center; color: #94a3b8; font-size: 12px;'>© 2026 | Developed for Narsingdi Government Polytechnic Institute</p>", unsafe_allow_html=True)