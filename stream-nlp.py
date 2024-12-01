import pickle
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from streamlit_option_menu import option_menu 
import pymysql
import sklearn


pymysql.install_as_MySQLdb()
# Tambahkan CSS untuk mempercantik tampilan
st.markdown("""
    <style>
        /* Background warna sidebar */
        .css-1d391kg {  
            background-color: #0073e6; /* Biru */
            color: white; /* Warna teks putih */
        }

        /* Background warna halaman utama */
        .css-18e3th9 { 
            background-color: #6a0dad; /* Ungu */
            color: white; /* Teks putih */
        }

        /* Judul utama */
        h1 {
            color: #0073e6; 
            font-family: 'Arial', sans-serif;
        }

        /* Label input */
        label {
            font-size: 14px; 
            font-weight: bold; 
            color: #2d3748; 
        }

        /* Tombol */
        .stButton > button {
            background-color: #0073e6;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            padding: 8px 16px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #005bb5;
            color: #ffffff;
        }

        /* Pesan sukses */
        .stAlert {
            background-color: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("Halaman Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if username == "ADMIN" and password == "ADMIN":
            st.session_state['logged_in'] = True
            st.success("Login berhasil!")
        else:
            st.error("Username atau password salah.")
else:
#membuat option menu
    with st.sidebar : 
        selected = option_menu ('SELAMAT DATANG', 
                            ['Biodata',
                             'Prediksi SMS'],
                             default_index=0)
                           
#masuk menu Prediksi
    if (selected =='Prediksi SMS') :

#load save model
        model_fraud = pickle.load(open('model_fraud.sav', 'rb'))
        tfidf = TfidfVectorizer
        loaded_vec = TfidfVectorizer(decode_error="replace", vocabulary=set(pickle.load(open("new_selected_feature.sav", "rb"))))

#judul halaman
        st.title ('Prediksi SMS Penipuan')

        clean_teks = st.text_input('Masukkan teks SMS')

        fraud_detection = ''

        if st.button('Hasil Deteksi'):
            predict_fraud = model_fraud.predict(loaded_vec.fit_transform([clean_teks]))

            if (predict_fraud==0):
                fraud_detection = 'SMS Normal'
            elif (predict_fraud==1):
                fraud_detection = 'SMS Penipuan'
            else:
                fraud_detection = 'SMS Promo'

        st.success(fraud_detection)
    
#masuk menu Biodata
    if (selected == 'Biodata') :
        st.title('Biodata')
        col1, col2 = st.columns(2)
        with col1 :
            Nama = st.text_input ('Masukkan nama anda :')
        with col2 :
            Tanggal_Lahir = st.text_input ('Masukkan NIK :')
        with col1 :
            Tempat_Lahir = st.text_input ('Masukkan Nomor HP :')
    
        Registrasi = st.button('Registrasi')
        if Registrasi :
            st.success(f'Berhasil Registrasi') 

