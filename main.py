"""
/****************/
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
/****************/
"""

# =============================================================================================
#  HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ
#  – Xây dựng hệ thống quản lý các thiết bị trong phòng thực hành (Lab)
#  – Áp dụng tính Kế thừa, Lớp trừu tượng, Interface và Đa hình
# =============================================================================================

from abc import ABC, abstractmethod
from enum import Enum
import datetime

# =============================================================================================
#  ENUM: DEVICE STATUS
#  – Khai báo các trạng thái hoạt động của thiết bị
# =============================================================================================
class DeviceStatus(Enum):
    Active = "Active"
    UnderMaintenance = "Under Maintenance"
    Retired = "Retired"


# =============================================================================================
#  INTERFACE: INETWORKABLE
#  – Biểu diễn khả năng kết nối mạng của một thiết bị
#  – Bất kỳ thiết bị nào implement interface này đều phải định nghĩa các hàm kết nối
# =============================================================================================
class INetworkable(ABC):
    @property
    @abstractmethod
    def IpAddress(self):
        pass

    @property
    @abstractmethod
    def IsConnected(self):
        pass

    @abstractmethod
    def Connect(self, IpAddress):
        pass

    @abstractmethod
    def Disconnect(self):
        pass
