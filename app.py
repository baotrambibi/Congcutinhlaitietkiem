import streamlit as st
st.image("logo.jpg", width=200)
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
    'Công cụ tính và theo dõi tiền gửi tiết kiệm theo từng kỳ hạn'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# LÃI SUẤT MẶC ĐỊNH
# =========================================================

# Muốn đổi lãi suất thì chỉ sửa số 6.0 bên dưới
LAI_SUAT_NAM = 6.0


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin gửi tiền")

    st.caption("Chỉ cần nhập số tiền và kỳ hạn gửi")

    st.markdown("### 💵 Số tiền gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    st.markdown("### ⏳ Kỳ hạn gửi")

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    st.markdown("---")

    st.info(
        f"📌 Lãi suất áp dụng hiện tại: **{LAI_SUAT_NAM:.2f}%/năm**"
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
        "Nhập **số tiền gửi** và **kỳ hạn gửi** ở thanh bên trái "
        "để xem chi tiết tiền lãi theo từng tháng."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# =========================================================
# CHUYỂN LÃI SUẤT
# =========================================================

lai_suat_nam = LAI_SUAT_NAM / 100


# =========================================================
# TÍNH LÃI ĐƠN THEO TỪNG THÁNG
# =========================================================

bang_lai_don = []

for thang in range(1, ky_han + 1):

    tien_lai_thang = (
        tien_gui
        * lai_suat_nam
        / 12
    )

    tong_lai = tien_lai_thang * thang

    tong_tien = tien_gui + tong_lai

    bang_lai_don.append({

        "Tháng": thang,

        "Tiền gốc": tien_gui,

        "Tiền lãi tháng": tien_lai_thang,

        "Tổng tiền lãi": tong_lai,

        "Tổng gốc + lãi": tong_tien
    })


df_lai_don = pd.DataFrame(bang_lai_don)


# =========================================================
# TÍNH LÃI KÉP THEO TỪNG THÁNG
# =========================================================

bang_lai_kep = []

so_du = tien_gui

for thang in range(1, ky_han + 1):

    tien_lai_thang = (
        so_du
        * lai_suat_nam
        / 12
    )

    so_du = so_du + tien_lai_thang

    bang_lai_kep.append({

        "Tháng": thang,

        "Tiền gốc đầu kỳ": so_du - tien_lai_thang,

        "Tiền lãi tháng": tien_lai_thang,

        "Tổng tiền lãi": so_du - tien_gui,

        "Tổng gốc + lãi": so_du
    })


df_lai_kep = pd.DataFrame(bang_lai_kep)


# =========================================================
# KẾT QUẢ CUỐI KỲ - LÃI ĐƠN
# =========================================================

tong_lai_don = df_lai_don.iloc[-1]["Tổng tiền lãi"]

tong_tien_don = df_lai_don.iloc[-1]["Tổng gốc + lãi"]


# =========================================================
# KẾT QUẢ CUỐI KỲ - LÃI KÉP
# =========================================================

tong_lai_kep = df_lai_kep.iloc[-1]["Tổng tiền lãi"]

tong_tien_kep = df_lai_kep.iloc[-1]["Tổng gốc + lãi"]


# =========================================================
# THÔNG TIN KHOẢN GỬI
# =========================================================

st.markdown(
    '<div class="section-title">📝 Thông tin khoản gửi</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Tiền gửi",
        format_money(tien_gui)
    )

with col2:

    st.metric(
        "⏳ Kỳ hạn",
        f"{ky_han} tháng"
    )

with col3:

    st.metric(
        "📈 Lãi suất",
        f"{LAI_SUAT_NAM:.2f}%/năm"
    )

with col4:

    st.metric(
        "📅 Số kỳ",
        f"{ky_han} kỳ"
    )


# =========================================================
# SO SÁNH LÃI ĐƠN - LÃI KÉP
# =========================================================

st.markdown(
    '<div class="section-title">📊 Kết quả cuối kỳ</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        <div class="result-card">

        <div class="result-icon">💵</div>

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

        <div class="result-icon">📈</div>

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
# BẢNG CHI TIẾT LÃI ĐƠN
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📅 Chi tiết tiền gửi theo từng tháng - Lãi đơn'
    '</div>',
    unsafe_allow_html=True
)

df_don_hien_thi = df_lai_don.copy()

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
# BẢNG CHI TIẾT LÃI KÉP
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Chi tiết tiền gửi theo từng tháng - Lãi kép'
    '</div>',
    unsafe_allow_html=True
)

df_kep_hien_thi = df_lai_kep.copy()

df_kep_hien_thi["Tiền gốc đầu kỳ"] = (
    df_kep_hien_thi["Tiền gốc đầu kỳ"]
    .apply(format_money)
)

df_kep_hien_thi["Tiền lãi tháng"] = (
    df_kep_hien_thi["Tiền lãi tháng"]
    .apply(format_money)
)

df_kep_hien_thi["Tổng tiền lãi"] = (
    df_kep_hien_thi["Tổng tiền lãi"]
    .apply(format_money)
)

df_kep_hien_thi["Tổng gốc + lãi"] = (
    df_kep_hien_thi["Tổng gốc + lãi"]
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

    "Lãi đơn": df_lai_don["Tổng gốc + lãi"],

    "Lãi kép": df_lai_kep["Tổng gốc + lãi"]

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
    '<div class="section-title">📐 Công thức</div>',
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

    📈 <b>Lãi suất:</b>
    {LAI_SUAT_NAM:.2f}%/năm

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
