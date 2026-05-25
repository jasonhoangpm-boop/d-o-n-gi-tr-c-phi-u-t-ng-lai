# 🔥 Dynamic Stock Symbol Database Setup

## Tóm tắt thay đổi

Hệ thống giờ **tự động tạo bảng database** khi bạn nhập một mã cổ phiếu mới vào Streamlit app.

---


### 1. **`project/database/db_config.py`** ➕
```python
def create_stock_table(symbol: str) -> None:
    """Tự động tạo bảng {symbol}_prices nếu chưa tồn tại"""
    # - Tạo bảng mới với cấu trúc chuẩn
    # - Thiết lập primary key (date, interval)
    # - Log kết quả
```

**Chức năng:**
- Tự động tạo bảng `acb_prices`, `vnm_prices`, etc. khi cần
- Không tạo lặp lại nếu bảng đã tồn tại

---

### 2. **`project/data_pipeline/store_data.py`** ➕
```python
def store_stock_data(symbol: str, df: pd.DataFrame, interval: str = "5m") -> None:
    """Lưu dữ liệu cổ phiếu vào bảng {symbol}_prices"""
    # - Gọi create_stock_table() trước tiên
    # - Định dạng dữ liệu
    # - Upsert vào bảng động
```

**Chức năng:**
- Fetch dữ liệu từ dataframe
- Tự động tạo bảng nếu chưa tồn tại
- Lưu vào `{symbol}_prices` table

---

### 3. **`project/data_pipeline/fetch_data.py`** ➕
```python
def fetch_stock_data(symbol: str, interval: str = DEFAULT_INTERVAL, 
                     fallback_to_daily: bool = True) -> pd.DataFrame:
    """Fetch dữ liệu cổ phiếu tùy ý từ vnstock API"""
    # - Hỗ trợ mọi mã cổ phiếu (VNINDEX, ACB, VNM, FPT, etc.)
    # - Xử lý timezone
    # - Resample nếu cần
```

**Chức năng:**
- Fetch dữ liệu từ API cho bất kỳ mã nào
- Fallback to daily nếu lỗi
- Chuẩn hóa dữ liệu

---

### 4. **`ui/streamlit_app.py`** 🔄
```python
# Thêm import
from project.data_pipeline.fetch_data import fetch_stock_data
from project.data_pipeline.store_data import store_stock_data
from project.database.db_config import create_stock_table

# Cập nhật render_pipeline_controls()
def render_pipeline_controls(symbol: str = "VNINDEX") -> None:
    if st.sidebar.button("Sync Latest Data", use_container_width=True):
        try:
            # Step 1: Tạo bảng tự động
            create_stock_table(symbol)
            
            # Step 2: Fetch dữ liệu
            latest_data = fetch_stock_data(symbol=symbol, interval="5m")
            
            # Step 3: Lưu vào database
            store_stock_data(symbol=symbol, df=latest_data)
            
            st.sidebar.success(f"✅ {symbol} data synced!")
        except Exception as exc:
            st.sidebar.error(f"❌ Sync failed: {exc}")
```

---

## 🚀 Cách sử dụng

### **Sơ đồ quy trình:**

```
Người dùng nhập mã cổ phiếu (VD: ACB)
    ↓
render_symbol_selector() lấy ACB
    ↓
Bấm "Sync Latest Data"
    ↓
create_stock_table("ACB") 
    ├─ Tạo bảng acb_prices (nếu chưa có)
    └─ Thiết lập primary key
    ↓
fetch_stock_data("ACB", "5m")
    ├─ Gọi API vnstock cho ACB
    └─ Trả về DataFrame
    ↓
store_stock_data("ACB", df)
    └─ Lưu vào acb_prices
    ↓
✅ Hoàn thành! "ACB data synced to acb_prices table"
```

---

## 📊 Database tables được tạo tự động

Mỗi khi bạn nhập mã mới, hệ thống tạo bảng với cấu trúc:

```sql
CREATE TABLE IF NOT EXISTS {symbol}_prices (
    date TIMESTAMP NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume BIGINT,
    interval VARCHAR(10) NOT NULL,
    PRIMARY KEY (date, interval)
);
```

**Ví dụ các bảng tạo ra:**
- `vnindex_prices` (mặc định)
- `acb_prices` (khi bạn nhập ACB)
- `vnm_prices` (khi bạn nhập VNM)
- `fpt_prices` (khi bạn nhập FPT)
- vv...

---

## ✅ Workflow đầu cuối

1. **Mở Streamlit app**
   ```bash
   streamlit run ui/streamlit_app.py
   ```

2. **Nhập mã cổ phiếu vào sidebar**
   - VD: `ACB`, `VNM`, `FPT`, `VNINDEX`

3. **Bấm "Sync Latest Data"**
   - ✅ Bảng `acb_prices` tạo tự động (nếu chưa có)
   - ✅ Dữ liệu được fetch từ API
   - ✅ Dữ liệu được lưu vào database

4. **Xem biểu đồ**
   - Chọn timeframe
   - Xem dự đoán giá
   - Xem các chỉ số

---

## 🔧 Các file không thay đổi

Những file này **vẫn hoạt động bình thường**:
- `stock_prediction_project/models/lstm_model.py` (huấn luyện model)
- `ui/components/*.py` (hiển thị UI)
- `project/data_pipeline/preprocess_data.py` (tiền xử lý)

---

## ⚠️ Lưu ý

1. **API key**: Đảm bảo `vnstock` library đã cấu hình đúng
2. **PostgreSQL**: Kiểm tra `.env` có POSTGRES_* variables
3. **Timezone**: Tất cả dữ liệu tự động convert về `Asia/Ho_Chi_Minh`
4. **Interval**: Mặc định fetch `5m`, có thể change thành `1D`, `1H`, `15m`, `1m`

---

## 📝 Ví dụ fetch các cổ phiếu khác

```python
# Fetch ACB
df_acb = fetch_stock_data("ACB", interval="5m")
store_stock_data("ACB", df_acb)

# Fetch VNM
df_vnm = fetch_stock_data("VNM", interval="1D")
store_stock_data("VNM", df_vnm)

# Fetch FPT
df_fpt = fetch_stock_data("FPT", interval="1H")
store_stock_data("FPT", df_fpt)
```

---

## 🎯 Kết quả

```
Before:  Phải tạo bảng SQL thủ công cho mỗi cổ phiếu
After:   Chỉ cần nhập mã → Bảng tạo tự động → Dữ liệu load → App chạy ✅
```
