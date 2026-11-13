import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    ADMINISTRATOR,
    DOCTOR_ROLE,
    FACILITY_ADMIN_ROLE,
    NURSE_ROLE,
    PHARMACIST_ROLE,
    STAFF_ROLE,
    VOLUNTEER_ROLE,
)


class PatientIdentifierConfigPermissions(enum.Enum):
    can_write_patient_identifier_config = Permission(
        "Crear configuración de identificadores de pacientes en el establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE],
    )
    can_read_patient_identifier_config = Permission(
        "Ver configuración de identificadores de pacientes",
        "",
        PermissionContext.FACILITY,
        [
            FACILITY_ADMIN_ROLE,
            ADMINISTRATOR,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            VOLUNTEER_ROLE,
            PHARMACIST_ROLE,
        ],
    )
