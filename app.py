import streamlit as st
from supabase import create_client, Client
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مكتب الفعاليات | تسجيل المتطوعين", page_icon="✨", layout="centered")

# --- أكواد CSS السحرية (الخلفية المتحركة، تأثير الزجاج، والتفاعلات) ---
st.markdown("""
    <style>
    /* استيراد خطوط احترافية */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&family=Tajawal:wght@500;700&display=swap');
    
    /* تغيير الخط الأساسي والتوجيه */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }

    /* الخلفية الحية المتحركة (ألوان الزمرد والأسود الملكي) */
    .stApp {
        background: linear-gradient(-45deg, #022c1e, #0f3e2e, #182825, #0a1f18);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* تأثير الزجاج الشفاف (Glassmorphism) للاستمارة */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-radius: 25px !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important; /* حدود ذهبية خفيفة */
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5) !important;
        padding: 40px !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stForm"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px 0 rgba(212, 175, 55, 0.15) !important;
    }

    /* تنسيق النصوص لتكون واضحة وفخمة */
    h1 {
        color: #D4AF37 !important; /* لون ذهبي */
        text-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4);
        font-family: 'Tajawal', sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px !important;
    }
    h3, p, label {
        color: #E0E0E0 !important;
    }

    /* تنسيق حقول الإدخال لتلائم الزجاج */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: white !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border: 1px solid #D4AF37 !important; /* توهج ذهبي عند الكتابة */
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.3) !important;
    }

    /* الزر السحري (تفاعل خارق) */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #F3E5AB 50%, #D4AF37 100%) !important;
        background-size: 200% auto !important;
        color: #000 !important;
        font-weight: 800 !important;
        font-size: 1.2em !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 30px !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4) !important;
        transition: 0.5s !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background-position: right center !important; /* حركة لمعان معدني */
        transform: scale(1.05) !important;
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.7) !important;
    }
    
    /* تعديل شريط الحماس */
    .stSlider > div > div > div {
        background-color: #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الاتصال بقاعدة البيانات ---
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("لم يتم العثور على الأسرار، يرجى التأكد من إعدادات Streamlit Cloud.")

# --- قسم اللوغو والعنوان ---
col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    try:
        # يفضل أن يكون اللوغو مفرغاً (PNG بخلفية شفافة) ليتناسق مع التصميم
        st.image("Logo.png", use_container_width=True)
    except:
        pass

st.markdown("<h1>✨ الانضمام لمكتب الفعاليات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #A8C3B8 !important;'>حيث نصنع الدهشة، ونرتقي بالنشاط الطلابي إلى مستويات غير مسبوقة</p>", unsafe_allow_html=True)
st.write("") # مسافة فارغة

# --- الاستمارة الفخمة ---
with st.form("luxury_volunteer_form", clear_on_submit=True):
    st.markdown("### 📋 بيانات المبدع:")
    name = st.text_input("👤 الاسم الثلاثي (كما تحب أن نكرمك به لاحقاً)")
    
    c1, c2 = st.columns(2)
    with c1:
        year = st.selectbox("🎓 السنة الدراسية", ["السنة الأولى", "السنة الثانية", "السنة الثالثة", "السنة الرابعة", "السنة الخامسة"])
    with c2:
        phone = st.text_input("📞 رقم الواتساب (للتواصل المباشر)")
        
    st.markdown("### 🎯 بصمتك الخاصة:")
    skills = st.text_area("🛠️ مهاراتك ومواهبك (قيادة، تصميم، تنظيم، مونتاج، تصوير، أو حتى طاقة إيجابية!)", height=100)
    
    st.markdown("### ⚡ مقياس الطاقة:")
    energy = st.select_slider("اختر مستوى حماسك للعمل ضمن الفريق", options=["مستعد 🌿", "نشيط 🌱", "متحمس 🌳", "طاقة جبارة 🔥"])
    
    st.write("")
    submit = st.form_submit_button("إرسال طلب الانضمام الآن 🚀")

# --- التفاعلات بعد الإرسال ---
if submit:
    if len(name) > 3 and len(phone) > 8:
        with st.spinner('⏳ جاري توثيق انضمامك لقائمة النخبة...'):
            try:
                # رفع البيانات
                data = {
                    "full_name": name, 
                    "academic_year": year, 
                    "phone_number": phone, 
                    "skills": skills, 
                    "energy_level": energy
                }
                supabase.table("volunteers").insert(data).execute()
                
                time.sleep(1) # تأثير تأخير بسيط لزيادة الفخامة
                st.balloons()
                
                # رسالة نجاح مبهرة
                st.markdown("""
                    <div style="background: rgba(46, 125, 50, 0.2); border: 1px solid #4CAF50; border-radius: 15px; padding: 20px; text-align: center; margin-top: 20px;">
                        <h3 style="color: #4CAF50 !important;">🎉 تمت العملية بنجاح!</h3>
                        <p style="color: white !important; font-size: 1.1em;">شكراً لك يا <b>{}</b>. لقد تم تسجيل بياناتك بنجاح، فريقنا متحمس جداً للتواصل معك قريباً.</p>
                    </div>
                """.format(name), unsafe_allow_html=True)
                
            except Exception as e:
                st.error("حدث خطأ أثناء الاتصال بقاعدة البيانات. يرجى المحاولة لاحقاً.")
    else:
        st.warning("⚠️ يرجى التأكد من كتابة الاسم الثلاثي ورقم الهاتف بشكل صحيح لضمان تواصلنا معك.")

# حقوق الملكية أو التوقيع أسفل الصفحة
st.markdown("""
    <div style="text-align: center; margin-top: 50px; opacity: 0.5;">
        <p style="font-size: 0.8em;">تصميم وتطوير بكل ❤️ من أجل كلية الهندسة الزراعية</p>
    </div>
""", unsafe_allow_html=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)