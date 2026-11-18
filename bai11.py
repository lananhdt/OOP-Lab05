# /****************/
# Mã sinh viên: 202418837
# Họ tên: Đinh Thị Lan Anh
# /****************/

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# ==========================================
# DATA MODEL & THRESHOLD CONSTANTS
# ==========================================

@dataclass(frozen=True)
class AlertEvent:
    """Đối tượng dữ liệu bất biến mô tả sự kiện cảnh báo"""
    sensor_name: str
    value: float
    unit: str
    severity: str
    occurred_at: datetime

# ==========================================
# ADAPTER PATTERN
# ==========================================

class ISensor(ABC):
    """Giao diện chuẩn mà module giám sát sử dụng"""
    @abstractmethod
    def read_value(self) -> float:
        pass

    @abstractmethod
    def get_unit(self) -> str:
        pass

class LegacySmokeDetector:
    """Lớp cảm biến khói có sẵn, không sửa đổi"""
    def __init__(self, smoke_level: int):
        self._smoke_level = max(0, min(1000, smoke_level))

    def get_smoke_level(self) -> int:
        return self._smoke_level 

    def get_description(self) -> str:
        return "Legacy smoke detector"

    def set_smoke_level(self, value: int):
        self._smoke_level = max(0, min(1000, value))

class SmokeSensorAdapter(ISensor):
    """Adapter chuyển đổi giao diện và thang đo từ cảm biến cũ"""
    def __init__(self, legacy: LegacySmokeDetector):
        if legacy is None:
            raise ValueError("LegacySmokeDetector không được null.")
        # Giữ tham chiếu trực tiếp tới đối tượng cũ, không sao chép trạng thái
        self._legacy = legacy

    def read_value(self) -> float:
        return self._legacy.get_smoke_level() / 10.0

    def get_unit(self) -> str:
        return "% smoke"

# ==========================================
# MEDIATOR PATTERN
# ==========================================

class IEmergencyMediator(ABC):
    """Hợp đồng điều phối giữa các thiết bị ứng phó khẩn cấp"""
    @abstractmethod
    def notify(self, sender: object, event: str, data: Optional[AlertEvent] = None):
        pass

class EmergencyDevice(ABC):
    """Lớp cơ sở cho các thiết bị chịu sự điều phối của Mediator"""
    def __init__(self, mediator: Optional[IEmergencyMediator] = None):
        self._mediator = mediator

    def set_mediator(self, mediator: IEmergencyMediator):
        self._mediator = mediator

class Alarm(EmergencyDevice):
    def __init__(self, mediator: Optional[IEmergencyMediator] = None):
        super().__init__(mediator)
        self.is_ringing = False

    def activate(self):
        if not self.is_ringing:
            self.is_ringing = True
            print("  [ALARM] Còi báo cháy hú vang toàn phòng máy!")

    def deactivate(self):
        if self.is_ringing:
            self.is_ringing = False
            print("  [ALARM] Đã tắt còi báo cháy.")

class DoorController(EmergencyDevice):
    def __init__(self, mediator: Optional[IEmergencyMediator] = None):
        super().__init__(mediator)
        self.is_locked = True

    def unlock_emergency_doors(self):
        if self.is_locked:
            self.is_locked = False
            print("  [DOOR] Đã mở khóa toàn bộ cửa thoát hiểm!")

    def lock_doors(self):
        if not self.is_locked:
            self.is_locked = True
            print("  [DOOR] Đã khóa lại cửa phòng máy.")
