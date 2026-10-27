# Component Spec: ML Need Score Gauge & Deny Engine (`ml_need_score_gauge`)

## 1. Metadata & Selector
- **Component ID**: `F04-COMP-ML-GAUGE`
- **Component Name**: AI/ML Need Score Gauge & Deny Rules Widget (`Screen L` & Drawer Widget `C5/D4`)
- **Module**: `f04` (Assess FAS & Apply Subsidies)
- **Target Route**: Embedded inside FAS Review Drawer (`/admin/fas/applications`)
- **Target Role**: `School Admin` & `MOE HQ User`
- **Element Tag**: `<section role="region" aria-label="AI ML Need Score Engine">`

### Playwright Locators (BSK Live DOM Standard)
```typescript
export const mlGaugeLocators = {
  container: 'section[aria-label="AI ML Need Score Engine"]',
  gauge: {
    svgChart: 'svg[data-testid="ml-gauge-svg"]',
    needle: 'path[data-testid="ml-gauge-needle"]',
    scoreText: 'span[data-testid="ml-score-value"]',
    scoreMaxText: 'span[data-testid="ml-score-max"]',
    riskLevelBadge: 'span[data-testid="ml-risk-badge"]',
  },
  denyRulesBanner: {
    container: 'div[data-testid="ml-deny-rule-banner"][role="alert"]',
    ruleCode: 'strong[data-testid="deny-rule-code"]',
    ruleDescription: 'p[data-testid="deny-rule-desc"]',
  },
  factorsBreakdown: {
    container: 'div[data-testid="ml-factors-breakdown"]',
    incomeFactor: 'div[data-testid="factor-income"] span[data-testid="factor-val"]',
    householdSizeFactor: 'div[data-testid="factor-size"] span[data-testid="factor-val"]',
    jobStabilityFactor: 'div[data-testid="factor-stability"] span[data-testid="factor-val"]',
    specialNeedsFactor: 'div[data-testid="factor-special-needs"] span[data-testid="factor-val"]',
  },
  recommendation: {
    recommendedTierChip: 'span[data-testid="ml-recommended-tier"]',
    fastTrackBadge: 'span[data-testid="ml-fast-track-badge"]',
    rationaleText: 'p[data-testid="ml-rationale-text"]',
  },
};
```

---

## 2. BR / AC Traceability
- **Business Rules (BR)**:
  - `FS F4 Section 7.2 & 14.1`: **Hard Deny Rules Matrix** (checked prior to score calculation). If any Deny Rule triggers $\rightarrow \text{Need Score} = 0.00$, both tiers marked Ineligible, flagged with specific risk indicator:
    - `DENY-NO-CHILDREN`: Household contains 0 school-age children.
    - `DENY-ONLY-CHILDREN`: Household consists entirely of minors without adult guardian.
    - `DENY-INVALID-SIZE`: Household member count $\le 0$.
    - `DENY-WORKERS-EXCEED-SIZE`: Reported employed workers $>$ Total household members.
    - `DENY-NEGATIVE-MONTHS`: Months since last assistance $< 0$.
  - `FS F4 Section 14.2`: **Need Score Calculation Formula**:
    $$\text{Score} = 100 \times (0.70 \times \text{Income} + 0.05 \times \text{Size} + 0.10 \times \text{Housing} + 0.10 \times \text{JobStability} + 0.05 \times \text{SpecialNeeds})$$
  - **Risk Classification Bands**:
    - High Need / Risk: $\text{Need Score} \ge 75.00$ (Red `#DC2626`).
    - Medium Need / Risk: $50.00 \le \text{Need Score} \le 74.99$ (Amber `#D97706`).
    - Low Need / Risk: $\text{Need Score} < 50.00$ or triggered Deny Rule (Green `#16A34A`).
  - `T35`: **Fast-Track Policy**: Household received approved aid within last 3 months $\rightarrow$ Recency weight = 0.90, activates `Fast-track` badge.
- **Acceptance Criteria (AC)**:
  - `TC-256`: Need Score $\ge 75.00$ renders High Risk badge and recommends Tier 1.
  - `TC-257`: Need Score between $50.00$ and $74.99$ renders Medium Risk badge and recommends Tier 2.
  - `TC-258`: Application with 0 school-age children triggers `DENY-NO-CHILDREN`, score resets to $0.00$.
  - `TC-261`: Declaring 4 workers in a 3-person household triggers `DENY-WORKERS-EXCEED-SIZE`.

---

## 3. Ma Trận 12 Lớp Validation (AI/ML Gauge & Deny Engine Matrix)

| Lớp | Loại Kiểm Thử | Dữ Liệu Input / Thao Tác | Kỳ Vọng Hệ Thống (Expected Behavior) | Mã Lỗi / UI Indicator |
| :--- | :--- | :--- | :--- | :--- |
| **L01** | High Risk Band BVA ($75.00$) | Tính toán điểm số đạt đúng $75.00$ | Hiển thị điểm `75/100`; Badge đỏ `[HIGH FINANCIAL RISK]`; Gợi ý `Tier 1 (100%)`. | High Risk Red Badge |
| **L02** | High Risk Lower BVA ($74.99$) | Tính toán điểm số đạt đúng $74.99$ | Hiển thị điểm `74.99/100`; Badge vàng cam `[MEDIUM RISK]`; Gợi ý `Tier 2`. | Medium Risk Amber Badge |
| **L03** | Medium Risk Lower BVA ($50.00$) | Điểm số đạt đúng $50.00$ | Badge vàng cam `[MEDIUM RISK]`; Gợi ý `Tier 2`. | Medium Risk Amber Badge |
| **L04** | Low Risk Upper BVA ($49.99$) | Điểm số đạt đúng $49.99$ | Badge xanh lá `[LOW RISK]`; Gợi ý `Reject / Not Recommended`. | Low Risk Green Badge |
| **L05** | Deny Rule: Zero Children | Hồ sơ không có con trong độ tuổi đi học | Kích hoạt `DENY-NO-CHILDREN`; Score = `0.00`; Banner cảnh báo đỏ xuất hiện. | `DENY-NO-CHILDREN` |
| **L06** | Deny Rule: Minors Only | Hồ sơ gồm 2 đứa trẻ 8 và 10 tuổi, không có cha mẹ/người giám hộ | Kích hoạt `DENY-ONLY-CHILDREN`; Score = `0.00`; cờ xác minh cơ cấu gia đình. | `DENY-ONLY-CHILDREN` |
| **L07** | Deny Rule: Workers Exceed Members | Khai 4 người đi làm trong khi số nhân khẩu chỉ có 3 | Kích hoạt `DENY-WORKERS-EXCEED-SIZE`; Score = `0.00`; cờ kiểm toán xung đột. | `DENY-WORKERS-EXCEED-SIZE` |
| **L08** | Deny Rule: Negative Months | Số tháng từ lần nhận trợ cấp gần nhất là `-2` | Kích hoạt `DENY-NEGATIVE-MONTHS`; Score = `0.00`; chặn tự động tính điểm. | `DENY-NEGATIVE-MONTHS` |
| **L09** | Fast-Track Indicator | Lần hỗ trợ gần nhất là 1 tháng trước | Hiển thị chip màu tím: `[Fast-Track: Approved within 3 months]`. | Fast-track chip |
| **L10** | Factor Linear Clamping | $\text{GHI} > \$12,000$ hoặc $\text{PCI} > \$3,000$ | Trọng số Income bị kẹp chặt tại $0.00$, không sinh điểm âm. | Clamped between [0, 1] |
| **L11** | i18n & Risk Label Integrity | Toàn bộ nhãn điểm số, lý do gợi ý | Không xuất hiện `ml.score.highRisk`, `deny.rules.*`. | Localized labels |
| **L12** | SVG Render & Animation Performance | Render đồng hồ đo bán nguyệt (Gauge) | Kim đồng hồ quay mượt tới góc tương ứng với điểm số (CSS `transition: transform 600ms ease-out`); không giật lag. | Smooth SVG Transition |

---

## 4. Error Handling & Visual Feedback
- **Hard Deny Banner Feedback**:
  - Khi một Deny Rule được kích hoạt:
  - Đồng hồ hiển thị số `0.00` màu xám.
  - Phía trên xuất hiện Banner cảnh báo:
    `div[data-testid="ml-deny-rule-banner"]`:
    *"Data Inconsistency Flag: Triggered {DENY_RULE_CODE}. Application requires manual audit before any approval can be considered."*
- **Model Fallback State**:
  - Nếu ML scoring service tạm thời mất kết nối (503 Service Unavailable):
  - Widget hiển thị Fallback Card: *"ML Recommendation Engine is temporarily offline. Please evaluate application using standard GHI/PCI criteria."*

---

## 5. JSON Fixtures Data Payload

```json
{
  "ml_gauge_fixtures": {
    "high_risk_score": {
      "application_id": "APP-2026-00412",
      "need_score": 78.50,
      "risk_band": "HIGH",
      "recommended_tier": "Tier 1",
      "fast_track": false,
      "factors": {
        "income_score": 0.85,
        "dependency_score": 0.60,
        "job_stability_score": 0.80,
        "special_needs_score": 0.00
      },
      "rationale": "High dependency ratio with 3 school-going children and unstable contract employment."
    },
    "deny_rule_trigger": {
      "application_id": "APP-2026-00999",
      "need_score": 0.00,
      "risk_band": "LOW",
      "triggered_deny_rule": "DENY-WORKERS-EXCEED-SIZE",
      "deny_reason": "Reported employed workers (4) exceeds total household size (3).",
      "recommended_tier": "INELIGIBLE"
    }
  }
}
```
