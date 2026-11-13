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


class ChargeItemDefinitionPermissions(enum.Enum):
    can_write_charge_item_definition = Permission(
        "Crear definición de cargo en el establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE],
    )
    can_read_charge_item_definition = Permission(
        "Ver definición de cargo",
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
    can_set_charge_item_definition = Permission(
        "Establecer definición de cargo en el establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE],
    )
