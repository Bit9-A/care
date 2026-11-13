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


class DiagnosticReportPermissions(enum.Enum):
    can_write_diagnostic_report = Permission(
        "Crear informe de diagnóstico en el establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE, DOCTOR_ROLE, NURSE_ROLE],
    )
    can_read_diagnostic_report = Permission(
        "Ver informe de diagnóstico",
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
        ],
    )
