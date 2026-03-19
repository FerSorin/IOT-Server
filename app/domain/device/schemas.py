from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.shared.enums import DeviceStatus


class DeviceCreate(BaseModel):
    name: str
    serial_number: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    config: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[DeviceStatus] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    config: Optional[str] = None
    is_active: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: UUID
    name: str
    serial_number: str
    status: DeviceStatus
    latitude: Optional[float]
    longitude: Optional[float]
    config: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
