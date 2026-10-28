# Recon — 02 Admin Dashboard Shell (Live DOM)

- **Thời điểm:** 2026-10-28 00:03:46
- **Target:** `http://localhost:5173/` (+ nested routes)
- **Script:** `2_Code_Automation/tools/recon_admin_shell.py` (headless Playwright, không chạy pytest)
- **Mục đích:** làm mới locator trước khi viết automation (Invariant 6 — evidence first).

## 1. Header (MOEHQ @ `/`)

```json
{
  "text": "Dashboard System Admin moehq",
  "links": [],
  "selects": [],
  "buttons": [
    {
      "text": "",
      "aria_label": "Collapse sidebar",
      "visible": true
    },
    {
      "text": "",
      "aria_label": "Open navigation",
      "visible": false
    }
  ]
}
```

## 2. Breadcrumb

```json
{
  "root": [
    {
      "tag": "NAV",
      "aria_label": "Breadcrumb",
      "cls": "_breadcrumbs_q9hkw_140",
      "text": "Dashboard"
    },
    {
      "tag": "OL",
      "aria_label": null,
      "cls": "_breadcrumbsList_q9hkw_355",
      "text": "Dashboard"
    },
    {
      "tag": "LI",
      "aria_label": null,
      "cls": "_breadcrumbItem_q9hkw_365",
      "text": "Dashboard"
    },
    {
      "tag": "SPAN",
      "aria_label": null,
      "cls": "_breadcrumbCurrent_q9hkw_375",
      "text": "Dashboard"
    }
  ],
  "nested_school_new": []
}
```

## 3. Sidebar groups & links (MOEHQ)

```json
[
  {
    "heading": "WORKSPACE",
    "links": [
      {
        "text": "Dashboard",
        "href": "/",
        "aria_current": "page",
        "cls": "_navigationLink_q9hkw_219 _navigationLinkActive_q9hkw_246",
        "visible": true
      }
    ]
  },
  {
    "heading": "EDUSAVE",
    "links": [
      {
        "text": "Education Accounts",
        "href": "/education-accounts",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "Top-up",
        "href": "/top-up",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "View As",
        "href": "/support-console",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      }
    ]
  },
  {
    "heading": "ACADEMIC RESOURCES",
    "links": [
      {
        "text": "School Users",
        "href": "/school-user-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "School management",
        "href": "/school-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "Students",
        "href": "/student-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      }
    ]
  },
  {
    "heading": "FINANCIAL",
    "links": [
      {
        "text": "Fee Batches",
        "href": "/fee-batches",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "Fees",
        "href": "/fee-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "FAS",
        "href": "/fas-application-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "MOEFAS",
        "href": "/moe-hq/moe-fas",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "FAS applications",
        "href": "/moe-hq/fas-applications",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      }
    ]
  }
]
```

## 4. Active state

- Root:
```json
[
  {
    "text": "Dashboard",
    "href": "/",
    "aria_current": "page",
    "cls": "_navigationLink_q9hkw_219 _navigationLinkActive_q9hkw_246",
    "visible": true
  }
]
```
- On `/school-management/new`:
```json
[]
```

## 5. Profile drawer & account menu

```json
{
  "trigger": {
    "text": "Sign out",
    "aria_label": "Sign out",
    "aria_haspopup": null,
    "cls": "_sidebarLogout_q9hkw_288"
  },
  "menu": {
    "error": "profile trigger not found"
  }
}
```

## 6. Language select

```json
null
```

## 7. Page identity & main content

```json
{
  "title": "EduFAMS | Admin Portal",
  "h1": [
    "Education Fanancial Account Management System"
  ],
  "main": {
    "id": "admin-main-content",
    "heading": "Education Fanancial Account Management System",
    "text": "Education Fanancial Account Management System This feature is scaffolded and ready for its business workflow."
  },
  "alerts": []
}
```

## 8. Access states

- MOEHQ → `/school-config` (SCHOOL-only):
```json
{
  "url": "http://localhost:5173/school-config",
  "alerts": []
}
```
- Unauthenticated → `/`:
```json
{
  "final_url": "http://localhost:5173/login"
}
```
- SCHOOL → `/school-management` (MOEHQ-only):
```json
{
  "url": "http://localhost:5173/",
  "alerts": [
    "Education Fanancial Account Management System",
    "Access restricted Your account does not have permission to view this area of the admin portal. ×"
  ]
}
```

## 10. SCHOOL persona sidebar (staff1@IAM.edu.vn)

```json
[
  {
    "heading": "WORKSPACE",
    "links": [
      {
        "text": "Dashboard",
        "href": "/",
        "aria_current": "page",
        "cls": "_navigationLink_q9hkw_219 _navigationLinkActive_q9hkw_246",
        "visible": true
      }
    ]
  },
  {
    "heading": "ACADEMIC RESOURCES",
    "links": [
      {
        "text": "School configuration",
        "href": "/school-config",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "Classes",
        "href": "/class-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "Students",
        "href": "/student-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      }
    ]
  },
  {
    "heading": "FINANCIAL",
    "links": [
      {
        "text": "Fee Batches",
        "href": "/fee-batches",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "Fees",
        "href": "/fee-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "FAS",
        "href": "/fas-application-management",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      },
      {
        "text": "SBFAS schemes",
        "href": "/sbfas-schemes",
        "aria_current": null,
        "cls": "_navigationLink_q9hkw_219",
        "visible": true
      }
    ]
  }
]
```

## 11. SCHOOL persona profile menu

```json
{
  "trigger": {
    "text": "Sign out",
    "aria_label": "Sign out",
    "aria_haspopup": null,
    "cls": "_sidebarLogout_q9hkw_288"
  },
  "menu": {
    "error": "profile trigger not found"
  },
  "alerts": []
}
```

## 12. Ghi chú đối chiếu spec

- So sánh với `02_admin_dashboard_shell.md` §1.1–§1.4: ghi lại mọi nhãn/selector khác biệt vào mục này.
- Recon này là nguồn DOM thật cho `pages/localhost-5173/locators.py`.
