"""
/****************/
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
/****************/
"""

# =============================================================================================
#  HỆ THỐNG QUẢN LÝ THIẾT BỊ VÀ HỢP ĐỒNG BẢO TRÌ
#  – Xây dựng hệ thống quản lý mượn/trả thiết bị
#  – Áp dụng Kế thừa, Lớp trừu tượng, Interface, Kết tập và Hợp thành
#  – Quản lý ngoại lệ nghiệp vụ (Custom Exceptions) để đảm bảo tính nhất quán dữ liệu
# =============================================================================================

from abc import ABC, abstractmethod
from enum import Enum
import datetime

# =============================================================================================
#  ENUM: DEVICE STATUS
#  – Khai báo các trạng thái của thiết bị
# =============================================================================================
class DeviceStatus(Enum):
    Available = "Available"
    Borrowed = "Borrowed"
    UnderMaintenance = "Under Maintenance"
    Retired = "Retired"

# =============================================================================================
#  ABSTRACT CLASS: DEVICE
#  – Lớp trừu tượng cho mọi thiết bị phục vụ học tập/giảng dạy
# =============================================================================================
class Device(ABC):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, maxBorrowDays, status=DeviceStatus.Available):
        self._deviceId = str(deviceId).strip()
        self.name = str(name).strip()
        self.yearOfUse = int(yearOfUse)
        self.purchasePrice = float(purchasePrice)
        self.maxBorrowDays = int(maxBorrowDays)
        self._status = status

        if not self._deviceId:
            raise ValueError("Mã thiết bị không được rỗng.")
        if self.purchasePrice <= 0:
            raise ValueError("Giá mua phải lớn hơn 0.")
        
        currentYear = datetime.date.today().year
        if self.yearOfUse > currentYear:
            raise ValueError("Năm đưa vào sử dụng không được lớn hơn năm hiện tại.")

    @property
    def deviceId(self):
        return self._deviceId

    @property
    def status(self):
        return self._status

    def markAsBorrowed(self):
        self._status = DeviceStatus.Borrowed

    def markAsAvailable(self):
        self._status = DeviceStatus.Available

    def getYearsUsed(self):
        currentYear = datetime.date.today().year
        return currentYear - self.yearOfUse

    @abstractmethod
    def calculateAnnualMaintenanceCost(self):
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self._deviceId} | Tên: {self.name} | Trạng thái: {self.status.value}"

# =============================================================================================
#  CLASS: CLASSROOM (Lớp học - Quan hệ kết tập với Device)
#  – Quản lý danh sách thiết bị cố định được lắp đặt trong một phòng
# =============================================================================================
class ClassRoom:
    def __init__(self, roomId, name, capacity):
        self.roomId = roomId
        self.name = name
        self.capacity = capacity
        self.deviceList = []

    def addDevice(self, device):
        if device is None:
            raise ValueError("Thiết bị không được null.")
        if self.findDevice(device.deviceId):
            print(f"  [!] Lỗi: Thiết bị mã {device.deviceId} đã tồn tại trong phòng {self.name}.")
            return
        self.deviceList.append(device)
        print(f"  [+] Đã phân bổ '{device.deviceId}' vào {self.name}.")

    def removeDevice(self, deviceId):
        dev = self.findDevice(deviceId)
        if dev:
            self.deviceList.remove(dev)
            return True
        return False

    def findDevice(self, deviceId):
        for dev in self.deviceList:
            if dev.deviceId == deviceId:
                return dev
        return None

    def calculateAnnualMaintenanceCost(self):
        return sum(dev.calculateAnnualMaintenanceCost() for dev in self.deviceList)

    def getDevicesRequiringMaintenance(self):
        return [dev for dev in self.deviceList if dev.status == DeviceStatus.UnderMaintenance and dev.getYearsUsed() > 5]

# =============================================================================================
#  INTERFACE: IBORROWER
#  – Biểu diễn thông tin người mượn và giới hạn số lượng thiết bị
# =============================================================================================
class IBorrower(ABC):
    @property
    @abstractmethod
    def borrowerId(self):
        pass

    @property
    @abstractmethod
    def fullName(self):
        pass

    @abstractmethod
    def getMaximumDevices(self):
        pass

# =============================================================================================
#  CLASS: LECTURER
#  – Thực thi IBorrower. Giảng viên được mượn tối đa 3 thiết bị.
# =============================================================================================
class Lecturer(IBorrower):
    def __init__(self, borrowerId, fullName):
        self._borrowerId = borrowerId
        self._fullName = fullName

    @property
    def borrowerId(self): return self._borrowerId

    @property
    def fullName(self): return self._fullName

    def getMaximumDevices(self):
        return 3

# =============================================================================================
#  CLASS: TEACHING ASSISTANT
#  – Thực thi IBorrower. Trợ giảng được mượn tối đa 2 thiết bị.
# =============================================================================================
class TeachingAssistant(IBorrower):
    def __init__(self, borrowerId, fullName):
        self._borrowerId = borrowerId
        self._fullName = fullName

    @property
    def borrowerId(self): return self._borrowerId

    @property
    def fullName(self): return self._fullName

    def getMaximumDevices(self):
        return 2
