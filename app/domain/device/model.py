from typing import Optional
from sqlmodel import Field
from app.shared.base_domain.model import BaseTable
from app.shared.enums import DeviceStatus


class Device(BaseTable, table=True):
    __tablename__ = "devices"

    name: str = Field(max_length=100, nullable=False)
    serial_number: str = Field(max_length=100, unique=True, nullable=False, index=True)
    status: DeviceStatus = Field(default=DeviceStatus.OFF, nullable=False)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    config: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)
