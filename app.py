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

.result-card {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 22px;
    min-height: 145px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

.result-icon {
    font-size: 25px;
    margin-bottom: 8px;
}

.result-title {
    font-size: 13px;
    font-weight: 700;
    color: #6b7280;
    margin-bottom: 8px;
}

.result-value {
    font-size: 24px;
    font-weight: 800;
    color: #172033;
}

.welcome-box {
    background-color: white;
    border-radius: 18px;
    padding: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

.summary-box {
    background-color: white;
    border-radius: 18px;
    padding: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

.rate-box {
    background-color: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-top: 40px;
    padding-bottom: 20px;
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

st.image("logo.jpg", width=200)


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
    'Công cụ tính tiền gửi tiết kiệm theo từng kỳ hạn'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# BẢNG LÃI SUẤT
# =========================================================
# Đây là bảng lãi suất MẪU.
# Có thể thay đổi các mức này tùy theo yêu cầu của bài.

bang_lai_suat = {
    1: 3.0,
    2: 3.0,
    3: 3.5,
    4: 3.5,
    5: 3.5,
    6: 4.8,
    7: 4.8,
    8: 4.8,
    9: 4.8,
    10: 5.0,
    11: 5.0,
    12: 5.2,
    13: 5.2,
    14: 5.2,
    15: 5.2,
    18: 5.5,
    24: 5.5
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin gửi tiền")

    st.caption(
        "Chỉ cần nhập số tiền và chọn kỳ hạn"
    )

    st.markdown("### 💵 Số tiền gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    st.markdown("### ⏳ Kỳ hạn gửi")

    ky_han = st.selectbox(
        "Chọn kỳ hạn",
        options=list(bang_lai_suat.keys()),
        format_func=lambda x: f"{x} tháng"
    )


# =========================================================
# KIỂM TRA
# =========================================================

if tien_gui <= 0:

    st.markdown(
        '<div class="welcome-box">',
        unsafe_allow_html=True
    )

    st.markdown("## 👋 Chào mừng bạn!")

    st.write(
        "Nhập số tiền gửi ở thanh bên trái để bắt đầu "
        "tính tiền lãi."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# =========================================================
# LẤY LÃI SUẤT THEO KỲ HẠN
# =========================================================

lai_suat = bang_lai_suat[ky_han]

lai_suat_nam = lai_suat / 100


# =========================================================
# THÔNG TIN KỲ HẠN ĐƯỢC CHỌN
# =========================================================

st.markdown(
    '<div class="section-title">📌 Kỳ hạn bạn đã chọn</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "💰 Số tiền gửi",
        format_money(tien_gui)
    )

with col2:

    st.metric(
        "⏳ Kỳ hạn",
        f"{ky_han} tháng"
    )

with col3:

    st.metric(
        "📈 Lãi suất áp dụng",
        f"{lai_suat:.2f}%/năm"
    )


# =========================================================
# TÍNH LÃI ĐƠN
# =========================================================

lai_thang_don = (
    tien_gui
    * lai_suat_nam
    / 12
)

tong_lai_don = (
    lai_thang_don
    * ky_han
)

tong_tien_don = (
    tien_gui
    + tong_lai_don
)


# =========================================================
# TÍNH LÃI KÉP
# =========================================================

so_du = tien_gui

bang_lai_kep = []

for thang in range(1, ky_han + 1):

    tien_lai_thang = (
        so_du
        * lai_suat_nam
        / 12
    )

    so_du_dau_ky = so_du

    so_du = so_du + tien_lai_thang

    bang_lai_kep.append({

        "Tháng": thang,

        "Số dư đầu kỳ": so_du_dau_ky,

        "Tiền lãi tháng": tien_lai_thang,

        "Số dư cuối kỳ": so_du

    })


tong_tien_kep = so_du

tong_lai_kep = (
    tong_tien_kep
    - tien_gui
)


# =========================================================
# KẾT QUẢ
# =========================================================

st.markdown(
    '<div class="section-title">📊 Kết quả tính toán</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-icon">
                💵
            </div>

            <div class="result-title">
                LÃI ĐƠN
            </div>

            <div class="result-value">
                {format_money(tong_tien_don)}
            </div>

            <br>

            Tổng tiền lãi:
            <b>{format_money(tong_lai_don)}</b>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-icon">
                📈
            </div>

            <div class="result-title">
                LÃI KÉP
            </div>

            <div class="result-value">
                {format_money(tong_tien_kep)}
            </div>

            <br>

            Tổng tiền lãi:
            <b>{format_money(tong_lai_kep)}</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# BẢNG LÃI SUẤT
# =========================================================

st.markdown(
    '<div class="section-title">📋 Bảng lãi suất theo kỳ hạn</div>',
    unsafe_allow_html=True
)

df_lai_suat = pd.DataFrame(
    [
        {
            "Kỳ hạn": f"{ky_han_item} tháng",
            "Lãi suất": f"{lai_suat_item:.2f}%/năm"
        }
        for ky_han_item, lai_suat_item
        in bang_lai_suat.items()
    ]
)

st.dataframe(
    df_lai_suat,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CHI TIẾT TỪNG THÁNG - LÃI ĐƠN
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📅 Chi tiết từng tháng - Lãi đơn'
    '</div>',
    unsafe_allow_html=True
)

bang_don = []

for thang in range(1, ky_han + 1):

    lai_tich_luy = (
        lai_thang_don
        * thang
    )

    tong_nhan = (
        tien_gui
        + lai_tich_luy
    )

    bang_don.append({

        "Tháng": thang,

        "Tiền gốc": tien_gui,

        "Tiền lãi tháng": lai_thang_don,

        "Tổng tiền lãi": lai_tich_luy,

        "Tổng gốc + lãi": tong_nhan

    })


df_don = pd.DataFrame(bang_don)


df_don_hien_thi = df_don.copy()

df_don_hien_thi["Tiền gốc"] = (
    df_don_hien_thi["Tiền gốc"]
    .apply(format_money)
)

df_don_hien_thi["Tiền lãi tháng"] = (
    df_don_hien_thi["Tiền lãi tháng"]
    .apply(format_money)
)

df_don_hien_thi["Tổng tiền lãi"] = (
    df_don_hien_thi["Tổng tiền lãi"]
    .apply(format_money)
)

df_don_hien_thi["Tổng gốc + lãi"] = (
    df_don_hien_thi["Tổng gốc + lãi"]
    .apply(format_money)
)

st.dataframe(
    df_don_hien_thi,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CHI TIẾT TỪNG THÁNG - LÃI KÉP
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Chi tiết từng tháng - Lãi kép'
    '</div>',
    unsafe_allow_html=True
)

df_kep = pd.DataFrame(bang_lai_kep)

df_kep_hien_thi = df_kep.copy()

df_kep_hien_thi["Số dư đầu kỳ"] = (
    df_kep_hien_thi["Số dư đầu kỳ"]
    .apply(format_money)
)

df_kep_hien_thi["Tiền lãi tháng"] = (
    df_kep_hien_thi["Tiền lãi tháng"]
    .apply(format_money)
)

df_kep_hien_thi["Số dư cuối kỳ"] = (
    df_kep_hien_thi["Số dư cuối kỳ"]
    .apply(format_money)
)

st.dataframe(
    df_kep_hien_thi,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# BIỂU ĐỒ
# =========================================================

st.markdown(
    '<div class="section-title">📈 Biểu đồ tăng trưởng</div>',
    unsafe_allow_html=True
)

chart = pd.DataFrame({

    "Lãi đơn": df_don["Tổng gốc + lãi"],

    "Lãi kép": df_kep["Số dư cuối kỳ"]

})

chart.index = range(
    1,
    ky_han + 1
)

chart.index.name = "Tháng"

st.line_chart(
    chart,
    use_container_width=True
)


# =========================================================
# CÔNG THỨC
# =========================================================

st.markdown(
    '<div class="section-title">📐 Công thức áp dụng</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 💵 Lãi đơn")

    st.latex(
        r"I = P \times r \times t"
    )

    st.caption(
        "Tiền lãi được tính dựa trên số tiền gốc ban đầu."
    )


with col2:

    st.markdown("### 📈 Lãi kép")

    st.latex(
        r"A = P(1+r)^n"
    )

    st.caption(
        "Tiền lãi được cộng vào số dư để tiếp tục sinh lãi."
    )


# =========================================================
# TÓM TẮT
# =========================================================

st.markdown(
    '<div class="section-title">✨ Tóm tắt khoản tiền gửi</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="summary-box">

    💰 <b>Số tiền gửi:</b>
    {format_money(tien_gui)}

    <br><br>

    ⏳ <b>Kỳ hạn:</b>
    {ky_han} tháng

    <br><br>

    📈 <b>Lãi suất áp dụng:</b>
    {lai_suat:.2f}%/năm

    <br><br>

    💵 <b>Tổng tiền lãi theo lãi đơn:</b>
    {format_money(tong_lai_don)}

    <br><br>

    📈 <b>Tổng tiền lãi theo lãi kép:</b>
    {format_money(tong_lai_kep)}

    <br><br>

    🏦 <b>Tổng tiền cuối kỳ theo lãi đơn:</b>
    {format_money(tong_tien_don)}

    <br><br>

    🏦 <b>Tổng tiền cuối kỳ theo lãi kép:</b>
    {format_money(tong_tien_kep)}

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        💰 APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM_CỦA BI

        <br>

        Công cụ tính toán tiền gửi tiết kiệm

    </div>
    """,
    unsafe_allow_html=True
)
