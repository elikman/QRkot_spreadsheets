from datetime import datetime

from app.models import BaseFields


def investing_process(
        target: BaseFields,
        sources: list[BaseFields],
) -> list[BaseFields]:
    changed = []
    for source in sources:
        amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (source, target):
            obj.invested_amount += amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
        changed.append(source)
        if target.fully_invested:
            break
    return changed
