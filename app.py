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

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Dự báo giá cổ phiếu VNM & Khuyến nghị Mua/Bán",
    page_icon="📈",
    layout="wide"
)

# 2. Cố định Random Seed để kết quả ổn định
def fix_seed(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    random.seed(seed)

fix_seed()

# Giao diện Tiêu đề
st.title("📈 Ứng dụng Dự báo Giá Cổ phiếu VNM (LSTM) & Khuyến nghị Đầu tư")
st.markdown("""
Ứng dụng sử dụng mô hình học sâu **LSTM (Long Short-Term Memory)** để học dữ liệu lịch sử giá cổ phiếu **VNM** (Vinamilk), 
đưa ra dự báo xu hướng trong tương lai và tích hợp phân tích kỹ thuật nhanh để đưa ra tín hiệu **Giữ/Bán/Mua**.
""")

# Sidebar cấu hình
st.sidebar.header("⚙️ Cấu hình Mô hình")
ticker = st.sidebar.text_input("Mã cổ phiếu", value="VNM.VN")
start_date = st.sidebar.date_input("Ngày bắt đầu", value=pd.to_datetime("2018-01-01"))
end_date = st.sidebar.date_input("Ngày kết thúc", value=pd.to_datetime("2026-10-14"))
epochs = st.sidebar.slider("Số Epochs huấn luyện", min_value=1, max_value=20, value=5)
batch_size = st.sidebar.selectbox("Batch Size", [16, 32, 64], index=1)

# Nút chạy mô hình
run_button = st.sidebar.button("🚀 Huấn luyện & Dự báo")

if run_button:
    with st.spinner("Đang tải dữ liệu và huấn luyện mô hình LSTM... Vui lòng đợi trong giây lát!"):
        
        # 3. Tải và xử lý dữ liệu
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty or 'Close' not in df.columns:
            st.error("Không tìm thấy dữ liệu cho mã cổ phiếu này hoặc khoảng thời gian không hợp lệ.")
            st.stop()
            
        data = df[['Close']].values
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

        # 4. Xây dựng mô hình LSTM
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

        # Hiển thị các chỉ số đánh giá
        st.success("Huấn luyện mô hình hoàn tất!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("RMSE (Sai số căn bậc hai)", f"{rmse:.2f}")
        col2.metric("MAE (Sai số tuyệt đối trung bình)", f"{mae:.2f}")
        col3.metric("R² Score (Độ phù hợp)", f"{r2:.4f}")

        # Vẽ biểu đồ Loss
        st.subheader("📉 Quá trình huấn luyện (Loss Train vs Validation)")
        fig_loss, ax_loss = plt.subplots(figsize=(10, 4))
        ax_loss.plot(history.history['loss'], label='Train Loss', color='blue')
        ax_loss.plot(history.history['val_loss'], label='Validation Loss', color='orange')
        ax_loss.set_title("Loss qua các Epochs")
        ax_loss.legend()
        st.pyplot(fig_loss)

        # Vẽ biểu đồ dự báo trên tập Test
        st.subheader("📊 So sánh Giá thực tế và Giá dự báo trên tập Test")
        fig_test, ax_test = plt.subplots(figsize=(12, 5))
        ax_test.plot(y_test_real, label="Giá thật", color='green')
        ax_test.plot(test_pred, label="Dự báo Test", color='red', linestyle='--')
        ax_test.set_title("Kết quả dự báo tập kiểm thử")
        ax_test.legend()
        st.pyplot(fig_test)

        # 6. Dự báo 10 ngày tới
        last_60_days = np.vstack((train_scaled, test_scaled))[-60:]
        last_60_days = last_60_days.reshape(1, 60, 1)
        future_predictions = []
        
        for _ in range(10):
            next_pred = model.predict(last_60_days)
            future_predictions.append(next_pred[0, 0])
            last_60_days = np.append(
                last_60_days[:, 1:, :],
                next_pred.reshape(1, 1, 1),
                axis=1
            )
            
        future_predictions = np.array(future_predictions).reshape(-1, 1)
        future_predictions = scaler.inverse_transform(future_predictions)

        # 7. Sáng tạo thêm: Logic Khuyến nghị Giữ / Bán / Mua
        current_price = float(data[-1]) # Giá phiên gần nhất
        predicted_mean_10d = float(np.mean(future_predictions)) # Trung bình dự báo 10 ngày tới
        price_change_pct = ((predicted_mean_10d - current_price) / current_price) * 100

        st.markdown("---")
        st.subheader("💡 Đề xuất Đầu tư Sáng tạo (Giữ / Bán / Mua)")
        
        col_rec1, col_rec2 = st.columns([1, 2])
        
        with col_rec1:
            st.metric("Giá hiện tại (Gần nhất)", f"{current_price:,.2f} VND")
            st.metric("Trung bình dự báo 10 ngày tới", f"{predicted_mean_10d:,.2f} VND", f"{price_change_pct:+.2f}%")

        with col_rec2:
            st.markdown("#### Khuyến nghị tự động từ hệ thống:")
            if price_change_pct > 2.0:
                st.success("🟢 **KHUYẾN NGHỊ: MUA / TÍCH LŨY**\n\nMô hình dự báo xu hướng tăng trưởng trong 10 ngày tới. Cơ hội tốt để xem xét gia tăng tỷ trọng.")
            elif price_change_pct < -2.0:
                st.error("🔴 **KHUYẾN NGHỊ: BÁN / CHỐT LỜI / CẮT LỖ**\n\nMô hình dự báo xu hướng giảm giá mạnh trong ngắn hạn. Cân nhắc hạ tỷ trọng để bảo vệ vốn.")
            else:
                st.warning("🟡 **KHUYẾN NGHỊ: GIỮ (HOLD)**\n\nThị trường dự kiến đi ngang hoặc biên độ biến động hẹp. Nên quan sát thêm các chỉ báo vĩ mô hoặc kỹ thuật khác.")

        # Biểu đồ tổng hợp (Giá thật + Dự báo test + 10 ngày tới)
        st.subheader("🔮 Biểu đồ Dự báo 10 ngày tới")
        fig_future, ax_future = plt.subplots(figsize=(12, 6))
        ax_future.plot(y_test_real, label="Giá thật", color='green')
        ax_future.plot(test_pred, label="Dự báo test", color='red', linestyle='--')
        
        future_x = range(len(y_test_real), len(y_test_real) + 10)
        ax_future.plot(future_x, future_predictions, marker='o', label="10 ngày tới", color='purple')
        ax_future.set_title("Dự báo xu hướng giá 10 ngày tiếp theo")
        ax_future.legend()
        st.pyplot(fig_future)

        # Hiển thị bảng giá trị dự báo 10 ngày
        df_future = pd.DataFrame({
            "Ngày thứ": [f"Ngày {i+1}" for i in range(10)],
            "Giá dự báo (VND)": future_predictions.flatten()
        })
        st.table(df_future)
else:
    st.info("👈 Vui lòng bấm nút **'Huấn luyện & Dự báo'** ở thanh bên trái để bắt đầu chạy mô hình.")
