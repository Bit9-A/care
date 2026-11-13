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
)


class FacilityLocationPermissions(enum.Enum):
    can_list_facility_locations = Permission(
        "Listar ubicaciones del establecimiento",
        "",
        PermissionContext.FACILITY,
        [
            ADMIN_ROLE,
            DOCTOR_ROLE,
            FACILITY_ADMIN_ROLE,
            ADMINISTRATOR,
            NURSE_ROLE,
            STAFF_ROLE,
            PHARMACIST_ROLE,
        ],
    )
    can_write_facility_locations = Permission(
        "Crear o actualizar ubicaciones del establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE, STAFF_ROLE],
    )
    can_list_facility_location_organizations = Permission(
        "Listar organizaciones de ubicaciones del establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE, STAFF_ROLE],
    )
    can_create_facility_location_organizations = Permission(
        "Crear o actualizar organizaciones de ubicaciones del establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE, STAFF_ROLE],
    )
