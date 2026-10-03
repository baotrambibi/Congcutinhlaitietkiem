import streamlit as st
import pandas as pd

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM CỦA BII",
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
        font-size: 38px;
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

    .info-title {
        font-size: 19px;
        font-weight: 750;
        color: #172033;
        margin-bottom: 15px;
    }

    /* ===== SIDEBAR TITLE ===== */
    .sidebar-title {
        font-size: 24px;
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
    '<div class="main-title">💰 Smart Savings Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Công cụ tính lãi tiền gửi tiết kiệm theo lãi đơn và lãi kép'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR - NHẬP DỮ LIỆU
# ============================================================
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚙️ Thông tin gửi tiền</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Nhập thông tin để bắt đầu tính toán'
        '</div>',
        unsafe_allow_html=True
    )

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
        ["Lãi đơn", "Lãi kép"]
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
        "✨ TÍNH TIỀN LÃI"
    )


# ============================================================
# KHI CHƯA NHẤN NÚT
# ============================================================
if not tinh_lai:

    st.markdown("""
    <div class="info-box">
        <div class="info-title">👋 Chào mừng bạn!</div>
        <p style="color:#687386;">
        Hãy nhập thông tin khoản tiền gửi ở thanh bên trái,
        sau đó nhấn <b>“TÍNH TIỀN LÃI”</b> để xem kết quả.
        </p>

        <p style="color:#687386;">
        Bạn có thể lựa chọn giữa <b>lãi đơn</b> và
        <b>lãi kép</b>, đồng thời thay đổi hình thức nhận lãi
        theo tháng, quý hoặc cuối kỳ.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💡 Bạn có thể tính")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            "**Lãi đơn**\n\n"
            "Tiền lãi được tính trên số tiền gốc ban đầu."
        )

    with c2:
        st.info(
            "**Lãi kép**\n\n"
            "Tiền lãi được cộng vào gốc để tiếp tục sinh lãi."
        )

    with c3:
        st.info(
            "**3 hình thức nhận lãi**\n\n"
            "Theo tháng, theo quý hoặc cuối kỳ."
        )

    st.stop()


# ============================================================
# KIỂM TRA DỮ LIỆU
# ============================================================
if tien_gui <= 0:
    st.error("❌ Số tiền gửi phải lớn hơn 0.")
    st.stop()

if lai_suat < 0:
    st.error("❌ Lãi suất không được nhỏ hơn 0.")
    st.stop()

if ky_han <= 0:
    st.error("❌ Kỳ hạn phải lớn hơn 0.")
    st.stop()


# ============================================================
# LÃI SUẤT NĂM
# ============================================================
lai_suat_nam = lai_suat / 100


# ============================================================
# XÁC ĐỊNH CHU KỲ
# ============================================================
if hinh_thuc == "Lãnh lãi hàng tháng":
    so_thang_moi_ky = 1

elif hinh_thuc == "Lãnh lãi hàng quý":
    so_thang_moi_ky = 3

else:
    so_thang_moi_ky = ky_han


# ============================================================
# KHỞI TẠO
# ============================================================
bang_chi_tiet = []


# ============================================================
# ===================== LÃI ĐƠN ==============================
# ============================================================
if loai_lai == "Lãi đơn":

    # Tổng lãi trong toàn bộ kỳ hạn
    tong_lai = (
        tien_gui
        * lai_suat_nam
        * ky_han
        / 12
    )

    tong_tien = tien_gui + tong_lai

    # Tạo bảng chi tiết
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
            "Tổng nhận": tien_gui + lai_ky
        })

        ky += 1

    # Lãi của kỳ đầu tiên
    lai_dinh_ky = bang_chi_tiet[0]["Tiền lãi"]


# ============================================================
# ===================== LÃI KÉP ==============================
# ============================================================
else:

    if hinh_thuc == "Lãnh lãi hàng tháng":

        so_ky = ky_han
        lai_suat_ky = lai_suat_nam / 12
        so_thang_moi_ky = 1

    elif hinh_thuc == "Lãnh lãi hàng quý":

        # Số kỳ, kể cả kỳ cuối nếu kỳ hạn không chia hết cho 3
        so_ky = (ky_han + 2) // 3
        lai_suat_ky = lai_suat_nam / 4
        so_thang_moi_ky = 3

    else:

        so_ky = 1
        lai_suat_ky = lai_suat_nam * ky_han / 12
        so_thang_moi_ky = ky_han

    so_du = tien_gui

    for ky in range(1, so_ky + 1):

        # Trường hợp lãnh lãi hàng quý
        # Xử lý cả kỳ cuối nếu kỳ hạn không đủ 3 tháng
        if hinh_thuc == "Lãnh lãi hàng quý":

            so_thang_thuc_te = min(
                3,
                ky_han - (ky - 1) * 3
            )

            lai_suat_ky_thuc_te = (
                lai_suat_nam
                * so_thang_thuc_te
                / 12
            )

        else:

            lai_suat_ky_thuc_te = lai_suat_ky

        lai_ky = so_du * lai_suat_ky_thuc_te

        so_du_moi = so_du + lai_ky

        thang = min(
            ky * so_thang_moi_ky,
            ky_han
        )

        bang_chi_tiet.append({
            "Kỳ": ky,
            "Tháng": thang,
            "Tiền lãi": lai_ky,
            "Tổng nhận": so_du_moi
        })

        so_du = so_du_moi

    tong_tien = so_du
    tong_lai = tong_tien - tien_gui

    lai_dinh_ky = bang_chi_tiet[0]["Tiền lãi"]


# ============================================================
# HEADER KẾT QUẢ
# ============================================================
st.markdown(
    '<div class="section-title">📊 Kết quả tính toán</div>',
    unsafe_allow_html=True
)


# ============================================================
# RESULT CARDS
# ============================================================
c1, c2, c3 = st.columns(3)

with c1:

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


with c2:

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


with c3:

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


# ============================================================
# THÔNG TIN KHOẢN GỬI
# ============================================================
st.markdown(
    '<div class="section-title">📝 Thông tin khoản gửi</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "💰 Tiền gốc",
        format_money(tien_gui)
    )

with c2:
    st.metric(
        "⏳ Kỳ hạn",
        f"{ky_han} tháng"
    )

with c3:
    st.metric(
        "📈 Lãi suất",
        f"{lai_suat:.2f}%/năm"
    )

with c4:
    st.metric(
        "🧮 Hình thức",
        loai_lai
    )


# ============================================================
# BIỂU ĐỒ
# ============================================================
st.markdown(
    '<div class="section-title">📈 Biểu đồ tăng trưởng</div>',
    unsafe_allow_html=True
)

chart_data = pd.DataFrame(bang_chi_tiet)

# Cột số dư dùng cho biểu đồ
chart_data["Số dư"] = chart_data["Tổng nhận"]

chart_for_chart = chart_data[
    ["Tháng", "Số dư"]
].copy()

chart_for_chart = chart_for_chart.set_index("Tháng")

st.line_chart(
    chart_for_chart,
    use_container_width=True
)


# ============================================================
# BẢNG CHI TIẾT
# ============================================================
st.markdown(
    '<div class="section-title">📅 Chi tiết từng kỳ</div>',
    unsafe_allow_html=True
)

# ============================================================
# QUAN TRỌNG:
# chart_data hiện có 5 cột:
# Kỳ | Tháng | Tiền lãi | Tổng nhận | Số dư
#
# Chỉ lấy 4 cột cần hiển thị trước khi đổi tên
# để tránh lỗi ValueError.
# ============================================================

df_hien_thi = chart_data[
    ["Kỳ", "Tháng", "Tiền lãi", "Tổng nhận"]
].copy()

# Định dạng tiền
df_hien_thi["Tiền lãi"] = df_hien_thi[
    "Tiền lãi"
].apply(format_money)

df_hien_thi["Tổng nhận"] = df_hien_thi[
    "Tổng nhận"
].apply(format_money)

# Đổi tên cột
df_hien_thi.columns = [
    "Kỳ",
    "Tháng",
    "Tiền lãi",
    "Tổng gốc + lãi"
]

st.dataframe(
    df_hien_thi,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CÔNG THỨC
# ============================================================
st.markdown(
    '<div class="section-title">📐 Công thức áp dụng</div>',
    unsafe_allow_html=True
)

if loai_lai == "Lãi đơn":

    st.latex(
        r"I = P \times r \times t"
    )

    st.caption(
        "I: tiền lãi • P: tiền gốc • "
        "r: lãi suất năm • t: thời gian gửi tính theo năm"
    )

else:

    st.latex(
        r"A = P(1+r)^n"
    )

    st.caption(
        "A: tổng tiền nhận được • P: tiền gốc • "
        "r: lãi suất mỗi kỳ • n: số kỳ ghép lãi"
    )


# ============================================================
# TÓM TẮT
# ============================================================
st.markdown(
    '<div class="section-title">✨ Tóm tắt khoản đầu tư</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="info-box">

    <b>💰 Số tiền ban đầu:</b> {format_money(tien_gui)}

    <br><br>

    <b>📅 Kỳ hạn:</b> {ky_han} tháng

    <br><br>

    <b>📈 Lãi suất:</b> {lai_suat:.2f}%/năm

    <br><br>

    <b>🧮 Phương pháp:</b> {loai_lai}

    <br><br>

    <b>🗓️ Nhận lãi:</b> {hinh_thuc}

    <br><br>

    <b>💵 Tổng tiền lãi:</b>
    <span style="font-size:20px; font-weight:800;">
    {format_money(tong_lai)}
    </span>

    <br><br>

    <b>🏦 Tổng số tiền cuối kỳ:</b>
    <span style="font-size:20px; font-weight:800;">
    {format_money(tong_tien)}
    </span>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        💰 Smart Savings Calculator &nbsp;•&nbsp;
        Công cụ tính toán lãi tiền gửi tiết kiệm
    </div>
    """,
    unsafe_allow_html=True
)
