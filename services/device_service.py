from repositories import DeviceRepository
from schemas.device_schema import (
    DeviceBase,
    DeviceConfigResponse,
    DeviceConfigUpdate
)
from utils.time_utils import utc_now
from utils.id_utils import normalize_device_id


class DeviceService:
    """
    Business logic layer for device lifecycle and configuration.
    Acts as the single authority for ESP device control.
    """

    def __init__(self):
        self.device_repo = DeviceRepository()

    # =========================
    # DEVICE REGISTRATION
    # =========================

    def register_device(self, device_data: DeviceBase):
        """
        Register a new ESP device.
        Called once during provisioning.
        """

        device_id = normalize_device_id(device_data.device_id)

        existing = self.device_repo.get_device_by_id(device_id)
        if existing:
            raise ValueError("Device already registered")

        device_record = device_data.dict()
        device_record["device_id"] = device_id
        device_record["created_at"] = utc_now()
        device_record["updated_at"] = utc_now()
        device_record["is_active"] = True

        self.device_repo.insert_one(device_record)

        return device_record

    # =========================
    # ESP CONFIG FETCH
    # =========================

    def get_device_config(self, device_id: str) -> DeviceConfigResponse:
        """
        Called by ESP firmware to fetch latest configuration.
        """

        device_id = normalize_device_id(device_id)

        device = self.device_repo.get_device_config(device_id)
        if not device:
            raise ValueError("Unknown device")

        if not device.get("is_active", False):
            raise ValueError("Device is inactive")

        self.device_repo.update_last_seen(device_id)

        return DeviceConfigResponse(**device)

    # =========================
    # ADMIN CONFIG UPDATE
    # =========================

    def update_device_config(
        self,
        device_id: str,
        update_data: DeviceConfigUpdate
    ):
        """
        Update device configuration from admin/app.
        """

        device_id = normalize_device_id(device_id)

        device = self.device_repo.get_device_by_id(device_id)
        if not device:
            raise ValueError("Device not found")

        update_dict = update_data.dict(exclude_unset=True)
        if not update_dict:
            return device  # nothing to update

        self.device_repo.update_device_config(
            device_id,
            update_dict
        )

        return self.device_repo.get_device_config(device_id)
