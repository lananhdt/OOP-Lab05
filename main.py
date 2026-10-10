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

# =============================================================================================
#  ABSTRACT CLASS: DEVICE
#  – Lớp cơ sở trừu tượng chứa các thông tin chung của mọi thiết bị
#  – Không thể khởi tạo trực tiếp đối tượng từ lớp này
# =============================================================================================
class Device(ABC):
    # =============================================================================================
    #  CONSTRUCTOR CỦA DEVICE
    #  – Khởi tạo thuộc tính và kiểm tra tính hợp lệ của dữ liệu đầu vào
    # =============================================================================================
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, status=DeviceStatus.Active):
        self._deviceId = str(deviceId).strip()
        self.name = str(name).strip()
        self.yearOfUse = int(yearOfUse)
        self.purchasePrice = float(purchasePrice)
        self.status = status

        # Kiểm tra tính hợp lệ của dữ liệu thiết bị
        if not self._deviceId:
            raise ValueError("Mã thiết bị không được rỗng.")
        if self.purchasePrice < 0:
            raise ValueError("Giá mua phải lớn hơn 0.")
        
        currentYear = datetime.date.today().year
        if self.yearOfUse > currentYear:
            raise ValueError("Năm đưa vào sử dụng không được lớn hơn năm hiện tại.")

    # Thuộc tính mã thiết bị chỉ được đọc (Read-only), không cho phép sửa sau khi tạo
    @property
    def deviceId(self):
        return self._deviceId

    # =============================================================================================
    #  HÀM TÍNH SỐ NĂM SỬ DỤNG
    #  – Lấy năm hiện tại trừ đi năm bắt đầu đưa vào sử dụng
    # =============================================================================================
    def getYearsUsed(self):
        currentYear = datetime.date.today().year
        return currentYear - self.yearOfUse

    # =============================================================================================
    #  HÀM TRỪU TƯỢNG: TÍNH CHI PHÍ BẢO TRÌ DỰ KIẾN
    #  – Ép buộc các lớp con (Computer, Printer, Projector) phải tự viết công thức riêng
    # =============================================================================================
    @abstractmethod
    def calculateAnnualMaintenanceCost(self):
        pass

    # Ghi đè phương thức in thông tin thiết bị dưới dạng chuỗi
    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self._deviceId} | Tên: {self.name} | Trạng thái: {self.status.value}"
