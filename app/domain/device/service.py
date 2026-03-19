from abc import ABC, abstractmethod
from app.shared.base_domain.service import IBaseService
from app.domain.device.model import Device
from typing import Annotated
from fastapi import Depends
from app.shared.base_domain.service import BaseService
from app.domain.device.repository import DeviceRepository
from app.database import SessionDep


class IDeviceService(IBaseService[Device], ABC):
    @abstractmethod
    def get_by_serial(self, serial_number: str) -> Device | None:
        raise NotImplementedError


class DeviceService(BaseService[Device], IDeviceService):
    entity_name = "Dispositivo"
    repository_class = DeviceRepository

    def get_by_serial(self, serial_number: str) -> Device | None:
        return self.repository.get_by_serial(serial_number)


def get_device_service(session: SessionDep) -> DeviceService:
    return DeviceService(session)


DeviceServiceDep = Annotated[DeviceService, Depends(get_device_service)]
