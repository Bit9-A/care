import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    ADMINISTRATOR,
    DOCTOR_ROLE,
    FACILITY_ADMIN_ROLE,
    NURSE_ROLE,
    STAFF_ROLE,
)


class SchedulePermissions(enum.Enum):
    can_write_schedule = Permission(
        "Crear en la programación",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE, STAFF_ROLE, FACILITY_ADMIN_ROLE, DOCTOR_ROLE, NURSE_ROLE],
    )
    can_list_schedule = Permission(
        "Listar programación del objeto",
        "",
        PermissionContext.FACILITY,
        [
            ADMIN_ROLE,
            STAFF_ROLE,
            FACILITY_ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
        ],
    )
    can_list_booking = Permission(
        "Listar reservas del objeto",
        "",
        PermissionContext.FACILITY,
        [
            ADMIN_ROLE,
            STAFF_ROLE,
            FACILITY_ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
        ],
    )
    can_write_booking = Permission(
        "Actualizar reservas del objeto",
        "",
        PermissionContext.FACILITY,
        [
            ADMIN_ROLE,
            STAFF_ROLE,
            FACILITY_ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
        ],
    )
    can_reschedule_booking = Permission(
        "Reprogramar reservas del objeto",
        "",
        PermissionContext.FACILITY,
        [
            DOCTOR_ROLE,
            STAFF_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
        ],
    )
