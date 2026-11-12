import enum
from dataclasses import dataclass, field


class RoleContext(enum.Enum):
    FACILITY = "FACILITY"
    GOVT_ORG = "GOVT_ORG"
    ROLE_ORG = "ROLE_ORG"


@dataclass
class Role:
    """
    This class can be inherited for role classes that are created by default
    """

    name: str
    description: str
    contexts: list[RoleContext] = field(default_factory=list)


VOLUNTEER_ROLE = Role(
    name="Voluntario",
    description="Voluntario en un establecimiento",
    contexts=[RoleContext.FACILITY, RoleContext.GOVT_ORG],
)
DOCTOR_ROLE = Role(
    name="Médico",
    description="Médico en un establecimiento",
    contexts=[RoleContext.FACILITY, RoleContext.GOVT_ORG],
)
NURSE_ROLE = Role(
    name="Enfermero",
    description="Enfermero en un establecimiento",
    contexts=[RoleContext.FACILITY, RoleContext.GOVT_ORG],
)
STAFF_ROLE = Role(
    name="Personal",
    description="Personal de un establecimiento",
    contexts=[RoleContext.FACILITY, RoleContext.GOVT_ORG],
)
PHARMACIST_ROLE = Role(
    name="Farmacéutico",
    description="Farmacéutico en un establecimiento",
    contexts=[RoleContext.FACILITY],
)
ADMINISTRATOR = Role(
    name="Administrador general",
    description="Administrador de un ámbito determinado",
    contexts=[RoleContext.FACILITY, RoleContext.GOVT_ORG],
)
FACILITY_ADMIN_ROLE = Role(
    name="Administrador de Establecimiento",
    description="Administrador de un establecimiento, asociado a la persona que lo crea.",
    contexts=[RoleContext.FACILITY],
)
ADMIN_ROLE = Role(
    name="Administrador",
    description="Administrador",
    contexts=[RoleContext.FACILITY, RoleContext.GOVT_ORG],
)

ROLE_ORGANIZATION_ADMIN_ROLE = Role(
    name="Administrador",
    description="Administrador de una organización de responsabilidad",
    contexts=[RoleContext.ROLE_ORG],
)
ROLE_ORGANIZATION_MANAGER_ROLE = Role(
    name="Gestor",
    description="Gestor de una organización de responsabilidad",
    contexts=[RoleContext.ROLE_ORG],
)
ROLE_ORGANIZATION_MEMBER_ROLE = Role(
    name="Miembro",
    description="Miembro de una organización de responsabilidad",
    contexts=[RoleContext.ROLE_ORG],
)


class RoleController:
    override_roles = []
    # Override Permission Controllers will be defined from plugs
    internal_roles = [
        DOCTOR_ROLE,
        STAFF_ROLE,
        NURSE_ROLE,
        ADMINISTRATOR,
        FACILITY_ADMIN_ROLE,
        ADMIN_ROLE,
        VOLUNTEER_ROLE,
        PHARMACIST_ROLE,
        ROLE_ORGANIZATION_ADMIN_ROLE,
        ROLE_ORGANIZATION_MANAGER_ROLE,
        ROLE_ORGANIZATION_MEMBER_ROLE,
    ]

    @classmethod
    def get_roles(cls):
        return cls.internal_roles + cls.override_roles

    @classmethod
    def map_old_role_to_new(cls, old_role):
        mapping = {
            "Transportation": STAFF_ROLE,
            "Pharmacist": STAFF_ROLE,
            "Volunteer": STAFF_ROLE,
            "StaffReadOnly": STAFF_ROLE,
            "Staff": STAFF_ROLE,
            "NurseReadOnly": NURSE_ROLE,
            "Nurse": NURSE_ROLE,
            "Doctor": DOCTOR_ROLE,
            "Reserved": DOCTOR_ROLE,
            "WardAdmin": ADMINISTRATOR,
            "LocalBodyAdmin": ADMINISTRATOR,
            "DistrictLabAdmin": ADMINISTRATOR,
            "DistrictReadOnlyAdmin": ADMINISTRATOR,
            "DistrictAdmin": ADMINISTRATOR,
            "StateLabAdmin": ADMINISTRATOR,
            "StateReadOnlyAdmin": ADMINISTRATOR,
            "StateAdmin": ADMINISTRATOR,
        }
        return mapping[old_role]

    @classmethod
    def register_role(cls, role: Role):
        # TODO : Do some deduplication Logic
        cls.override_roles.append(role)
