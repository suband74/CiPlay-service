import datetime
from fastapi import Depends, FastAPI
from sqlalchemy import select, delete, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from .settings import get_session
from .models import Event, EventCreate, EventRead

app = FastAPI()

@app.get("/events")
async def get_events(
    from_date: datetime.date,
    to_date: datetime.date,
    order_field: str,
    session: AsyncSession = Depends(get_session),
):
    dct = {
        "clicks": func.sum(Event.clicks),
        "views": func.sum(Event.views),
        "cost": func.sum(Event.cost),
        "date": Event.event_date,
    }
    x = await session.execute(select(Event))
    if x.all():
        result = await session.execute(
            select(
                Event.event_date,
                func.sum(Event.clicks).label("s_clicks"),
                func.sum(Event.views).label("s_views"),
                func.sum(Event.cost).label("s_cost"),
                case(
                    (
                        func.sum(Event.clicks) > 0,
                        func.sum(Event.cost) / func.sum(Event.clicks),
                    ),
                    else_=0,
                ).label("price_clicks"),
                case(
                    (
                        func.sum(Event.views) > 0,
                        func.sum(Event.cost) / func.sum(Event.views),
                    ),
                    else_=0,
                ).label("price_views"),
            )
            .where(Event.event_date <= to_date, Event.event_date >= from_date)
            .group_by(Event.event_date)
            .order_by(dct[order_field])
        )
        events = result.all()
        rspns = [
            {
                "event_date": event.event_date,
                "s_clicks": event.s_clicks,
                "s_views": event.s_views,
                "s_cost": event.s_cost,
                "price_clicks": round(event.price_clicks, 2),
                "price_views": round(event.price_views, 2),
            }
            for event in events
        ]
        return rspns
    return []


@app.post("/event", response_model=EventRead)
async def add_event(event: EventCreate, session: AsyncSession = Depends(get_session)):
    event = Event.from_orm(event)
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


@app.delete("/events")
async def delete_events(session: AsyncSession = Depends(get_session)):
    await session.execute(delete(Event))
    await session.commit()
    return {"Deleted": "All events"}
