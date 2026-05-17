"""
Assign login server account ownership to web user accounts.

Single assignment:
    python manage.py assign_ownership --web-user "john_doe" --login-account "JohnEQ"

Bulk from CSV (columns: web_username, login_account_name):
    python manage.py assign_ownership --csv ownership.csv

The command is idempotent: existing records are skipped, not duplicated.
Re-running after a partial failure is safe.
"""
import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from accounts.models import LoginAccountOwnership, LoginAccounts


class Command(BaseCommand):
    help = 'Assign login server account ownership to web user accounts'

    def add_arguments(self, parser):
        source = parser.add_mutually_exclusive_group(required=True)
        source.add_argument(
            '--csv',
            dest='csv_file',
            metavar='FILE',
            help='CSV file with headers: web_username, login_account_name',
        )
        source.add_argument(
            '--web-user',
            dest='web_user',
            metavar='USERNAME',
            help='Web account username (pair with --login-account)',
        )
        parser.add_argument(
            '--login-account',
            dest='login_account',
            metavar='NAME',
            help='Login server account name (pair with --web-user)',
        )

    def handle(self, *args, **options):
        if options['csv_file']:
            self._process_csv(options['csv_file'])
        else:
            if not options['login_account']:
                raise CommandError('--login-account is required when using --web-user')
            result = self._assign(options['web_user'], options['login_account'])
            if result == 'created':
                self.stdout.write(self.style.SUCCESS(
                    f"Created: {options['web_user']} → {options['login_account']}"
                ))
            elif result == 'exists':
                self.stdout.write(self.style.WARNING(
                    f"Already exists: {options['web_user']} → {options['login_account']}"
                ))

    # ------------------------------------------------------------------

    def _process_csv(self, csv_path):
        created = skipped = failed = 0
        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not {'web_username', 'login_account_name'}.issubset(reader.fieldnames or []):
                    raise CommandError(
                        f'CSV must have columns "web_username" and "login_account_name". '
                        f'Found: {reader.fieldnames}'
                    )
                for lineno, row in enumerate(reader, start=2):
                    web_user = row.get('web_username', '').strip()
                    ls_name = row.get('login_account_name', '').strip()
                    if not web_user or not ls_name:
                        self.stderr.write(f'Line {lineno}: skipping blank row')
                        failed += 1
                        continue
                    result = self._assign(web_user, ls_name, lineno=lineno)
                    if result == 'created':
                        created += 1
                    elif result == 'exists':
                        skipped += 1
                    else:
                        failed += 1
        except FileNotFoundError:
            raise CommandError(f'File not found: {csv_path}')

        self.stdout.write('\nSummary:')
        self.stdout.write(self.style.SUCCESS(f'  Created : {created}'))
        self.stdout.write(self.style.WARNING(f'  Skipped : {skipped}  (already existed)'))
        if failed:
            self.stdout.write(self.style.ERROR(f'  Failed  : {failed}  (see errors above)'))
        else:
            self.stdout.write(f'  Failed  : {failed}')

    def _assign(self, web_username, login_account_name, lineno=None):
        prefix = f'Line {lineno}: ' if lineno else ''

        try:
            user = User.objects.get(username=web_username)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                f'{prefix}Web user not found: {web_username!r}'
            ))
            return 'error'

        try:
            ls_account = LoginAccounts.objects.using('login_server_database').get(
                account_name=login_account_name
            )
        except LoginAccounts.DoesNotExist:
            self.stderr.write(self.style.ERROR(
                f'{prefix}Login account not found: {login_account_name!r}'
            ))
            return 'error'
        except LoginAccounts.MultipleObjectsReturned:
            self.stderr.write(self.style.ERROR(
                f'{prefix}Multiple login accounts match {login_account_name!r} — skipping'
            ))
            return 'error'

        _, created = LoginAccountOwnership.objects.get_or_create(
            user=user,
            login_account_id=ls_account.id,
        )
        if created:
            self.stdout.write(
                f'  {prefix}Created : {web_username} → {login_account_name} '
                f'(ls_id={ls_account.id})'
            )
            return 'created'
        else:
            self.stdout.write(
                f'  {prefix}Skipped : {web_username} → {login_account_name} (already exists)'
            )
            return 'exists'
