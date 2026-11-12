from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models
from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _

from care.emr.models import FacilityOrganization
from care.emr.models.organization import FacilityOrganizationUser
from care.facility.models.facility_flag import FacilityFlag
from care.security.models import RoleModel
from care.security.roles.role import FACILITY_ADMIN_ROLE
from care.utils.models.base import BaseModel
from care.utils.models.choices import reverse_choices
from care.utils.models.validators import mobile_or_landline_number_validator

User = get_user_model()

class HubRelationship(IntegerChoices):
    REGULAR_HUB = 1, _("Regular Hub")
    TELE_ICU_HUB = 2, _("Tele ICU Hub")


class FacilityFeature(models.IntegerChoices):
    CT_SCAN_FACILITY = 1, "CT Scan Facility"
    MATERNITY_CARE = 2, "Maternity Care"
    X_RAY_FACILITY = 3, "X-Ray Facility"
    NEONATAL_CARE = 4, "Neonatal Care"
    OPERATION_THEATER = 5, "Operation Theater"
    BLOOD_BANK = 6, "Blood Bank"

FACILITY_TYPES = [
    # Venezuelan health infrastructure (MPPS red asistencial).
    # Integer values are internal identifiers only. Value 2 is held by
    # existing rows, so it is preserved; the labels are what the API and
    # the UI expose.
    (1, "Instituto de Educación Médica"),
    (2, "Hospital Privado"),
    (3, "Otro"),
    (4, "Consulta / Consultorio"),
    (5, "Clínica Privada"),
    (6, "Hospital Penitenciario"),
    (7, "TeleMedicina"),
    (9, "Laboratorio Público"),
    (10, "Laboratorio Privado"),
    # Use 8xx for public ambulatory and first-level care
    (800, "Ambulatorio Rural"),
    (802, "Centro de Salud Sexual y Reproductiva"),
    (803, "Ambulatorio Urbano"),
    (830, "Hospital Municipal"),
    (840, "Casa de la Mujer"),
    (860, "Hospital Regional"),
    (870, "Hospital Universitario"),
    (900, "Hospital General"),
    (910, "Instituto Autónomo Hospitalario"),
    # Use 1xxx for specialised and second/third level care
    (1010, "Centro de Diagnóstico Integral (CDI)"),
    (1100, "Hospital de Especialidades"),
    (1200, "Hospital Pediátrico"),
    (1300, "Hospital Gineco-Obstétrico"),
    (1400, "Hospital Mental"),
    (1500, "Centro de Rehabilitación Integral (CRI)"),
    (1510, "Policlílico"),
    (1600, "Hospital Militar"),
    # Use 3xxx/4xxx for non-governmental and community organisations
    (3000, "Organización No Gubernamental Clínica"),
    (3001, "Organización No Gubernamental No Clínica"),
    (4000, "Organización Comunitaria"),
]

REVERSE_FACILITY_TYPES = reverse_choices(FACILITY_TYPES)
REVERSE_REVERSE_FACILITY_TYPES = {v: k for k, v in REVERSE_FACILITY_TYPES.items()}

DOCTOR_TYPES = [
    (1, "Medicina General"),
    (2, "Neumonología"),
    (3, "Medicina Intensiva"),
    (4, "Pediatría"),
    (5, "Otros"),
    (6, "Anestesiología"),
    (7, "Cirugía Cardíaca"),
    (8, "Cardiología"),
    (9, "Odontología"),
    (10, "Dermatología"),
    (11, "Diabetología"),
    (12, "Medicina de Emergencias"),
    (13, "Endocrinología"),
    (14, "Medicina Familiar"),
    (15, "Gastroenterología"),
    (16, "Cirugía General"),
    (17, "Geriatría"),
    (18, "Hematología"),
    (19, "Inmunología"),
    (20, "Enfermedades Infecciosas"),
    (21, "Médico licenciado"),
    (22, "Oficial Médico"),
    (23, "Nefrología"),
    (24, "Neurocirugía"),
    (25, "Neurología"),
    (26, "Obstetricia y Ginecología"),
    (27, "Oncología"),
    (28, "Cirugía Oncológica"),
    (29, "Oftalmología"),
    (30, "Cirugía Oral y Maxilofacial"),
    (31, "Traumatología"),
    (32, "Cirugía Ortopédica"),
    (33, "Otorrinolaringología (ENT)"),
    (34, "Medicina Paliativa"),
    (35, "Patología"),
    (36, "Cirugía Pediátrica"),
    (37, "Médico"),
    (38, "Cirugía Plástica"),
    (39, "Psiquiatría"),
    (40, "Neumología"),
    (41, "Técnico en Radiología"),
    (42, "Radiología"),
    (43, "Reumatología"),
    (44, "Medicina Deportiva"),
    (45, "Cirugía Toracovascular"),
    (46, "Medicina de Transfusión"),
    (47, "Urología"),
    (48, "Enfermería"),
    (49, "Alergología e Inmunología"),
    (50, "Cirugía Cardiothorácica"),
    (51, "Oncología Ginecológica"),
    (52, "Hepatología"),
    (53, "Medicina Interna"),
    (54, "Neonatología"),
    (55, "Medicina del Dolor"),
    (56, "Medicina Física y Rehabilitación"),
    (57, "Podología"),
    (58, "Medicina Preventiva"),
    (59, "Oncología Radioterápica"),
    (60, "Medicina del Sueño"),
    (61, "Cirugía de Trasplantes"),
    (62, "Cirugía de Trauma"),
    (63, "Cirugía Vascular"),
    (64, "Medicina Crítica"),
]



class Facility(BaseModel):
    name = models.CharField(max_length=1000, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    facility_type = models.IntegerField(choices=FACILITY_TYPES)
    features = ArrayField(
        models.SmallIntegerField(choices=FacilityFeature),
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True
    )
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True
    )
    pincode = models.IntegerField(default=None, null=True)
    address = models.TextField()

    geo_organization = models.ForeignKey(
        "emr.Organization", on_delete=models.SET_NULL, null=True, blank=True
    )
    geo_organization_cache = ArrayField(models.IntegerField(), default=list)

    default_internal_organization = models.ForeignKey(
        "emr.FacilityOrganization",
        on_delete=models.SET_NULL,
        related_name="default_facilities",
        null=True,
        blank=True,
    )
    internal_organization_cache = ArrayField(models.IntegerField(), default=list)

    phone_number = models.CharField(
        max_length=14, blank=True, validators=[mobile_or_landline_number_validator]
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    cover_image_url = models.CharField(
        blank=True, null=True, default=None, max_length=500
    )
    middleware_address = models.CharField(null=True, default=None, max_length=200)

    is_public = models.BooleanField(default=False)

    print_templates = models.JSONField(default=list)

    extensions = models.JSONField(default=dict)

    class Meta:
        verbose_name_plural = "Facilities"


    def read_cover_image_url(self):
        if self.cover_image_url:
            if settings.FACILITY_CDN:
                return f"{settings.FACILITY_CDN}/{self.cover_image_url}"
            return f"{settings.FACILITY_S3_BUCKET_EXTERNAL_ENDPOINT}/{settings.FACILITY_S3_BUCKET}/{self.cover_image_url}"
        return None

    def __str__(self):
        return f"{self.name}"

    def sync_cache(self):
        self.geo_organization_cache = []
        if self.geo_organization:
            self.geo_organization_cache = [
                *self.geo_organization.parent_cache,
                self.geo_organization.id,
            ]

        facility_organizations = FacilityOrganization.objects.filter(facility=self)
        cache = []
        for facility_organization in facility_organizations:
            cache = [
                *cache,
                *facility_organization.parent_cache,
                facility_organization.id,
            ]
        cache = list(set(cache))
        self.internal_organization_cache = cache
        super().save(
            update_fields=["geo_organization_cache", "internal_organization_cache"]
        )

    def save(self, *args, **kwargs) -> None:
        is_create = self.pk is None
        super().save(*args, **kwargs)

        if is_create:
            facility_organization = FacilityOrganization.objects.create(
                org_type="root",
                name="Administración",
                system_generated=True,
                facility=self,
            )
            self.default_internal_organization = facility_organization
            super().save(update_fields=["default_internal_organization"])
            FacilityOrganizationUser.objects.create(
                organization=facility_organization,
                user=self.created_by,
                role=RoleModel.objects.get_or_create(name=FACILITY_ADMIN_ROLE.name)[0],
            )
        self.sync_cache()

    def get_facility_flags(self):
        return FacilityFlag.get_all_flags(self.id)
