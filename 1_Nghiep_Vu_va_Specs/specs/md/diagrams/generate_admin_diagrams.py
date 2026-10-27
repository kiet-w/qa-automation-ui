#!/usr/bin/env python3
"""
generate_admin_diagrams.py
Generates 5 full editorial vector SVG diagrams and an interactive HTML viewer for
EAFAMS Admin Portal (R1 to R7) compliant with combo-diagram specifications:
- Solid opaque canvas (#0B101B)
- macOS bezel CAD stage (🔴 🟡 🟢)
- 6 connector rules (r=8 rounded right-angles, label masks with 6-10px gap, no overlapping lines)
- Semantic hierarchy & editorial typography
"""

from pathlib import Path

OUT_DIR = Path("/home/baudui/Projects/fs/document/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Common SVG Defs
COMMON_DEFS = """
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B101B"/>
      <stop offset="100%" stop-color="#0E1524"/>
    </linearGradient>
    <linearGradient id="zone-hq" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-school" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-engine" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#818cf8" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-ext" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="zone-ledger" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c084fc" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#c084fc" stop-opacity="0.02"/>
    </linearGradient>

    <!-- Markers -->
    <marker id="m-sky" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#38bdf8"/>
    </marker>
    <marker id="m-emerald" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#10b981"/>
    </marker>
    <marker id="m-amber" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#f59e0b"/>
    </marker>
    <marker id="m-purple" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#c084fc"/>
    </marker>
    <marker id="m-rose" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 1 L 7 4 L 0 7 z" fill="#f43f5e"/>
    </marker>
"""

def header_svg(width, title, badge_text, badge_color="#38bdf8", badge_fill="#0369a1"):
    return f"""
  <!-- STAGE HEADER -->
  <rect x="0" y="0" width="{width}" height="42" fill="#151C2C" rx="14" />
  <rect x="0" y="32" width="{width}" height="10" fill="#151C2C" />
  <line x1="0" y1="42" x2="{width}" y2="42" stroke="#1e293b" stroke-width="1.2"/>
  <circle cx="24" cy="21" r="5" fill="#f43f5e"/>
  <circle cx="40" cy="21" r="5" fill="#f59e0b"/>
  <circle cx="56" cy="21" r="5" fill="#10b981"/>
  <text x="76" y="25" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="12" font-weight="600">{title}</text>
  <rect x="{width-180}" y="10" width="165" height="22" rx="4" fill="{badge_fill}" fill-opacity="0.3" stroke="{badge_color}" stroke-width="1"/>
  <text x="{width-97}" y="25" fill="{badge_color}" font-family="'Geist Mono', monospace" font-size="10.5" font-weight="700" text-anchor="middle">{badge_text}</text>
"""

# ==============================================================================
# DIAGRAM 1: MASTER ARCHITECTURE & RBAC WORKFLOW (R1 to R7)
# ==============================================================================
def build_master_diagram():
    w, h = 1240, 720
    return f"""<svg viewBox="0 0 {w} {h}" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d1-title d1-desc">
  <title id="d1-title">EAFAMS Admin Portal Master Architecture (R1-R7)</title>
  <desc id="d1-desc">Comprehensive system architecture and dataflow across MOE HQ, School Users, Core Processing Engines, and Government Services</desc>
  <defs>{COMMON_DEFS}</defs>
  <rect width="100%" height="100%" rx="14" fill="url(#bg-grad)"/>
  {header_svg(w, "EAFAMS ADMIN PORTAL // COMPLETE 7-MODULE ARCHITECTURE &amp; RBAC TOPOLOGY", "R1 - R7 FULL MATRIX", "#38bdf8", "#0369a1")}

  <!-- ZONES -->
  <!-- Zone 1: Actors & Ingress (Left) -->
  <rect x="25" y="60" width="220" height="635" rx="12" fill="url(#zone-hq)" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="40" y="52" width="150" height="18" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="115" y="65" fill="#38bdf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">👥 ADMIN ACTORS</text>

  <!-- Zone 2: Core Admin Business Engines (Middle-Left) -->
  <rect x="275" y="60" width="370" height="635" rx="12" fill="url(#zone-engine)" stroke="#818cf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="295" y="52" width="240" height="18" rx="4" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
  <text x="415" y="65" fill="#818cf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">⚙️ ADMIN CORE MODULES (R1–R6)</text>

  <!-- Zone 3: Security & Simulation Safeguards (Middle-Right) -->
  <rect x="675" y="60" width="260" height="635" rx="12" fill="url(#zone-ledger)" stroke="#c084fc" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="695" y="52" width="220" height="18" rx="4" fill="#0f172a" stroke="#c084fc" stroke-width="1"/>
  <text x="805" y="65" fill="#c084fc" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">🔒 R7 SIMULATION &amp; LEDGER</text>

  <!-- Zone 4: External Integrations & AI (Right) -->
  <rect x="965" y="60" width="250" height="635" rx="12" fill="url(#zone-ext)" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="985" y="52" width="210" height="18" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1"/>
  <text x="1090" y="65" fill="#fbbf24" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">🌐 EXTERNAL ECOSYSTEM &amp; AI</text>

  <!-- CONNECTORS (Drawn BEFORE Node Cards) -->
  <!-- MOE HQ to R1/R2/R3/R6/R7 -->
  <path d="M 225 125 L 295 125" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 225 155 L 255 155 Q 263 155 263 163 L 263 212 Q 263 220 271 220 L 295 220" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 225 175 L 245 175 Q 253 175 253 183 L 253 622 Q 253 630 261 630 L 695 630" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>

  <!-- School User to R3/R4/R5/R6 -->
  <path d="M 225 365 L 250 365 Q 258 365 258 357 L 258 328 Q 258 320 266 320 L 295 320" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 225 395 L 250 395 Q 258 395 258 403 L 258 412 Q 258 420 266 420 L 295 420" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 225 415 L 245 415 Q 253 415 253 423 L 253 512 Q 253 520 261 520 L 295 520" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Module to Ledger Pipes -->
  <path d="M 625 125 L 695 125" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 625 220 L 660 220 Q 668 220 668 212 L 668 150 Q 668 142 676 142 L 695 142" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 625 320 L 695 320" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>
  <path d="M 625 420 L 660 420 Q 668 420 668 340 Q 668 332 676 332 L 695 332" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Module to External Ecosystem -->
  <path d="M 625 105 L 665 105 Q 673 105 673 97 L 673 85 Q 673 77 681 77 L 950 77 Q 958 77 958 85 L 958 112 Q 958 120 966 120 L 985 120" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#m-amber)"/>
  <path d="M 625 440 L 945 440 Q 953 440 953 328 Q 953 320 961 320 L 985 320" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#m-amber)"/>
  <path d="M 625 520 L 985 520" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#m-amber)"/>

  <!-- Connector Masks & Labels -->
  <rect x="238" y="117" width="50" height="16" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <text x="263" y="129" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R1/R2</text>

  <rect x="635" y="117" width="52" height="16" rx="3" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <text x="661" y="129" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">CREDIT</text>

  <rect x="635" y="312" width="52" height="16" rx="3" fill="#0f172a" stroke="#818cf8" stroke-width="0.8"/>
  <text x="661" y="324" fill="#818cf8" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">BILLING</text>

  <rect x="635" y="412" width="52" height="16" rx="3" fill="#0f172a" stroke="#10b981" stroke-width="0.8"/>
  <text x="661" y="424" fill="#10b981" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">SUBSIDY</text>

  <!-- ==================== NODES ==================== -->
  <!-- ACTOR 1: MOE HQ User -->
  <g id="node-moehq">
    <rect x="40" y="85" width="185" height="110" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.8"/>
    <rect x="145" y="93" width="70" height="16" rx="3" fill="#0369a1"/>
    <text x="180" y="104" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">HQ SPECIALIST</text>
    <text x="52" y="112" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">🏛️ MOE HQ Users</text>
    <text x="52" y="130" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• R1: Nationwide EA View</text>
    <text x="52" y="146" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• R2: Top-Up &amp; Campaigns</text>
    <text x="52" y="162" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• R3: Master Data &amp; Fee Rates</text>
    <text x="52" y="178" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9" font-weight="600">• R7: User Simulation Host</text>
  </g>

  <!-- ACTOR 2: School User -->
  <g id="node-schooluser">
    <rect x="40" y="325" width="185" height="120" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.8"/>
    <rect x="145" y="333" width="70" height="16" rx="3" fill="#047857"/>
    <text x="180" y="344" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">SCHOOL ADMIN</text>
    <text x="52" y="352" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">🏫 School Users</text>
    <text x="52" y="370" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• R3: Classes &amp; Enrolment</text>
    <text x="52" y="386" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• R3: Publish School Fees</text>
    <text x="52" y="402" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9" font-weight="600">• R4: SBFAS Review &amp; Tiering</text>
    <text x="52" y="418" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• R5: Upload OCR Hardcopy</text>
    <text x="52" y="434" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">RBAC Scoped to School ID</text>
  </g>

  <!-- MODULE R1: EA Lifecycle -->
  <g id="node-r1">
    <rect x="295" y="85" width="330" height="80" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.4"/>
    <rect x="545" y="93" width="70" height="16" rx="3" fill="#0369a1"/>
    <text x="580" y="104" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R1 LIFECYCLE</text>
    <text x="310" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">R1: Education Account Lifecycle</text>
    <text x="310" y="126" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Daily 00:00 SGT Sync: Auto-open EA for Singaporean age 7</text>
    <text x="310" y="142" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• Backend-Triggered Check: Auto-close at 16y or lost SC</text>
    <text x="310" y="156" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Initial Bal: $0.00 | Closure: CPF Transfer / Deferred</text>
  </g>

  <!-- MODULE R2: Top-Up Management -->
  <g id="node-r2">
    <!-- Focal Accent 1 -->
    <rect x="295" y="180" width="330" height="85" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <rect x="545" y="188" width="70" height="16" rx="3" fill="#0284c7"/>
    <text x="580" y="199" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R2 TOP-UP</text>
    <text x="310" y="204" fill="#38bdf8" font-family="'Geist', sans-serif" font-size="12" font-weight="800">R2: Top-Up Engine &amp; Correction</text>
    <text x="310" y="222" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Individual: Closure Check + IdempotencyKey + FundingRef</text>
    <text x="310" y="238" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Bulk Campaign: Filter (Age + Balance + Schooling) &amp; Budget</text>
    <text x="310" y="254" fill="#f59e0b" font-family="'Geist Mono', monospace" font-size="8.5">• Correction: Debit Adjustment (Max &lt;= Available Balance)</text>
  </g>

  <!-- MODULE R3: School, Student & Fee Management -->
  <g id="node-r3">
    <rect x="295" y="280" width="330" height="85" rx="8" fill="#1e293b" stroke="#818cf8" stroke-width="1.4"/>
    <rect x="535" y="288" width="80" height="16" rx="3" fill="#4338ca"/>
    <text x="575" y="299" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R3 SCHOOL/FEE</text>
    <text x="310" y="304" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">R3: Master Data, Enrolment &amp; Fees</text>
    <text x="310" y="322" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Class Assignment -> Enrolment Profile -> Auto-link SC EA</text>
    <text x="310" y="338" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Fee Rate Rules: Stages (P1-JC2) × Resident (SC/PR/IS) + GST</text>
    <text x="310" y="354" fill="#818cf8" font-family="'Geist Mono', monospace" font-size="8.5">• Fee Publication -> Resolve Cohort -> Student Charges (POSTED)</text>
  </g>

  <!-- MODULE R4: FAS Core & ML -->
  <g id="node-r4">
    <!-- Focal Accent 2 -->
    <rect x="295" y="380" width="330" height="95" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <rect x="545" y="388" width="70" height="16" rx="3" fill="#059669"/>
    <text x="580" y="399" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R4 FAS CORE</text>
    <text x="310" y="404" fill="#34d399" font-family="'Geist', sans-serif" font-size="12" font-weight="800">R4: Financial Assistance (MOE/SB)</text>
    <text x="310" y="422" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9" font-weight="700">• MOEFAS: Auto-Grant if SC &amp; (GHI &lt;=$4,000 OR PCI &lt;=$1,000)</text>
    <text x="310" y="438" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• SBFAS: School Admin Review Drawer with ML Need Score</text>
    <text x="310" y="454" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="9">• ML AI Recommendation: Need Score (0-100) + Risk Tiering</text>
    <text x="310" y="468" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Net Payable = Original Amount - Subsidy Amount</text>
  </g>

  <!-- MODULE R5: Hardcopy FAS Applications -->
  <g id="node-r5">
    <rect x="295" y="490" width="330" height="85" rx="8" fill="#1e293b" stroke="#818cf8" stroke-width="1.4"/>
    <rect x="525" y="498" width="90" height="16" rx="3" fill="#4338ca"/>
    <text x="570" y="509" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R5 HARDCOPY OCR</text>
    <text x="310" y="514" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">R5: Hardcopy FAS Ingestion</text>
    <text x="310" y="532" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Upload Scans (PDF/JPG, max 5) -> Simulated OCR 2-pane</text>
    <text x="310" y="548" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Auto-match: NRIC -> Parent/Child Lock, Gov Income Autofill</text>
    <text x="310" y="564" fill="#c084fc" font-family="'Geist Mono', monospace" font-size="8.5">• Submit -> Split Family Unit into Child Apps (FAM-YYYY-NNNNN)</text>
  </g>

  <!-- MODULE R6: Budget & Statistics -->
  <g id="node-r6">
    <rect x="295" y="590" width="330" height="85" rx="8" fill="#1e293b" stroke="#818cf8" stroke-width="1.4"/>
    <rect x="545" y="598" width="70" height="16" rx="3" fill="#4338ca"/>
    <text x="580" y="609" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R6 BUDGET</text>
    <text x="310" y="614" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">R6: Budget &amp; Statistics</text>
    <text x="310" y="632" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Budget Pools: MOE HQ (MOEFAS) &amp; School (SBFAS)</text>
    <text x="310" y="648" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Auto-decrement on Grant; Depletion -> Insufficient Budget</text>
    <text x="310" y="664" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Analytics: Scheme, Stage, Class &amp; Tier Breakdown</text>
  </g>

  <!-- LEDGER & R7 ZONE -->
  <g id="node-ledger">
    <rect x="695" y="85" width="220" height="280" rx="8" fill="#1e293b" stroke="#c084fc" stroke-width="1.5"/>
    <rect x="835" y="93" width="70" height="16" rx="3" fill="#7e22ce"/>
    <text x="870" y="104" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">POSTGRESQL</text>
    <text x="710" y="112" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">Double-Entry Ledger</text>
    <text x="710" y="130" fill="#c084fc" font-family="'Geist Mono', monospace" font-size="9">Immutable Financial State</text>
    <line x1="710" y1="142" x2="895" y2="142" stroke="#334155" stroke-width="1"/>
    <text x="710" y="162" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• EA Wallet Balances (F1)</text>
    <text x="710" y="182" fill="#f59e0b" font-family="'Geist Mono', monospace" font-size="9">• Top-Up Journal &amp; FundingRef</text>
    <text x="710" y="202" fill="#818cf8" font-family="'Geist Mono', monospace" font-size="9">• Student Charges (POSTED)</text>
    <text x="710" y="222" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Subsidy Offsets &amp; Waivers</text>
    <text x="710" y="242" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="9">• Remaining Budget Counters</text>
    <line x1="710" y1="256" x2="895" y2="256" stroke="#334155" stroke-width="1"/>
    <text x="710" y="274" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="8.5">ACID Guaranteed</text>
    <text x="710" y="290" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="8.5">Zero Negative Balance Rule</text>
    <text x="710" y="306" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="8.5">Append-Only Audit Log</text>
  </g>

  <!-- MODULE R7: Simulation Mode -->
  <g id="node-r7">
    <rect x="695" y="380" width="220" height="295" rx="8" fill="#1e293b" stroke="#f43f5e" stroke-width="1.8"/>
    <rect x="835" y="388" width="70" height="16" rx="3" fill="#be123c"/>
    <text x="870" y="399" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R7 SIMULATION</text>
    <text x="710" y="407" fill="#f43f5e" font-family="'Geist', sans-serif" font-size="12" font-weight="700">R7: User Simulation Mode</text>
    <text x="710" y="425" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">MOE HQ Support Tool</text>
    <line x1="710" y1="437" x2="895" y2="437" stroke="#334155" stroke-width="1"/>
    <text x="710" y="457" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Personas: School User / Parent</text>
    <text x="710" y="475" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• 100% Exact Read-Only View</text>
    <text x="710" y="493" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• View Balances, Bills, FAS Status</text>
    <line x1="710" y1="507" x2="895" y2="507" stroke="#334155" stroke-width="1"/>
    <text x="710" y="527" fill="#f43f5e" font-family="'Geist Mono', monospace" font-size="9" font-weight="700">SAFETY GUARDS:</text>
    <text x="710" y="545" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Amber Banner Persistent</text>
    <text x="710" y="563" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Mutating Calls Blocked (403)</text>
    <text x="710" y="581" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Zero Test Money Disbursed</text>
    <text x="710" y="599" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Detailed Simulation Audit Trail</text>
    <rect x="710" y="618" width="190" height="24" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1"/>
    <text x="805" y="634" fill="#f43f5e" font-family="'Geist Mono', monospace" font-size="9" font-weight="700" text-anchor="middle">MUTATION INTERCEPTOR ACTIVE</text>
  </g>

  <!-- EXTERNAL NODES -->
  <g id="node-ext-gov">
    <rect x="985" y="85" width="210" height="90" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.4"/>
    <rect x="1115" y="93" width="70" height="16" rx="3" fill="#b45309"/>
    <text x="1150" y="104" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">GOV API</text>
    <text x="998" y="112" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">Mock Gov Citizen API</text>
    <text x="998" y="130" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Daily Sync: 7yo Birthdays</text>
    <text x="998" y="146" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Live Real-time Age Check</text>
    <text x="998" y="162" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="9">• Citizenship &amp; NRIC Master</text>
  </g>

  <g id="node-ext-tax">
    <rect x="985" y="195" width="210" height="85" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.4"/>
    <rect x="1115" y="203" width="70" height="16" rx="3" fill="#b45309"/>
    <text x="1150" y="214" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">FINANCE</text>
    <text x="998" y="222" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">Gov Income &amp; CPF API</text>
    <text x="998" y="240" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Automated GHI/PCI Lookup</text>
    <text x="998" y="256" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• No Payslip Upload Needed</text>
    <text x="998" y="270" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">IRAS / CPF Direct Feeds</text>
  </g>

  <g id="node-ext-ml">
    <rect x="985" y="300" width="210" height="90" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
    <rect x="1115" y="308" width="70" height="16" rx="3" fill="#7e22ce"/>
    <text x="1150" y="319" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">AI ENGINE</text>
    <text x="998" y="327" fill="#c084fc" font-family="'Geist', sans-serif" font-size="12" font-weight="800">ML Need Score Engine</text>
    <text x="998" y="345" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Need Score: 0 - 100</text>
    <text x="998" y="361" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Risk Level: Low / Med / High</text>
    <text x="998" y="377" fill="#c084fc" font-family="'Geist Mono', monospace" font-size="9">• SBFAS Tier 1/2/3 Suggester</text>
  </g>

  <g id="node-ext-ocr">
    <rect x="985" y="410" width="210" height="85" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.4"/>
    <rect x="1115" y="418" width="70" height="16" rx="3" fill="#b45309"/>
    <text x="1150" y="429" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">VISION</text>
    <text x="998" y="437" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">Simulated OCR Vision</text>
    <text x="998" y="455" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Extracts Scan PDF / Images</text>
    <text x="998" y="471" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Highlights Low-Confidence</text>
    <text x="998" y="485" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Side-by-side Dual Verification</text>
  </g>

  <g id="node-ext-cpf">
    <rect x="985" y="515" width="210" height="85" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.4"/>
    <rect x="1115" y="523" width="70" height="16" rx="3" fill="#b45309"/>
    <text x="1150" y="534" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">PENSION</text>
    <text x="998" y="542" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">CPF Board Transfer</text>
    <text x="998" y="560" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• EA Residual Balance Payout</text>
    <text x="998" y="576" fill="#f59e0b" font-family="'Geist Mono', monospace" font-size="9">• MVP: Closure Deferred</text>
    <text x="998" y="590" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Triggered on 16th Birthday</text>
  </g>

</svg>"""

# ==============================================================================
# DIAGRAM 2: R1 LIFECYCLE & R2 TOP-UP PIPELINE
# ==============================================================================
def build_r1_r2_diagram():
    w, h = 1180, 560
    return f"""<svg viewBox="0 0 {w} {h}" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d2-title d2-desc">
  <title id="d2-title">EAFAMS R1 EA Lifecycle and R2 Top-Up Pipeline</title>
  <desc id="d2-desc">Detailed state lifecycle of Singaporean student Education Accounts from creation to closure, plus individual, bulk campaign and correction top-up flows</desc>
  <defs>{COMMON_DEFS}</defs>
  <rect width="100%" height="100%" rx="14" fill="url(#bg-grad)"/>
  {header_svg(w, "R1 &amp; R2 PIPELINE // EDUCATION ACCOUNT LIFECYCLE, TOP-UP CAMPAIGNS &amp; CORRECTION", "FINANCIAL CORE", "#38bdf8", "#0369a1")}

  <!-- ZONES -->
  <rect x="30" y="60" width="540" height="475" rx="12" fill="url(#zone-hq)" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="50" y="52" width="220" height="18" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="160" y="65" fill="#38bdf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">🏛️ R1: EA LIFECYCLE STATE ENGINE</text>

  <rect x="600" y="60" width="550" height="475" rx="12" fill="url(#zone-engine)" stroke="#818cf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="620" y="52" width="210" height="18" rx="4" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
  <text x="725" y="65" fill="#818cf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">💳 R2: TOP-UP &amp; LEDGER WRITES</text>

  <!-- CONNECTORS (R1 Lifecycle) -->
  <path d="M 160 145 L 160 185" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 160 255 L 160 295" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Active to Backend Check -->
  <path d="M 270 330 L 320 330" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>

  <!-- Decision Check: No (Stay Active) vs Yes (Close) -->
  <path d="M 425 295 L 425 240 Q 425 232 417 232 L 270 232" stroke="#10b981" stroke-width="1.8" stroke-dasharray="4 3" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 425 365 L 425 415" stroke="#f43f5e" stroke-width="1.8" fill="none" marker-end="url(#m-rose)"/>

  <!-- Closed to CPF -->
  <path d="M 425 485 L 425 500 Q 425 508 417 508 L 270 508" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#m-amber)"/>

  <!-- R2 Connectors -->
  <path d="M 750 145 L 750 185" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 990 145 L 990 185" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>

  <!-- Execution to Ledger F1 -->
  <path d="M 750 255 L 750 300 Q 750 308 758 308 L 860 308" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 990 255 L 990 300 Q 990 308 982 308 L 860 308" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Ledger F1 to Correction -->
  <path d="M 870 375 L 870 415" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#m-amber)"/>

  <!-- Connector Masks & Badges -->
  <rect x="390" y="248" width="70" height="16" rx="3" fill="#0f172a" stroke="#059669" stroke-width="0.8"/>
  <text x="425" y="260" fill="#10b981" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">&lt; 16 &amp; SC</text>

  <rect x="382" y="380" width="86" height="16" rx="3" fill="#0f172a" stroke="#be123c" stroke-width="0.8"/>
  <text x="425" y="392" fill="#f43f5e" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">&gt;=16 OR NON-SC</text>

  <!-- ==================== R1 NODES ==================== -->
  <g id="r1-gov-api">
    <rect x="50" y="85" width="220" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="65" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">Mock Citizen API</text>
    <text x="65" y="124" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Initial Sync: 7-15 SC Citizens</text>
    <text x="65" y="138" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• Daily 00:00 SGT Incremental (Age 7)</text>
  </g>

  <g id="r1-student-profile">
    <rect x="50" y="185" width="220" height="70" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1.2"/>
    <text x="65" y="208" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">Student Profile Creation</text>
    <text x="65" y="226" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Validates Unique NRIC</text>
    <text x="65" y="242" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Duplicate Prevention Index</text>
  </g>

  <g id="r1-active-ea">
    <rect x="50" y="295" width="220" height="70" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <rect x="195" y="303" width="65" height="16" rx="3" fill="#047857"/>
    <text x="227" y="314" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">ACTIVE</text>
    <text x="65" y="318" fill="#34d399" font-family="'Geist', sans-serif" font-size="12" font-weight="800">EA Account Opened</text>
    <text x="65" y="336" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">Initial Balance: SGD 0.00</text>
    <text x="65" y="352" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">Read-write transactions allowed</text>
  </g>

  <g id="r1-backend-check">
    <rect x="320" y="295" width="210" height="70" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="335" y="318" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">Backend Closure Check</text>
    <text x="335" y="336" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Pre-flight hook on every API</text>
    <text x="335" y="352" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• Real-time DOB &amp; SC Verification</text>
  </g>

  <g id="r1-closed-ea">
    <rect x="320" y="415" width="210" height="70" rx="6" fill="#1e293b" stroke="#f43f5e" stroke-width="1.8"/>
    <rect x="455" y="423" width="65" height="16" rx="3" fill="#be123c"/>
    <text x="487" y="434" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">CLOSED</text>
    <text x="335" y="438" fill="#f43f5e" font-family="'Geist', sans-serif" font-size="12" font-weight="800">EA Status: CLOSED</text>
    <text x="335" y="456" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">Actual Closure Date stamped</text>
    <text x="335" y="472" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">Blocks Top-Up &amp; Payment</text>
  </g>

  <g id="r1-cpf-transfer">
    <rect x="50" y="475" width="220" height="50" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="65" y="496" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11" font-weight="700">CPF Payout / Closure Deferred</text>
    <text x="65" y="512" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="8.5">Remaining Balance -> CPF Account</text>
  </g>

  <!-- ==================== R2 NODES ==================== -->
  <g id="r2-individual">
    <rect x="630" y="85" width="240" height="60" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="645" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F2.1 Individual Top-Up</text>
    <text x="645" y="124" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Exact NRIC / Account Lookup</text>
    <text x="645" y="138" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• IdempotencyKey + FundingRef</text>
  </g>

  <g id="r2-bulk">
    <rect x="880" y="85" width="250" height="60" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1.2"/>
    <text x="895" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F2.4 Bulk Top-Up Campaign</text>
    <text x="895" y="124" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• AND Filters: Age + Bal + Enrolment</text>
    <text x="895" y="138" fill="#818cf8" font-family="'Geist Mono', monospace" font-size="9">• Budget Limit Check &amp; Preview</text>
  </g>

  <g id="r2-execution">
    <rect x="630" y="185" width="500" height="70" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.4"/>
    <text x="645" y="208" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">Campaign Execution Engine (F2.7)</text>
    <text x="645" y="226" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Modes: Run Now | Scheduled Once | Recurring (Monthly / Quarterly / Annual)</text>
    <text x="645" y="242" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Atomic sequential execution | Results: Successful, Skipped (Exceed Budget), Failed</text>
  </g>

  <g id="r2-ledger-f1">
    <rect x="680" y="305" width="400" height="70" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <rect x="1005" y="313" width="65" height="16" rx="3" fill="#047857"/>
    <text x="1037" y="324" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">POSTED</text>
    <text x="700" y="328" fill="#34d399" font-family="'Geist', sans-serif" font-size="12" font-weight="800">Double-Entry Ledger Credit (Function 1)</text>
    <text x="700" y="346" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">Immutable Credit: DR Treasury / CR Student EA</text>
    <text x="700" y="362" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">Effective Amount = Original - Total Corrected</text>
  </g>

  <g id="r2-correction">
    <rect x="680" y="415" width="400" height="95" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>
    <rect x="995" y="423" width="75" height="16" rx="3" fill="#b45309"/>
    <text x="1032" y="434" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">CORRECTION</text>
    <text x="700" y="438" fill="#fbbf24" font-family="'Geist', sans-serif" font-size="12" font-weight="700">F2.3 Top-Up Correction Safeguard</text>
    <text x="700" y="456" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Targets original Successful top-up | Keeps transaction immutable</text>
    <text x="700" y="472" fill="#f43f5e" font-family="'Geist Mono', monospace" font-size="9" font-weight="700">• BALANCE CONSTRAINT: Correction Amount &lt;= Available Balance</text>
    <text x="700" y="490" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Prevents negative account balance if parent spent funds on fees</text>
  </g>

</svg>"""

# ==============================================================================
# DIAGRAM 3: R3 SCHOOL, STUDENT & FEE MANAGEMENT
# ==============================================================================
def build_r3_diagram():
    w, h = 1180, 520
    return f"""<svg viewBox="0 0 {w} {h}" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d3-title d3-desc">
  <title id="d3-title">EAFAMS R3 School, Student &amp; Fee Management Pipeline</title>
  <desc id="d3-desc">Master data structure, student class assignment, SC EA auto-linkage, fee rate rules, and cohort publication charge generation</desc>
  <defs>{COMMON_DEFS}</defs>
  <rect width="100%" height="100%" rx="14" fill="url(#bg-grad)"/>
  {header_svg(w, "R3 PIPELINE // SCHOOL STRUCTURE, STUDENT ENROLMENT &amp; FEE RESOLUTION", "FEE &amp; CHARGE ENGINE", "#818cf8", "#4338ca")}

  <!-- 4 Process Stages (LR Pipeline) -->
  <rect x="30" y="60" width="260" height="435" rx="10" fill="url(#zone-hq)" stroke="#38bdf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="45" y="52" width="160" height="18" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
  <text x="125" y="65" fill="#38bdf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">1. STRUCTURE &amp; MASTER</text>

  <rect x="310" y="60" width="260" height="435" rx="10" fill="url(#zone-school)" stroke="#10b981" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="325" y="52" width="170" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1"/>
  <text x="410" y="65" fill="#34d399" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">2. STUDENT &amp; EA LINK</text>

  <rect x="590" y="60" width="270" height="435" rx="10" fill="url(#zone-engine)" stroke="#818cf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="605" y="52" width="180" height="18" rx="4" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
  <text x="695" y="65" fill="#818cf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">3. FEE RULES &amp; TAX</text>

  <rect x="880" y="60" width="270" height="435" rx="10" fill="url(#zone-ledger)" stroke="#c084fc" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="895" y="52" width="200" height="18" rx="4" fill="#0f172a" stroke="#c084fc" stroke-width="1"/>
  <text x="995" y="65" fill="#c084fc" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">4. PUBLICATION &amp; BILLS</text>

  <!-- CONNECTORS -->
  <path d="M 270 200 L 330 200" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 440 235 L 440 275" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 550 310 L 610 310" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 840 200 L 900 200" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>
  <path d="M 1015 235 L 1015 275" stroke="#c084fc" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>
  <path d="M 1015 365 L 1015 405" stroke="#f59e0b" stroke-width="1.8" fill="none" marker-end="url(#m-amber)"/>

  <!-- ==================== STAGE 1 NODES ==================== -->
  <g>
    <rect x="50" y="85" width="220" height="70" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="65" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F01 School Master (HQ)</text>
    <text x="65" y="126" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• MOE HQ creates Schools</text>
    <text x="65" y="142" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Issues School User Accounts</text>
  </g>

  <g>
    <rect x="50" y="170" width="220" height="95" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="65" y="193" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F02–F04 Academic Setup</text>
    <text x="65" y="211" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Academic Year &amp; Global Levels</text>
    <text x="65" y="227" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• School Level Offering (P1-P6)</text>
    <text x="65" y="243" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Class Setup (e.g., P6A)</text>
  </g>

  <!-- ==================== STAGE 2 NODES ==================== -->
  <g>
    <rect x="330" y="85" width="220" height="65" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
    <text x="345" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F05 Student Record</text>
    <text x="345" y="126" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• School User manual intake</text>
    <text x="345" y="142" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• NRIC, Name, DOB, Residency</text>
  </g>

  <g>
    <rect x="330" y="165" width="220" height="70" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.4"/>
    <text x="345" y="188" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F06 Class Assignment</text>
    <text x="345" y="206" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Assign student to Class</text>
    <text x="345" y="222" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Creates Enrolment Profile</text>
  </g>

  <g>
    <rect x="330" y="275" width="220" height="95" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <rect x="475" y="283" width="65" height="16" rx="3" fill="#047857"/>
    <text x="507" y="294" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">SC ONLY</text>
    <text x="345" y="298" fill="#34d399" font-family="'Geist', sans-serif" font-size="11.5" font-weight="800">F08 EA Auto-Linkage</text>
    <text x="345" y="316" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• SC Match: Auto-link to R1 EA</text>
    <text x="345" y="332" fill="#f59e0b" font-family="'Geist Mono', monospace" font-size="9">• PR / IS: No EA Account</text>
    <text x="345" y="348" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">• F07 Transfer: Preserves history</text>
  </g>

  <!-- ==================== STAGE 3 NODES ==================== -->
  <g>
    <rect x="610" y="85" width="230" height="75" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1.2"/>
    <text x="625" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F09–F10 Fee Components</text>
    <text x="625" y="126" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• HQ: School Fee, Misc Fee</text>
    <text x="625" y="142" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• School: Transport, Enrichment</text>
  </g>

  <g>
    <rect x="610" y="175" width="230" height="95" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1.4"/>
    <text x="625" y="198" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F11 Fee Rate Rules</text>
    <text x="625" y="216" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Stage (P1-P6) × Resident (SC/PR/IS)</text>
    <text x="625" y="232" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="9">• Tax flag (is_apply_tax) at Component</text>
    <text x="625" y="248" fill="#818cf8" font-family="'Geist Mono', monospace" font-size="8.5">• Effective Date Range versioning</text>
  </g>

  <!-- ==================== STAGE 4 NODES ==================== -->
  <g>
    <rect x="900" y="85" width="230" height="150" rx="6" fill="#1e293b" stroke="#c084fc" stroke-width="1.5"/>
    <rect x="1050" y="93" width="70" height="16" rx="3" fill="#7e22ce"/>
    <text x="1085" y="104" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">PUBLISH</text>
    <text x="915" y="112" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">F12–F14 Fee Publication</text>
    <text x="915" y="130" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Scope: All School / Custom Target</text>
    <text x="915" y="146" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Target by Level, Class, SC/PR/IS</text>
    <text x="915" y="162" fill="#c084fc" font-family="'Geist Mono', monospace" font-size="9">• Resolves at eligibility_date</text>
    <text x="915" y="178" fill="#c084fc" font-family="'Geist Mono', monospace" font-size="9">• Pricing at pricing_date + GST</text>
    <text x="915" y="196" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Sets charge_date &amp; due_date</text>
  </g>

  <g>
    <rect x="900" y="275" width="230" height="90" rx="6" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <rect x="1055" y="283" width="65" height="16" rx="3" fill="#047857"/>
    <text x="1087" y="294" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">POSTED</text>
    <text x="915" y="300" fill="#34d399" font-family="'Geist', sans-serif" font-size="12" font-weight="800">F15 Student Charges</text>
    <text x="915" y="318" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">Charge Status: POSTED</text>
    <text x="915" y="334" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">Pushed to e-Service (R9) for Parent</text>
    <text x="915" y="348" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Generates student bill receivable</text>
  </g>

  <g>
    <rect x="900" y="405" width="230" height="70" rx="6" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
    <text x="915" y="428" fill="#fbbf24" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F16 Charge Adjustment</text>
    <text x="915" y="446" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Credit / Debit memo adjustment</text>
    <text x="915" y="460" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Preserves immutable Original Amount</text>
  </g>

</svg>"""

# ==============================================================================
# DIAGRAM 4: R4, R5 & R6 FAS ASSESSMENT, ML & BUDGET PIPELINE
# ==============================================================================
def build_r4_r5_r6_diagram():
    w, h = 1200, 560
    return f"""<svg viewBox="0 0 {w} {h}" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d4-title d4-desc">
  <title id="d4-title">EAFAMS R4, R5 and R6 FAS Assessment, ML and Budget Pipeline</title>
  <desc id="d4-desc">Dual intake via online and OCR hardcopy, MOEFAS automated rule engine, SBFAS school committee review powered by ML Need Score, and budget decrementing</desc>
  <defs>{COMMON_DEFS}</defs>
  <rect width="100%" height="100%" rx="14" fill="url(#bg-grad)"/>
  {header_svg(w, "R4, R5 &amp; R6 PIPELINE // FAS DUAL INTAKE, RULE ENGINE, ML NEED SCORE &amp; BUDGET", "AI &amp; DECISION FLOW", "#10b981", "#047857")}

  <!-- ZONES -->
  <rect x="25" y="60" width="260" height="475" rx="10" fill="url(#zone-school)" stroke="#10b981" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="40" y="52" width="180" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="1"/>
  <text x="130" y="65" fill="#34d399" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">R5 HARDCOPY &amp; INTAKE</text>

  <rect x="310" y="60" width="310" height="475" rx="10" fill="url(#zone-engine)" stroke="#818cf8" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="325" y="52" width="220" height="18" rx="4" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
  <text x="435" y="65" fill="#818cf8" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">R4 RULE EVALUATION ENGINE</text>

  <rect x="645" y="60" width="530" height="475" rx="10" fill="url(#zone-ext)" stroke="#f59e0b" stroke-width="1" stroke-dasharray="4 4"/>
  <rect x="665" y="52" width="260" height="18" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1"/>
  <text x="795" y="65" fill="#fbbf24" font-family="'Geist', sans-serif" font-size="10.5" font-weight="700" text-anchor="middle">R4 SBFAS ML REVIEW &amp; R6 BUDGET</text>

  <!-- CONNECTORS -->
  <path d="M 155 160 L 155 200" stroke="#38bdf8" stroke-width="1.8" fill="none" marker-end="url(#m-sky)"/>
  <path d="M 155 310 L 155 350" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>
  <path d="M 265 400 L 330 400 Q 338 400 338 392 L 338 238 Q 338 230 346 230 L 355 230" stroke="#818cf8" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>
  <path d="M 265 110 L 330 110 Q 338 110 338 152 L 338 190 Q 338 198 346 198 L 355 198" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Rule Engine Branch 1: MOEFAS Pass (Top) -->
  <path d="M 575 180 L 670 180" stroke="#10b981" stroke-width="2" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Rule Engine Branch 2: SBFAS Fallback (Bottom) -->
  <path d="M 575 240 L 620 240 Q 628 240 628 248 L 628 362 Q 628 370 636 370 L 670 370" stroke="#f59e0b" stroke-width="2" fill="none" marker-end="url(#m-amber)"/>

  <!-- SBFAS to ML Engine -->
  <path d="M 900 370 L 945 370" stroke="#c084fc" stroke-width="1.8" fill="none" marker-end="url(#m-purple)"/>

  <!-- Outcomes to R6 Budget Deduction -->
  <path d="M 890 180 L 960 180 Q 968 180 968 195 L 968 220 Q 968 228 976 228 L 985 228" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>
  <path d="M 900 400 L 960 400 Q 968 400 968 310 Q 968 302 976 302 L 985 302" stroke="#10b981" stroke-width="1.8" fill="none" marker-end="url(#m-emerald)"/>

  <!-- Connector Masks -->
  <rect x="590" y="171" width="60" height="18" rx="3" fill="#0f172a" stroke="#059669" stroke-width="0.8"/>
  <text x="620" y="184" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9" font-weight="700" text-anchor="middle">PASS SC</text>

  <rect x="585" y="320" width="70" height="18" rx="3" fill="#0f172a" stroke="#d97706" stroke-width="0.8"/>
  <text x="620" y="333" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">FAIL/NON-SC</text>

  <!-- ==================== R5 NODES ==================== -->
  <g>
    <rect x="45" y="85" width="220" height="75" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
    <text x="60" y="108" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F01 Upload Scans (R5)</text>
    <text x="60" y="126" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• School Admin uploads PDF/JPG</text>
    <text x="60" y="142" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• Simulated OCR auto-extraction</text>
  </g>

  <g>
    <rect x="45" y="200" width="220" height="110" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1.4"/>
    <text x="60" y="222" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F02 2-Pane Verification</text>
    <text x="60" y="240" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Left: Image | Right: Form P1-P5</text>
    <text x="60" y="256" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="9">• P1: Parent NRIC -> Locked autofill</text>
    <text x="60" y="272" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• P2: Child NRIC -> School/Class</text>
    <text x="60" y="288" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• P3: Gov Tax/CPF Income (auto)</text>
    <text x="60" y="302" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">• P4: Context | P5: Declaration</text>
  </g>

  <g>
    <rect x="45" y="350" width="220" height="85" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.4"/>
    <rect x="180" y="358" width="75" height="16" rx="3" fill="#047857"/>
    <text x="217" y="369" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">SPLIT APPS</text>
    <text x="60" y="374" fill="#34d399" font-family="'Geist', sans-serif" font-size="11.5" font-weight="700">F03 Split Child Apps</text>
    <text x="60" y="392" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Shared FAM-YYYY-NNNNN Ref</text>
    <text x="60" y="408" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Dispatches child to school flow</text>
    <text x="60" y="424" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Enters automated rule pipeline</text>
  </g>

  <!-- ==================== R4 RULE ENGINE ==================== -->
  <g>
    <rect x="330" y="160" width="265" height="120" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <rect x="495" y="168" width="90" height="16" rx="3" fill="#0284c7"/>
    <text x="540" y="179" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">RULE ENGINE</text>
    <text x="345" y="185" fill="#38bdf8" font-family="'Geist', sans-serif" font-size="12.5" font-weight="800">MOEFAS Rule Engine</text>
    <text x="345" y="205" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9.5">Hard Criteria Check:</text>
    <text x="345" y="222" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9.5">1. Citizenship: Singaporean (SC)</text>
    <text x="345" y="238" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9.5">2. Income Thresholds:</text>
    <text x="355" y="254" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• GHI &lt;= SGD 4,000 / month  OR</text>
    <text x="355" y="270" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• PCI &lt;= SGD 1,000 / month</text>
  </g>

  <!-- ==================== OUTCOMES & SBFAS ==================== -->
  <g>
    <!-- Outcome 1: MOEFAS Auto-Grant -->
    <rect x="670" y="140" width="220" height="95" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
    <rect x="805" y="148" width="75" height="16" rx="3" fill="#047857"/>
    <text x="842" y="159" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">AUTO-GRANT</text>
    <text x="685" y="165" fill="#34d399" font-family="'Geist', sans-serif" font-size="12" font-weight="800">MOEFAS Auto-Grant</text>
    <text x="685" y="183" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• 100% Subsidy on School &amp; Misc</text>
    <text x="685" y="199" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Zero Tier Division (Flat 100%)</text>
    <text x="685" y="215" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Auto-approved by system</text>
  </g>

  <g>
    <!-- Outcome 2: SBFAS School Review -->
    <rect x="670" y="320" width="230" height="135" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.8"/>
    <rect x="825" y="328" width="65" height="16" rx="3" fill="#b45309"/>
    <text x="857" y="339" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">SBFAS</text>
    <text x="685" y="345" fill="#fbbf24" font-family="'Geist', sans-serif" font-size="12" font-weight="700">SBFAS School Review</text>
    <text x="685" y="363" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• Assigned to School Admin</text>
    <text x="685" y="379" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="9">• HQ User has READ-ONLY access</text>
    <text x="685" y="395" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Approve: Select Tier + Comment</text>
    <text x="685" y="411" fill="#f43f5e" font-family="'Geist Mono', monospace" font-size="9">• Reject: Mandatory Reason + Note</text>
    <text x="685" y="432" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">Discretionary Assistance Matrix</text>
  </g>

  <g>
    <!-- ML AI Engine -->
    <rect x="945" y="320" width="215" height="135" rx="8" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
    <rect x="1080" y="328" width="70" height="16" rx="3" fill="#7e22ce"/>
    <text x="1115" y="339" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">ML ENGINE</text>
    <text x="960" y="345" fill="#c084fc" font-family="'Geist', sans-serif" font-size="12" font-weight="800">ML Need Score</text>
    <text x="960" y="365" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Need Score: 0 - 100</text>
    <text x="960" y="381" fill="#f8fafc" font-family="'Geist Mono', monospace" font-size="9">• Risk: Low / Med / High</text>
    <text x="960" y="397" fill="#c084fc" font-family="'Geist Mono', monospace" font-size="9">• Pre-selects Tier 1/2/3 in UI</text>
    <text x="960" y="415" fill="#94a3b8" font-family="'Geist Mono', monospace" font-size="8.5">Trained on Income, Dependents</text>
    <text x="960" y="431" fill="#64748b" font-family="'Geist Mono', monospace" font-size="8.5">&amp; Job stability features</text>
  </g>

  <g>
    <!-- R6 Budget & Ledger Offset -->
    <rect x="975" y="160" width="185" height="150" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.8"/>
    <rect x="1075" y="168" width="75" height="16" rx="3" fill="#047857"/>
    <text x="1112" y="179" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="8.5" font-weight="700" text-anchor="middle">R6 BUDGET</text>
    <text x="990" y="188" fill="#f8fafc" font-family="'Geist', sans-serif" font-size="12" font-weight="700">Budget &amp; Offset</text>
    <text x="990" y="206" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">• Auto-decrements</text>
    <text x="990" y="222" fill="#10b981" font-family="'Geist Mono', monospace" font-size="9">  Remaining Budget</text>
    <text x="990" y="238" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="8.5">• If Depleted: Routes to</text>
    <text x="990" y="252" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="8.5">  "Eligible - Insufficient"</text>
    <text x="990" y="272" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="9">• Net Payable recalculated:</text>
    <text x="990" y="288" fill="#38bdf8" font-family="'Geist Mono', monospace" font-size="8.5">  Net = Original - Subsidy</text>
  </g>

</svg>"""

# ==============================================================================
# DIAGRAM 5: R7 USER SIMULATION & SECURITY INTERCEPTOR
# ==============================================================================
def build_r7_diagram():
    w, h = 1140, 500
    return f"""<svg viewBox="0 0 {w} {h}" class="w-full h-auto select-none font-sans" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="d5-title d5-desc">
  <title id="d5-title">EAFAMS R7 User Simulation and Security Safeguard Flow</title>
  <desc id="d5-desc">Sequence flow of MOE HQ activating simulation mode for School Users or Parents, with persistent UI banner and mutating request interception</desc>
  <defs>{COMMON_DEFS}</defs>
  <rect width="100%" height="100%" rx="14" fill="url(#bg-grad)"/>
  {header_svg(w, "R7 SIMULATION FLOW // PERSONA SWITCH, READ-ONLY SHADOWING &amp; MUTATION INTERCEPTOR", "SAFETY AIRGAP", "#f43f5e", "#be123c")}

  <!-- 4 Lifelines -->
  <g font-size="11.5" font-weight="700" text-anchor="middle">
    <!-- Actor 0 -->
    <rect x="50" y="65" width="180" height="38" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="140" y="89" fill="#f8fafc">🏛️ MOE HQ Specialist</text>
    <line x1="140" y1="103" x2="140" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 1 -->
    <rect x="330" y="65" width="180" height="38" rx="6" fill="#1e293b" stroke="#818cf8" stroke-width="1.5"/>
    <text x="420" y="89" fill="#f8fafc">🌐 Gateway / Auth</text>
    <line x1="420" y1="103" x2="420" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 2 -->
    <rect x="610" y="65" width="180" height="38" rx="6" fill="#0f172a" stroke="#f43f5e" stroke-width="2"/>
    <text x="700" y="89" fill="#f43f5e">🛡️ Safety Interceptor</text>
    <line x1="700" y1="103" x2="700" y2="475" stroke="#334155" stroke-dasharray="4 4"/>

    <!-- Actor 3 -->
    <rect x="890" y="65" width="180" height="38" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1.5"/>
    <text x="980" y="89" fill="#f8fafc">💾 Ledger &amp; DB</text>
    <line x1="980" y1="103" x2="980" y2="475" stroke="#334155" stroke-dasharray="4 4"/>
  </g>

  <!-- SEQUENCE STEPS -->
  <!-- Step 1: Request Sim Token -->
  <line x1="140" y1="130" x2="420" y2="130" stroke="#38bdf8" stroke-width="1.8" marker-end="url(#m-sky)"/>
  <rect x="180" y="118" width="200" height="18" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="0.8"/>
  <text x="280" y="131" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">1. Start Sim (Target: Parent / School)</text>

  <!-- Step 2: Mint Sim Token -->
  <line x1="420" y1="165" x2="140" y2="165" stroke="#818cf8" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#m-purple)"/>
  <rect x="180" y="153" width="200" height="18" rx="4" fill="#0f172a" stroke="#818cf8" stroke-width="0.8"/>
  <text x="280" y="166" fill="#c084fc" font-size="10" font-weight="600" text-anchor="middle">2. JWT Issued: role=SIM, read_only=1</text>

  <!-- Step 3: UI Renders Amber Banner -->
  <rect x="70" y="195" width="400" height="28" rx="6" fill="#b45309" fill-opacity="0.3" stroke="#f59e0b" stroke-width="1.2"/>
  <text x="270" y="213" fill="#fbbf24" font-family="'Geist Mono', monospace" font-size="10" font-weight="700" text-anchor="middle">⚠️ SIMULATION ACTIVE: VIEWING AS PARENT S1234567A</text>

  <!-- Step 4: Legitimate Read Request -->
  <line x1="140" y1="250" x2="700" y2="250" stroke="#10b981" stroke-width="1.8" marker-end="url(#m-emerald)"/>
  <rect x="250" y="238" width="220" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="0.8"/>
  <text x="360" y="251" fill="#34d399" font-size="10" font-weight="600" text-anchor="middle">3. GET /api/ea/balance &amp; /charges</text>

  <!-- Step 5: Read Passes to DB -->
  <line x1="700" y1="250" x2="980" y2="250" stroke="#10b981" stroke-width="1.8" marker-end="url(#m-emerald)"/>

  <!-- Step 6: DB Returns 100% Exact Data -->
  <line x1="980" y1="285" x2="140" y2="285" stroke="#10b981" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#m-emerald)"/>
  <rect x="420" y="273" width="280" height="18" rx="4" fill="#0f172a" stroke="#10b981" stroke-width="0.8"/>
  <text x="560" y="286" fill="#10b981" font-size="10" font-weight="600" text-anchor="middle">4. Return exact balance $142.50 &amp; posted charges</text>

  <!-- BOUNDARY / VIOLATION BOX: ACCIDENTAL MUTATION -->
  <rect x="70" y="325" width="970" height="135" rx="8" fill="#1e293b" fill-opacity="0.4" stroke="#f43f5e" stroke-width="1.2" stroke-dasharray="4 4"/>
  <rect x="85" y="318" width="260" height="16" rx="3" fill="#be123c"/>
  <text x="215" y="330" fill="#ffffff" font-family="'Geist Mono', monospace" font-size="9" font-weight="700" text-anchor="middle">SAFETY INTERCEPTOR TEST: ACCIDENTAL MUTATION</text>

  <!-- Step 7: HQ attempts mutation -->
  <line x1="140" y1="365" x2="700" y2="365" stroke="#f43f5e" stroke-width="2" marker-end="url(#m-rose)"/>
  <rect x="230" y="353" width="260" height="18" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="0.8"/>
  <text x="360" y="366" fill="#f43f5e" font-size="9.5" font-weight="600" text-anchor="middle">5. POST /api/payment/pay-now (ACCIDENTAL)</text>

  <!-- Step 8: Interceptor BLOCKS Mutation -->
  <circle cx="700" cy="365" r="9" fill="#be123c" stroke="#f43f5e" stroke-width="1.5"/>
  <text x="700" y="369" fill="#ffffff" font-size="11" font-weight="800" text-anchor="middle">✕</text>

  <!-- Step 9: Rejects with 403 Forbidden -->
  <line x1="700" y1="405" x2="140" y2="405" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#m-rose)"/>
  <rect x="210" y="393" width="300" height="20" rx="4" fill="#be123c" stroke="#f43f5e" stroke-width="1"/>
  <text x="360" y="407" fill="#ffffff" font-size="10" font-weight="800" text-anchor="middle">6. 403 FORBIDDEN: SIMULATION IS READ-ONLY</text>

  <!-- Step 10: Interceptor Logs to Audit Trail -->
  <line x1="700" y1="435" x2="980" y2="435" stroke="#f59e0b" stroke-width="1.8" marker-end="url(#m-amber)"/>
  <rect x="740" y="423" width="200" height="18" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="0.8"/>
  <text x="840" y="436" fill="#fbbf24" font-size="9.5" font-weight="600" text-anchor="middle">7. Write Audit: Blocked Mutation Attempt</text>

</svg>"""

# ==============================================================================
# INTERACTIVE HTML BUILDER
# ==============================================================================
def build_html_viewer(d1, d2, d3, d4, d5):
    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EAFAMS Admin Portal // Interactive Architectural Diagrams</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Geist', sans-serif;
      background-color: #070B13;
      color: #E2E8F0;
    }}
    .font-mono {{ font-family: 'Geist Mono', monospace; }}
    .tab-btn.active {{
      background: #0284C7;
      color: #FFFFFF;
      border-color: #38BDF8;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }}
    .diagram-panel {{ display: none; }}
    .diagram-panel.active {{ display: block; }}
  </style>
</head>
<body class="min-h-screen p-4 md:p-8">

  <!-- TOP HERO HEADER -->
  <header class="max-w-7xl mx-auto mb-8 border-b border-slate-800 pb-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-2">
          <span class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-sky-950 text-sky-400 border border-sky-800">COMBO-DIAGRAM 2.6</span>
          <span class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">EDITORIAL VECTOR SVG</span>
          <span class="px-2.5 py-1 rounded text-xs font-mono font-bold bg-purple-950 text-purple-400 border border-purple-800">EAFAMS ADMIN PORTAL</span>
        </div>
        <h1 class="text-3xl font-extrabold text-white tracking-tight">EAFAMS Admin Portal Architecture &amp; Workflow Suite</h1>
        <p class="text-slate-400 text-sm mt-1">Sơ đồ tương tác toàn diện 7 phân hệ nghiệp vụ cốt lõi (R1 – R7) dành cho MOE HQ Users &amp; School Users.</p>
      </div>
      <div class="flex items-center gap-3">
        <a href="#matrix" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-mono text-slate-300 border border-slate-700 transition">📋 R1-R7 RBAC Table</a>
        <button onclick="window.print()" class="px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-xs font-mono font-semibold text-white transition">🖨️ Export PDF</button>
      </div>
    </div>

    <!-- TAB NAVIGATION -->
    <nav class="flex flex-wrap gap-2 mt-6">
      <button onclick="switchTab(1)" id="tab-btn-1" class="tab-btn active px-4 py-2 rounded-lg text-xs font-mono font-bold border border-slate-800 bg-slate-900 text-slate-400 transition">
        1. MASTER ARCHITECTURE (R1-R7)
      </button>
      <button onclick="switchTab(2)" id="tab-btn-2" class="tab-btn px-4 py-2 rounded-lg text-xs font-mono font-bold border border-slate-800 bg-slate-900 text-slate-400 transition">
        2. R1 LIFECYCLE &amp; R2 TOP-UP
      </button>
      <button onclick="switchTab(3)" id="tab-btn-3" class="tab-btn px-4 py-2 rounded-lg text-xs font-mono font-bold border border-slate-800 bg-slate-900 text-slate-400 transition">
        3. R3 SCHOOL, STUDENT &amp; FEES
      </button>
      <button onclick="switchTab(4)" id="tab-btn-4" class="tab-btn px-4 py-2 rounded-lg text-xs font-mono font-bold border border-slate-800 bg-slate-900 text-slate-400 transition">
        4. R4, R5, R6 FAS &amp; ML DECISION
      </button>
      <button onclick="switchTab(5)" id="tab-btn-5" class="tab-btn px-4 py-2 rounded-lg text-xs font-mono font-bold border border-slate-800 bg-slate-900 text-slate-400 transition">
        5. R7 SIMULATION SAFEGUARD
      </button>
    </nav>
  </header>

  <!-- MAIN DIAGRAM VIEWER STAGE -->
  <main class="max-w-7xl mx-auto space-y-8">

    <!-- PANEL 1: MASTER ARCHITECTURE -->
    <section id="panel-1" class="diagram-panel active">
      <div class="rounded-xl border border-slate-800 bg-[#0B101B] shadow-2xl overflow-hidden p-2">
        {d1}
      </div>
      <div class="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 font-mono flex items-center justify-between">
        <span>Sơ đồ 1: Tổng thể hệ sinh thái Admin Portal kết nối các Actor (HQ, School), 7 Module lõi, Double-Entry Ledger và các API ngoại vi.</span>
        <span class="text-sky-400 font-bold">1240 × 720 px</span>
      </div>
    </section>

    <!-- PANEL 2: R1 & R2 -->
    <section id="panel-2" class="diagram-panel">
      <div class="rounded-xl border border-slate-800 bg-[#0B101B] shadow-2xl overflow-hidden p-2">
        {d2}
      </div>
      <div class="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 font-mono flex items-center justify-between">
        <span>Sơ đồ 2: Vòng đời tự động của tài khoản EA (quét lúc 7 tuổi, đóng lúc 16 tuổi) và cơ chế nạp tiền lẻ / bulk campaign / hiệu chỉnh ghi nợ an toàn.</span>
        <span class="text-sky-400 font-bold">1180 × 560 px</span>
      </div>
    </section>

    <!-- PANEL 3: R3 -->
    <section id="panel-3" class="diagram-panel">
      <div class="rounded-xl border border-slate-800 bg-[#0B101B] shadow-2xl overflow-hidden p-2">
        {d3}
      </div>
      <div class="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 font-mono flex items-center justify-between">
        <span>Sơ đồ 3: Thiết lập trường, cấp học, lớp, tự động đối chiếu NRIC để link tài khoản EA cho học sinh Singapore, và phát hành hóa đơn POSTED.</span>
        <span class="text-sky-400 font-bold">1180 × 520 px</span>
      </div>
    </section>

    <!-- PANEL 4: R4, R5, R6 -->
    <section id="panel-4" class="diagram-panel">
      <div class="rounded-xl border border-slate-800 bg-[#0B101B] shadow-2xl overflow-hidden p-2">
        {d4}
      </div>
      <div class="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 font-mono flex items-center justify-between">
        <span>Sơ đồ 4: Luồng xử lý đơn trợ cấp FAS qua 2 kênh (Online R10 &amp; Đơn giấy OCR R5), Rule Engine Auto-Grant MOEFAS, School Review với ML Need Score và trừ ngân sách R6.</span>
        <span class="text-sky-400 font-bold">1200 × 560 px</span>
      </div>
    </section>

    <!-- PANEL 5: R7 -->
    <section id="panel-5" class="diagram-panel">
      <div class="rounded-xl border border-slate-800 bg-[#0B101B] shadow-2xl overflow-hidden p-2">
        {d5}
      </div>
      <div class="mt-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 font-mono flex items-center justify-between">
        <span>Sơ đồ 5: Chế độ mô phỏng người dùng của MOE HQ. Đảm bảo góc nhìn 100% trung thực nhưng tuyệt đối không phát sinh giao dịch tiền giả qua lớp chặn Interceptor.</span>
        <span class="text-sky-400 font-bold">1140 × 500 px</span>
      </div>
    </section>

    <!-- SUMMARY SECTION -->
    <section id="matrix" class="mt-12 p-6 rounded-xl bg-[#0E1524] border border-slate-800">
      <h2 class="text-lg font-bold text-white mb-4">📋 Bảng Tóm tắt Phân quyền &amp; Cơ chế Tự động Hóa (R1 – R7)</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs font-mono border-collapse">
          <thead>
            <tr class="border-b border-slate-800 text-slate-400">
              <th class="py-2.5 px-3">Phân hệ / Feature</th>
              <th class="py-2.5 px-3">Mô tả nghiệp vụ cốt lõi</th>
              <th class="py-2.5 px-3">MOE HQ User</th>
              <th class="py-2.5 px-3">School User</th>
              <th class="py-2.5 px-3">Cơ chế Tự động hóa / AI Engine</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60 text-slate-300">
            <tr>
              <td class="py-2.5 px-3 font-bold text-sky-400">R1: EA Lifecycle</td>
              <td class="py-2.5 px-3">Mở / đóng tài khoản EA cho học sinh SC</td>
              <td class="py-2.5 px-3">Xem toàn quốc</td>
              <td class="py-2.5 px-3 text-slate-500">Không truy cập</td>
              <td class="py-2.5 px-3 text-emerald-400">Daily Sync 00:00 SGT mở EA tuổi 7; Backend Check đóng EA tuổi 16</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 font-bold text-sky-400">R2: Top-Up Management</td>
              <td class="py-2.5 px-3">Nạp lẻ, nạp campaign theo đợt &amp; hiệu chỉnh</td>
              <td class="py-2.5 px-3">Toàn quyền thực thi</td>
              <td class="py-2.5 px-3 text-slate-500">Không có quyền</td>
              <td class="py-2.5 px-3 text-emerald-400">Lịch Bulk Campaign (Ad-hoc / Scheduled / Recurring) + Idempotency</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 font-bold text-sky-400">R3: School, Student &amp; Fee</td>
              <td class="py-2.5 px-3">Master trường, lớp, học sinh &amp; phát hành phí</td>
              <td class="py-2.5 px-3">Quản trị chung toàn quốc</td>
              <td class="py-2.5 px-3">Xếp lớp &amp; Publish phí trường</td>
              <td class="py-2.5 px-3 text-emerald-400">Auto-link EA cho học sinh SC; Resolve đối tượng tính phí &amp; GST</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 font-bold text-emerald-400">R4: FAS Core &amp; SBFAS</td>
              <td class="py-2.5 px-3">Xét duyệt trợ cấp học phí MOEFAS &amp; SBFAS</td>
              <td class="py-2.5 px-3">Xem toàn quốc, MOEFAS Scheme</td>
              <td class="py-2.5 px-3">Duyệt SBFAS trường mình</td>
              <td class="py-2.5 px-3 text-purple-400">Rule Engine: Auto-Grant MOEFAS; ML Need Score: Gợi ý Tier &amp; Risk</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 font-bold text-sky-400">R5: Hardcopy FAS Ingestion</td>
              <td class="py-2.5 px-3">Nhập đơn giấy thu trực tiếp tại trường</td>
              <td class="py-2.5 px-3 text-slate-500">Không truy cập</td>
              <td class="py-2.5 px-3">Nhập &amp; Đối soát đơn</td>
              <td class="py-2.5 px-3 text-amber-400">Simulated OCR trích xuất file scan, auto-fill NRIC &amp; Split đơn con</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 font-bold text-sky-400">R6: Budget &amp; Statistics</td>
              <td class="py-2.5 px-3">Quản lý hạn mức ngân sách &amp; báo cáo</td>
              <td class="py-2.5 px-3">Ngân sách MOEFAS</td>
              <td class="py-2.5 px-3">Ngân sách SBFAS trường</td>
              <td class="py-2.5 px-3 text-emerald-400">Tự động trừ hạn mức khi duyệt FAS; Báo động khi cạn ngân sách</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 font-bold text-rose-400">R7: User Simulation</td>
              <td class="py-2.5 px-3">Mô phỏng góc nhìn phụ huynh / trường học</td>
              <td class="py-2.5 px-3">Đóng vai School/Parent</td>
              <td class="py-2.5 px-3 text-slate-500">Không có quyền</td>
              <td class="py-2.5 px-3 text-rose-400">Mutation Interceptor chặn mọi giao dịch ghi; Banner cảnh báo cố định</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <script>
    function switchTab(idx) {{
      document.querySelectorAll('.diagram-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('panel-' + idx).classList.add('active');
      document.getElementById('tab-btn-' + idx).classList.add('active');
    }}
  </script>
</body>
</html>"""

def main():
    print("Generating editorial vector SVGs compliant with combo-diagram...")
    d1 = build_master_diagram()
    d2 = build_r1_r2_diagram()
    d3 = build_r3_diagram()
    d4 = build_r4_r5_r6_diagram()
    d5 = build_r7_diagram()

    f1 = OUT_DIR / "EAFAMS_ADMIN_PORTAL_MASTER_FLOW.svg"
    f2 = OUT_DIR / "EAFAMS_R1_R2_LIFECYCLE_TOPUP_FLOW.svg"
    f3 = OUT_DIR / "EAFAMS_R3_FEE_BILLING_FLOW.svg"
    f4 = OUT_DIR / "EAFAMS_R4_R5_R6_FAS_ASSESSMENT_FLOW.svg"
    f5 = OUT_DIR / "EAFAMS_R7_SIMULATION_FLOW.svg"
    f_html = OUT_DIR / "EAFAMS_ADMIN_PORTAL_INTERACTIVE_DIAGRAMS.html"

    f1.write_text(d1, encoding="utf-8")
    f2.write_text(d2, encoding="utf-8")
    f3.write_text(d3, encoding="utf-8")
    f4.write_text(d4, encoding="utf-8")
    f5.write_text(d5, encoding="utf-8")

    html_content = build_html_viewer(d1, d2, d3, d4, d5)
    f_html.write_text(html_content, encoding="utf-8")

    print(f"✓ Generated Master Diagram: {f1}")
    print(f"✓ Generated R1/R2 Diagram:   {f2}")
    print(f"✓ Generated R3 Diagram:      {f3}")
    print(f"✓ Generated R4/R5/R6 Diagram:{f4}")
    print(f"✓ Generated R7 Diagram:      {f5}")
    print(f"✓ Generated HTML Suite:      {f_html}")

if __name__ == "__main__":
    main()
