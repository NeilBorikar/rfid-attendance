from repositories import DeviceRepository

from schemas.device_schema import DeviceBase
from utils.time_utils import utc_now
from utils.id_utils import normalize_device_id


class DeviceService:

    def __init__(self):
        self.device_repo = DeviceRepository()

    def register_device(self, device_data: DeviceBase):
        """
        Register a new device in the system.
        """

        # 1️⃣ Normalize device identity
        normalized_device_id = normalize_device_id(device_data.device_id)

        # 2️⃣ Prepare device record
        device_record = device_data.dict()
        device_record["device_id"] = normalized_device_id
        device_record["created_at"] = utc_now()
        device_record["is_active"] = True

        # 3️⃣ Persist device
        self.device_repo.insert_one(device_record)
