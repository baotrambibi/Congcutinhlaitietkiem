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
# DỮ LIỆU LÃI SUẤT
# Đơn vị: %/năm
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
    },

    "HDBank": {
        1: 4.75,
        3: 4.75,
        6: 6.10,
        12: 6.30,
        18: 6.40,
        24: 6.40,
        36: 6.40
    },

    "VIB": {
        1: 4.50,
        3: 4.50,
        6: 5.70,
        12: 5.90,
        18: 5.90,
        24: 5.90,
        36: 5.90
    },

    "MSB": {
        1: 4.50,
        3: 4.50,
        6: 5.80,
        12: 6.00,
        18: 6.00,
        24: 6.00,
        36: 6.00
    },

    "Nam A Bank": {
        1: 4.50,
        3: 4.50,
        6: 5.80,
        12: 6.10,
        18: 6.30,
        24: 6.30,
        36: 6.30
    },

    "Eximbank": {
        1: 4.50,
        3: 4.50,
        6: 5.50,
        12: 5.90,
        18: 5.90,
        24: 5.90,
        36: 5.90
    },

    "VietABank": {
        1: 4.50,
        3: 4.50,
        6: 6.00,
        12: 6.20,
        18: 6.40,
        24: 6.40,
        36: 6.40
    },

    "KienlongBank": {
        1: 4.50,
        3: 4.50,
        6: 5.80,
        12: 6.00,
        18: 6.20,
        24: 6.20,
        36: 6.20
    },

    "NCB": {
        1: 4.50,
        3: 4.50,
        6: 6.00,
        12: 6.20,
        18: 6.30,
        24: 6.30,
        36: 6.30
    },

    "ABBank": {
        1: 4.50,
        3: 4.50,
        6: 5.70,
        12: 5.90,
        18: 5.90,
        24: 5.90,
        36: 5.90
    },

    "TPBank": {
        1: 4.30,
        3: 4.50,
        6: 5.50,
        12: 5.70,
        18: 5.70,
        24: 5.70,
        36: 5.70
    },

    "LPBank": {
        1: 4.20,
        3: 4.50,
        6: 5.40,
        12: 5.60,
        18: 5.60,
        24: 5.60,
        36: 5.60
    },

    "Sacombank": {
        1: 4.20,
        3: 4.50,
        6: 5.40,
        12: 5.60,
        18: 5.60,
        24: 5.60,
        36: 5.60
    },

    "ACB": {
        1: 4.10,
        3: 4.30,
        6: 5.30,
        12: 5.50,
        18: 5.50,
        24: 5.50,
        36: 5.50
    },

    "MB Bank": {
        1: 4.00,
        3: 4.20,
        6: 5.10,
        12: 5.30,
        18: 5.30,
        24: 5.30,
        36: 5.30
    },

    "Techcombank": {
        1: 3.95,
        3: 4.15,
        6: 4.95,
        12: 5.15,
        18: 5.15,
        24: 5.15,
        36: 5.15
    },

    "VPBank": {
        1: 4.00,
        3: 4.20,
        6: 5.20,
        12: 5.50,
        18: 5.50,
        24: 5.50,
        36: 5.50
    },

    "SHB": {
        1: 4.00,
        3: 4.20,
        6: 5.20,
        12: 5.50,
        18: 5.50,
        24: 5.50,
        36: 5.50
    },

    "SeABank": {
        1: 4.00,
        3: 4.20,
        6: 5.20,
        12: 5.40,
        18: 5.40,
        24: 5.40,
        36: 5.40
    },

    "Vietcombank": {
        1: 1.60,
        3: 1.90,
        6: 2.90,
        12: 4.60,
        18: 4.60,
        24: 4.60,
        36: 4.60
    },

    "BIDV": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.70,
        18: 4.70,
        24: 4.70,
        36: 4.70
    },

    "VietinBank": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.70,
        18: 4.70,
        24: 4.70,
        36: 4.70
    },

    "Agribank": {
        1: 1.70,
        3: 2.00,
        6: 3.00,
        12: 4.70,
        18: 4.70,
        24: 4.70,
        36: 4.70
    }
}


# =========================================================
# BẢNG LÃI SUẤT
# =========================================================

st.markdown(
    '<div class="section-title">📊 BẢNG LÃI SUẤT TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.caption("Đơn vị: %/năm")

bang_lai_suat = pd.DataFrame.from_dict(
    lai_suat_data,
    orient="index"
)

bang_lai_suat = bang_lai_suat.rename(
    columns={
        1: "1 tháng",
        3: "3 tháng",
        6: "6 tháng",
        12: "12 tháng",
        18: "18 tháng",
        24: "24 tháng",
        36: "36 tháng"
    }
)

bang_lai_suat.index.name = "Ngân hàng"

st.dataframe(
    bang_lai_suat,
    use_container_width=True,
    height=600
)


# =========================================================
# ĐƯỜNG PHÂN CÁCH
# =========================================================

st.divider()


# =========================================================
# CÔNG CỤ TÍNH TIỀN GỞI
# =========================================================

st.markdown(
    '<div class="section-title">🧮 CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.write(
    "Chọn ngân hàng và kỳ hạn. Hệ thống sẽ tự động lấy lãi suất tương ứng."
)


# =========================================================
# NHẬP THÔNG TIN
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    ngan_hang = st.selectbox(
        "🏦 Chọn ngân hàng",
        list(lai_suat_data.keys())
    )

with col2:
    ky_han = st.selectbox(
        "📅 Chọn kỳ hạn",
        [1, 3, 6, 12, 18, 24, 36],
        format_func=lambda x: f"{x} tháng"
    )

with col3:
    tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=100000,
        value=10000000,
        step=1000000,
        format="%d"
    )


# =========================================================
# LẤY LÃI SUẤT TỰ ĐỘNG
# =========================================================

lai_suat = lai_suat_data[ngan_hang][ky_han]

st.info(
    f"🏦 **{ngan_hang}** | "
    f"📅 Kỳ hạn: **{ky_han} tháng** | "
    f"📈 Lãi suất: **{lai_suat:.2f}%/năm**"
)


# =========================================================
# TÍNH LÃI
# =========================================================

so_nam = ky_han / 12

# Lãi đơn
tien_lai_don = tien_gui * (lai_suat / 100) * so_nam
tong_tien_don = tien_gui + tien_lai_don

# Lãi kép theo tháng
lai_thang = lai_suat / 100 / 12
so_thang = ky_han

tong_tien_kep = tien_gui * ((1 + lai_thang) ** so_thang)
tien_lai_kep = tong_tien_kep - tien_gui


# =========================================================
# KẾT QUẢ
# =========================================================

st.markdown(
    '<div class="section-title">💰 KẾT QUẢ TÍNH TOÁN</div>',
    unsafe_allow_html=True
)

r1, r2, r3 = st.columns(3)

with r1:
    st.metric(
        "Tiền gốc",
        format_money(tien_gui)
    )

with r2:
    st.metric(
        "Lãi đơn",
        format_money(tien_lai_don)
    )

with r3:
    st.metric(
        "Tổng tiền - Lãi đơn",
        format_money(tong_tien_don)
    )


r4, r5 = st.columns(2)

with r4:
    st.metric(
        "Lãi kép theo tháng",
        format_money(tien_lai_kep)
    )

with r5:
    st.metric(
        "Tổng tiền - Lãi kép",
        format_money(tong_tien_kep)
    )


# =========================================================
# BẢNG CHI TIẾT THEO THÁNG
# =========================================================

st.markdown(
    '<div class="section-title">📋 BẢNG TĂNG TRƯỞNG TIỀN GỬI</div>',
    unsafe_allow_html=True
)

thang_list = list(range(0, ky_han + 1))

gia_tri_don = [
    tien_gui * (1 + (lai_suat / 100) * (thang / 12))
    for thang in thang_list
]

gia_tri_kep = [
    tien_gui * ((1 + lai_thang) ** thang)
    for thang in thang_list
]

chi_tiet = pd.DataFrame({
    "Tháng": thang_list,
    "Tiền gốc": [tien_gui] * len(thang_list),
    "Giá trị - Lãi đơn": gia_tri_don,
    "Giá trị - Lãi kép": gia_tri_kep
})

chi_tiet_hien_thi = chi_tiet.copy()

chi_tiet_hien_thi["Tiền gốc"] = chi_tiet_hien_thi["Tiền gốc"].apply(format_money)
chi_tiet_hien_thi["Giá trị - Lãi đơn"] = chi_tiet_hien_thi[
    "Giá trị - Lãi đơn"
].apply(format_money)

chi_tiet_hien_thi["Giá trị - Lãi kép"] = chi_tiet_hien_thi[
    "Giá trị - Lãi kép"
].apply(format_money)

st.dataframe(
    chi_tiet_hien_thi,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# BIỂU ĐỒ
# =========================================================

st.markdown(
    '<div class="section-title">📈 BIỂU ĐỒ TĂNG TRƯỞNG</div>',
    unsafe_allow_html=True
)

chart_data = chi_tiet.set_index("Tháng")[
    ["Giá trị - Lãi đơn", "Giá trị - Lãi kép"]
]

st.line_chart(chart_data)


# =========================================================
# CÔNG THỨC
# =========================================================

st.markdown(
    '<div class="section-title">📐 CÔNG THỨC TÍNH</div>',
    unsafe_allow_html=True
)

with st.expander("Xem công thức"):

    st.markdown("### 1. Lãi đơn")

    st.latex(
        r"I = P \times r \times t"
    )

    st.write(
        "Trong đó:"
    )

    st.write(
        "- P: số tiền gốc"
    )

    st.write(
        "- r: lãi suất năm"
    )

    st.write(
        "- t: thời gian gửi tính theo năm"
    )

    st.markdown("### 2. Lãi kép theo tháng")

    st.latex(
        r"A = P\left(1+\frac{r}{12}\right)^n"
    )

    st.write(
        "Trong đó:"
    )

    st.write(
        "- A: số tiền nhận được"
    )

    st.write(
        "- P: số tiền gốc"
    )

    st.write(
        "- r: lãi suất năm"
    )

    st.write(
        "- n: số tháng gửi"
    )


# =========================================================
# LƯU Ý
# =========================================================

st.warning(
    "⚠️ Lãi suất trong bảng mang tính tham khảo cho mục đích học tập. "
    "Lãi suất thực tế có thể thay đổi theo thời điểm, số tiền gửi, "
    "hình thức gửi và chính sách của từng ngân hàng."
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '💰 APP CÔNG CỤ TÍNH TIỀN GỞI TIẾT KIỆM_CỦA BI'
    '<br>'
    'Ứng dụng phục vụ mục đích học tập'
    '</div>',
    unsafe_allow_html=True
)
