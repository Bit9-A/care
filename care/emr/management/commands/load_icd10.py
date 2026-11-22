import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from care.emr.models.icd10 import ICD10Code, fold_text

DEFAULT_DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "cie10-array.json"


class Command(BaseCommand):
    help = (
        "Load the CIE-10 (ICD-10) catalog with its Spanish display names. "
        "Rerunning is safe; existing codes are kept."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default=str(DEFAULT_DATA_FILE),
            help="Path to the JSON file with the [{c, d}] records",
        )
        parser.add_argument(
            "--truncate",
            default=False,
            type=bool,
            help="Delete every existing CIE-10 code before loading",
        )

    def handle(self, *args, **options):
        path = Path(options["file"])
        if not path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        records = json.loads(path.read_text(encoding="utf-8"))
        if options["truncate"]:
            ICD10Code.objects.all().delete()

        codes = [
            ICD10Code(
                code=record["c"],
                display=record["d"],
                search_text=fold_text(record["d"]),
                is_group=len(record["c"]) <= 3,
            )
            for record in records
        ]
        with transaction.atomic():
            ICD10Code.objects.bulk_create(
                codes, batch_size=2000, ignore_conflicts=True
            )

        total = ICD10Code.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {len(codes)} CIE-10 codes ({total} in database)")
        )
