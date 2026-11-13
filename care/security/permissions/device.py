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


class DevicePermissions(enum.Enum):
    can_list_devices = Permission(
        "Listar dispositivos del establecimiento",
        "",
        PermissionContext.FACILITY,
        [
            STAFF_ROLE,
            ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            FACILITY_ADMIN_ROLE,
            PHARMACIST_ROLE,
        ],
    )
    can_manage_device_associations_to_encounters = Permission(
        "Gestionar asociaciones de dispositivos con episodios clínicos",
        "",
        PermissionContext.FACILITY,
        [STAFF_ROLE, ADMIN_ROLE, DOCTOR_ROLE, NURSE_ROLE, FACILITY_ADMIN_ROLE],
    )
    can_manage_devices = Permission(
        "Gestionar dispositivos del establecimiento",
        "",
        PermissionContext.FACILITY,
        [STAFF_ROLE, ADMIN_ROLE, FACILITY_ADMIN_ROLE, PHARMACIST_ROLE],
    )
