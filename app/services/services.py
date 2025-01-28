from datetime import datetime

from app.models import InvestmentBaseModel


def find_charity(
        target: InvestmentBaseModel,
        sources: list[InvestmentBaseModel]
) -> list[InvestmentBaseModel]:
    investment_sources = []
    for source in sources:
        remaining_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (source, target):
            obj.invested_amount += remaining_amount
            obj.fully_invested = obj.invested_amount == obj.full_amount
            if obj.fully_invested:
                obj.close_date = datetime.now()
        investment_sources.append(source)
        if target.fully_invested:
            break
    return investment_sources
