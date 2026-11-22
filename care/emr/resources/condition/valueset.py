from care.emr.registries.care_valueset.care_valueset import CareValueset
from care.emr.resources.common.valueset import ValueSetCompose, ValueSetInclude
from care.emr.resources.valueset.spec import ValueSetStatusOptions
from care.emr.terminologies import ICD10_SYSTEM

CARE_CODITION_CODE_VALUESET = CareValueset(
    "Condition", "system-condition-code", ValueSetStatusOptions.active.value
)

CARE_CODITION_CODE_VALUESET.register_valueset(
    ValueSetCompose(
        include=[
            ValueSetInclude(
                system="http://snomed.info/sct",
                filter=[{"property": "concept", "op": "is-a", "value": "404684003"}],
            ),
            # Venezuelan clinicians code diagnoses with CIE-10, and it is the
            # only catalog with a complete official Spanish edition.
            ValueSetInclude(system=ICD10_SYSTEM),
        ]
    )
)

CARE_CODITION_CODE_VALUESET.register_as_system()

# Picker-only valueset: searching `system-condition-code` would mix English
# SNOMED CT results with the Spanish CIE-10 catalog, so the diagnosis picker
# asks for this CIE-10-only valueset instead.
CARE_CONDITION_CODE_ICD10_VALUESET = CareValueset(
    "Diagnóstico (CIE-10)",
    "system-condition-code-icd10",
    ValueSetStatusOptions.active.value,
)

CARE_CONDITION_CODE_ICD10_VALUESET.register_valueset(
    ValueSetCompose(include=[ValueSetInclude(system=ICD10_SYSTEM)])
)

CARE_CONDITION_CODE_ICD10_VALUESET.register_as_system()
