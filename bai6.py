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

# =============================================================================================
#  CLASS: BORROW ITEM
#  – Lưu thông tin mượn một thiết bị cụ thể trong phiếu mượn
# =============================================================================================
class BorrowItem:
    def __init__(self, device, borrowedDate, dueDate):
        if device is None:
            raise ValueError("Thiết bị không được null.")
        if dueDate < borrowedDate:
            raise ValueError("Hạn trả không được trước ngày mượn.")

        self._device = device
        self._borrowedDate = borrowedDate
        self._dueDate = dueDate
        self._returnedDate = None
        self._isReturned = False

    @property
    def device(self): return self._device

    @property
    def borrowedDate(self): return self._borrowedDate

    @property
    def dueDate(self): return self._dueDate

    @property
    def returnedDate(self): return self._returnedDate

    @property
    def isReturned(self): return self._isReturned

    def returnDevice(self, returnedDate):
        if self._isReturned:
            raise DeviceAlreadyReturnedException(self.device.deviceId)
        if returnedDate < self._borrowedDate:
            raise InvalidReturnDateException(self.device.deviceId)
        
        self._returnedDate = returnedDate
        self._isReturned = True

    def getLateDays(self):
        if not self._isReturned:
            return 0
        lateDelta = (self._returnedDate - self._dueDate).days
        return lateDelta

# =============================================================================================
#  CLASS: BORROWING SLIP
#  – Phiếu mượn của một giảng viên/trợ giảng cho một phòng học
#  – Hợp thành các BorrowItem bên trong
# =============================================================================================
class BorrowingSlip:
    def __init__(self, slipId, borrower, teachingRoom, borrowedDate):
        if not slipId or not borrower or not teachingRoom:
            raise ValueError("Mã phiếu, người mượn và phòng học không hợp lệ (null).")
            
        self.slipId = slipId
        self.borrower = borrower
        self.teachingRoom = teachingRoom
        self.borrowedDate = borrowedDate
        self._items = []
        self._LATE_FEE_PER_DAY = 50000 # 50,000 VND/ngày trễ

    @property
    def items(self):
        return self._items

    # =============================================================================================
    #  THÊM THIẾT BỊ VÀO PHIẾU
    #  – Kiểm tra toàn bộ ngoại lệ trước, nếu pass hết mới tiến hành đổi trạng thái và thêm vào list
    # =============================================================================================
    def addDevice(self, device, borrowDays):
        if device is None:
            raise ValueError("Thiết bị yêu cầu thêm bị null.")
        
        if borrowDays <= 0 or borrowDays > device.maxBorrowDays:
            raise InvalidBorrowPeriodException(device.deviceId, borrowDays, device.maxBorrowDays)

        if device.status != DeviceStatus.Available:
            raise DeviceUnavailableException(device.deviceId, device.status.value)

        # Kiểm tra giới hạn mượn của tài khoản
        if len(self._items) > self.borrower.getMaximumDevices():
            raise BorrowLimitExceededException(self.borrower.borrowerId, self.borrower.getMaximumDevices())

        for item in self._items:
            if item.device.deviceId == device.deviceId:
                raise DuplicateDeviceException(device.deviceId)

        dueDate = self.borrowedDate + datetime.timedelta(days=borrowDays)
        newItem = BorrowItem(device, self.borrowedDate, dueDate)
        
        self._items.append(newItem)
        print(f"  [OK] Đã thêm '{device.name}' (ID: {device.deviceId}) vào phiếu {self.slipId}.")

    # =============================================================================================
    #  TRẢ THIẾT BỊ TRONG PHIẾU
    #  – Kiểm tra hợp lệ, ghi nhận ngày trả, đổi trạng thái Available, và tính phí phạt trễ hạn
    # =============================================================================================
    def returnDevice(self, deviceId, returnedDate):
        targetItem = None
        for item in self._items:
            if item.device.deviceId == deviceId:
                targetItem = item
                break
        
        if targetItem is None:
            raise DeviceNotInSlipException(deviceId)

        targetItem.returnDevice(returnedDate)
        
        # Đổi trạng thái thiết bị về kho
        targetItem.device.markAsAvailable()
        
        lateDays = targetItem.getLateDays()
        fee = lateDays * self._LATE_FEE_PER_DAY
        
        statusMsg = f"Đúng hạn." if lateDays == 0 else f"TRỄ {lateDays} NGÀY. Phạt: {fee:,.0f} VND"
        print(f"  [OK] Trả '{targetItem.device.name}' thành công. {statusMsg}")
        return fee

    def calculateTotalLateFee(self):
        totalLateFee = 0
        for item in self._items:
            if item.isReturned:
                totalLateFee += item.getLateDays() * self._LATE_FEE_PER_DAY
        return totalLateFee

    def printSlipInfo(self):
        print(f"\n--- THÔNG TIN PHIẾU MƯỢN: {self.slipId} ---")
        print(f"  Người mượn: {self.borrower.fullName} (Quyền: Tối đa {self.borrower.getMaximumDevices()} thiết bị)")
        print(f"  Phòng dạy : {self.teachingRoom}")
        print(f"  Ngày mượn : {self.borrowedDate.strftime('%Y-%m-%d')}")
        print("  DANH SÁCH THIẾT BỊ:")
        for item in self._items:
            retStatus = f"Đã trả ({item.returnedDate.strftime('%Y-%m-%d')})" if item.isReturned else "Chưa trả"
            print(f"    - {item.device.deviceId} ({item.device.name}) | Hạn: {item.dueDate.strftime('%Y-%m-%d')} | {retStatus}")
        print(f"  TỔNG PHẠT TRỄ: {self.calculateTotalLateFee():,.0f} VND")
        print("-" * 50)
