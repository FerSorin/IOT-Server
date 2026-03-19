from app.shared.base_domain.controller import FullCrudApiController
from app.domain.device.schemas import DeviceCreate, DeviceResponse, DeviceUpdate
from app.domain.device.service import DeviceServiceDep


class DeviceController(FullCrudApiController):
    prefix = "/devices"
    tags = ["Devices"]
    service_dep = DeviceServiceDep
    response_schema = DeviceResponse
    create_schema = DeviceCreate
    update_schema = DeviceUpdate


router = DeviceController().router


@router.get("/searchBySerial/{serial_number}", response_model=DeviceResponse)
def get_device_by_serial(serial_number: str, service: DeviceServiceDep):
    print(f"get_device_by_serial: {serial_number}")
    return service.get_by_serial(serial_number)
