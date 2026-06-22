# Prompt tổng hợp project — Steel Bar Takeoff

> Dùng prompt dưới đây để tạo lại toàn bộ app từ đầu, hoặc bàn giao cho người / AI khác.

---

**Xây dựng một app web bóc tách khối lượng cốt thép (steel bar takeoff) từ file PDF bản vẽ shop.**

**Cách chạy:** App là 1 file `steel-bar-takeoff.html` (HTML/CSS/JS thuần) + 1 server relay Python (`server.py`, dùng thư viện chuẩn) + 1 file `start-takeoff.bat` để chạy 1-click trên Windows. Server phục vụ trang tại `http://localhost:8765` và **chuyển tiếp (relay) request sang Claude API ở phía server** để tránh lỗi CORS / "Failed to fetch" của trình duyệt. API key người dùng nhập chỉ đi thẳng từ máy họ tới Anthropic, không lưu lại.

**Luồng xử lý:** Người dùng kéo-thả PDF → nhập Claude API key (`sk-ant-...`) → bấm "Extract bars". App trích text bằng pdf.js; nếu PDF là ảnh scan thì chạy OCR bằng Tesseract.js. Text được gửi tới model `claude-opus-4-8` kèm prompt yêu cầu trả về JSON mảng các thanh thép.

**Định dạng ký hiệu cần hiểu:** số trong vòng tròn = bar mark; chuỗi dạng `18Ø14a200 L=4320` nghĩa là 18 thanh, đường kính 14mm, khoảng cách a200mm, dài 4320mm. Mỗi thanh có các trường: `mark, diameter, spacing, length, count, totalLength (m), weight (kg), zone`.

**Tính khối lượng:** `kg/m = (đường kính² × π/4) × 7850 / 1.000.000`, rồi `weight = kg/m × tổng chiều dài`. Mọi khối lượng hiển thị bằng **kg, làm tròn 2 chữ số thập phân**.

**Dashboard kết quả:**
- Các ô số tổng (filter-aware): số bar mark, tổng số thanh, tổng chiều dài, **tổng khối lượng (kg)** — đổi theo bộ lọc.
- **Bảng tổng hợp theo đường kính**: mỗi Ø một dòng với số thanh, tổng dài, **tổng phụ khối lượng (kg)**, % và dòng Total.
- **Bảng chi tiết** có **gộp các bar mark trùng nhau** (cộng dồn số lượng / chiều dài / khối lượng, gộp zone), kèm nút bật/tắt gộp.
- Lọc theo đường kính / zone, ô tìm kiếm, sắp xếp cột.

**Xuất dữ liệu:** nút "Download Excel" tạo file `.xlsx` (dùng SheetJS) gồm 2 sheet — *Bar takeoff* (chi tiết + dòng tổng) và *Summary by diameter* (tổng hợp theo đường kính + dòng tổng); kèm nút Copy CSV.

**Giao diện:** sạch, phẳng, có dark mode, responsive. Kèm xử lý lỗi rõ ràng (CORS, hết credit API, server tắt, PDF scan, PDF quá dài). Có file hướng dẫn sử dụng bằng tiếng Việt.

---

## Các file trong project

| File | Vai trò |
|---|---|
| `steel-bar-takeoff.html` | App chính (giao diện + logic) |
| `server.py` | Server Python phục vụ trang + relay Claude API |
| `start-takeoff.bat` | Chạy app 1-click trên Windows |
| `HUONG-DAN-SU-DUNG.md` | Hướng dẫn sử dụng tiếng Việt |
| `PROMPT-PROJECT.md` | File này — prompt tổng hợp project |
| `.claude/launch.json` | Cấu hình chạy server cho preview |
