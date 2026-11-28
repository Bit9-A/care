"""Seed: los 25 ASIC del estado Táchira como organizaciones govt bajo Táchira.

Crea (idempotentemente) los nodos ASIC como hijos directos de Táchira, a
partir del listado oficial del MPPS para el estado. Si Táchira no existe,
crea primero la cadena Venezuela → Táchira.

Uso:
    python manage.py load_fixtures --path care/fixtures/scripts/tachira_asics.py
"""

from care.emr.models.organization import Organization
from care.fixtures.context import care_fixture_context

GOVT = "govt"

# (nombre, descripción) — ASIC del Estado Táchira, total: 25
ASICS = [
    ("ASIC Fernández Feo", "Municipio Fernández Feo"),
    ("ASIC Panamericano", "Municipios Panamericano y San Judas Tadeo"),
    ("ASIC Hugo Murzi", "Municipio San Cristóbal (sector norte)"),
    ("ASIC Cárdenas", "Municipio Cárdenas"),
    ("ASIC Libertad", "Municipio Libertad"),
    ("ASIC Torbes", "Municipio Torbes"),
    ("ASIC Uribante", "Municipio Uribante"),
    (
        "ASIC Antonio Rómulo Costa",
        "Municipios Antonio Rómulo Costa y Seboruco",
    ),
    ("ASIC Guásimos", "Municipio Guásimos"),
    ("ASIC García de Hevia", "Municipio García de Hevia"),
    ("ASIC Sucre", "Municipios Sucre y Francisco de Miranda"),
    ("ASIC Andrés Bello", "Municipio Andrés Bello"),
    ("ASIC Independencia", "Municipio Independencia (Capacho Nuevo)"),
    ("ASIC Michelena", "Municipios Michelena y Lobatera"),
    ("ASIC Ayacucho", "Municipio Ayacucho"),
    ("ASIC Libertador", "Municipio Libertador (Abejales)"),
    ("ASIC Córdoba", "Municipio Córdoba (Santa Ana del Táchira)"),
    ("ASIC Sabaneta", "Municipio San Cristóbal (sector sur)"),
    ("ASIC José María Vargas", "Municipio San Cristóbal (sector oeste)"),
    ("ASIC Ureña", "Municipio Pedro María Ureña"),
    ("ASIC Junín", "Municipios Junín y Rafael Urdaneta"),
    ("ASIC Jacinto Convit", "Municipio San Cristóbal (sector este)"),
    ("ASIC Jáuregui", "Municipios Jáuregui y José María Vargas"),
    (
        "ASIC Samuel Darío Maldonado",
        "Municipios Samuel Darío Maldonado y Simón Rodríguez",
    ),
    ("ASIC Bolívar", "Municipio Bolívar (San Antonio del Táchira)"),
]


def log(message):
    print(message)  # noqa: T201


def ensure_govt_chain(base):
    tachira = Organization.objects.filter(
        org_type=GOVT, name="Táchira", parent__name="Venezuela"
    ).first()
    if tachira:
        return tachira

    venezuela = Organization.objects.filter(
        org_type=GOVT, name="Venezuela", parent__isnull=True
    ).first()
    if not venezuela:
        venezuela = base.create_organization(org_type=GOVT, name="Venezuela")
        log("Organización Venezuela creada")
        venezuela = Organization.objects.get(
            org_type=GOVT, name="Venezuela", parent__isnull=True
        )

    tachira = base.create_organization(
        org_type=GOVT, parent=venezuela.external_id, name="Táchira"
    )
    log("Organización Táchira creada")
    return Organization.objects.get(
        org_type=GOVT, name="Táchira", parent=venezuela
    )


def load_tachira_asics(base):
    tachira = ensure_govt_chain(base)
    created = 0
    skipped = 0

    for name, description in ASICS:
        if Organization.objects.filter(
            org_type=GOVT, name=name, parent=tachira
        ).exists():
            skipped += 1
            continue
        base.create_organization(
            org_type=GOVT,
            parent=tachira.external_id,
            name=name,
            description=description,
        )
        created += 1
        log(f"  ASIC creado: {name}")

    log(f"Seed ASIC Táchira completado: {created} creados, {skipped} ya existían")


if __name__ == "__main__":
    with care_fixture_context() as base:
        load_tachira_asics(base)
