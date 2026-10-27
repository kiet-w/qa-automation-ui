# TESTCASES REPOSITORY ARCHITECTURE

> Thư mục lưu trữ tài sản kiểm thử nghiệp vụ (Business Test Assets) đồng bộ giữa bảng tính **Excel (.xlsx)** phục vụ đối soát/báo cáo và đặc tả **Markdown (.md)** định dạng chuẩn để **AI Coding Agents** tự động đọc và sinh mã kiểm thử Playwright/pytest.

---

## Cấu trúc Phân Cấp Module & Component (Cha / Con)

```text
testcases/
├── fs08/                               # Phân hệ FS-08: Parent Portal & SingPass
│   └── fs08-parent-profile/            # Màn hình My Details / Parent Profile (/profile)
│       ├── TC_FS08_Parent_Profile.xlsx # File Excel bảng tính (10 cột ISTQB, Summary & Locators)
│       └── TC_FS08_Parent_Profile.md   # File Markdown đặc tả chi tiết cho AI Coders
├── fs09/                               # Phân hệ FS-09: (Future Modules)
└── README.md                           # Hướng dẫn quy chuẩn kiến trúc
```

## Vai Trò Của Các File Trong Từng Component:
1. **File `.xlsx`**: Phục vụ đối soát với BA, Product Owner, QA Lead (chứa 3 Sheets: *Executive Summary*, *Test Cases Matrix 19 cột chuẩn Google Sheet AvePoint*, *BSK DOM Locators*).
2. **File `.md`**: Tài liệu Single Source of Truth cho AI Coding Agent (chứa đầy đủ Page Object mapping, BSK Live DOM selectors, Fixture JSON, kịch bản chi tiết step-by-step, mock API payload và Invariant 7 assertion rules).

---

## 🎯 QUY CHUẨN MA TRẬN KIỂM THỬ ĐẶC TẢ Ô NHẬP LIỆU (UNIVERSAL INPUT FIELD MATRIX)
Mọi tài liệu test case khi đặc tả các trường input (`<input>`, `<textarea>`) BẮT BUỘC phải triển khai trọn vẹn 2 nhóm kiểm thử:
- **Nhóm Chung (12 Lớp Kiểm Thử)**:
  1. Rỗng trường bắt buộc (`MSG-0001` - thông báo cụ thể cho từng trường).
  2. Rỗng trường không bắt buộc (Optional - cho phép lưu thành công).
  3. Chỉ toàn dấu cách (`"     "`) -> Tự trim và kích hoạt lỗi bắt buộc `MSG-0001` (Quy tắc `ASM-15`).
  4. Dấu cách đầu / cuối (`"  abc  "`) -> Tự trim sạch hoặc báo lỗi theo rule.
  5. Độ dài biên dưới ($Min-1, Min, Min+1$).
  6. Độ dài biên trên ($Max-1, Max, Max+1$) -> Ký tự thứ $Max+1$ bị chặn bởi `maxlength` hoặc báo lỗi.
  7. Dán chuỗi cực dài (Stress Paste 1000+ ký tự) -> Không treo, không vỡ layout, an toàn.
  8. Ký tự đặc biệt & Ký tự cấm (`!@#$%^&*()`, `< > { } ;`).
  9. Emoji, Tiếng Việt có dấu, chữ Trung/Nhật (`😀`, `Nguyễn`, `中文`) -> Bảo toàn UTF-8.
  10. Chuỗi tấn công cơ bản (`<script>alert(1)</script>`, `' OR 1=1 --`) -> Mã hóa an toàn HTML entities.
  11. **Xác thực Thông báo Lỗi UI & Chống Lộ Translation Key (i18n Key Leakage Prevention - BẮT BUỘC)**:
      - ⛔ **CẤM HIỂN THỊ RAW I18N KEY**: Tuyệt đối không được lộ các key dịch thuật như `features.parentProfile.validation.mobileInvalid`, `features.*`, `validation.*`.
      - Thông báo lỗi phải hiển thị đúng câu từ tiếng Anh chuẩn doanh nghiệp (`MSG-0805`, `MSG-0806`,...).
      - Visual Feedback: Ô nhập lỗi phải có viền đỏ (`aria-invalid="true"`, red border).
      - Tự động biến mất viền đỏ và thông báo lỗi ngay khi sửa đúng giá trị.
  12. Lưu bền vững và Reload: Dữ liệu sau khi lưu và tải lại trang phải chính xác 100%.

- **Nhóm Chuyên Biệt Theo Loại Ô**:
  - **Ô SỐ (Mobile, Postal Code)**: Đúng định dạng, lẫn chữ, chỉ chữ, dấu cách giữa, ký tự toán học/thập phân/âm, full-width `９１２３４５６７`, thiếu/thừa số, **bảo toàn số 0 ở đầu (`018956`)**, quy tắc đầu số Singapore (6/8/9), inputmode.
  - **Ô CHỮ (Full Name, Country)**: Thường/hoa/lẫn lộn, cấm số, chữ có dấu, gạch nối/nháy đơn (`Anne-Marie`, `O'Connor`), nhiều dấu cách.
  - **Ô CHỮ + SỐ (Block, Street, Unit)**: Chữ và số, chỉ số, chỉ chữ, Singapore Unit (`#12-34`), ký tự địa chỉ hợp lệ (`/ , . - #`) vs ký tự cấm (`< > { } ;`), biên 20/100 ký tự, xuống dòng khi dán.
  - **Ô EMAIL**: RFC 5322 hợp lệ, subdomain, chuẩn hóa chữ thường, chuỗi sai định dạng (`abc`, `abc@`, `@gmail.com`, `abc@@gmail.com`, `a b@gmail.com`, `abc@gmail..com`, `abc@gmail,com`, `abc@gmail.c`), biên >254 ký tự.
