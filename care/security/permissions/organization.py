import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    ADMINISTRATOR,
    DOCTOR_ROLE,
    FACILITY_ADMIN_ROLE,
    NURSE_ROLE,
    PHARMACIST_ROLE,
    ROLE_ORGANIZATION_ADMIN_ROLE,
    ROLE_ORGANIZATION_MANAGER_ROLE,
    ROLE_ORGANIZATION_MEMBER_ROLE,
    STAFF_ROLE,
    VOLUNTEER_ROLE,
)


class OrganizationPermissions(enum.Enum):
    can_view_organization = Permission(
        "Ver organizaciones",
        "",
        PermissionContext.ORGANIZATION,
        [
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            ADMINISTRATOR,
            NURSE_ROLE,
            VOLUNTEER_ROLE,
            PHARMACIST_ROLE,
            ROLE_ORGANIZATION_ADMIN_ROLE,
            ROLE_ORGANIZATION_MANAGER_ROLE,
            ROLE_ORGANIZATION_MEMBER_ROLE,
        ],
    )
    can_create_organization = Permission(
        "Crear organizaciones",
        "",
        PermissionContext.ORGANIZATION,
        [ADMIN_ROLE],
    )
    can_delete_organization = Permission(
        "Eliminar organizaciones",
        "",
        PermissionContext.ORGANIZATION,
        [ADMIN_ROLE],
    )
    can_manage_organization = Permission(
        "Gestionar organizaciones",
        "Esto incluye cambiar nombres, descripciones, metadatos, etc.",
        PermissionContext.ORGANIZATION,
        [ADMIN_ROLE, ROLE_ORGANIZATION_ADMIN_ROLE],
    )
    can_manage_organization_users = Permission(
        "Gestionar usuarios de una organización",
        "Agregar, quitar y asignar roles a usuarios en una organización",
        PermissionContext.ORGANIZATION,
        [ADMIN_ROLE, ADMINISTRATOR, FACILITY_ADMIN_ROLE, ROLE_ORGANIZATION_ADMIN_ROLE],
    )
    can_manage_connected_role_organizations = Permission(
        "Gestionar organizaciones de roles conectadas",
        "Agregar, quitar y asignar roles a usuarios en organizaciones de roles conectadas",
        PermissionContext.ORGANIZATION,
        [ROLE_ORGANIZATION_ADMIN_ROLE, ROLE_ORGANIZATION_MANAGER_ROLE],
    )
    can_list_organization_users = Permission(
        "Listar usuarios de una organización",
        "",
        PermissionContext.ORGANIZATION,
        [
            FACILITY_ADMIN_ROLE,
            ADMIN_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            ADMINISTRATOR,
            NURSE_ROLE,
            VOLUNTEER_ROLE,
            PHARMACIST_ROLE,
            ROLE_ORGANIZATION_ADMIN_ROLE,
            ROLE_ORGANIZATION_MANAGER_ROLE,
        ],
    )
    is_geo_admin = Permission(
        "Administrador geográfico",
        "Los administradores geográficos pueden gestionar establecimientos en su organización",
        PermissionContext.ORGANIZATION,
        [],
    )
