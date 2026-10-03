```python
import streamlit as st
import pandas as pd

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM_CỦA BI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
}

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #172033;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #172033;
    margin-top: 30px;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-top: 40px;
    padding-bottom: 20px;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================================================
# LOGO
# =========================================================

st.image("logo.jpg", width=180)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">'
    '💰 APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM_CỦA BI'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Tra cứu lãi suất và tính tiền gửi tiết kiệm theo từng ngân hàng'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DỮ LIỆU LÃI SUẤT THỰC TẾ
# Cập nhật: 02/10/2026
#
# Đơn vị: %/năm
# Hình thức: tiền gửi VND tại quầy - khách hàng cá nhân
# =========================================================

lai_suat_data = {

    "Bắc Á Bank": {
        1: 4.75,
        3: 4.75,
        6: 7.05,
        12: 7.10,
        18: 6.95,
        24: 6.95,
        36: 6.95
    },

    "Saigonbank": {
        1: 4.75,
        3: 4.75,
        6: 6.40,
        12: 6.70,
        18: 6.50,
        24: 6.00,
        36: 6.10
    },

    "PGBank": {
        1: 4.75,
        3: 4.75,
        6: 6.60,
        12: 6.70,
        18: 6.80,
        24: 6.80,
        36: 6.80
    },

    "OCB": {
        1: 4.75,
        3: 4.75,
        6: 6.40,
        12: 6.70,
        18: 6.60,
        24: 6.80,
        36: 7.00
```
