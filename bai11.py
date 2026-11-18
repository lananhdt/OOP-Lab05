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

class VentilationController(EmergencyDevice):
    def __init__(self, mediator: Optional[IEmergencyMediator] = None):
        super().__init__(mediator)
        self.is_running = True

    def shutdown_ventilation(self):
        if self.is_running:
            self.is_running = False
            print("  [VENTILATION] Đã ngắt hệ thống điều hòa/thông gió để ngăn khói lan rộng!")

    def start_ventilation(self):
        if not self.is_running:
            self.is_running = True
            print("  [VENTILATION] Đã khởi động lại hệ thống thông gió.")

class EmergencyMediator(IEmergencyMediator):
    """Trung tâm điều phối Alarm, DoorController và VentilationController"""
    def __init__(self, alarm: Alarm, door: DoorController, ventilation: VentilationController):
        self.alarm = alarm
        self.door = door
        self.ventilation = ventilation

        # Gán mediator cho từng thiết bị thành phần
        self.alarm.set_mediator(self)
        self.door.set_mediator(self)
        self.ventilation.set_mediator(self)

    def notify(self, sender: object, event: str, data: Optional[AlertEvent] = None):
        if event == "FIRE_DETECTED":
            sensor_info = f" từ {data.sensor_name} ({data.value:.1f}{data.unit})" if data else ""
            print(f"\n>>> [MEDIATOR] Kích hoạt kịch bản KHẨN CẤP (FIRE_DETECTED){sensor_info}:")
            self.alarm.activate()
            self.door.unlock_emergency_doors()
            self.ventilation.shutdown_ventilation()
        elif event == "ALL_CLEAR":
            print("\n>>> [MEDIATOR] Khôi phục trạng thái an toàn (ALL_CLEAR):")
            self.alarm.deactivate()
            self.door.lock_doors()
            self.ventilation.start_ventilation()

# ==========================================
# OBSERVER PATTERN
# ==========================================

class IAlertObserver(ABC):
    """Hợp đồng nhận cảnh báo cho các bên quan tâm."""
    @abstractmethod
    def update(self, alert_event: AlertEvent):
        pass

class SensorMonitor:
    """Subject quản lý danh sách observer, đọc cảm biến, đánh giá ngưỡng và cảnh báo"""
    def __init__(self):
        self._observers: List[IAlertObserver] = []

    def attach(self, observer: IAlertObserver):
        if observer is None:
            raise ValueError("Observer không được null.")
        # Không cho phép cùng một observer đăng ký hai lần
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IAlertObserver):
        if observer in self._observers:
            self._observers.remove(observer)

    def check_sensor(self, sensor_name: str, sensor: ISensor):
        value = sensor.read_value()

        # Phân loại mức độ cảnh báo theo ngưỡng quy ước
        if value >= 70.0:
            severity = "CRITICAL"
        elif value >= 50.0:
            severity = "WARNING"
        else:
            print(f"[MONITOR] {sensor_name}: {value:.1f}{sensor.get_unit()} -> Bình thường (Không phát cảnh báo).")
            return

        alert_event = AlertEvent(
            sensor_name=sensor_name,
            value=value,
            unit=sensor.get_unit(),
            severity=severity,
            occurred_at=datetime.now()
        )
        self._notify(alert_event)

    def _notify(self, alert_event: AlertEvent):
        # Duyệt trên bản sao list() để tránh lỗi nếu một observer tự detach trong lúc đang thông báo
        for observer in list(self._observers):
            try:
                observer.update(alert_event)
            except Exception as ex:
                # Cô lập lỗi: Một observer gặp sự cố không làm ảnh hưởng các observer khác
                print(f"  [ERROR] Observer {observer.__class__.__name__} gặp lỗi khi xử lý: {ex}")
