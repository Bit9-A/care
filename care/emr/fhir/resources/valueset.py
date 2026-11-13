import json
import os
from functools import lru_cache

from django.utils.translation import get_language
from pydantic.main import BaseModel

from care.emr.fhir.resources.base import ResourceManger
from care.emr.fhir.resources.code_concept import MinimalCodeConcept
from care.emr.resources.common.coding import Coding
from care.emr.resources.common.valueset import ValueSetInclude

# Localised display names for terminology codes served by the external
# Snowstorm server, which only publishes the English international
# edition. Shape: {"es": {"<code>": "<translated display>"}}.
DISPLAY_OVERRIDES_PATH = os.path.join(
    os.path.dirname(__file__), "valueset_display_overrides.json"
)


@lru_cache(maxsize=1)
def load_display_overrides() -> dict:
    if not os.path.exists(DISPLAY_OVERRIDES_PATH):
        return {}
    with open(DISPLAY_OVERRIDES_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def localized_display(result: dict) -> str:
    """Return a translated display for the code when one is available.

    Falls back to the upstream display, so an unmapped or unsupported
    language keeps behaving exactly as before.
    """
    language = (get_language() or "en").split("-")[0].lower()
    translated = load_display_overrides().get(language, {})
    return translated.get(str(result.get("code"))) or result["display"]



class ValueSetFilterValidation(BaseModel):
    include: list[ValueSetInclude] = None
    exclude: list[ValueSetInclude] = None
    search: str = None
    count: int = None


class ValueSetResource(ResourceManger):
    allowed_properties = ["include", "exclude", "search", "count", "display_language"]

    def serialize(self, result):
        return MinimalCodeConcept(
            system=result["system"],
            code=result["code"],
            display=localized_display(result),
            designation=result.get("designation", []),
        )

    def validate_filter(self):
        ValueSetFilterValidation(**self._filters)

    def lookup(self, code: Coding):
        parameters = [
            {
                "name": "valueSet",
                "resource": {
                    "resourceType": "ValueSet",
                    "compose": {
                        "include": self._filters.get("include", []),
                        "exclude": self._filters.get("exclude", []),
                    },
                },
            },
            {"name": "coding", "valueCoding": code.model_dump(exclude_defaults=True)},
        ]
        request_json = {"resourceType": "Parameters", "parameter": parameters}

        full_result = self.query("POST", "ValueSet/$validate-code", request_json)
        if "parameter" not in full_result:
            raise ValueError("Valueset does not have specified code")
        results = full_result["parameter"]
        for result in results:
            if result["name"] == "result":
                return result["valueBoolean"]
        return False

    def search(self):
        parameters = []
        if self._filters.get("search"):
            parameters.append(
                {"name": "filter", "valueString": self._filters["search"]}
            )
        if "count" in self._filters:
            parameters.append({"name": "count", "valueInteger": self._filters["count"]})
        if "display_language" in self._filters:
            parameters.append(
                {
                    "name": "displayLanguage",
                    "valueString": self._filters["display_language"],
                }
            )
        parameters.append(
            {
                "name": "valueSet",
                "resource": {
                    "resourceType": "ValueSet",
                    "compose": {
                        "include": self._filters.get("include", []),
                        "exclude": self._filters.get("exclude", []),
                    },
                },
            }
        )
        parameters.append({"name": "includeDesignations", "valueBoolean": True})
        request_json = {"resourceType": "Parameters", "parameter": parameters}
        full_result = self.query("POST", "ValueSet/$expand", request_json)
        # TODO Add Exception Handling
        if "expansion" not in full_result:
            return []
        results = full_result["expansion"]
        if "contains" not in results:
            return []
        return self.handle_list(results["contains"])
