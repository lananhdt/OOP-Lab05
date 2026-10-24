"""
/****************/
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
/****************/
"""

# =============================================================================================
#  HỆ THỐNG QUẢN LÝ THIẾT BỊ DẠY HỌC
#  – Áp dụng đa hình để thay đổi hành vi theo loại thiết bị và chiến lược
#  – Áp dụng Generics để xây dựng kho lưu trữ và dịch vụ lựa chọn tổng quát
# =============================================================================================

from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic, List, Callable, Dict, Optional, Set

# =============================================================================================
#  ENUM: DEVICE STATUS
#  – Trạng thái của thiết bị
# =============================================================================================
class DeviceStatus(Enum):
    Available = "Available"
    Borrowed = "Borrowed"
    UnderMaintenance = "Under Maintenance"


# =============================================================================================
#  INTERFACE: IIDENTIFIABLE
#  – Interface nhận diện đối tượng, cho phép các cấu trúc tổng quát (Generic) 
#    có thể tìm kiếm đối tượng theo mã ID mà không phụ thuộc vào lớp cụ thể
# =============================================================================================
class IIdentifiable(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
