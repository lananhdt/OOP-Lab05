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
