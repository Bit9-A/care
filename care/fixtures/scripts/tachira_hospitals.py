"""Seed: red asistencial del estado Táchira, Venezuela.

Crea la jerarquía geográfica Venezuela → Táchira → municipio, un
hospital por municipio (Fundahosta en Tariba, cabecera de la red) y
una cartera de pacientes de demostración por establecimiento.

Ejecutar con:

    python manage.py load_fixtures --path care/fixtures/scripts/tachira_hospitals.py

Los datos geográficos (coordenadas y códigos postales) son
aproximados y sirven para desarrollo; sustitúyelos por los valores
oficiales antes de cualquier uso real.
"""

from care.emr.resources.organization.spec import OrganizationTypeChoices
from care.fixtures.context import care_fixture_context

GOVT = OrganizationTypeChoices.govt.value

# municipality -> (postal code, latitude, longitude)
MUNICIPALITIES = {
    "Tariba": ("5205", 7.6364, -72.2297),
    "San Cristóbal": ("5001", 7.7669, -72.2250),
    "Rubio": ("5060", 7.4975, -72.3517),
    "Delicias": ("5062", 7.5644, -72.3567),
    "Lobatera": ("5054", 7.7667, -72.3500),
    "Michelena": ("5070", 7.7167, -72.2000),
    "Ureña": ("5050", 7.5167, -72.4500),
    "San Juan de Colón": ("5070", 7.9167, -72.2833),
}

# municipality -> list of (name, facility_type, street address, phone)
HOSPITALS = {
    "Tariba": [
        ("Fundahosta", "Hospital Regional", "Calle 5, Sector Centro, Tariba", "+584141234567"),
        ("Ambulatorio Urbano Tariba", "Ambulatorio Urbano", "Av. Principal, Tariba", "+584142234567"),
    ],
    "San Cristóbal": [
        ("Hospital Central de San Cristóbal", "Hospital Universitario", "Av. Libertador, Sector Urdaneta, San Cristóbal", "+584143234567"),
        ("Hospital Pediátrico de San Cristóbal", "Hospital Pediátrico", "Calle 6 con Av. 3, San Cristóbal", "+584144234567"),
    ],
    "Rubio": [
        ("Hospital General de Rubio", "Hospital General", "Calle Bolívar, Rubio", "+584145234567"),
    ],
    "Delicias": [
        ("Hospital de Delicias", "Hospital Municipal", "Av. 23 de Enero, Delicias", "+584146234567"),
    ],
    "Lobatera": [
        ("Hospital de Lobatera", "Hospital Municipal", "Calle Miranda, Lobatera", "+584147234567"),
    ],
    "Michelena": [
        ("Ambulatorio Urbano Michelena", "Ambulatorio Urbano", "Av. Principal, Michelena", "+584148234567"),
    ],
    "Ureña": [
        ("Hospital de Ureña", "Hospital Municipal", "Calle Comercio, Ureña", "+584149234567"),
    ],
    "San Juan de Colón": [
        ("Hospital de San Juan de Colón", "Hospital Municipal", "Calle Bolívar, San Juan de Colón", "+584140234567"),
    ],
}

PATIENTS_PER_FACILITY = 3


def log(message):
    print(message)  # noqa: T201


def load_tachira(base):
    venezuela = base.create_organization(org_type=GOVT, name="Venezuela")
    log("Organización Venezuela creada")

    tachira = base.create_organization(
        org_type=GOVT, parent=venezuela.id, name="Táchira"
    )
    log("Organización Táchira creada")

    total_facilities = 0
    total_patients = 0

    for municipality, (pincode, latitude, longitude) in MUNICIPALITIES.items():
        geo = base.create_organization(
            org_type=GOVT, parent=tachira.id, name=municipality
        )

        for name, facility_type, address, phone in HOSPITALS[municipality]:
            facility = base.create_facility(
                geo.id,
                name=name,
                facility_type=facility_type,
                address=f"{address}, {municipality}, Táchira, Venezuela",
                pincode=pincode,
                phone_number=phone,
                latitude=latitude,
                longitude=longitude,
                is_public=True,
                description=f"Establecimiento de salud del municipio {municipality}, estado Táchira.",
            )
            total_facilities += 1
            log(f"  Hospital creado: {name} ({facility_type})")

            for index in range(PATIENTS_PER_FACILITY):
                base.create_patient(
                    geo.id,
                    address=f"{address}, {municipality}, Táchira",
                    pincode=pincode,
                )
                total_patients += 1

    log(
        f"Seed de Táchira completado: {len(MUNICIPALITIES)} municipios, "
        f"{total_facilities} establecimientos, {total_patients} pacientes"
    )


if __name__ == "__main__":
    with care_fixture_context() as base:
        load_tachira(base)
