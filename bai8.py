"""
/****************/
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
/****************/
"""

# =============================================================================================
#  HỆ THỐNG QUẢN LÝ THIẾT BỊ DẠY HỌC (LAB 08)
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
