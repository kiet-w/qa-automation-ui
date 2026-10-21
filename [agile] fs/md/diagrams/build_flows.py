#!/usr/bin/env python3
"""
build_flows.py - Generates editorial vector SVG flow diagrams for EAFAMS
compliant with combo-diagram (Solid #0B101B background, 6 connector rules,
orthogonal elbows r=8, crisp typography, and semantic color palettes).
"""

import os
from pathlib import Path

OUT_DIR = Path("/home/baudui/Projects/fs/document/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# FLOW 1: GLOBAL INTERACTION & ARCHITECTURE FLOW (LR PIPELINE)
# -------------------------------------------------------------
def generate_global_flow():
    svg = """<svg viewBox="0 0 1180 560" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B101B"/>
      <stop offset="100%" stop-color="#0E1524"/>
    </linearGradient>
    <linearGradient id="zone-admin" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-parent" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-core" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6366f1" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-ext" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.02"/>
    </linearGradient>

    <!-- Markers -->
    <marker id="arr-sky" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#38bdf8"/>
    </marker>
    <marker id="arr-emerald" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#10b981"/>
    </marker>
    <marker id="arr-amber" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#f59e0b"/>
    </marker>
    <marker id="arr-purple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#a855f7"/>
    </marker>
  </defs>

  <!-- Canvas Solid Opaque Background -->
  <rect width="100%" height="100%" rx="14" fill="url(#bg-grad)"/>

  <!-- GRID / STAGE HEADER -->
  <rect x="0" y="0" width="1180" height="42" fill="#151C2C" rx="14" />
  <rect x="0" y="32" width="1180" height="10" fill="#151C2C" />
  <line x1="0" y1="42" x2="1180" y2="42" stroke="#1e293b" stroke-width="1.2"/>
  <circle cx="24" cy="21" r="5" fill="#f43f5e"/>
  <circle cx="40" cy="21" r="5" fill="#f59e0b"/>
  <circle cx="56" cy="21" r="5" fill="#10b981"/>
  <text x="76" y="25" fill="#94a3b8" font-family="monospace" font-size="12" font-weight="600">EAFAMS // END-TO-END SYSTEM INTERACTION &amp; SERVICE INTEGRATION ARCHITECTURE</text>
  <rect x="1000" y="10" width="160" height="22" rx="4" fill="#0369a1" fill-opacity="0.3" stroke="#38bdf8" stroke-width="1"/>
  <text x="1080" y="25" fill="#38bdf8" font-family="monospace" font-size="10.5" font-weight="700" text-anchor="middle">LIVE TOPOLOGY FLOW</text>

  <!-- ==================== ZONES ==================== -->
  <!-- Zone 1: Admin Portal Zone (Top Left) -->
  <rect x="30" y="60" width="260" height="225" rx="12" fill="url(#zone-admin)" stroke="#0284c7" stroke-width="1.2" stroke-dasharray="4 4"/>
  <rect x="45" y="52" width="140" height="18" rx="4" fill="#0f172a" stroke="#0284c7" stroke-width="1"/>
  <text x="115" y="65" fill="#38bdf8" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">🏛️ ADMIN PORTAL</text>

  <!-- Zone 2: e-Service Portal Zone (Bottom Left) -->
  <rect x="30" y="305" width="260" height="230" rx="12" fill="url(#zone-parent)" stroke="#10b981" stroke-width="1.2" stroke-dasharray="4 4"/>
  <rect x="45" y="297" width="155" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1"/>
  <text x="122" y="310" fill="#34d399" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">📱 e-SERVICE PORTAL</text>

  <!-- Zone 3: Core Service Modules (Middle) -->
  <rect x="340" y="60" width="500" height="475" rx="12" fill="url(#zone-core)" stroke="#6366f1" stroke-width="1.2" stroke-dasharray="4 4"/>
  <rect x="360" y="52" width="220" height="18" rx="4" fill="#0f172a" stroke="#6366f1" stroke-width="1"/>
  <text x="470" y="65" fill="#818cf8" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">⚙️ CORE APPLICATION &amp; LEDGER</text>

  <!-- Zone 4: External Providers & Integrations (Right) -->
  <rect x="880" y="60" width="270" height="475" rx="12" fill="url(#zone-ext)" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="4 4"/>
  <rect x="900" y="52" width="210" height="18" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1"/>
  <text x="1005" y="65" fill="#fbbf24" font-family="sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">🌐 EXTERNAL ECOSYSTEM &amp; AI</text>

  <!-- ==================== CONNECTORS (Rendered BEFORE nodes) ==================== -->
  <!-- Admin to Core -->
  <path d="M 270 120 L 370 120" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#arr-sky)"/>
  <path d="M 270 185 L 315 185 Q 323 185 323 193 L 323 232 Q 323 240 331 240 L 370 240" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#arr-sky)"/>
  
  <!-- Parent to Core -->
  <path d="M 270 370 L 370 370" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#arr-emerald)"/>
  <path d="M 270 450 L 320 450 Q 328 450 328 458 L 328 472 Q 328 480 336 480 L 370 480" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#arr-emerald)"/>

  <!-- Core Internal Pipes -->
  <path d="M 570 120 L 610 120" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#arr-purple)"/>
  <path d="M 570 240 L 610 240" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#arr-purple)"/>
  <path d="M 570 370 L 610 370" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#arr-purple)"/>
  <path d="M 570 480 L 610 480" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#arr-purple)"/>

  <!-- Core to External Integrations -->
  <path d="M 810 120 L 910 120" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#arr-amber)"/>
  <path d="M 810 240 L 910 240" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#arr-amber)"/>
  <path d="M 810 370 L 910 370" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#arr-amber)"/>
  <path d="M 810 480 L 910 480" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#arr-amber)"/>

  <!-- Connector Masks & Labels -->
  <rect x="282" y="112" width="76" height="16" rx="3" fill="#0f172a" stroke="#0284c7" stroke-width="0.8"/>
  <text x="320" y="124" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="600" text-anchor="middle">R1/R2/R3</text>

  <rect x="282" y="362" width="76" height="16" rx="3" fill="#0f172a" stroke="#059669" stroke-width="0.8"/>
  <text x="320" y="374" fill="#34d399" font-family="monospace" font-size="9" font-weight="600" text-anchor="middle">R9 Pay / Rev</text>

  <rect x="822" y="112" width="76" height="16" rx="3" fill="#0f172a" stroke="#d97706" stroke-width="0.8"/>
  <text x="860" y="124" fill="#fbbf24" font-family="monospace" font-size="9" font-weight="600" text-anchor="middle">Citizen Sync</text>

  <rect x="822" y="362" width="76" height="16" rx="3" fill="#0f172a" stroke="#d97706" stroke-width="0.8"/>
  <text x="860" y="374" fill="#fbbf24" font-family="monospace" font-size="9" font-weight="600" text-anchor="middle">Sandbox Pay</text>

  <!-- ==================== NODE CARDS ==================== -->
  <!-- Admin Nodes -->
  <g id="node-moehq">
    <rect x="50" y="85" width="220" height="68" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="65" y="110" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">MOE HQ Specialist</text>
    <text x="65" y="128" fill="#94a3b8" font-family="monospace" font-size="9.5">R1 Lifecycle · R2 Bulk TopUp · R7 Sim</text>
    <rect x="205" y="93" width="55" height="16" rx="3" fill="#0369a1" stroke="#38bdf8" stroke-width="0.8"/>
    <text x="232" y="104" fill="#ffffff" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">HQ USER</text>
  </g>

  <g id="node-schooluser">
    <rect x="50" y="165" width="220" height="95" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="65" y="190" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">School Admin / Staff</text>
    <text x="65" y="208" fill="#94a3b8" font-family="monospace" font-size="9.5">R3 Class/Fee · R4 SBFAS · R5 OCR</text>
    <text x="65" y="224" fill="#64748b" font-family="monospace" font-size="9">RBAC Scoped to School ID</text>
    <rect x="195" y="173" width="65" height="16" rx="3" fill="#0369a1" stroke="#38bdf8" stroke-width="0.8"/>
    <text x="227" y="184" fill="#ffffff" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">SCH USER</text>
  </g>

  <!-- Parent Nodes -->
  <g id="node-singpass">
    <rect x="50" y="335" width="220" height="70" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
    <text x="65" y="360" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">Parents &amp; Guardians</text>
    <text x="65" y="378" fill="#94a3b8" font-family="monospace" font-size="9.5">Singpass Mock · NRIC Linkage</text>
    <text x="65" y="394" fill="#64748b" font-family="monospace" font-size="9">R8 Child Cards &amp; EA Balances</text>
    <rect x="200" y="343" width="60" height="16" rx="3" fill="#047857" stroke="#10b981" stroke-width="0.8"/>
    <text x="230" y="354" fill="#ffffff" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">CITIZEN</text>
  </g>

  <g id="node-parent-fas">
    <rect x="50" y="420" width="220" height="95" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
    <text x="65" y="445" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">Family Self-Service</text>
    <text x="65" y="463" fill="#94a3b8" font-family="monospace" font-size="9.5">R10 Family Unit FAS · R8 Chatbot</text>
    <text x="65" y="480" fill="#10b981" font-family="monospace" font-size="9.5">AI Prefill &amp; Live GHI/PCI Calc</text>
    <rect x="205" y="428" width="55" height="16" rx="3" fill="#047857" stroke="#10b981" stroke-width="0.8"/>
    <text x="232" y="439" fill="#ffffff" font-family="monospace" font-size="8.5" font-weight="700" text-anchor="middle">FAMILY</text>
  </g>

  <!-- Core Nodes (Middle Column 1) -->
  <g id="node-lifecycle">
    <rect x="370" y="85" width="200" height="70" rx="8" fill="#1e293b" stroke="#818cf8" stroke-width="1.2"/>
    <text x="385" y="110" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">R1 Lifecycle &amp; R2 TopUp</text>
    <text x="385" y="128" fill="#94a3b8" font-family="monospace" font-size="9">Auto-Open 7y · Auto-Close 16y</text>
    <text x="385" y="144" fill="#64748b" font-family="monospace" font-size="9">Bulk Rules &amp; Correction Engine</text>
  </g>

  <g id="node-fee-mgmt">
    <rect x="370" y="205" width="200" height="70" rx="8" fill="#1e293b" stroke="#818cf8" stroke-width="1.2"/>
    <text x="385" y="230" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">R3 Fee &amp; Enrolment Master</text>
    <text x="385" y="248" fill="#94a3b8" font-family="monospace" font-size="9">Fee Rates · Cohort Publications</text>
    <text x="385" y="264" fill="#64748b" font-family="monospace" font-size="9">Student Charges (POSTED)</text>
  </g>

  <g id="node-payment-orch">
    <!-- FOCAL ACCENT 1 -->
    <rect x="370" y="335" width="200" height="70" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <text x="385" y="360" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="800">R9 Payment Orchestrator</text>
    <text x="385" y="378" fill="#f8fafc" font-family="monospace" font-size="9.5">3 Modes: EA / Online / Split</text>
    <text x="385" y="394" fill="#10b981" font-family="monospace" font-size="9" font-weight="700">EA REVERSAL SAFEGUARD</text>
    <rect x="520" y="343" width="42" height="15" rx="3" fill="#0284c7"/>
    <text x="541" y="354" fill="#ffffff" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">FOCAL</text>
  </g>

  <g id="node-fas-core">
    <!-- FOCAL ACCENT 2 -->
    <rect x="370" y="445" width="200" height="70" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
    <text x="385" y="470" fill="#c084fc" font-family="sans-serif" font-size="12" font-weight="800">R4/R5 FAS &amp; Subsidy Engine</text>
    <text x="385" y="488" fill="#f8fafc" font-family="monospace" font-size="9.5">MOEFAS Auto-Grant (&lt;=$4000)</text>
    <text x="385" y="504" fill="#94a3b8" font-family="monospace" font-size="9">SBFAS Review &amp; Duplicate Check</text>
    <rect x="520" y="453" width="42" height="15" rx="3" fill="#7e22ce"/>
    <text x="541" y="464" fill="#ffffff" font-family="monospace" font-size="8" font-weight="700" text-anchor="middle">FOCAL</text>
  </g>

  <!-- Core Nodes (Middle Column 2: Data & Audit) -->
  <g id="node-ledger">
    <rect x="610" y="85" width="200" height="190" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="1.2"/>
    <text x="625" y="110" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">Double-Entry Financial Ledger</text>
    <text x="625" y="128" fill="#94a3b8" font-family="monospace" font-size="9.5">PostgreSQL Immutable Balances</text>
    <line x1="625" y1="140" x2="795" y2="140" stroke="#334155" stroke-width="1"/>
    <text x="625" y="160" fill="#38bdf8" font-family="monospace" font-size="9">• EA Wallet Account Balances</text>
    <text x="625" y="180" fill="#10b981" font-family="monospace" font-size="9">• Student Charge Receivables</text>
    <text x="625" y="200" fill="#f59e0b" font-family="monospace" font-size="9">• Top-Up &amp; Reversal Journal</text>
    <text x="625" y="220" fill="#a855f7" font-family="monospace" font-size="9">• R6 Budget Utilization Logs</text>
    <text x="625" y="245" fill="#64748b" font-family="monospace" font-size="8.5">ACID Compliance · Zero Negative Bal</text>
  </g>

  <g id="node-audit-sim">
    <rect x="610" y="335" width="200" height="180" rx="8" fill="#1e293b" stroke="#64748b" stroke-width="1.2"/>
    <text x="625" y="360" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">R7 Simulation &amp; Safety Proxy</text>
    <text x="625" y="378" fill="#c084fc" font-family="monospace" font-size="9.5">Read-Only Mutating Interceptor</text>
    <line x1="625" y1="390" x2="795" y2="390" stroke="#334155" stroke-width="1"/>
    <text x="625" y="410" fill="#94a3b8" font-family="monospace" font-size="9">• Enforces Simulation Banner</text>
    <text x="625" y="430" fill="#94a3b8" font-family="monospace" font-size="9">• Disables Mutation Pay/TopUp</text>
    <text x="625" y="450" fill="#94a3b8" font-family="monospace" font-size="9">• Full Audit Trail Logging</text>
    <text x="625" y="475" fill="#10b981" font-family="monospace" font-size="8.5">Active Session Token Isolation</text>
  </g>

  <!-- External Integrations (Right Column) -->
  <g id="node-ext-citizen">
    <rect x="910" y="85" width="220" height="70" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="925" y="110" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">Mock Government Citizen API</text>
    <text x="925" y="128" fill="#94a3b8" font-family="monospace" font-size="9">Daily Incremental Sync (Age 7)</text>
    <text x="925" y="144" fill="#64748b" font-family="monospace" font-size="9">Real-time DoB &amp; Citizenship Check</text>
  </g>

  <g id="node-ext-ml">
    <rect x="910" y="205" width="220" height="70" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="925" y="230" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">ML Need Score Engine</text>
    <text x="925" y="248" fill="#94a3b8" font-family="monospace" font-size="9">Scoring (0-100) &amp; Risk Classifier</text>
    <text x="925" y="264" fill="#10b981" font-family="monospace" font-size="9">Low / Medium / High Risk Tiers</text>
  </g>

  <g id="node-ext-payment">
    <rect x="910" y="335" width="220" height="70" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="925" y="360" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">Sandbox Payment Gateway</text>
    <text x="925" y="378" fill="#94a3b8" font-family="monospace" font-size="9">PayNow / Credit Card / eNETS</text>
    <text x="925" y="394" fill="#64748b" font-family="monospace" font-size="9">Success / Failure / Timeout Webhook</text>
  </g>

  <g id="node-ext-ocr">
    <rect x="910" y="445" width="220" height="70" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="925" y="470" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">Simulated OCR &amp; LLM Service</text>
    <text x="925" y="488" fill="#94a3b8" font-family="monospace" font-size="9">R5 Hardcopy Form Extractor</text>
    <text x="925" y="504" fill="#94a3b8" font-family="monospace" font-size="9">R8 Chatbot &amp; R10 AI Form Prefill</text>
  </g>

</svg>"""
    return svg


# -------------------------------------------------------------
# FLOW 2: SPLIT PAYMENT & EA REVERSAL SAFEGUARD (SEQUENCE FLOW)
# -------------------------------------------------------------
def generate_split_payment_flow():
    svg = """<svg viewBox="0 0 1140 500" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="sq-sky" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#38bdf8"/>
    </marker>
    <marker id="sq-emerald" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#10b981"/>
    </marker>
    <marker id="sq-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#f43f5e"/>
    </marker>
    <marker id="sq-purple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#c084fc"/>
    </marker>
  </defs>

  <!-- Canvas Solid Opaque Background -->
  <rect width="100%" height="100%" rx="14" fill="#0B101B"/>

  <!-- GRID / STAGE HEADER -->
  <rect x="0" y="0" width="1140" height="42" fill="#151C2C" rx="14" />
  <rect x="0" y="32" width="1140" height="10" fill="#151C2C" />
  <line x1="0" y1="42" x2="1140" y2="42" stroke="#1e293b" stroke-width="1.2"/>
  <circle cx="24" cy="21" r="5" fill="#f43f5e"/>
  <circle cx="40" cy="21" r="5" fill="#f59e0b"/>
  <circle cx="56" cy="21" r="5" fill="#10b981"/>
  <text x="76" y="25" fill="#94a3b8" font-family="monospace" font-size="12" font-weight="600">R9 PAYMENT FLOW // 3-MODE CHECKOUT, SPLIT TRANSACTION &amp; AUTOMATIC EA REVERSAL SAFEGUARD</text>
  <rect x="970" y="10" width="150" height="22" rx="4" fill="#be123c" fill-opacity="0.3" stroke="#f43f5e" stroke-width="1"/>
  <text x="1045" y="25" fill="#f43f5e" font-family="monospace" font-size="10" font-weight="700" text-anchor="middle">CRITICAL SAFETY</text>

  <!-- 5 Lifelines -->
  <!-- Actor 0: Parent (X=110) -->
  <!-- Actor 1: e-Service UI (X=330) -->
  <!-- Actor 2: Payment Orchestrator (X=560) -->
  <!-- Actor 3: EA Ledger Engine (X=790) -->
  <!-- Actor 4: Sandbox Gateway (X=1010) -->

  <g font-size="11.5" font-weight="700" text-anchor="middle">
    <!-- Actor 0 -->
    <rect x="30" y="60" width="160" height="36" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="110" y="82" fill="#f8fafc">👤 Parent / Guardian</text>
    <line x1="110" y1="96" x2="110" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 1 -->
    <rect x="250" y="60" width="160" height="36" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
    <text x="330" y="82" fill="#f8fafc">📱 e-Service Checkout</text>
    <line x1="330" y1="96" x2="330" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 2 -->
    <rect x="480" y="60" width="160" height="36" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="2"/>
    <text x="560" y="82" fill="#818cf8">⚙️ Payment Core</text>
    <line x1="560" y1="96" x2="560" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 3 -->
    <rect x="710" y="60" width="160" height="36" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1.5"/>
    <text x="790" y="82" fill="#f8fafc">💰 EA Wallet Ledger</text>
    <line x1="790" y1="96" x2="790" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 4 -->
    <rect x="930" y="60" width="160" height="36" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="1010" y="82" fill="#f8fafc">🏦 Bank Gateway</text>
    <line x1="1010" y1="96" x2="1010" y2="475" stroke="#334155" stroke-dasharray="4 4"/>
  </g>

  <!-- Sequence Steps -->
  <!-- Step 1: Select Charges (Y=120) -->
  <line x1="110" y1="120" x2="330" y2="120" stroke="#38bdf8" stroke-width="1.8" marker-end="url(#sq-sky)"/>
  <rect x="150" y="108" width="140" height="18" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <text x="220" y="121" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">1. Select Invoices ($23.00)</text>

  <!-- Step 2: Choose Split Mode (Y=160) -->
  <line x1="110" y1="160" x2="330" y2="160" stroke="#38bdf8" stroke-width="1.8" marker-end="url(#sq-sky)"/>
  <rect x="135" y="148" width="170" height="18" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <text x="220" y="161" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">2. Split: $15 EA + $8 Online</text>

  <!-- Step 3: Trigger Split Payment (Y=200) -->
  <line x1="330" y1="200" x2="560" y2="200" stroke="#10b981" stroke-width="1.8" marker-end="url(#sq-emerald)"/>
  <rect x="380" y="188" width="130" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="0.8"/>
  <text x="445" y="201" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">3. Post Split Intent</text>

  <!-- Step 4: Deduct EA $15 (Y=240) -->
  <line x1="560" y1="240" x2="790" y2="240" stroke="#c084fc" stroke-width="1.8" marker-end="url(#sq-purple)"/>
  <rect x="605" y="228" width="140" height="18" rx="4" fill="#0f172a" stroke="#c084fc" stroke-width="0.8"/>
  <text x="675" y="241" fill="#c084fc" font-size="10" font-weight="600" text-anchor="middle">4. Deduct EA: $15.00 SGD</text>

  <!-- Step 5: EA Confirmed OK (Y=275) -->
  <line x1="790" y1="275" x2="560" y2="275" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#sq-emerald)"/>
  <rect x="625" y="263" width="100" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="0.8"/>
  <text x="675" y="276" fill="#10b981" font-size="10" font-weight="600" text-anchor="middle">EA Debited OK</text>

  <!-- Step 6: Dispatch Online $8 (Y=315) -->
  <line x1="560" y1="315" x2="1010" y2="315" stroke="#f59e0b" stroke-width="1.8" marker-end="url(#sq-sky)"/>
  <rect x="735" y="303" width="140" height="18" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="0.8"/>
  <text x="805" y="316" fill="#fbbf24" font-size="10" font-weight="600" text-anchor="middle">5. Charge Online: $8.00</text>

  <!-- BRANCHING ZONE: SUCCESS VS FAILURE (Y=350 to 460) -->
  <rect x="490" y="345" width="630" height="115" rx="8" fill="#1e293b" fill-opacity="0.4" stroke="#f43f5e" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="500" y="338" width="220" height="16" rx="3" fill="#be123c"/>
  <text x="610" y="350" fill="#ffffff" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">FAILURE BRANCH: ONLINE TIMEOUT / REJECT</text>

  <!-- Step 7a: Online Fails (Y=375) -->
  <line x1="1010" y1="375" x2="560" y2="375" stroke="#f43f5e" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#sq-red)"/>
  <rect x="725" y="363" width="160" height="18" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="0.8"/>
  <text x="805" y="376" fill="#f43f5e" font-size="9.5" font-weight="600" text-anchor="middle">6. Webhook: FAILED / TIMEOUT</text>

  <!-- Step 7b: IMMEDIATE EA REVERSAL (Y=415) -->
  <line x1="560" y1="415" x2="790" y2="415" stroke="#f43f5e" stroke-width="2.2" marker-end="url(#sq-red)"/>
  <rect x="590" y="403" width="170" height="20" rx="4" fill="#be123c" stroke="#f43f5e" stroke-width="1"/>
  <text x="675" y="417" fill="#ffffff" font-size="10" font-weight="800" text-anchor="middle">7. REVERSAL: REFUND $15.00</text>

  <!-- Step 7c: Notify Parent (Y=445) -->
  <line x1="560" y1="445" x2="110" y2="445" stroke="#f43f5e" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#sq-red)"/>
  <rect x="235" y="433" width="200" height="18" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="0.8"/>
  <text x="335" y="446" fill="#f43f5e" font-size="9.5" font-weight="600" text-anchor="middle">8. Alert: Online Failed, $15 EA Restored</text>

</svg>"""
    return svg


# -------------------------------------------------------------
# FLOW 3: FAS ASSESSMENT & ML NEED SCORE DECISION FLOW (LR FLOWCHART)
# -------------------------------------------------------------
def generate_fas_flow():
    svg = """<svg viewBox="0 0 1140 480" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="fas-arr" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#38bdf8"/>
    </marker>
    <marker id="fas-ok" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#10b981"/>
    </marker>
    <marker id="fas-warn" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#f59e0b"/>
    </marker>
    <marker id="fas-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#f43f5e"/>
    </marker>
  </defs>

  <!-- Canvas Solid Opaque Background -->
  <rect width="100%" height="100%" rx="14" fill="#0B101B"/>

  <!-- GRID / STAGE HEADER -->
  <rect x="0" y="0" width="1140" height="42" fill="#151C2C" rx="14" />
  <rect x="0" y="32" width="1140" height="10" fill="#151C2C" />
  <line x1="0" y1="42" x2="1140" y2="42" stroke="#1e293b" stroke-width="1.2"/>
  <circle cx="24" cy="21" r="5" fill="#f43f5e"/>
  <circle cx="40" cy="21" r="5" fill="#f59e0b"/>
  <circle cx="56" cy="21" r="5" fill="#10b981"/>
  <text x="76" y="25" fill="#94a3b8" font-family="monospace" font-size="12" font-weight="600">FAS ASSESSMENT PIPELINE // DUAL-INTAKE (ONLINE/OCR) &gt; RULE ENGINE &gt; ML NEED SCORE &gt; DISBURSEMENT</text>
  <rect x="990" y="10" width="130" height="22" rx="4" fill="#6d28d9" fill-opacity="0.3" stroke="#a855f7" stroke-width="1"/>
  <text x="1055" y="25" fill="#c084fc" font-family="monospace" font-size="10" font-weight="700" text-anchor="middle">AI + RULES DUAL</text>

  <!-- ==================== CONNECTORS ==================== -->
  <!-- Intake to Assessment Engine -->
  <path d="M 190 120 L 260 120 Q 268 120 268 128 L 268 185 Q 268 193 276 193 L 300 193" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#fas-arr)"/>
  <path d="M 190 270 L 260 270 Q 268 270 268 262 L 268 205 Q 268 197 276 197 L 300 197" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#fas-arr)"/>

  <!-- Assessment to Branches -->
  <!-- Branch 1: MOEFAS Auto Grant (Top) -->
  <path d="M 500 170 L 550 170 Q 558 170 558 152 L 558 120 Q 558 112 566 112 L 600 112" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#fas-ok)"/>
  <!-- Branch 2: SBFAS School Review (Bottom) -->
  <path d="M 500 220 L 550 220 Q 558 220 558 248 L 558 285 Q 558 293 566 293 L 600 293" stroke="#f59e0b" stroke-width="2" fill="none" marker-end="url(#fas-warn)"/>

  <!-- SBFAS to ML Engine & School Approver -->
  <path d="M 800 293 L 850 293" stroke="#a855f7" stroke-width="1.8" fill="none" marker-end="url(#fas-arr)"/>

  <!-- Outputs to Ledger / Charges -->
  <path d="M 800 112 L 910 112 Q 918 112 918 130 L 918 175 Q 918 183 926 183 L 950 183" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#fas-ok)"/>
  <path d="M 1030 270 L 1030 225" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#fas-ok)"/>

  <!-- Connector Masks & Badges -->
  <rect x="520" y="103" width="60" height="16" rx="3" fill="#0f172a" stroke="#059669" stroke-width="0.8"/>
  <text x="550" y="115" fill="#10b981" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">PASS</text>

  <rect x="515" y="284" width="70" height="16" rx="3" fill="#0f172a" stroke="#d97706" stroke-width="0.8"/>
  <text x="550" y="296" fill="#fbbf24" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">EXCEED/SBFAS</text>

  <!-- ==================== NODES ==================== -->
  <!-- Node 1: Online Intake (R10) -->
  <g>
    <rect x="30" y="85" width="160" height="70" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
    <text x="45" y="110" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">R10 Online FAS</text>
    <text x="45" y="128" fill="#94a3b8" font-family="monospace" font-size="9.5">Family Unit Intake</text>
    <text x="45" y="144" fill="#34d399" font-family="monospace" font-size="9">AI Prefill &amp; Live Calc</text>
  </g>

  <!-- Node 2: Hardcopy Intake (R5) -->
  <g>
    <rect x="30" y="235" width="160" height="70" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="45" y="260" fill="#f8fafc" font-family="sans-serif" font-size="12" font-weight="700">R5 Offline Hardcopy</text>
    <text x="45" y="278" fill="#94a3b8" font-family="monospace" font-size="9.5">Simulated OCR Intake</text>
    <text x="45" y="294" fill="#f59e0b" font-family="monospace" font-size="9">Confidence &amp; Dup Check</text>
  </g>

  <!-- Node 3: Assessment Rule Engine (Center) -->
  <g>
    <rect x="300" y="160" width="200" height="75" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <text x="315" y="185" fill="#38bdf8" font-family="sans-serif" font-size="12" font-weight="800">Rule Assessment Engine</text>
    <text x="315" y="203" fill="#f8fafc" font-family="monospace" font-size="9.5">GHI &lt;= $4,000 OR PCI &lt;= $1,000</text>
    <text x="315" y="220" fill="#94a3b8" font-family="monospace" font-size="9">Citizen Verification (Gov API)</text>
  </g>

  <!-- Node 4: MOEFAS Auto-Grant Outcome (Top Branch) -->
  <g>
    <rect x="600" y="75" width="200" height="75" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <text x="615" y="100" fill="#10b981" font-family="sans-serif" font-size="12" font-weight="800">MOEFAS AUTO-GRANT</text>
    <text x="615" y="118" fill="#f8fafc" font-family="monospace" font-size="9.5">100% School &amp; Misc Subsidy</text>
    <text x="615" y="135" fill="#94a3b8" font-family="monospace" font-size="9">Immediate System Approval</text>
  </g>

  <!-- Node 5: SBFAS ML Review Drawer (Bottom Branch) -->
  <g>
    <rect x="600" y="255" width="200" height="75" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.8"/>
    <text x="615" y="280" fill="#fbbf24" font-family="sans-serif" font-size="12" font-weight="700">SBFAS School Review</text>
    <text x="615" y="298" fill="#f8fafc" font-family="monospace" font-size="9.5">Manual Committee Review</text>
    <text x="615" y="315" fill="#94a3b8" font-family="monospace" font-size="9">Discretionary Subsidy Tiers</text>
  </g>

  <!-- Node 6: ML Need Score Engine (AI Widget) -->
  <g>
    <rect x="850" y="255" width="180" height="75" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
    <text x="865" y="280" fill="#c084fc" font-family="sans-serif" font-size="12" font-weight="800">ML Need Score (0-100)</text>
    <text x="865" y="298" fill="#f8fafc" font-family="monospace" font-size="9.5">Low / Med / High Risk</text>
    <text x="865" y="315" fill="#a855f7" font-family="monospace" font-size="9">Recommends Tier 1 or Tier 2</text>
  </g>

  <!-- Node 7: Charge Register & Budget Disbursement -->
  <g>
    <rect x="950" y="150" width="160" height="75" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.8"/>
    <text x="965" y="175" fill="#f8fafc" font-family="sans-serif" font-size="11.5" font-weight="700">Fee Ledger Offset</text>
    <text x="965" y="193" fill="#10b981" font-family="monospace" font-size="9">Net Payable Reduced ($0)</text>
    <text x="965" y="210" fill="#94a3b8" font-family="monospace" font-size="9">R6 Budget Utilized</text>
  </g>

</svg>"""
    return svg

def main():
    f1 = OUT_DIR / "EAFAMS_GLOBAL_INTERACTION_FLOW.svg"
    f2 = OUT_DIR / "EAFAMS_SPLIT_PAYMENT_REVERSAL_FLOW.svg"
    f3 = OUT_DIR / "EAFAMS_FAS_ASSESSMENT_FLOW.svg"

    f1.write_text(generate_global_flow(), encoding="utf-8")
    f2.write_text(generate_split_payment_flow(), encoding="utf-8")
    f3.write_text(generate_fas_flow(), encoding="utf-8")

    print(f"Generated Flow 1: {f1}")
    print(f"Generated Flow 2: {f2}")
    print(f"Generated Flow 3: {f3}")

if __name__ == "__main__":
    main()
