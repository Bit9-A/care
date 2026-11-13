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


class FacilityOrganizationPermissions(enum.Enum):
    can_create_facility_organization = Permission(
        "Crear organizaciones del establecimiento",
        "",
        PermissionContext.FACILITY_ORGANIZATION,
        [FACILITY_ADMIN_ROLE],
    )
    can_create_facility_organization_root = Permission(
        "Crear raíz de organizaciones del establecimiento",
        "",
        PermissionContext.FACILITY_ORGANIZATION,
        [FACILITY_ADMIN_ROLE],
    )
    can_view_facility_organization = Permission(
        "Ver organizaciones del establecimiento",
        "",
        PermissionContext.FACILITY_ORGANIZATION,
        [
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            ADMINISTRATOR,
            NURSE_ROLE,
            VOLUNTEER_ROLE,
        ],
    )
    can_delete_facility_organization = Permission(
        "Eliminar organizaciones del establecimiento",
        "",
        PermissionContext.FACILITY_ORGANIZATION,
        [FACILITY_ADMIN_ROLE],
    )
    can_manage_facility_organization = Permission(
        "Gestionar organizaciones del establecimiento",
        "Esto incluye cambiar nombres, descripciones, metadatos, etc.",
        PermissionContext.FACILITY_ORGANIZATION,
        [FACILITY_ADMIN_ROLE, ADMINISTRATOR],
    )
    can_list_facility_organization_users = Permission(
        "Listar usuarios de organizaciones del establecimiento",
        "",
        PermissionContext.FACILITY_ORGANIZATION,
        [
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            ADMINISTRATOR,
            NURSE_ROLE,
        ],
    )
    can_manage_facility_organization_users = Permission(
        "Gestionar usuarios de una organización del establecimiento",
        "Agregar, quitar y asignar roles a usuarios en una organización del establecimiento",
        PermissionContext.FACILITY_ORGANIZATION,
        [FACILITY_ADMIN_ROLE, ADMINISTRATOR],
    )
