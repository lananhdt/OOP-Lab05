"""
/****************/
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
/****************/
"""

# =============================================================================================
#  HỆ THỐNG QUẢN LÝ THIẾT BỊ DẠY HỌC
#  – Áp dụng Event-Driven Architecture (Publisher - Subscriber)
#  – Áp dụng Delegate/Callback cho cơ chế lọc cảnh báo (Alert Filter)
# =============================================================================================

from enum import Enum
from datetime import datetime
from typing import List, Callable, Any, Optional

# =============================================================================================
#  1. ENUMS
# =============================================================================================
class DeviceStatus(Enum):
    Available = "Available"
    Borrowed = "Borrowed"
    UnderMaintenance = "Under Maintenance"

class AlertSeverity(Enum):
    Information = "Information"
    Warning = "Warning"
    Critical = "Critical"

# =============================================================================================
#  2. CLASSES DỮ LIỆU SỰ KIỆN (EVENT ARGS)
# =============================================================================================
class EventArgs:
    pass

class DeviceStatusChangedEventArgs(EventArgs):
    def __init__(self, deviceId: str, oldStatus: DeviceStatus, newStatus: DeviceStatus, changedAt: datetime):
        self.deviceId = deviceId
        self.oldStatus = oldStatus
        self.newStatus = newStatus
        self.changedAt = changedAt

class DeviceAlertEventArgs(EventArgs):
    def __init__(self, deviceId: str, message: str, severity: AlertSeverity, occurredAt: datetime):
        self.deviceId = deviceId
        self.message = message
        self.severity = severity
        self.occurredAt = occurredAt

# =============================================================================================
#  3. EXCEPTION
# =============================================================================================
class InvalidDeviceReadingException(Exception):
    def __init__(self, deviceId: str, invalidValue: int):
        self.deviceId = deviceId
        self.invalidValue = invalidValue
        super().__init__(f"Lỗi: Giá trị {invalidValue} không hợp lệ cho thiết bị {deviceId} (Phải từ 0-100).")

# =============================================================================================
#  4. GIẢ LẬP EVENT
# =============================================================================================
class Event:
    def __init__(self):
        self._handlers: List[Callable[[Any, Any], None]] = []

    def __iadd__(self, handler: Callable[[Any, Any], None]):
        if handler not in self._handlers:
            self._handlers.append(handler)
        return self

    def __isub__(self, handler: Callable[[Any, Any], None]):
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def invoke(self, sender: Any, args: Any):
        for handler in self._handlers:
            handler(sender, args)

# =============================================================================================
#  5. LỚP TRỪU TƯỢNG TEACHING DEVICE (PUBLISHER)
# =============================================================================================
class TeachingDevice:
    def __init__(self, deviceId: str, name: str):
        self._id = deviceId.strip()
        self._name = name.strip()
        self._status = DeviceStatus.Available
        
        # Events
        self.statusChanged = Event()
        self.alertRaised = Event()

    @property
    def id(self) -> str: return self._id

    @property
    def name(self) -> str: return self._name

    @property
    def status(self) -> DeviceStatus: return self._status

    def changeStatus(self, newStatus: DeviceStatus):
        if self._status == newStatus:
            return  # Không phát sinh event nếu trạng thái không đổi
            
        oldStatus = self._status
        self._status = newStatus  # Cập nhật trạng thái trước
        
        # Phát sinh event sau khi cập nhật
        self._onStatusChanged(DeviceStatusChangedEventArgs(self.id, oldStatus, newStatus, datetime.now()))

    def _raiseAlert(self, message: str, severity: AlertSeverity):
        self._onAlertRaised(DeviceAlertEventArgs(self.id, message, severity, datetime.now()))

    def _onStatusChanged(self, e: DeviceStatusChangedEventArgs):
        self.statusChanged.invoke(self, e)

    def _onAlertRaised(self, e: DeviceAlertEventArgs):
        self.alertRaised.invoke(self, e)

# =============================================================================================
#  6. CÁC LỚP THIẾT BỊ CỤ THỂ
# =============================================================================================
class ProjectorRemote(TeachingDevice):
    def __init__(self, deviceId: str, name: str):
        super().__init__(deviceId, name)
        self.batteryLevel = 100

    def updateBatteryLevel(self, newLevel: int):
        if newLevel < 0 or newLevel > 100:
            raise InvalidDeviceReadingException(self.id, newLevel)
            
        self.batteryLevel = newLevel
        if self.batteryLevel == 0:
            self._raiseAlert("Pin cạn kiệt (0%).", AlertSeverity.Critical)
        elif self.batteryLevel < 20:
            self._raiseAlert("Pin yếu dưới 20%.", AlertSeverity.Warning)

class AirConditionerRemote(TeachingDevice):
    def __init__(self, deviceId: str, name: str, assignedRoom: str):
        super().__init__(deviceId, name)
        self.assignedRoom = assignedRoom
        self.isResponsive = True

    def updateResponseState(self, isResponsive: bool):
        if self.isResponsive and not isResponsive:
            self.isResponsive = False
            self._raiseAlert(f"Mất kết nối với phòng {self.assignedRoom}.", AlertSeverity.Critical)
        elif not self.isResponsive and isResponsive:
            self.isResponsive = True
            self._raiseAlert("Đã khôi phục kết nối.", AlertSeverity.Information)

class WirelessMicrophone(TeachingDevice):
    def __init__(self, deviceId: str, name: str):
        super().__init__(deviceId, name)
        self.batteryLevel = 100
        self.signalQuality = 100

    def updateBatteryLevel(self, newLevel: int):
        if newLevel < 0 or newLevel > 100:
            raise InvalidDeviceReadingException(self.id, newLevel)
            
        self.batteryLevel = newLevel
        if self.batteryLevel == 0:
            self._raiseAlert("Micro hết sạch pin.", AlertSeverity.Critical)
        elif self.batteryLevel < 30:
            self._raiseAlert("Pin Micro yếu (< 30%).", AlertSeverity.Warning)

    def updateSignalQuality(self, newQuality: int):
        if newQuality < 0 or newQuality > 100:
            raise InvalidDeviceReadingException(self.id, newQuality)
            
        self.signalQuality = newQuality
        if self.signalQuality == 0:
            self._raiseAlert("Mất hoàn toàn tín hiệu.", AlertSeverity.Critical)
        elif self.signalQuality < 40:
            self._raiseAlert("Chất lượng tín hiệu kém (< 40%).", AlertSeverity.Warning)
