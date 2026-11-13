import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    DOCTOR_ROLE,
    FACILITY_ADMIN_ROLE,
    NURSE_ROLE,
    PHARMACIST_ROLE,
    STAFF_ROLE,
)


class MedicationPermissions(enum.Enum):
    is_pharmacist = Permission(
        "Farmacéutico en Care",
        "Los farmacéuticos en Care tienen acceso a todas las solicitudes de medicamentos y pueden crear dispensaciones para pacientes",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE, PHARMACIST_ROLE],
    )
    read_medication_dispense = Permission(
        "Ver dispensación de medicamentos",
        "Los usuarios pueden ver las dispensaciones de medicamentos",
        PermissionContext.FACILITY,
        [
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            PHARMACIST_ROLE,
        ],
    )
    write_medication_dispense = Permission(
        "Crear o actualizar dispensación de medicamentos",
        "Los usuarios pueden crear o actualizar dispensaciones de medicamentos",
        PermissionContext.FACILITY,
        [
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            PHARMACIST_ROLE,
        ],
    )
