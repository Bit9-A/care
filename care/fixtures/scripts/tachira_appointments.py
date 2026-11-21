"""Seed: casos reales de citas y sala de espera en Fundahosta (Tariba).

Crea un profesional de la salud, la programación de consulta del día,
la cola con sus sub-colas y categorías, y un conjunto de citas de hoy
con sus turnos en distintos estados para poder ver la sala de espera
y la atención de citas funcionando:

    FULFILLED   → ya atendidos
    IN_PROGRESS → en atención ahora
    creado      → esperando en sala de espera

Ejecutar con:

    python manage.py load_fixtures --path care/fixtures/scripts/tachira_appointments.py
"""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from care.emr.models.organization import Organization
from care.facility.models import Facility
from care.fixtures.constants import DEFAULT_AVAILABILITY
from care.fixtures.context import care_fixture_context

PASSWORD = "Ohcn@123"

PRACTITIONER = {
    "username": "dra_rondon",
    "email": "dra.rondon@fundahosta.gob.ve",
    "first_name": "María Fernanda",
    "last_name": "Rondón",
}

PATIENTS = [
    ("Yonathan", "Briceño", "V-27.123.456", "1987-04-12"),
    ("Andreína", "Quintero", "V-26.987.111", "1993-09-03"),
    ("Luis Alejandro", "Márquez", "V-25.445.678", "1978-01-27"),
    ("Karla Virginia", "Sequera", "V-28.332.900", "2001-06-15"),
    ("José Gregorio", "Pernía", "V-24.110.774", "1969-11-08"),
    ("Daliana", "Rincón", "V-27.884.201", "1996-02-19"),
    ("Elías", "Tovar", "V-26.550.013", "1983-07-30"),
    ("Mireya", "Carrillo", "V-28.771.640", "1990-12-05"),
]

# Cantidad de turnos en cada estado, en el orden en que se crean los
# pacientes. El resto queda esperando en sala de espera.
PLAN_ESTADOS = [
    ("FULFILLED", "Atendido: control de hipertensión arterial"),
    ("FULFILLED", "Atendido: consulta de medicina general"),
    ("FULFILLED", "Atendido: revisión de receta"),
    ("IN_PROGRESS", "En atención: primera consulta"),
    ("CREATED", "Esperando: derivación desde ambulatorio"),
    ("CREATED", "Esperando: control programado"),
    ("CREATED", "Esperando: consulta nueva"),
    ("CREATED", "Esperando: resultado de laboratorio"),
]


def log(message):
    print(message)  # noqa: T201


def _reverse(viewname, **kwargs):
    return reverse(viewname, kwargs=kwargs)


def load_tachira_appointments(base):
    facility = Facility.objects.get(name="Fundahosta")
    facility_id = facility.external_id
    tariba = Organization.objects.get(name="Tariba", org_type="govt")
    geo_id = tariba.external_id

    log(f"Caso base: {facility.name} ({facility.address or 'Tariba'})")

    roles = base.get_roles()
    role_org = Organization.objects.get(org_type="role", name="Médico")
    department = next(
        (
            org
            for org in base.get_facility_organizations(facility_id)
            if org.name == "Administración"
        ),
        None,
    )

    # 1. Profesional de la salud (se crea solo si todavía no existe)
    try:
        practitioner = base.get_user(PRACTITIONER["username"])
        log("  Profesional ya existente: %s" % PRACTITIONER["username"])
    except Exception:
        practitioner = base.create_user(
            geo_id,
            role_orgs=[
                {
                    "organization": role_org.external_id,
                    "role": roles["Médico"].id,
                }
            ],
            password=PASSWORD,
            **PRACTITIONER,
        )
        log("  Profesional creado: %s" % PRACTITIONER["username"])

    if department and practitioner:
        base.add_user_to_facility_organization(
            facility_id,
            department.id,
            practitioner.id,
            roles["Médico"].id,
        )
        log("  Profesional vinculado a Administración")

    resource_id = practitioner.id

    # 2. Programación de consulta. El validador exige valid_from >= ahora
    #    en el instante exacto de la petición, así que se manda con margen
    #    para que el tiempo transcurrido durante el envío no lo rechace.
    now = timezone.now()
    valid_from = (now + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S")
    valid_to = (now + timedelta(days=14)).strftime("%Y-%m-%dT23:59:59")
    base.create_schedule(
        facility_id,
        resource_type="practitioner",
        resource_id=resource_id,
        name="Consulta de Medicina General",
        valid_from=valid_from,
        valid_to=valid_to,
        availabilities=[DEFAULT_AVAILABILITY],
    )
    log("  Programación de consulta creada (vigente desde ahora)")

    # 3. Día con turnos disponibles: hoy si quedan, si no mañana
    target_day = now.strftime("%Y-%m-%d")
    slots = base.get_slots_for_day(
        facility_id,
        resource_type="practitioner",
        resource_id=resource_id,
        day=target_day,
    ).get("results", [])
    if not slots:
        target_day = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        slots = base.get_slots_for_day(
            facility_id,
            resource_type="practitioner",
            resource_id=resource_id,
            day=target_day,
        ).get("results", [])
        log(f"  Sin turnos disponibles hoy → se trabaja sobre {target_day}")

    queue = base.create_token_queue(
        facility_id,
        resource_type="practitioner",
        resource_id=resource_id,
        name="Consulta General",
        date=target_day,
    )
    sala_espera = base.create_token_sub_queue(
        facility_id,
        resource_type="practitioner",
        resource_id=resource_id,
        name="Sala de espera",
    )
    consultorio = base.create_token_sub_queue(
        facility_id,
        resource_type="practitioner",
        resource_id=resource_id,
        name="Consultorio 1",
    )
    cat_general = base.create_token_category(
        facility_id,
        resource_type="practitioner",
        name="Consulta General",
        shorthand="GEN",
    )
    cat_urgencia = base.create_token_category(
        facility_id,
        resource_type="practitioner",
        name="Urgencia",
        shorthand="URG",
    )
    log(f"  Cola del {target_day}: sala de espera + consultorio 1")

    # 4. Pacientes
    patients = []
    for nombre, apellido, cedula, nacimiento in PATIENTS:
        patients.append(
            base.create_patient(
                geo_id,
                name=f"{nombre} {apellido}",
                date_of_birth=nacimiento,
                phone_number="+584141000001",
                address=f"Calle {apellido}, Tariba, Táchira",
            )
        )
    log(f"  {len(patients)} pacientes creados")

    # 5. Citas sobre los turnos encontrados
    if not slots:
        log("  AVISO: no hay turnos disponibles")
        return

    bookings = []
    for idx, patient in enumerate(patients[: len(slots)]):
        bookings.append(
            base.create_appointment(
                facility_id,
                slot_id=slots[idx].id,
                patient_id=patient.id,
                note=PLAN_ESTADOS[idx][1],
            )
        )
    log(f"  {len(bookings)} citas creadas para hoy")

    # 6. Turnos de cola, con estado según el plan
    queue_url = _reverse(
        "token-queue-detail",
        facility_external_id=facility_id,
        external_id=queue.id,
    )
    for idx, booking in enumerate(bookings):
        estado, nota = PLAN_ESTADOS[idx]
        categoria = cat_urgencia if idx == 3 else cat_general
        token = base.post(
            _reverse(
                "appointments-generate-token",
                facility_external_id=facility_id,
                external_id=booking.id,
            ),
            {
                "category": categoria.id,
                "note": nota,
                # Sin esto generate_token crea una cola "System Generated"
                # y el token termina fuera de la cola que estamos poblando.
                "queue": queue.id,
            },
        )
        sub_queue = consultorio if estado in (
            "FULFILLED",
            "IN_PROGRESS",
        ) else sala_espera
        base.patch(
            _reverse(
                "queue-detail",
                facility_external_id=facility_id,
                token_queue_external_id=queue.id,
                external_id=token.id,
            ),
            {
                "status": estado,
                "sub_queue": sub_queue.id,
                "note": nota,
            },
        )
        log(f"    N.º {token.number:<3} {estado:<12} {nota}")

    # 7. El siguiente en ser llamado
    en_atencion = next(
        (b for b, (estado, _) in zip(bookings, PLAN_ESTADOS) if estado == "IN_PROGRESS"),
        None,
    )
    if en_atencion and en_atencion.token:
        base.post(
            _reverse(
                "queue-set-next",
                facility_external_id=facility_id,
                token_queue_external_id=queue.id,
                external_id=en_atencion.token.id,
            ),
            {},
        )
        log("  Marcado como siguiente: N.º %s" % en_atencion.token.number)

    log(
        f"\nListo. {facility.name} — cola del {target_day}: "
        f"{sum(1 for e, _ in PLAN_ESTADOS if e == 'FULFILLED')} atendidos, "
        f"{sum(1 for e, _ in PLAN_ESTADOS if e == 'IN_PROGRESS')} en atención, "
        f"{sum(1 for e, _ in PLAN_ESTADOS if e == 'CREATED')} en espera"
    )


if __name__ == "__main__":
    with care_fixture_context() as base:
        load_tachira_appointments(base)
