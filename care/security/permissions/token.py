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


class TokenPermissions(enum.Enum):
    can_write_token_category = Permission(
        "Crear en la categoría de tokens",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE, STAFF_ROLE, FACILITY_ADMIN_ROLE],
    )
    can_list_token_category = Permission(
        "Listar categorías de tokens del establecimiento",
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
    can_write_token = Permission(
        "Crear token",
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
    can_list_token = Permission(
        "Listar tokens del objeto",
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
