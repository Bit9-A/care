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


class ObservationDefinitionPermissions(enum.Enum):
    can_write_observation_definition = Permission(
        "Crear definición de observación en el establecimiento",
        "",
        PermissionContext.FACILITY,
        [FACILITY_ADMIN_ROLE, ADMIN_ROLE],
    )
    can_read_observation_definition = Permission(
        "Ver definición de observación",
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
