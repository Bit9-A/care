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


class PatientPermissions(enum.Enum):
    can_create_patient = Permission(
        "Crear paciente",
        "",
        PermissionContext.PATIENT,
        [
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
            ADMIN_ROLE,
            FACILITY_ADMIN_ROLE,
        ],
    )
    can_write_patient = Permission(
        "Actualizar datos del paciente",
        "",
        PermissionContext.PATIENT,
        [
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
            ADMIN_ROLE,
            FACILITY_ADMIN_ROLE,
        ],
    )
    can_list_patients = Permission(
        "Listar pacientes",
        "",
        PermissionContext.PATIENT,
        [
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMINISTRATOR,
            ADMIN_ROLE,
            FACILITY_ADMIN_ROLE,
            VOLUNTEER_ROLE,
            PHARMACIST_ROLE,
        ],
    )
    can_view_clinical_data = Permission(
        "Ver datos clínicos de pacientes",
        "",
        PermissionContext.PATIENT,
        [STAFF_ROLE, DOCTOR_ROLE, NURSE_ROLE, ADMIN_ROLE, FACILITY_ADMIN_ROLE],
    )  # To be split into finer grain permissions
    can_view_questionnaire_responses = Permission(
        "Ver respuestas de cuestionario del paciente",
        "",
        PermissionContext.PATIENT,
        [
            VOLUNTEER_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMIN_ROLE,
            FACILITY_ADMIN_ROLE,
            ADMINISTRATOR,
            PHARMACIST_ROLE,
        ],
    )
    can_submit_patient_questionnaire = Permission(
        "Enviar cuestionario sobre pacientes",
        "",
        PermissionContext.PATIENT,
        [
            VOLUNTEER_ROLE,
            STAFF_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            ADMIN_ROLE,
            FACILITY_ADMIN_ROLE,
            ADMINISTRATOR,
        ],
    )
