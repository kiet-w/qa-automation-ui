#!/usr/bin/env python3
import openpyxl

m_wb = openpyxl.load_workbook("/home/baudui/Projects/automation-ui/automation-uat/MASTER_TEST_EXECUTION_EVIDENCE_ALL_MODULES.xlsx", data_only=True)
ws_m = m_wb["Drive 06 Class Mgmt"]
for r in list(ws_m.iter_rows(values_only=True))[1:22]:
    print("Master Row:", r[:4])

c5_wb = openpyxl.load_workbook("reports/testcase5173/06_class_management/TEST_EXECUTION_EVIDENCE_06_Class_Management.xlsx", data_only=True)
ws_c5 = c5_wb["Test Cases"]
for r in list(ws_c5.iter_rows(values_only=True))[1:22]:
    print("Cand 5 Row:", r[:4])
