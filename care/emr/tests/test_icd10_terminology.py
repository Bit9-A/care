from unittest.mock import patch

from model_bakery import baker

from care.emr.models import ValueSet
from care.emr.models.icd10 import ICD10Code
from care.emr.resources.common.coding import Coding
from care.emr.terminologies import ICD10_SYSTEM
from care.utils.tests.base import CareAPITestBase


class TestIcd10Terminology(CareAPITestBase):
    """The CIE-10 catalog is served locally, never by the Snowstorm server."""

    def setUp(self):
        super().setUp()
        baker.make(ICD10Code, code="I10", display="Hipertension esencial (primaria)")
        baker.make(ICD10Code, code="I15", display="Hipertension secundaria")
        baker.make(ICD10Code, code="A00", display="Cólera")
        self.valueset = baker.make(
            ValueSet,
            slug="condition-codes-icd10-test",
            name="Condition CIE-10",
            status="active",
            compose={"include": [{"system": ICD10_SYSTEM}]},
        )

    def test_search_returns_local_rows_without_hitting_the_fhir_server(self):
        with patch("care.emr.models.valueset.ValueSetResource") as resource:
            results = self.valueset.search(search="hipertension", count=5)

        resource.assert_not_called()
        self.assertEqual([result.code for result in results], ["I10", "I15"])
        self.assertTrue(all(result.system == ICD10_SYSTEM for result in results))

    def test_search_ignores_accents_in_both_directions(self):
        self.assertEqual(
            [result.code for result in self.valueset.search(search="cólera")], ["A00"]
        )
        self.assertEqual(
            [result.code for result in self.valueset.search(search="colera")], ["A00"]
        )

    def test_search_matches_the_code_itself(self):
        self.assertEqual(
            [result.code for result in self.valueset.search(search="I10")], ["I10"]
        )

    def test_lookup_accepts_a_known_code_and_rejects_an_unknown_one(self):
        self.assertTrue(
            self.valueset.lookup(Coding(system=ICD10_SYSTEM, code="I10", display="x"))
        )
        self.assertFalse(
            self.valueset.lookup(Coding(system=ICD10_SYSTEM, code="ZZZ9", display="x"))
        )

    def test_lookup_rejects_a_local_code_the_valueset_does_not_include(self):
        snomed_only = baker.make(
            ValueSet,
            slug="condition-codes-snomed-test",
            name="Condition SNOMED",
            status="active",
            compose={"include": [{"system": "http://snomed.info/sct"}]},
        )
        with patch("care.emr.models.valueset.ValueSetResource") as resource:
            resource.return_value.filter.return_value.lookup.return_value = False
            self.assertFalse(
                snomed_only.lookup(
                    Coding(system=ICD10_SYSTEM, code="I10", display="x")
                )
            )

    def test_remote_systems_still_use_the_fhir_server(self):
        snomed_only = baker.make(
            ValueSet,
            slug="condition-codes-remote-test",
            name="Condition SNOMED",
            status="active",
            compose={"include": [{"system": "http://snomed.info/sct"}]},
        )
        with patch("care.emr.models.valueset.ValueSetResource") as resource:
            resource.return_value.filter.return_value.search.return_value = []
            snomed_only.search(search="hypertension", count=3)
        resource.return_value.filter.return_value.search.assert_called_once()
