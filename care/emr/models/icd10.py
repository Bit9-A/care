import unicodedata

from django.db import models


def fold_text(value: str) -> str:
    """Lowercase and strip diacritics so Spanish search ignores accents.

    The CIE-10 catalog mixes both spellings ("Hipertension" and
    "Hipertensión"), so a clinician typing either one must get the same hits.
    """
    decomposed = unicodedata.normalize("NFKD", value or "")
    return "".join(char for char in decomposed if not unicodedata.combining(char)).lower()


class ICD10Code(models.Model):
    """CIE-10 (ICD-10) code with its official Spanish display name.

    Snowstorm only serves the English SNOMED CT edition, so the diagnosis
    picker had no searchable catalog in Spanish. These rows are loaded from
    `cie10-array.json` by the `load_icd10` management command and are searched
    locally instead of through the external FHIR server.
    """

    code = models.CharField(max_length=16, unique=True, db_index=True)
    display = models.CharField(max_length=512)
    # Accent-folded, lowercase copy of `display` used for searching.
    search_text = models.CharField(max_length=512, db_index=True)
    # 3-character codes are categories (chapter/subcategory headings); the
    # billable detail level is 4 characters.
    is_group = models.BooleanField(default=False)

    class Meta:
        ordering = ["code"]
        verbose_name = "CIE-10 code"
        verbose_name_plural = "CIE-10 codes"

    def save(self, *args, **kwargs):
        self.search_text = fold_text(self.display)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.display}"
