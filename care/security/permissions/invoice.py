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


class InvoicePermissions(enum.Enum):
    can_write_invoice = Permission(
        "Crear o actualizar factura",
        "",
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
    can_read_invoice = Permission(
        "Ver factura",
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
    can_destroy_invoice = Permission(
        "Eliminar factura",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE],
    )
    can_manage_locked_invoice = Permission(
        "Gestionar factura bloqueada",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE],
    )
