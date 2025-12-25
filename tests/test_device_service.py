from services.device_service import DeviceService
from schemas.device_schema import DeviceBase


def test_register_device(mocker):
    service = DeviceService()
    service.device_repo.insert_one = mocker.Mock()

    device = DeviceBase(
        device_id="GATE_1",
        location_name="Main Gate"
    )

    service.register_device(device)

    service.device_repo.insert_one.assert_called_once()
