# Cursor Billing & Support Failure: $278.25 Across 6 Invoices in 3 Days, No Human Response for 29 Days — Evidence Pack
![Cursor Billing & Security Incident Audit](hero-evidence.png)
> **Official GitHub Repository & Source Code (`audit_csv.py`):** [https://github.com/mopayment1-cmd/cursor-internal-token-drain-audit](https://github.com/mopayment1-cmd/cursor-internal-token-drain-audit)

Evidence-based audit of a Cursor (Anysphere) billing incident: 6 invoices totalling $278.25 (25–27 Oct 2026), Ultra tier change, $40.24 refund, $218.01 stated as non-returnable, and 29 days without a substantive human response. Invoices, tickets, and correspondence with redactions. No secrets, no card data, no API keys.


# Cursor Billing & Support Failure — Evidence Pack

> This repository does not allege intent, fraud, or a crime by Cursor / Anysphere.
> It presents dated invoices, dated support correspondence, and a reconciliation
> that does not close, and asks for a transaction-by-transaction answer.

## The core claim, in one paragraph

Between 25–27 Oct 2026, six Cursor invoices totalling **$278.25** were issued
on one account: $20.00 Pro + $20.03 usage + $40.24 usage + $95.65 Ultra
(after 50% loyalty discount) + $60.21 usage + $42.12 usage (27 Oct).
On 23 Nov 2026, Cursor Trust & Safety acknowledged "suspicious activity",
refunded **$40.24** — exactly the amount of Invoice 0018 — and stated
**$218.01** could not be returned.
$278.25 − $40.24 − $218.01 = **$20.00**, exactly the Pro subscription in
Invoice 0016. No invoice or message in this pack explains whether that
$20.00 is the reconciliation for the gap.

## What this repo proves / does not prove

**Proved by the invoices in this repo:**
- 6 invoices, numbers, dates, and amounts listed in RECONCILIATION.md
- A tier change to Ultra ($200, discounted to $95.65) on 25 Oct
- Usage volumes with very large cache-read token counts

**Not proved by the invoices alone:**
- "91.7M tokens in <1 second" — that claim comes from the CSV export,
  not from the invoices. See `evidence/CSV-NOTE.md`.
- "Stripe blocked Cursor" — no Stripe document is included in this
  version. See `evidence/STRIPE-NOTE.md`.
- "$80.34 demand on 13 Nov" — no invoice for that amount is in the
  merged PDF. See `evidence/MISSING-EXHIBIT-07.md`.

## Evidence index

| File | What it is | Status |
| :--- | :--- | :--- |
| `evidence/01_invoices_0016-0021_redacted.pdf` | 6 Cursor invoices, 25–27 Oct | Included, redacted |
| `evidence/02_ticket_T-I38194_escalation_27Oct.png` | Escalation email, 27 Oct 23:17 | Included, redacted |
| `evidence/03_human_review_request_28Oct.png` | Human review request, 28 Oct 11:56 | Included, redacted |
| `evidence/04_duplicate_closure_T-I55882.png` | AI Assistant Sam closes duplicate | Included, redacted |
| `evidence/05_trust_safety_23Nov.png` | $40.24 refund + $218.01 non-returnable | Included, redacted |
| `evidence/06_usage_csvs/` | CSV exports 14 Nov + 17 Nov | Hashes only until redacted |
| `evidence/07_stripe_19-20Nov.png` | Stripe intervention | **MISSING — add or remove claim** |
| `evidence/08_invoice_80.34_13Nov.png` | $80.34 demand | **MISSING — add or remove claim** |

## Reconciliation

See `RECONCILIATION.md` for the full invoice-by-invoice table.

## The 5 questions we are asking Anysphere

1. Provide a transaction-by-transaction reconciliation for $278.25 / $40.24 / $218.01 / $20.00.
2. Why was a Pro → Ultra tier change ($200) applied on 25 Oct, and what authentication was required?
3. Why was a $42.12 usage invoice issued on 27 Oct after cancellation on 25 Oct?
4. Why did a billing dispute receive only AI / automated handling from 25 Oct to 23 Nov?
5. What server-side spend-cap / circuit-breaker, if any, limits token-based usage in a single session?

## Contact for comment

Anysphere was contacted on [DATE] with these 5 questions. This repo will be
updated with any response, verbatim and unedited.

## Redaction

All exhibits are redacted: name, full address, email, card numbers, account IDs,
API keys, and project secrets are removed. Amounts, dates, invoice numbers,
ticket numbers, and message bodies are preserved.
