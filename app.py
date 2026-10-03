import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# HÀM FORMAT TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

col3, col4 = st.columns(2)

with col3:
    loai_lai = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

with col4:
    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r = lai_suat / 100

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # Xác định số tháng/kỳ nhận lãi
    if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":
        so_thang_moi_ky = 1
    elif hinh_thuc_nhan_lai == "Lãnh lãi hàng quý":
        so_thang_moi_ky = 3
    else:
        so_thang_moi_ky = ky_han

    # Số kỳ nhận lãi
    so_ky = ky_han // so_thang_moi_ky

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        tong_lai = tien_gui * r * so_nam
        tong_tien = tien_gui + tong_lai

        # Lãi mỗi kỳ
        lai_moi_ky = tien_gui * r * (so_thang_moi_ky / 12)

        # Tạo bảng chi tiết
        data = []

        for i in range(1, so_ky + 1):
            thang_ket_thuc = min(i * so_thang_moi_ky, ky_han)

            lai_ky = tien_gui * r * (so_thang_moi_ky / 12)

            # Kỳ cuối có thể có số tháng khác nếu kỳ hạn không chia hết
            if i == so_ky and ky_han % so_thang_moi_ky != 0:
                thang_thuc_te = ky_han - (i - 1) * so_thang_moi_ky
                lai_ky = tien_gui * r * (thang_thuc_te / 12)

            data.append({
                "Kỳ": i,
                "Thời điểm nhận lãi": f"Tháng {thang_ket_thuc}",
                "Tiền lãi kỳ này": format_money(lai_ky),
                "Tiền gốc": format_money(tien_gui),
                "Tổng nhận": format_money(tien_gui + lai_ky)
            })

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Với lãi kép:
        # - Lãnh lãi hàng tháng: ghép lãi mỗi tháng
        # - Lãnh lãi hàng quý: ghép lãi mỗi quý
        # - Lãnh lãi cuối kỳ: ghép lãi một lần vào cuối kỳ

        if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":
            so_ky_ghep = ky_han
            lai_suat_ky = r / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi hàng quý":
            so_ky_ghep = ky_han // 3
            lai_suat_ky = r / 4

        else:
            so_ky_ghep = 1
            lai_suat_ky = r

        # Tổng tiền cuối kỳ
        tong_tien = tien_gui * (1 + lai_suat_ky) ** so_ky_ghep
        tong_lai = tong_tien - tien_gui

        # Tạo bảng chi tiết
        data = []

        so_du = tien_gui

        if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":

            data.append({
                "Kỳ": 1,
                "Thời điểm nhận lãi": f"Tháng {ky_han}",
                "Tiền lãi kỳ này": format_money(tong_lai),
                "Tiền gốc": format_money(tien_gui),
                "Tổng nhận": format_money(tong_tien)
            })

        else:

            for i in range(1, so_ky_ghep + 1):

                so_du_moi = so_du * (1 + lai_suat_ky)
                lai_ky = so_du_moi - so_du

                if hinh_thuc_nhan_lai == "Lãnh lãi hàng tháng":
                    thang = i
                    ky_text = f"Tháng {thang}"
                else:
                    thang = i * 3
                    ky_text = f"Tháng {thang}"

                data.append({
                    "Kỳ": i,
                    "Thời điểm nhận lãi": ky_text,
                    "Tiền lãi kỳ này": format_money(lai_ky),
                    "Tiền gốc": format_money(so_du),
                    "Tổng nhận": format_money(so_du_moi)
                })

                so_du = so_du_moi

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(
                data[0]["Tiền lãi kỳ này"]
                .replace(".", "")
                .replace(" VNĐ", "")
            )
        )

    with col2:
        st.metric(
            "💰 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col3:
        st.metric(
            "🏦 Tổng gốc + lãi",
            format_money(tong_tien)
        )

    st.divider()

    # =========================
    # THÔNG TIN ĐÃ CHỌN
    # =========================
    st.subheader("📝 Thông tin khoản gửi")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")

    with info_col2:
        st.write(f"**Hình thức tính:** {loai_lai}")
        st.write(f"**Nhận lãi:** {hinh_thuc_nhan_lai}")

    st.divider()

    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.subheader("📅 Chi tiết tiền lãi")

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # CÔNG THỨC
    # =========================
    st.divider()

    st.subheader("📐 Công thức tính")

    if loai_lai == "Lãi đơn":
        st.latex(
            r"I = P \times r \times t"
        )
        st.caption(
            "Trong đó: P là tiền gốc, r là lãi suất năm, "
            "t là thời gian gửi tính theo năm."
        )

    else:
        st.latex(
            r"A = P(1+r)^n"
        )
        st.caption(
            "Trong đó: P là tiền gốc, r là lãi suất mỗi kỳ "
            "và n là số kỳ ghép lãi."
        )
