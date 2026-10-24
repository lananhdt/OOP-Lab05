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


# =============================================================================================
#  ABSTRACT CLASS: TEACHING DEVICE
#  – Lớp cơ sở trừu tượng thực thi IIdentifiable
#  – Định nghĩa khung thông tin chung và hành vi mượn/trả của thiết bị
# =============================================================================================
class TeachingDevice(IIdentifiable):
    def __init__(self, deviceId: str, name: str, storageLocation: str):
        if not deviceId or not name or not storageLocation:
            raise ValueError("ID, Tên và Vị trí lưu trữ không được rỗng.")
            
        self._id = deviceId.strip()
        self.name = name.strip()
        self.storageLocation = storageLocation.strip()
        self._status = DeviceStatus.Available

    @property
    def id(self) -> str:
        return self._id

    @property
    def status(self) -> DeviceStatus:
        return self._status

    def borrow(self):
        # Borrow() chỉ thành công nếu IsReadyForUse() trả về true
        if not self.isReadyForUse():
            raise DeviceNotReadyException(self.id, self.status.value)
        self._status = DeviceStatus.Borrowed

    def returnDevice(self):
        # Return() chỉ thành công nếu trạng thái là Borrowed
        if self._status != DeviceStatus.Borrowed:
            raise Exception(f"Thiết bị '{self.id}' đang không được mượn.")
        self._status = DeviceStatus.Available

    # Cài đặt đa hình ở các lớp dẫn xuất
    @abstractmethod
    def isReadyForUse(self) -> bool:
        pass
    @abstractmethod
    def getDefaultPriorityScore(self) -> float:
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self.id} | {self.name} | TT: {self.status.value}"
