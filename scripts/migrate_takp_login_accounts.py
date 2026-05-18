#!/usr/bin/env python3
"""
Migrate TAKP tblLoginServerAccounts to PEQ login_accounts.

Step 1 — export from TAKP (run on the TAKP server):
    mysql -u USER -p TAKP_DB --batch --raw \\
        -e "SELECT * FROM tblLoginServerAccounts" > takp_accounts.tsv

Step 2 — export game accounts for orphan detection (run on the PEQ/game server):
    mysql -u USER -p GAME_DB --batch --raw \\
        -e "SELECT id, name, lsaccount_id FROM account" > game_accounts.tsv

Step 3 — run this script:
    python migrate_takp_login_accounts.py \\
        --input takp_accounts.tsv \\
        --game-accounts game_accounts.tsv \\
        [--skip-orphans]

Outputs:
    login_accounts_import.sql   INSERT statements for PEQ login_accounts
    ownership_import.csv        web_username,login_account_name for assign_ownership
    orphaned_accounts.tsv       Login accounts with no matching game account (review before import)

Field mapping:
    AccountName       → account_name
    AccountPassword   → account_password       (EQEmu translates hash format on first login)
    AccountEmail      → account_email          ('0' placeholder cleaned to empty string)
    AccountCreateDate → created_at
    LastLoginDate     → last_login_date
    LastIPAddress     → last_ip_address
    (constant)        → source_loginserver = 'local'
    ForumName         → ownership_import.csv   (drives assign_ownership)
    Num_IP_Bypass     → noted in orphan report only (maps to ip_exemptions, not login_accounts)

Dropped fields:
    LoginServerID, created_by, client_unlock, creationIP, max_accts, lastpass_change
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

BATCH_SIZE = 200           # rows per INSERT statement (avoids max_allowed_packet issues)
SOURCE_LOGINSERVER = 'local'
FALLBACK_DATETIME = '1970-01-01 00:00:00'  # sentinel for NOT NULL datetime columns


# ---------------------------------------------------------------------------
# SQL helpers
# ---------------------------------------------------------------------------

def sql_str(value):
    """Escape and quote a string value for MySQL."""
    if value is None:
        return 'NULL'
    escaped = value.replace('\\', '\\\\').replace("'", "\\'")
    return f"'{escaped}'"


def sql_datetime(value):
    """Return a quoted datetime literal, falling back to FALLBACK_DATETIME if blank/invalid."""
    v = (value or '').strip()
    if not v or v == 'NULL' or v.startswith('0000-00-00'):
        return f"'{FALLBACK_DATETIME}'"
    return f"'{v}'"


def sql_datetime_nullable(value):
    """Return a quoted datetime literal or NULL."""
    v = (value or '').strip()
    if not v or v == 'NULL' or v.startswith('0000-00-00'):
        return 'NULL'
    return f"'{v}'"


def clean_email(value):
    """Replace TAKP's '0' placeholder with an empty string."""
    v = (value or '').strip()
    return '' if v == '0' else v


# ---------------------------------------------------------------------------
# TSV parsing
# ---------------------------------------------------------------------------

def load_tsv(path):
    with open(path, newline='', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f, delimiter='\t')
        rows = list(reader)
    return rows


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def build_insert_block(rows):
    """Return a complete INSERT statement for a batch of value tuples."""
    # id is explicitly included to preserve the TAKP LoginServerID so that
    # world server account.lsaccount_id references remain valid after import.
    columns = (
        'id, account_name, account_password, account_email, source_loginserver, '
        'last_ip_address, last_login_date, created_at'
    )
    values_sql = []
    for row in rows:
        values_sql.append(
            '  ({}, {}, {}, {}, {}, {}, {}, {})'.format(
                row['id'],
                sql_str(row['account_name']),
                sql_str(row['account_password']),
                sql_str(row['account_email']),
                sql_str(SOURCE_LOGINSERVER),
                sql_str(row['last_ip_address']),
                sql_datetime(row['last_login_date']),
                sql_datetime_nullable(row['created_at']),
            )
        )
    return (
        f'INSERT INTO login_accounts ({columns})\nVALUES\n'
        + ',\n'.join(values_sql)
        + ';'
    )


def main():
    parser = argparse.ArgumentParser(
        description='Migrate TAKP login accounts to PEQ login_accounts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--input', required=True,
                        metavar='FILE', help='TSV export of tblLoginServerAccounts')
    parser.add_argument('--game-accounts', metavar='FILE',
                        help='TSV export of game account table (columns: id, name, lsaccount_id)')
    parser.add_argument('--skip-orphans', action='store_true',
                        help='Exclude orphaned login accounts from the SQL output')
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Load TAKP accounts
    # ------------------------------------------------------------------
    print(f'Loading TAKP accounts from {args.input} ...')
    takp_rows = load_tsv(args.input)
    print(f'  {len(takp_rows)} rows loaded')

    # ------------------------------------------------------------------
    # Load game accounts → build set of known lsaccount_ids
    # ------------------------------------------------------------------
    game_lsids = None   # None means "no orphan detection requested"
    game_account_names = {}  # lsaccount_id → game account name (for reporting)

    if args.game_accounts:
        print(f'Loading game accounts from {args.game_accounts} ...')
        game_rows = load_tsv(args.game_accounts)
        game_lsids = set()
        for ga in game_rows:
            raw = (ga.get('lsaccount_id') or '').strip()
            if raw and raw not in ('NULL', '0', ''):
                game_lsids.add(raw)
                game_account_names[raw] = ga.get('name', '').strip()
        print(f'  {len(game_rows)} game accounts loaded, '
              f'{len(game_lsids)} have a valid lsaccount_id')

    # ------------------------------------------------------------------
    # Process rows
    # ------------------------------------------------------------------
    import_rows = []       # rows to INSERT into PEQ
    ownership_rows = []    # ForumName → account_name pairs
    orphan_rows = []       # login accounts with no matching game account
    no_forum_name = 0
    ip_bypass_accounts = []  # accounts with Num_IP_Bypass > 0 (for manual ip_exemptions)

    for takp in takp_rows:
        ls_id        = (takp.get('LoginServerID') or '').strip()
        acct_name    = (takp.get('AccountName') or '').strip()
        password     = (takp.get('AccountPassword') or '').strip()
        email        = clean_email(takp.get('AccountEmail', ''))
        create_date  = (takp.get('AccountCreateDate') or '').strip()
        last_login   = (takp.get('LastLoginDate') or '').strip()
        last_ip      = (takp.get('LastIPAddress') or '').strip()
        forum_name   = (takp.get('ForumName') or '').strip()
        num_bypass   = (takp.get('Num_IP_Bypass') or '0').strip()

        # Orphan check
        is_orphan = False
        if game_lsids is not None:
            is_orphan = ls_id not in game_lsids
            if is_orphan:
                orphan_rows.append({
                    'LoginServerID':  ls_id,
                    'AccountName':    acct_name,
                    'ForumName':      forum_name,
                    'LastLoginDate':  last_login,
                    'Num_IP_Bypass':  num_bypass,
                })
                if args.skip_orphans:
                    continue

        import_rows.append({
            'id':               ls_id,
            'account_name':     acct_name,
            'account_password': password,
            'account_email':    email,
            'last_ip_address':  last_ip,
            'last_login_date':  last_login,
            'created_at':       create_date,
        })

        # Ownership mapping (only if ForumName is set)
        if forum_name:
            ownership_rows.append({
                'web_username':        forum_name,
                'login_account_name':  acct_name,
            })
        else:
            no_forum_name += 1

        # Flag accounts with IP bypass > 0 for manual ip_exemptions review
        try:
            if int(num_bypass or 0) > 0:
                ip_bypass_accounts.append({
                    'AccountName':   acct_name,
                    'LastIPAddress': last_ip,
                    'Num_IP_Bypass': num_bypass,
                    'ForumName':     forum_name,
                })
        except ValueError:
            pass

    # ------------------------------------------------------------------
    # Write login_accounts_import.sql
    # ------------------------------------------------------------------
    sql_path = Path('login_accounts_import.sql')
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write('-- PEQ login_accounts import migrated from TAKP\n')
        f.write(f'-- Generated : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'-- Source    : {args.input}\n')
        f.write(f'-- Rows      : {len(import_rows)}\n')
        if args.skip_orphans and orphan_rows:
            f.write(f'-- Orphans skipped : {len(orphan_rows)}\n')
        f.write('--\n')
        f.write('-- Run against the PEQ login server database (e.g. the db containing login_accounts)\n')
        f.write('-- Review orphaned_accounts.tsv before running if orphan detection was used.\n')
        f.write('\n')
        f.write('SET NAMES utf8mb4;\n')
        f.write('SET foreign_key_checks = 0;\n\n')

        # Batch the INSERTs
        for i in range(0, len(import_rows), BATCH_SIZE):
            batch = import_rows[i:i + BATCH_SIZE]
            f.write(build_insert_block(batch))
            f.write('\n\n')

        f.write('SET foreign_key_checks = 1;\n')

    print(f'\nWritten : {sql_path}  ({len(import_rows)} rows, '
          f'{(len(import_rows) + BATCH_SIZE - 1) // BATCH_SIZE} batches of {BATCH_SIZE})')

    # ------------------------------------------------------------------
    # Write ownership_import.csv
    # ------------------------------------------------------------------
    csv_path = Path('ownership_import.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['web_username', 'login_account_name'])
        writer.writeheader()
        writer.writerows(ownership_rows)

    print(f'Written : {csv_path}  ({len(ownership_rows)} rows)')
    if no_forum_name:
        print(f'  Note  : {no_forum_name} account(s) had no ForumName — not included in ownership CSV')

    # ------------------------------------------------------------------
    # Write orphaned_accounts.tsv
    # ------------------------------------------------------------------
    if game_lsids is not None:
        orphan_path = Path('orphaned_accounts.tsv')
        with open(orphan_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['LoginServerID', 'AccountName', 'ForumName', 'LastLoginDate', 'Num_IP_Bypass'],
                delimiter='\t',
            )
            writer.writeheader()
            writer.writerows(orphan_rows)
        print(f'Written : {orphan_path}  ({len(orphan_rows)} orphaned login accounts)')

    # ------------------------------------------------------------------
    # Write ip_bypass_review.tsv (manual ip_exemptions candidates)
    # ------------------------------------------------------------------
    if ip_bypass_accounts:
        bypass_path = Path('ip_bypass_review.tsv')
        with open(bypass_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['AccountName', 'LastIPAddress', 'Num_IP_Bypass', 'ForumName'],
                delimiter='\t',
            )
            writer.writeheader()
            writer.writerows(ip_bypass_accounts)
        print(f'Written : {bypass_path}  ({len(ip_bypass_accounts)} account(s) with Num_IP_Bypass > 0)')
        print(f'  Note  : These do not auto-import — review and add to ip_exemptions manually')

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print('\n--- Summary ---')
    print(f'  TAKP accounts total       : {len(takp_rows)}')
    print(f'  Rows in SQL import        : {len(import_rows)}')
    print(f'  Ownership CSV rows        : {len(ownership_rows)}')
    print(f'  No ForumName (unlinked)   : {no_forum_name}')
    if game_lsids is not None:
        skipped = len(orphan_rows) if args.skip_orphans else 0
        print(f'  Orphaned (no game acct)   : {len(orphan_rows)}'
              + (f'  ({skipped} skipped from SQL)' if skipped else ' (included in SQL)'))
    if ip_bypass_accounts:
        print(f'  IP bypass candidates      : {len(ip_bypass_accounts)}  (see ip_bypass_review.tsv)')
    print()
    print('Next steps:')
    print('  1. Review orphaned_accounts.tsv and decide which to include/exclude')
    print(f'  2. Run:  mysql -u USER -p LOGIN_DB < {sql_path}')
    print(f'  3. Run:  python manage.py assign_ownership --csv {csv_path}')
    if ip_bypass_accounts:
        print('  4. Review ip_bypass_review.tsv and add entries to ip_exemptions manually')


if __name__ == '__main__':
    main()
