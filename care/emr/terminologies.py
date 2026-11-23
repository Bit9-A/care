"""Terminology systems served locally instead of by the Snowstorm FHIR server.

Snowstorm publishes only the English SNOMED CT edition, so any system that
needs a complete Spanish catalog (currently CIE-10) is stored in Postgres and
queried here. Valuesets can mix remote and local systems transparently.
"""

import json
import os
import re
from functools import lru_cache

from django.db.models import Case, IntegerField, Q, Value, When
from django.db.models.functions import Length

from care.emr.fhir.resources.code_concept import MinimalCodeConcept

ICD10_SYSTEM = "http://hl7.org/fhir/sid/icd-10"

LOCAL_SYSTEMS = {ICD10_SYSTEM}

# The upstream CIE-10 file drops most diacritics ("Hipertension", "Colera").
# This curated map restores them; it is generated from the Spanish hunspell
# dictionaries plus manual review, and only ever adds accents, never changes
# letters. Words that are already valid Spanish are absent on purpose, so
# homographs like "ano" (anus) are never turned into "año".
ACCENT_FIXES_PATH = os.path.join(
    os.path.dirname(__file__), "data", "cie10_accent_fixes.json"
)
WORD_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")


@lru_cache(maxsize=1)
def load_accent_fixes() -> dict:
    if not os.path.exists(ACCENT_FIXES_PATH):
        return {}
    with open(ACCENT_FIXES_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def fix_display(text: str) -> str:
    """Restore the missing Spanish accents of an upstream CIE-10 display."""

    fixes = load_accent_fixes()

    def replace(match):
        word = match.group(0)
        if word.isupper():
            return word
        fixed = fixes.get(word.lower())
        if not fixed:
            return word
        return fixed[0].upper() + fixed[1:] if word[0].isupper() else fixed

    return WORD_PATTERN.sub(replace, text or "")


def is_local_system(system: str) -> bool:
    return system in LOCAL_SYSTEMS


def _search_icd10(search: str, count: int) -> list[MinimalCodeConcept]:
    from care.emr.models.icd10 import ICD10Code, fold_text

    queryset = ICD10Code.objects.all()
    term = fold_text((search or "").strip())
    if term:
        # Codes are stored uppercase; `search_text` is already folded, so both
        # "Hipertensión" and "hipertension" hit the same rows.
        queryset = queryset.filter(
            Q(search_text__contains=term) | Q(code__istartswith=term.upper())
        ).annotate(
            match_rank=Case(
                When(code__iexact=term.upper(), then=Value(0)),
                When(code__istartswith=term.upper(), then=Value(1)),
                When(search_text__startswith=term, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            ),
            code_length=Length("code"),
        )
        # Parent categories (I10) rank above their children (I150) so the
        # broader diagnosis is offered first.
        queryset = queryset.order_by("match_rank", "code_length", "code")
    return [
        MinimalCodeConcept(system=ICD10_SYSTEM, code=row.code, display=row.display)
        for row in queryset[:count]
    ]


def search_local(
    system: str, search: str = "", count: int = 10
) -> list[MinimalCodeConcept]:
    if system == ICD10_SYSTEM:
        return _search_icd10(search, count or 10)
    return []


def lookup_local(system: str, code: str) -> bool:
    if system == ICD10_SYSTEM:
        from care.emr.models.icd10 import ICD10Code

        return ICD10Code.objects.filter(code__iexact=str(code or "").strip()).exists()
    return False
