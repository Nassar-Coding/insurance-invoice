import csv, json, sys, tempfile
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / "src"))
from insurance_audit.io import INVOICE_COLUMNS, LINE_COLUMNS, load_hospital
from insurance_audit.audit import audit
from insurance_audit.confidence import assign_confidence
from insurance_audit.submission import validate_result

contract = json.loads((root / "contracts/hospital_1.json").read_text())
maps = json.loads((root / "mappings/hospital_1.json").read_text())
policy = json.loads((root / "evaluation/confidence_policy.json").read_text())
services = {s["id"]: s for s in contract["services"]}
aliases = {
    sid: next(r["raw_descriptions"][0] for r in maps["records"]
              if r["state"] == "accepted" and r["service_id"] == sid
              and r["grade"] == "explicit")
    for sid in ["H1-S004", "H1-S100"]
}

def header(ident, patient, invoice_date="2024-01-03"):
    return dict(invoice_id=ident, hospital_id="H1",
                contract_number=contract["contract_number"],
                invoice_date=invoice_date, patient_id=patient,
                facility_code="F-MAIN", plan_tier="BRONZE",
                admission_date="2024-01-01", discharge_date="2024-01-02",
                invoice_total_cents=9200 if ident == "I1" else 124450)

def line(ident, line_id, sid):
    svc = services[sid]
    rate = svc["versions"][0]["cents"]
    return dict(line_id=line_id, invoice_id=ident, line_no=1,
                service_date="2024-01-02", description=aliases[sid],
                quantity=1, unit_basis_as_billed=svc["unit"],
                unit_price_cents=rate, line_total_cents=rate)

with tempfile.TemporaryDirectory() as directory:
    for malformed in [False, True]:
        snapshot = Path(directory) / str(malformed)
        (snapshot / "invoices").mkdir(parents=True)
        headers = [header("I1", "P1"), header("I2", "P1"),
                   header("I2", "P2", "2024-02-30" if malformed
                          else "2024-01-03")]
        lines = [line("I1", "L1", "H1-S004"),
                 line("I2", "L2", "H1-S100")]
        for kind, columns, rows in [
            ("invoices", INVOICE_COLUMNS, headers),
            ("line_items", LINE_COLUMNS, lines),
        ]:
            path = snapshot / "invoices" / f"hospital_1_{kind}.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows)
        data = load_hospital(snapshot, "H1")
        result = audit(data, contract, maps)
        assign_confidence(result, policy)
        validation = validate_result(result, data, policy)
        opinion = next((o for o in result["opinions"]
                        if o["invoice_id"] == "I1"), None)
        print(json.dumps({"malformed_header": malformed,
                          "I1_opinion": opinion,
                          "validation": validation}, indent=2))
