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
# CSS - GIAO DIỆN
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
}

/* Tiêu đề */
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

/* Section */
.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #172033;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Card */
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

/* Welcome box */
.welcome-box {
    background-color: white;
    border-radius: 18px;
    padding: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

/* Summary box */
.summary-box {
    background-color: white;
    border-radius: 18px;
    padding: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
}

/* Button */
.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
}

/* Footer */
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
# TIÊU ĐỀ APP
# =========================================================

st.markdown(
    '<div class="main-title">💰 APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM_CỦA BI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Công cụ tính lãi tiền gửi tiết kiệm theo lãi đơn và lãi kép</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR - NHẬP THÔNG TIN
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Thông tin gửi tiền")

    st.caption("Nhập thông tin khoản tiền gửi của bạn")

    st.markdown("### 💵 Khoản tiền gửi")

    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    st.markdown("### ⏳ Thời gian")

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    st.markdown("### 📈 Lãi suất")

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1
    )

    st.markdown("### 🧮 Phương pháp tính")

    loai_lai = st.radio(
        "Chọn hình thức",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    st.markdown("### 🗓️ Hình thức nhận lãi")

    hinh_thuc = st.selectbox(
        "Nhận lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

    st.markdown("---")

    tinh_lai = st.button(
        "✨ TÍNH TIỀN LÃI",
        type="primary"
    )


# =========================================================
# MÀN HÌNH BAN ĐẦU
# =========================================================

if not tinh_lai:

    st.markdown(
        '<div class="welcome-box">',
        unsafe_allow_html=True
    )

    st.markdown("## 👋 Chào mừng bạn!")

    st.write(
        "Hãy nhập thông tin khoản tiền gửi ở thanh bên trái, "
        "sau đó nhấn **TÍNH TIỀN LÃI** để xem kết quả."
    )

    st.write(
        "Bạn có thể lựa chọn giữa **lãi đơn** và **lãi kép**, "
        "đồng thời lựa chọn hình thức nhận lãi theo "
        "tháng, quý hoặc cuối kỳ."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 💡 Bạn có thể tính")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**💵 Lãi đơn**\n\n"
            "Tiền lãi được tính dựa trên số tiền gốc ban đầu."
        )

    with col2:
        st.info(
            "**📈 Lãi kép**\n\n"
            "Tiền lãi được cộng vào tiền gốc để tiếp tục sinh lãi."
        )

    with col3:
        st.info(
            "**🗓️ 3 hình thức nhận lãi**\n\n"
            "Theo tháng, theo quý hoặc cuối kỳ."
        )

    st.stop()


# =========================================================
# KIỂM TRA DỮ LIỆU
# =========================================================

if tien_gui <= 0:
    st.error("❌ Số tiền gửi phải lớn hơn 0.")
    st.stop()

if ky_han <= 0:
    st.error("❌ Kỳ hạn phải lớn hơn 0.")
    st.stop()

if lai_suat < 0:
    st.error("❌ Lãi suất không được nhỏ hơn 0.")
    st.stop()


# =========================================================
# CHUYỂN LÃI SUẤT
# =========================================================

lai_suat_nam = lai_suat / 100


# =========================================================
# TÍNH TOÁN
# =========================================================

bang_chi_tiet = []


# ---------------------------------------------------------
# LÃI ĐƠN
# ---------------------------------------------------------

if loai_lai == "Lãi đơn":

    # Tổng tiền lãi trong toàn bộ kỳ hạn
    tong_lai = tien_gui * lai_suat_nam * ky_han / 12

    # Tổng gốc + lãi
    tong_tien = tien_gui + tong_lai

    # Xác định số tháng mỗi kỳ
    if hinh_thuc == "Lãnh lãi hàng tháng":
        so_thang_moi_ky = 1

    elif hinh_thuc == "Lãnh lãi hàng quý":
        so_thang_moi_ky = 3

    else:
        so_thang_moi_ky = ky_han

    thang_da_tinh = 0
    ky = 1

    while thang_da_tinh < ky_han:

        so_thang = min(
            so_thang_moi_ky,
            ky_han - thang_da_tinh
        )

        lai_ky = (
            tien_gui
            * lai_suat_nam
            * so_thang
            / 12
        )

        thang_da_tinh += so_thang

        bang_chi_tiet.append({
            "Kỳ": ky,
            "Tháng": thang_da_tinh,
            "Tiền lãi": lai_ky,
            "Tổng gốc + lãi": tien_gui + lai_ky
        })

        ky += 1

    lai_dinh_ky = bang_chi_tiet[0]["Tiền lãi"]


# ---------------------------------------------------------
# LÃI KÉP
# ---------------------------------------------------------

else:

    so_du = tien_gui

    if hinh_thuc == "Lãnh lãi hàng tháng":

        so_ky = ky_han
        so_thang_moi_ky = 1

    elif hinh_thuc == "Lãnh lãi hàng quý":

        so_ky = (ky_han + 2) // 3
        so_thang_moi_ky = 3

    else:

        so_ky = 1
        so_thang_moi_ky = ky_han

    for ky in range(1, so_ky + 1):

        # Số tháng thực tế của kỳ hiện tại
        thang_bat_dau = (ky - 1) * so_thang_moi_ky

        so_thang_thuc_te = min(
            so_thang_moi_ky,
            ky_han - thang_bat_dau
        )

        # Lãi suất của kỳ
        lai_suat_ky = (
            lai_suat_nam
            * so_thang_thuc_te
            / 12
        )

        # Tiền lãi kỳ này
        lai_ky = so_du * lai_suat_ky

        # Cộng lãi vào gốc
        so_du = so_du + lai_ky

        thang = min(
            ky * so_thang_moi_ky,
            ky_han
        )

        bang_chi_tiet.append({
            "Kỳ": ky,
            "Tháng": thang,
            "Tiền lãi": lai_ky,
            "Tổng gốc + lãi": so_du
        })

    tong_tien = so_du

    tong_lai = tong_tien - tien_gui

    lai_dinh_ky = bang_chi_tiet[0]["Tiền lãi"]


# =========================================================
# KẾT QUẢ
# =========================================================

st.markdown(
    '<div class="section-title">📊 Kết quả tính toán</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-icon">💵</div>
            <div class="result-title">TIỀN LÃI ĐỊNH KỲ</div>
            <div class="result-value">
                {format_money(lai_dinh_ky)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-icon">📈</div>
            <div class="result-title">TỔNG TIỀN LÃI</div>
            <div class="result-value">
                {format_money(tong_lai)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-icon">🏦</div>
            <div class="result-title">TỔNG GỐC + LÃI</div>
            <div class="result-value">
                {format_money(tong_tien)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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
        "💰 Tiền gốc",
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
        f"{lai_suat:.2f}%/năm"
    )

with col4:
    st.metric(
        "🧮 Phương pháp",
        loai_lai
    )


# =========================================================
# BIỂU ĐỒ
# =========================================================

st.markdown(
    '<div class="section-title">📈 Biểu đồ tăng trưởng</div>',
    unsafe_allow_html=True
)

chart_data = pd.DataFrame(bang_chi_tiet)

chart_for_chart = chart_data[
    ["Tháng", "Tổng gốc + lãi"]
].copy()

chart_for_chart = chart_for_chart.set_index("Tháng")

st.line_chart(
    chart_for_chart,
    use_container_width=True
)


# =========================================================
# BẢNG CHI TIẾT
# =========================================================

st.markdown(
    '<div class="section-title">📅 Chi tiết từng kỳ</div>',
    unsafe_allow_html=True
)

df_hien_thi = chart_data.copy()

df_hien_thi["Tiền lãi"] = df_hien_thi[
    "Tiền lãi"
].apply(format_money)

df_hien_thi["Tổng gốc + lãi"] = df_hien_thi[
    "Tổng gốc + lãi"
].apply(format_money)

st.dataframe(
    df_hien_thi,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CÔNG THỨC
# =========================================================

st.markdown(
    '<div class="section-title">📐 Công thức áp dụng</div>',
    unsafe_allow_html=True
)

if loai_lai == "Lãi đơn":

    st.latex(
        r"I = P \times r \times t"
    )

    st.caption(
        "I: tiền lãi | P: tiền gốc | "
        "r: lãi suất năm | t: thời gian gửi tính theo năm"
    )

else:

    st.latex(
        r"A = P(1+r)^n"
    )

    st.caption(
        "A: tổng tiền nhận được | P: tiền gốc | "
        "r: lãi suất mỗi kỳ | n: số kỳ ghép lãi"
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

    💰 <b>Số tiền ban đầu:</b>
    {format_money(tien_gui)}

    <br><br>

    📅 <b>Kỳ hạn:</b>
    {ky_han} tháng

    <br><br>

    📈 <b>Lãi suất:</b>
    {lai_suat:.2f}%/năm

    <br><br>

    🧮 <b>Phương pháp:</b>
    {loai_lai}

    <br><br>

    🗓️ <b>Nhận lãi:</b>
    {hinh_thuc}

    <br><br>

    💵 <b>Tổng tiền lãi:</b>
    <b>{format_money(tong_lai)}</b>

    <br><br>

    🏦 <b>Tổng gốc + lãi:</b>
    <b>{format_money(tong_tien)}</b>

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
        Công cụ tính toán lãi tiền gửi tiết kiệm
    </div>
    """,
    unsafe_allow_html=True
)
