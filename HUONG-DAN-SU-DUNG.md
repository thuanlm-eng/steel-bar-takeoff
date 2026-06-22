# Hướng dẫn sử dụng — Phần mềm Bóc tách thép (Steel Bar Takeoff)

Phần mềm giúp bạn **bóc tách khối lượng cốt thép** tự động từ file PDF bản vẽ shop. Bạn tải file PDF lên, phần mềm dùng AI (Claude) để đọc các ký hiệu thép và xuất ra bảng số lượng, chiều dài, khối lượng (kg) — sau đó tải về file Excel.

---

## 1. Chuẩn bị trước khi dùng (chỉ làm 1 lần)

Bạn cần 2 thứ:

### a) Python (đã có sẵn trên máy này)
Phần mềm chạy bằng Python. Máy của bạn đã cài sẵn nên không cần làm gì.
Nếu chuyển sang máy khác chưa có Python, tải tại: https://www.python.org/downloads/
(Khi cài nhớ tích vào ô **"Add Python to PATH"**.)

### b) Khóa API của Claude (API key) — và phải có tiền (credit)
Phần mềm cần "chìa khóa" để gọi AI đọc bản vẽ.

1. Vào trang **https://console.anthropic.com**
2. Đăng nhập → vào mục **API Keys** → tạo một khóa mới (bắt đầu bằng `sk-ant-...`)
3. **Quan trọng:** vào mục **Plans & Billing** → nạp tiền (credit). Tối thiểu thường là 5 USD.

> ⚠️ Lưu ý: Tài khoản API **tính tiền riêng**, không liên quan đến gói Claude Pro/Max.
> Nếu chưa nạp tiền, phần mềm sẽ báo lỗi *"credit balance is too low"*.
> Mỗi lần bóc 1 bản vẽ chỉ tốn khoảng **vài xu (cents)**, nên 5 USD dùng được rất nhiều lần.

---

## 2. Khởi động phần mềm

**Nhấp đúp (double-click) vào file `start-takeoff.bat`**

- Một cửa sổ màu đen (Terminal) sẽ hiện ra — **đừng đóng nó** trong khi đang dùng.
- Trình duyệt (Chrome/Edge) sẽ tự mở trang phần mềm tại địa chỉ: **http://localhost:8765**

> 👉 Phải mở qua đường link `http://localhost:8765` này thì mới chạy được.
> **Không** nhấp đúp trực tiếp vào file `steel-bar-takeoff.html` — sẽ bị lỗi "Failed to fetch".

Khi dùng xong, đóng cửa sổ màu đen lại để tắt phần mềm.

---

## 3. Các bước bóc tách thép

1. **Tải bản vẽ lên:** kéo–thả file PDF vào ô tải lên, hoặc bấm vào ô đó để chọn file.
2. **Dán khóa API:** dán khóa `sk-ant-...` vào ô "Claude API key".
3. **OCR cho bản vẽ scan:** nếu bản vẽ là ảnh scan (không phải chữ gõ), giữ nguyên ô tích **"Enable OCR"** (chậm hơn nhưng đọc được ảnh).
4. **Bấm nút `⚡ Extract bars`** (Bóc tách thép).
5. Chờ một lúc (có thanh tiến trình). Khi xong, bảng kết quả sẽ hiện ra.

---

## 4. Phần mềm hiểu ký hiệu thép như thế nào

Phần mềm đọc đúng định dạng ký hiệu trên bản vẽ của bạn, ví dụ:

> **⑮  18Ø14a200  L=4320**

| Ký hiệu | Ý nghĩa |
|---|---|
| **⑮** (số trong vòng tròn) | Số hiệu thanh thép (bar mark) |
| **18** | Số lượng = 18 thanh |
| **Ø14** | Đường kính = 14 mm |
| **a200** | Khoảng cách giữa các thanh = 200 mm |
| **L=4320** | Chiều dài 1 thanh = 4320 mm |

---

## 5. Đọc kết quả

**Các ô số tổng (phía trên):** số ký hiệu thép, tổng số thanh, tổng chiều dài, và **tổng khối lượng (kg)**.

**Bảng "Weight summary by diameter" (Tổng hợp khối lượng theo đường kính):**
- Mỗi đường kính (Ø12, Ø14, Ø20…) có một dòng riêng.
- Hiển thị **tổng khối lượng (kg)** của từng loại đường kính + phần trăm.
- Dòng **Total** ở dưới cùng là tổng cộng tất cả.

**Bảng chi tiết (phía dưới):**
- Liệt kê từng thanh thép: số hiệu, đường kính, khoảng cách, chiều dài, số lượng, tổng dài (m), khối lượng (kg), vị trí.
- **Gộp ký hiệu trùng nhau:** các thanh có cùng số hiệu sẽ được cộng gộp thành 1 dòng (ví dụ `15 ×2` nghĩa là gộp từ 2 dòng). Bỏ tích ô **"group identical bar marks"** nếu muốn xem từng dòng riêng.

---

## 6. Lọc và xem tổng theo từng đường kính

- Chọn một đường kính trong ô **"All diameters"** → toàn bộ bảng và các ô số tổng sẽ **chỉ tính riêng cho đường kính đó** (ví dụ: *Total weight (Ø14 mm) = 125.29 kg*).
- Chọn vị trí cấu kiện trong ô **"All zones"** để lọc theo dầm/cột/sàn.
- Gõ vào ô **Search** để tìm nhanh.

---

## 7. Xuất file Excel

- Bấm nút **`⬇ Download Excel`** → tải về file `.xlsx` gồm 2 sheet:
  - **Bar takeoff** — bảng chi tiết từng thanh thép (kèm dòng tổng).
  - **Summary by diameter** — bảng tổng hợp khối lượng theo đường kính (kèm dòng tổng).
- Hoặc bấm **`📋 Copy CSV`** để sao chép rồi dán thẳng vào Excel.

> File xuất ra theo đúng bộ lọc đang xem. Muốn xuất toàn bộ thì để "All diameters" và "All zones".

---

## 8. Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân & cách khắc phục |
|---|---|
| **"Failed to fetch"** | Bạn đang mở file `.html` trực tiếp. → Hãy mở qua `start-takeoff.bat` và dùng link `http://localhost:8765`. |
| **"credit balance is too low"** | Tài khoản API chưa có tiền. → Vào console.anthropic.com → Plans & Billing → nạp credit. |
| **"Could not reach the local server"** | Cửa sổ màu đen (server) đã bị đóng. → Chạy lại `start-takeoff.bat`. |
| **Không tìm thấy thanh thép nào** | Bản vẽ là ảnh scan. → Giữ tích ô "Enable OCR" rồi bóc tách lại. |
| **Thiếu một số thanh thép** | Phần mềm chỉ đọc ~18.000 ký tự đầu của PDF. → Nếu bản vẽ rất dài, tách riêng trang có bảng thép rồi tải lên. |

---

## 9. Công thức tính khối lượng

Khối lượng thép được tính theo công thức tiêu chuẩn:

> **Khối lượng/mét = (Đường kính² × π/4) × 7850 / 1.000.000**  (đơn vị kg/m)
> **Khối lượng = Khối lượng/mét × Tổng chiều dài**

Kết quả khớp với bảng tra tiêu chuẩn (Ø12 = 0,888 kg/m; Ø14 = 1,21 kg/m; Ø20 = 2,47 kg/m).

---

*Mọi đơn vị khối lượng hiển thị bằng **kilôgam (kg)**, làm tròn 2 chữ số thập phân.*
