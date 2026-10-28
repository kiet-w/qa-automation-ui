# Component Specification: Split Payment Amount Input (Billing & Payment)

## 1. Metadata & Selector

| Attribute | Specification |
| :--- | :--- |
| **Component Name** | `SplitPaymentAmountInputComponent` |
| **Target Page / Route** | `/billing/{studentId}` (`BillingPaymentPage`, SCR-04) |
| **Element Hierarchy** | Split container `<div>`, EA amount input wrapper `<div>`, Numeric input `<input>`, Online remainder display `<p>` / `<span>`, Error alert `<div>` |
| **Input Tag** | `<input inputmode="decimal" type="text" name="splitEaAmount" step="0.01">` |
| **Visual State** | Step 2 (Hiển thị có điều kiện khi chọn phương thức thanh toán `Both` / Split) |
| **Component Scope** | Cho phép phụ huynh tùy chỉnh số tiền trích từ Education Account; phần còn lại tự động tính trả qua Online Gateway |

### Playwright Live DOM Locators
```python
# Extracted from pages/fs09/billing_payment_page.py
FUNDING_BREAKDOWN = "div[class*='fundingBreakdown'], div[class*='splitBreakdown']"
SPLIT_EA_INPUT = "input[inputmode='decimal'], [class*='splitAmountField'] input, input[type='number']"
SPLIT_ERROR_ALERT = "[class*='splitBreakdown'] [role='alert'], [class*='splitAmountField'] [role='alert']"
ONLINE_REMAINDER_VAL = "p:has-text('Online portion'), span[class*='onlineRemainder']"
STEP2_CONTINUE_BTN = "div[class*='method'] button:has-text('Continue')"
```

---

## 2. Business Rules & Acceptance Criteria Traceability

| ID | Type | Description | Source Reference |
| :--- | :--- | :--- | :--- |
| **BR-F9-10** | Business Rule | Split payment must have 2 non-zero funding legs: Education Account leg and Online Payment leg. Neither leg can be $0.00$. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **BR-F9-11** | Business Rule | Mathematical balance constraint: $\text{EA portion} + \text{Online portion} = \text{Total Net Amount}$. Online portion cannot be edited directly; it is calculated as $Net - EA$. | `specs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md` |
| **AC-15** | Acceptance Criteria | Split Amount Validation: EA portion must be $> 0$, $< Net$, and $\le$ available EA balance. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-16** | Acceptance Criteria | Real-time calculation: Modifying the EA portion automatically and instantly updates the Online portion. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |
| **AC-19** | Acceptance Criteria | Validation errors: If EA portion $> \text{EA balance}$, display `EA_INSUFFICIENT_BALANCE`. If sum or bounds invalid, display `SPLIT_AMOUNT_INVALID`. | `specs/md/Test Cases/TC_R9_Outstanding_Fees_and_Payment.md` |

---

## 3. Ma trận 12 lớp Validation & UI Integrity

| Lớp (Layer) | Phân Loại Kiểm Thử | Dữ Liệu Đầu Vào (Input Vector) | Trạng Thái / Hành Vi UI Kỳ Vọng | Tiêu Chí Đạt (Pass Criteria) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Default Pre-population** | Giá trị mặc định khi mở | Net = `$70.63`, EA Balance = `$20.00` | Mặc định điền toàn bộ số dư khả dụng: `20.00`. Phần online tự tính hiển thị `50.63`. | Input value = `"20.00"`, Online = `"50.63"`. |
| **2. Empty Required** | Để trống ô chia tiền | Xóa trắng ô EA input (`""`) | Kích hoạt lỗi `SPLIT_AMOUNT_INVALID`. Chặn bấm Continue sang Step 3. | Thông báo lỗi xuất hiện, nút Continue disabled. |
| **3. All Whitespace** | Nhập toàn khoảng trắng | `"   "` (spaces) | Trim sạch, coi như rỗng, kích hoạt `SPLIT_AMOUNT_INVALID`. | Ô có viền đỏ. |
| **4. Zero Amount ($Min-1$)** | Nhập số 0 ($EA = 0$) | `0`, `0.00` | Bị từ chối vì chia đôi yêu cầu EA phải $> 0$. Kích hoạt `SPLIT_AMOUNT_INVALID`. | Báo lỗi: *"The two amounts must be more than zero and add up to the total."* |
| **5. Negative Amount** | Số âm | `-5`, `-20.00` | Bị chặn nhập hoặc kích hoạt lỗi `SPLIT_AMOUNT_INVALID`. | Không chấp nhận số âm. |
| **6. BVA Min Valid ($0.01$)** | Biên dưới hợp lệ ($Min$) | `0.01` | Hợp lệ. Phần Online tự tính = $Net - 0.01$. Không báo lỗi. | Online remainder = $Net - 0.01$. |
| **7. Equal to Net ($Max$)** | Nhập bằng đúng Net | EA portion = Net (vd: `70.63`) | Bị từ chối vì khi đó phần Online = $0$ (nên dùng tùy chọn Full EA thay vì Split). Kích hoạt `SPLIT_AMOUNT_INVALID`. | Báo lỗi `SPLIT_AMOUNT_INVALID`. |
| **8. Exceeding EA Balance** | Vượt quá số dư EA | EA Balance = $20.00$, nhập `25.00` | Kích hoạt lỗi `EA_INSUFFICIENT_BALANCE`. Chặn Continue. | Báo lỗi: *"Your Education Account balance is not enough for this amount..."* |
| **9. Real-Time Math Synchronicity**| Đồng bộ toán học thời gian thực| Gõ từng ký tự: `1` -> `10` -> `15` | Phần Online lập tức nhảy số tương ứng không có độ trễ: $Net - 1$, $Net - 10$, $Net - 15$. | Tổng 2 phần luôn chính xác $Net$. |
| **10. 3+ Decimal Places** | Vượt quá 2 chữ số thập phân | Nhập `20.005` hoặc `15.123` | Bị chặn bởi `step="0.01"` hoặc làm tròn chuẩn ngân hàng 2 chữ số thập phân. | Không cho phép 3 chữ số thập phân. |
| **11. Non-Numeric & Symbols** | Ký tự chữ và ký hiệu lạ | `S$20`, `20abc`, `20,00` | Bị từ chối hoặc chặn nhập ký tự lạ, giữ nguyên định dạng số. | Ký tự chữ bị loại bỏ. |
| **12. Security / Injection** | Tiêm mã độc vào ô số | `<script>alert(1)</script>`, `' OR 1=1` | Xử lý kiểu số thuần túy, loại bỏ hoàn toàn mã script độc hại. | Báo lỗi `SPLIT_AMOUNT_INVALID`. |

---

## 4. Error Handling & Visual Feedback

| Tình Huống Kích Hoạt | Mã Lỗi Chuẩn | Nội Dung Thông Báo Bắt Buộc | Trạng Thái DOM & Style |
| :--- | :--- | :--- | :--- |
| Ô trống, số 0, số âm, hoặc bằng Net | `SPLIT_AMOUNT_INVALID` | *"The two amounts must be more than zero and add up to the total."* | `aria-invalid="true"`, viền đỏ, alert hiển thị ngay dưới ô input. |
| Số tiền EA nhập lớn hơn số dư hiện có | `EA_INSUFFICIENT_BALANCE`| *"Your Education Account balance is not enough for this amount. You can pay the rest online."* | `aria-invalid="true"`, viền đỏ rực, thông báo hướng dẫn. |
| Nhập lại số tiền hợp lệ | N/A | Tự động xóa lỗi (Auto-dismissed) | `aria-invalid="false"`, xóa alert, bật lại nút Continue. |

---

## 5. JSON Fixtures Data Payload

```json
{
  "split_payment_fixtures": {
    "baseline_context": {
      "student_name": "Chloe Chan",
      "net_amount": 70.63,
      "ea_balance": 20.00,
      "default_ea_portion": 20.00,
      "default_online_portion": 50.63
    },
    "valid_mutations": [
      { "ea_portion": 10.00, "expected_online": 60.63, "description": "Partial EA 10.00" },
      { "ea_portion": 0.01, "expected_online": 70.62, "description": "Min BVA boundary 0.01" },
      { "ea_portion": 19.99, "expected_online": 50.64, "description": "Just under balance" }
    ],
    "invalid_cases": [
      { "ea_portion": 0.00, "expected_code": "SPLIT_AMOUNT_INVALID", "description": "Zero amount" },
      { "ea_portion": -5.00, "expected_code": "SPLIT_AMOUNT_INVALID", "description": "Negative amount" },
      { "ea_portion": 70.63, "expected_code": "SPLIT_AMOUNT_INVALID", "description": "Equal to net, online would be zero" },
      { "ea_portion": 25.00, "expected_code": "EA_INSUFFICIENT_BALANCE", "description": "Exceeds available EA balance 20.00" }
    ]
  }
}
```
