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
