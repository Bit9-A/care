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


class QuestionnairePermissions(enum.Enum):
    can_write_questionnaire = Permission(
        "Crear o actualizar cuestionarios",
        "",
        PermissionContext.QUESTIONNAIRE,
        [ADMIN_ROLE, FACILITY_ADMIN_ROLE],
    )
    can_archive_questionnaire = Permission(
        "Archivar cuestionarios",
        "",
        PermissionContext.QUESTIONNAIRE,
        [ADMIN_ROLE, FACILITY_ADMIN_ROLE],
    )
    can_read_questionnaire = Permission(
        "Ver cuestionarios",
        "",
        PermissionContext.QUESTIONNAIRE,
        [
            ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
            STAFF_ROLE,
            FACILITY_ADMIN_ROLE,
            VOLUNTEER_ROLE,
            PHARMACIST_ROLE,
            ROLE_ORGANIZATION_ADMIN_ROLE,
            ROLE_ORGANIZATION_MANAGER_ROLE,
            ROLE_ORGANIZATION_MEMBER_ROLE,
        ],
    )
    can_submit_questionnaire = Permission(
        "Enviar cuestionarios",
        "",
        PermissionContext.QUESTIONNAIRE,
        [
            ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
            STAFF_ROLE,
            FACILITY_ADMIN_ROLE,
            VOLUNTEER_ROLE,
            ROLE_ORGANIZATION_ADMIN_ROLE,
            ROLE_ORGANIZATION_MEMBER_ROLE,
            ROLE_ORGANIZATION_MANAGER_ROLE,
        ],
    )
    can_manage_questionnaire = Permission(
        "Gestionar cuestionarios",
        "Permite a los usuarios agregar o quitar organizaciones de los cuestionarios, es decir, controlar la gestión de acceso",
        PermissionContext.QUESTIONNAIRE,
        [ADMIN_ROLE, FACILITY_ADMIN_ROLE, ROLE_ORGANIZATION_ADMIN_ROLE],
    )
