import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from datetime import datetime, timedelta

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hệ thống Dự báo Giá Cổ phiếu & Khuyến nghị Đầu tư",
    page_icon="📈",
    layout="wide"
)

# 2. Cố định Random Seed để kết quả ổn định
def fix_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    random.seed(seed)

fix_seed()

# Giao diện Tiêu đề chính
st.markdown("<h2 style='text-align: center; color: #1f77b4;'>📈 HỆ THỐNG DỰ BÁO GIÁ CỔ PHIẾU VÀ KHUYẾN NGHỊ THÔNG MINH</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ứng dụng mô hình học sâu LSTM kết hợp phân tích kỹ thuật xu hướng ngắn hạn</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar cấu hình giao diện
st.sidebar.markdown("### ⚙️ Cấu Hình Ứng Dụng")
ticker = st.sidebar.text_input("Nhập mã cổ phiếu (Ví dụ: VNM.VN, FPT.VN, AAPL):", value="VNM.VN")
start_date = st.sidebar.date_input("Ngày bắt đầu phân tích:", value=pd.to_datetime("2018-01-01"))
end_date = st.sidebar.date_input("Ngày kết thúc phân tích:", value=pd.to_datetime("2026-10-14"))

# Thanh trượt chọn số ngày dự báo tương lai (Khớp với giao diện mẫu của bạn)
forecast_days = st.sidebar.slider("Số ngày muốn dự đoán tương lai:", min_value=1, max_value=30, value=10)

# Cấu hình nâng cao trong sidebar
with st.sidebar.expander("🔧 Cài đặt mô hình nâng cao"):
    epochs = st.slider("Số Epochs huấn luyện", min_value=1, max_value=30, value=5)
    batch_size = st.selectbox("Batch Size", [16, 32, 64], index=1)

run_button = st.sidebar.button("🚀 Bắt đầu Phân tích & Dự đoán", type="primary")

if run_button:
    with st.spinner("⏳ Đang tải dữ liệu từ Yahoo Finance và huấn luyện mô hình LSTM... Vui lòng đợi trong giây lát!"):
        
        # 3. Tải và xử lý dữ liệu
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty or 'Close' not in df.columns:
            st.error("❌ Không tìm thấy dữ liệu cho mã cổ phiếu này hoặc khoảng thời gian không hợp lệ.")
            st.stop()
            
        # Sửa lỗi kiểu dữ liệu: Chuyển hẳn thành mảng 1 chiều dạng float gốc để tránh lỗi TypeError khi trích xuất giá
        close_series = df['Close']
        if isinstance(close_series, pd.DataFrame):
            close_series = close_series.iloc[:, 0]
        data = close_series.values.astype(float).reshape(-1, 1)

        train_size = int(0.8 * len(data))
        train_data = data[:train_size]
        test_data = data[train_size:]

        # Chuẩn hóa dữ liệu
        scaler = MinMaxScaler()
        train_scaled = scaler.fit_transform(train_data)
        test_scaled = scaler.transform(test_data)

        def create_sequences(seq_data, window_size=60):
            X, y = [], []
            for i in range(window_size, len(seq_data)):
                X.append(seq_data[i-window_size:i])
                y.append(seq_data[i])
            return np.array(X), np.array(y)

        X_train, y_train = create_sequences(train_scaled)
        test_combined = np.vstack((train_scaled[-60:], test_scaled))
        X_test, y_test = create_sequences(test_combined)

        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        # Tập Validation
        val_size = int(0.1 * len(X_train))
        X_val = X_train[-val_size:]
        y_val = y_train[-val_size:]
        X_train_final = X_train[:-val_size]
        y_train_final = y_train[:-val_size]

        # 4. Xây dựng và huấn luyện mô hình LSTM
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(60, 1)),
            LSTM(50),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')

        early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

        history = model.fit(
            X_train_final, y_train_final,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            shuffle=False,
            callbacks=[early_stop],
            verbose=0
        )

        # 5. Dự báo trên tập Test
        test_pred = model.predict(X_test)
        test_pred = scaler.inverse_transform(test_pred)
        y_test_real = scaler.inverse_transform(y_test.reshape(-1, 1))

        # Đánh giá mô hình
        rmse = np.sqrt(mean_squared_error(y_test_real, test_pred))
        mae = mean_absolute_error(y_test_real, test_pred)
        r2 = r2_score(y_test_real, test_pred)

        st.success("✅ Huấn luyện mô hình thành công!")
        
        # Hiển thị chỉ số đánh giá bằng Metrics đẹp mắt
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("📉 RMSE (Sai số căn bậc hai)", f"{rmse:,.2f}")
        col_m2.metric("📊 MAE (Sai số tuyệt đối trung bình)", f"{mae:,.2f}")
        col_m3.metric("🎯 R² Score (Độ phù hợp)", f"{r2:.4f}")

        # Bảng thông tin tổng quát 10 phiên mới nhất (Khớp giao diện yêu cầu)
        st.subheader(f"📋 Bảng thông tin tổng quát về giá cổ phiếu ({ticker})")
        recent_df = df.tail(10).copy()
        recent_df.index = recent_df.index.strftime('%Y-%m-%d')
        st.dataframe(recent_df, use_container_width=True)

        # 6. Dự báo tương lai theo số ngày tùy chọn trên thanh trượt
        last_60_days = np.vstack((train_scaled, test_scaled))[-60:]
        last_60_days = last_60_days.reshape(1, 60, 1)
        future_predictions = []
        
        for _ in range(forecast_days):
            next_pred = model.predict(last_60_days)
            future_predictions.append(next_pred[0, 0])
            last_60_days = np.append(
                last_60_days[:, 1:, :],
                next_pred.reshape(1, 1, 1),
                axis=1
            )
            
        future_predictions = np.array(future_predictions).reshape(-1, 1)
        future_predictions = scaler.inverse_transform(future_predictions)

        # Tạo danh sách ngày tương lai (giả lập ngày giao dịch tiếp theo bỏ qua cuối tuần hoặc tăng dần đơn giản)
        last_date = df.index[-1]
        future_dates = []
        curr = last_date
        for _ in range(forecast_days):
            curr += timedelta(days=1)
            # Bỏ qua thứ 7 và chủ nhật nếu cần thiết, ở đây cộng dồn ngày đơn giản
            while curr.weekday() >= 5: 
                curr += timedelta(days=1)
            future_dates.append(curr.strftime('%Y-%m-%d'))

        # 7. Sáng tạo: Đề xuất Đầu tư Tự động (Mua / Bán / Giữ)
        current_price = float(data[-1])
        predicted_mean = float(np.mean(future_predictions))
        price_change_pct = ((predicted_mean - current_price) / current_price) * 100

        st.markdown("---")
        st.subheader("💡 Đề xuất Đầu tư Thông minh (Giữ / Bán / Mua)")
        
        col_rec1, col_rec2 = st.columns([1, 2])
        with col_rec1:
            st.metric("Giá hiện tại gần nhất", f"{current_price:,.2f} VND")
            st.metric(f"Trung bình dự báo {forecast_days} ngày tới", f"{predicted_mean:,.2f} VND", f"{price_change_pct:+.2f}%")

        with col_rec2:
            st.markdown("#### 📌 Nhận định hệ thống:")
            if price_change_pct > 1.5:
                st.success("🟢 **KHUYẾN NGHỊ: MUA / TÍCH LŨY (BUY)**\n\nXu hướng ngắn hạn dự kiến tăng trưởng tốt. Phù hợp để gia tăng tỷ trọng cổ phiếu.")
            elif price_change_pct < -1.5:
                st.error("🔴 **KHUYẾN NGHỊ: BÁN / CHỐT LỜI (SELL)**\n\nXu hướng ngắn hạn cho thấy áp lực điều chỉnh giảm. Cân nhắc hạ tỷ trọng quản trị rủi ro.")
            else:
                st.warning("🟡 **KHUYẾN NGHỊ: GIỮ / QUAN SÁT (HOLD)**\n\nBiến động giá đi ngang trong biên độ hẹp. Tiếp tục theo dõi thêm các tín hiệu kỹ thuật khác.")

        # 8. Hiển thị kết quả dự báo và biểu đồ trực quan
        st.markdown("---")
        st.subheader(f"🔮 Kết quả dự đoán giá đóng cửa trong {forecast_days} ngày tới")
        
        col_table, col_chart = st.columns([1, 1.5])
        
        with col_table:
            st.markdown("**Bảng giá trị dự báo chi tiết:**")
            df_future = pd.DataFrame({
                "Ngày dự báo": future_dates,
                "Giá dự đoán (VND)": [f"{val:,.2f}" for val in future_predictions.flatten()]
            })
            st.dataframe(df_future, use_container_width=True, hide_index=True)

        with col_chart:
            fig_future, ax_future = plt.subplots(figsize=(10, 5))
            ax_future.plot(y_test_real, label="Giá thực tế (Tập Test)", color='blue', linewidth=1.5)
            ax_future.plot(test_pred, label="Giá mô hình đoán thử (Tập Test)", color='deepskyblue', linestyle='--', alpha=0.7)
            
            future_x = range(len(y_test_real), len(y_test_real) + forecast_days)
            ax_future.plot(future_x, future_predictions, marker='o', color='red', linestyle='--', label=f"Dự báo tương lai ({forecast_days} ngày)")
            
            ax_future.set_title(f"Biểu đồ so sánh giá thật và kết quả dự báo cổ phiếu {ticker}")
            ax_future.set_xlabel("Số phiên thời gian giao dịch")
            ax_future.set_ylabel("Mức giá đóng cửa")
            ax_future.legend(loc="upper left")
            ax_future.grid(True, linestyle=':', alpha=0.5)
            st.pyplot(fig_future)

else:
    st.info("👈 Vui lòng cấu hình tham số ở thanh bên trái và bấm nút **'Bắt đầu Phân tích & Dự đoán'** để chạy ứng dụng.")
