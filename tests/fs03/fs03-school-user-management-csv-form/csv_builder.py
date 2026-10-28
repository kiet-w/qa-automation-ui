"""
tests/fs03/fs03-school-user-management-csv-form/csv_builder.py - CSV fixture builders for TC-FS03-SUM-0xx.
All row content derives from data/fs03/fs03_school_user_mgmt.json; identities are runtime-unique
(Invariant 2: no hardcoded test data, no mutation of shared fixtures).
"""
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def make_identity(prefix: str = "sum") -> Tuple[str, str]:
    """Return a unique (NRIC, email) pair; NRIC is S + 7 digits + checksum letter (ui_bsk §2.2)."""
    digits = f"{uuid.uuid4().int % 10_000_000:07d}"
    weights = [2, 7, 6, 5, 4, 3, 2]
    checksum = "JZIHGFEDCBA"[sum(int(d) * w for d, w in zip(digits, weights)) % 11]
    return f"S{digits}{checksum}", f"{prefix}_{digits}@schools.gov.sg"


class CsvBuilder:
    """Builds CSV/text fixture files under pytest tmp_path from the JSON data module."""

    def __init__(self, tmp_path: Path, data: Dict[str, Any]):
        self.tmp_path = Path(tmp_path)
        self.data = data
        self.identities: List[Dict[str, str]] = []

    # --- low level ---
    def write(self, name: str, content) -> str:
        path = self.tmp_path / name
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return str(path)

    def headers(self, omit: Optional[str] = None) -> str:
        return ",".join(h for h in self.data["csv"]["headers"] if h != omit)

    def row(self, template: Dict[str, str], nric: str, email: str) -> str:
        return ",".join(
            [template["no"], nric, email, template["first_name"], template["last_name"], template["school_code"]]
        )

    def _record(self, template: Dict[str, str], nric: str, email: str) -> Dict[str, str]:
        identity = {"nric": nric, "email": email, "school_code": template["school_code"]}
        self.identities.append(identity)
        return identity

    # --- fixtures ---
    def valid_file(self, name: str = "valid_school_users.csv") -> Tuple[str, List[Dict[str, str]]]:
        """Header + assigned/second/unassigned rows; returns (path, identities)."""
        rows = [self.headers()]
        identities = []
        for template in self.data["csv"]["row_templates"]:
            nric, email = make_identity("csv_ok")
            identities.append(self._record(template, nric, email))
            rows.append(self.row(template, nric, email))
        return self.write(name, "\n".join(rows) + "\n"), identities

    def missing_header_file(self, omit: str) -> Tuple[str, Dict[str, str]]:
        """Valid row under a header line missing one documented column; returns (path, identity)."""
        template = self.data["csv"]["row_templates"][0]
        nric, email = make_identity("csv_hdr")
        content = "\n".join([self.headers(omit=omit), self.row(template, nric, email)]) + "\n"
        return self.write(f"missing_{omit.replace(' ', '_')}.csv", content), self._record(template, nric, email)

    def header_only_file(self) -> str:
        """Header line with zero data rows."""
        return self.write("header_only.csv", self.headers() + "\n")

    def zero_byte_file(self) -> str:
        """0-byte file."""
        return self.write("empty.csv", b"")

    def too_many_columns_file(self) -> Tuple[str, Dict[str, str]]:
        """Valid row plus an extra-column row; returns (path, identity of the valid row)."""
        template = self.data["csv"]["row_templates"][0]
        nric, email = make_identity("csv_ovf")
        content = "\n".join(
            [self.headers(), self.row(template, nric, email), self.data["csv"]["too_many_columns_row"]]
        ) + "\n"
        return self.write("too_many_columns.csv", content), self._record(template, nric, email)

    def malformed_quoted_file(self) -> str:
        """Unclosed quoting to trigger the parser error path."""
        return self.write("malformed_quotes.csv", self.data["csv"]["malformed_quoted_content"] + "\n")

    def prose_txt_file(self) -> str:
        """Non-CSV prose content with .txt extension."""
        return self.write("notes.txt", self.data["csv"]["prose_txt_content"])

    def executable_file(self) -> str:
        """Binary executable-like payload with .exe extension."""
        return self.write("payload.exe", b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00")

    def disguised_file(self) -> str:
        """Binary payload behind a double extension (payload.csv.exe)."""
        return self.write("payload.csv.exe", b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00")

    def mismatched_csv_file(self) -> str:
        """.csv name with non-CSV binary content."""
        return self.write("mismatched.csv", b"\x00\x01\x02\xff\xfe\xfd binary payload \x00\x00")

    def valid_csv_as_txt_file(self) -> Tuple[str, Dict[str, str]]:
        """Genuine CSV content under a non-.csv name (extension-only validation probe)."""
        template = self.data["csv"]["row_templates"][0]
        nric, email = make_identity("csv_txt")
        content = "\n".join([self.headers(), self.row(template, nric, email)]) + "\n"
        return self.write("disguised_valid.csv.txt", content), self._record(template, nric, email)
