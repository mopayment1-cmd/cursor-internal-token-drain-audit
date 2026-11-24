import csv
import sys
import hashlib
from datetime import datetime, timezone
from collections import defaultdict

def parse_number(val_str):
    if not val_str:
        return 0.0
    cleaned = val_str.replace('$', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def audit_cursor_csv(file_path):
    print("\n" + "=" * 68)
    print("  CURSOR IDE USAGE & BILLING ANOMALY AUDITOR (v2.1)")
    print("=" * 68)
    print(f"[*] Target File: {file_path}\n")

    single_spikes = []
    minute_buckets = defaultdict(lambda: {'count': 0, 'tokens': 0, 'cost': 0.0})
    total_tokens = 0
    total_cost = 0.0
    row_count = 0

    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                print("[Error] CSV file appears to be empty or invalid.")
                return

            for row_num, row in enumerate(reader, start=2):
                row_count += 1
                norm = {k.lower().strip(): (v.strip() if v else "") for k, v in row.items()}

                tokens = 0
                if 'total tokens' in norm and norm['total tokens']:
                    tokens = int(parse_number(norm['total tokens']))
                elif 'tokens' in norm and norm['tokens']:
                    tokens = int(parse_number(norm['tokens']))
                else:
                    in_tok = parse_number(norm.get('input tokens', '0'))
                    out_tok = parse_number(norm.get('output tokens', '0'))
                    cache_tok = parse_number(norm.get('cache read tokens', '0'))
                    tokens = int(in_tok + out_tok + cache_tok)

                cost = 0.0
                for c_key in ['cost', 'total cost', 'price', 'amount']:
                    if c_key in norm and norm[c_key]:
                        cost = parse_number(norm[c_key])
                        break

                kind = norm.get('kind', norm.get('type', norm.get('model', 'standard')))
                date_str = norm.get('date', norm.get('timestamp', norm.get('time', 'N/A')))

                total_tokens += tokens
                total_cost += cost

                if tokens >= 500000:
                    single_spikes.append({
                        'row': row_num,
                        'date': date_str,
                        'kind': kind,
                        'tokens': tokens,
                        'cost': cost
                    })

                if date_str != 'N/A' and len(date_str) >= 16:
                    minute_key = date_str[:16]
                    minute_buckets[minute_key]['count'] += 1
                    minute_buckets[minute_key]['tokens'] += tokens
                    minute_buckets[minute_key]['cost'] += cost

        burst_minutes = [
            (m, data) for m, data in minute_buckets.items()
            if data['count'] >= 15 or data['tokens'] >= 1000000
        ]

        print(f"  Total Events Scanned : {row_count:,}")
        print(f"  Total Tokens Logged  : {total_tokens:,}")
        print(f"  Total Cost Logged    : ${total_cost:,.2f}")
        print("-" * 68)

        if single_spikes:
            print(f"\n[!] CRITICAL: Found {len(single_spikes)} Single-Event Unthrottled Spike(s) (>= 500k tokens):")
            for s in single_spikes[:15]:
                print(f"    -> Row {s['row']} | {s['date']} | {s['kind']} | {s['tokens']:,} tokens (${s['cost']:.2f})")
            if len(single_spikes) > 15:
                print(f"    ... and {len(single_spikes) - 15} more spikes.")
        else:
            print("\n[+] Single-Event Check: No individual requests >= 500,000 tokens detected.")

        if burst_minutes:
            print(f"\n[!] WARNING: Found {len(burst_minutes)} High-Velocity Burst Minute(s) (>= 15 req/min or >= 1M tok/min):")
            for m, data in sorted(burst_minutes, key=lambda x: x['tokens'], reverse=True)[:10]:
                print(f"    -> {m} | {data['count']} requests | {data['tokens']:,} tokens | ${data['cost']:.2f}")
        else:
            print("[+] Velocity Check: No automated per-minute burst loops detected.")

        # Generate anonymized shareable summary & verification hash
        scan_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        raw_sig = f"{row_count}:{total_tokens}:{len(single_spikes)}:{len(burst_minutes)}:{scan_date}"
        anon_hash = hashlib.sha256(raw_sig.encode()).hexdigest()[:12].upper()

        status_label = "CLEAN" if (len(single_spikes) == 0 and len(burst_minutes) == 0) else "ANOMALIES_DETECTED"
        shareable_line = (
            f"Audit Result [{status_label}]: {len(single_spikes)} single spikes (>=500k), "
            f"{len(burst_minutes)} burst minutes | Events: {row_count:,} | "
            f"Date: {scan_date} | Sig: #{anon_hash}"
        )

        print("\n" + "=" * 68)
        print("  ANONYMIZED SHAREABLE SUMMARY (NO PERSONAL DATA INCLUDED)")
        print("  Copy & paste the line below into the GitHub Issues tracker to")
        print("  contribute to the community baseline, and Star the repo to help")
        print("  others audit their billing logs:")
        print("-" * 68)
        print(f"  {shareable_line}")
        print("=" * 68 + "\n")

    except FileNotFoundError:
        print(f"[Error] File not found: '{file_path}'")
    except Exception as e:
        print(f"[Error] Unexpected error parsing CSV: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 audit_csv.py <path_to_cursor_usage.csv>")
        sys.exit(1)
    audit_cursor_csv(sys.argv[1])
