from sqlmodel import SQLModel, Field
import datetime
from typing import Optional
from pydantic import condecimal, validator


class EventBase(SQLModel):
    event_date: datetime.date
    views: Optional[int] = Field(default=0)
    clicks: Optional[int] = Field(default=0)
    cost: Optional[condecimal(max_digits=11, decimal_places=2)] = Field(default=0)

    @validator('clicks')
    def check_clicks(cls, v, values):
        if v > values["views"]:
            raise ValueError('clicks can not be less than views')
        return v


class Event(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int


class ListEvents(EventRead):
    cpc: condecimal(max_digits=11, decimal_places=2)
    cpm: condecimal(max_digits=11, decimal_places=2)