```python
import streamlit as st
import pandas as pd

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM_CỦA BI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS - GIAO DIỆN
# ============================================================
st.markdown("""
<style>

    /* ===== BACKGROUND ===== */
    .stApp {
        background-color: #f5f7fb;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e8ebf0;
    }

    /* ===== MAIN TITLE ===== */
    .main-title {
        font-size: 36px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #687386;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* ===== RESULT CARDS ===== */
    .result-card {
        background: white;
        border-radius: 18px;
        padding: 22px 24px;
        border: 1px solid #e8ebf0;
        box-shadow: 0 4px 15px rgba(20, 30, 50, 0.05);
        min-height: 145px;
    }

    .result-title {
        color: #718096;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .result-value {
        color: #172033;
        font-size: 25px;
        font-weight: 800;
    }

    .result-icon {
        font-size: 24px;
        margin-bottom: 8px;
    }

    /* ===== INFO BOX ===== */
    .info-box {
        background: white;
        border-radius: 18px;
        padding: 22px;
        border: 1px solid #e8ebf0;
        box-shadow: 0 4px 15px rgba(20, 30, 50, 0.04);
        margin-top: 20px;
    }

    /* ===== SIDEBAR TITLE ===== */
    .sidebar-title {
        font-size: 23px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 4px;
    }

    .sidebar-subtitle {
        font-size: 13px;
        color: #7a8494;
        margin-bottom: 25px;
    }

    /* ===== SECTION TITLE ===== */
    .section-title {
        font-size: 23px;
        font-weight: 800;
        color: #172033;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: #929aaa;
        font-size: 13px;
        padding: 30px 0 10px 0;
    }

    /* ===== BUTTON ===== */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        font-weight: 700;
        font-size: 16px;
    }

    /* ===== DATAFRAME ===== */
    [data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ============================================================
# HEADER
# ============================================================
st.markdown(
    '<div class="main-title">'
    '💰 APP CÔNG CỤ TÍNH
```
