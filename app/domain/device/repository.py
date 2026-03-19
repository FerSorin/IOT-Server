from abc import ABC, abstractmethod
from app.shared.base_domain.repository import IBaseRepository
from app.domain.device.model import Device
from sqlmodel import Session, select, func
from app.shared.base_domain.repository import BaseRepository


class IDeviceRepository(IBaseRepository[Device], ABC):
    @abstractmethod
    def get_by_serial(self, serial_number: str) -> Device | None:
        raise NotImplementedError

    @abstractmethod
    def get_active(self, offset: int = 0, limit: int = 20) -> tuple[list[Device], int]:
        raise NotImplementedError


class DeviceRepository(BaseRepository[Device], IDeviceRepository):
    model = Device

    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_serial(self, serial_number: str) -> Device | None:
        return self.session.exec(
            select(Device).where(Device.serial_number == serial_number)
        ).first()

    def get_active(self, offset: int = 0, limit: int = 20) -> tuple[list[Device], int]:

        query = select(Device).where(Device.is_active)

        items = self.session.exec(query.offset(offset).limit(limit)).all()

        total = self.session.exec(
            select(func.count()).select_from(Device).where(Device.is_active)
        ).one()

        return list(items), total
