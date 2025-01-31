from datetime import datetime

from app.models.base import BaseCharityDonationModel


def distribute_investments(
    target: BaseCharityDonationModel,
    sources: list[BaseCharityDonationModel],
) -> list[BaseCharityDonationModel]:
    """Распределяет средства между проектами и обновляет их статусы.

    Args:
        target (BaseCharityDonationModel): Проект, на который направляются
        средства.
        sources (list[BaseCharityDonationModel]): Список проектов, из которых
        берутся средства.

    Returns:
        list[BaseCharityDonationModel]: Обновлённый список исходных проектов.
    """

    modified_sources = []

    for source in sources:
        transfer_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount,
        )

        for obj in [target, source]:
            obj.invested_amount += transfer_amount
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()

        modified_sources.append(source)

        if target.fully_invested:
            break

    return modified_sources
