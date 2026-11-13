import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    ADMINISTRATOR,
    DOCTOR_ROLE,
    FACILITY_ADMIN_ROLE,
    NURSE_ROLE,
    STAFF_ROLE,
    VOLUNTEER_ROLE,
)

ALL_ROLES = [
    ADMIN_ROLE,
    DOCTOR_ROLE,
    NURSE_ROLE,
    ADMINISTRATOR,
    STAFF_ROLE,
    FACILITY_ADMIN_ROLE,
    VOLUNTEER_ROLE,
]

CLINICAL_DATA_ACCESS_ROLES = [
    ADMIN_ROLE,
    DOCTOR_ROLE,
    NURSE_ROLE,
    FACILITY_ADMIN_ROLE,
]


class EncounterPermissions(enum.Enum):
    can_create_encounter = Permission(
        "Crear episodio clínico",
        "",
        PermissionContext.ENCOUNTER,
        CLINICAL_DATA_ACCESS_ROLES,
    )
    can_list_encounter = Permission(
        "Listar episodios clínicos",
        "Los datos clínicos no están asociados con este permiso",
        PermissionContext.ENCOUNTER,
        CLINICAL_DATA_ACCESS_ROLES,
    )
    can_write_encounter = Permission(
        "Actualizar datos no clínicos del episodio clínico",
        "",
        PermissionContext.ENCOUNTER,
        CLINICAL_DATA_ACCESS_ROLES,
    )
    can_write_encounter_clinical_data = Permission(
        "Actualizar datos clínicos relacionados con el episodio clínico",
        "",
        PermissionContext.ENCOUNTER,
        CLINICAL_DATA_ACCESS_ROLES,
    )
    can_read_encounter = Permission(
        "Ver episodio clínico",
        "",
        PermissionContext.ENCOUNTER,
        CLINICAL_DATA_ACCESS_ROLES,
    )
    can_read_encounter_clinical_data = Permission(
        "Ver datos clínicos relacionados con el episodio clínico",
        "",
        PermissionContext.ENCOUNTER,
        CLINICAL_DATA_ACCESS_ROLES,
    )
    can_submit_encounter_questionnaire = Permission(
        "Enviar cuestionario sobre episodios clínicos del paciente",
        "",
        PermissionContext.PATIENT,
        [
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMIN_ROLE,
            FACILITY_ADMIN_ROLE,
        ],
    )
