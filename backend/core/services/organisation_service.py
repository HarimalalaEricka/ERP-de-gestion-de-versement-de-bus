import uuid

from core.models import Organisation


def get_by_id(organisation_id: uuid.UUID | str) -> Organisation | None:
    try:
        return Organisation.objects.get(id=organisation_id)
    except (Organisation.DoesNotExist, ValueError):
        return None