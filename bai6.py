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

# =============================================================================================
#  HỆ THỐNG NGOẠI LỆ NGHIỆP VỤ
# =============================================================================================
class BorrowingException(Exception):
    """Ngoại lệ cơ sở"""
    pass

class DeviceUnavailableException(BorrowingException):
    def __init__(self, deviceId, currentStatus):
        self.deviceId = deviceId
        self.currentStatus = currentStatus
        super().__init__(f"Thiết bị '{deviceId}' không khả dụng. Trạng thái hiện tại: {currentStatus}")

class BorrowLimitExceededException(BorrowingException):
    def __init__(self, borrowerId, maximumDevices):
        self.borrowerId = borrowerId
        self.maximumDevices = maximumDevices
        super().__init__(f"Người mượn '{borrowerId}' đã vượt quá giới hạn mượn ({maximumDevices} thiết bị).")

class InvalidBorrowPeriodException(BorrowingException):
    def __init__(self, deviceId, requestedDays, maxDays):
        self.deviceId = deviceId
        self.requestedDays = requestedDays
        self.maxDays = maxDays
        super().__init__(f"Thời gian mượn thiết bị '{deviceId}' ({requestedDays} ngày) không hợp lệ hoặc vượt quá giới hạn ({maxDays} ngày).")

class DuplicateDeviceException(BorrowingException):
    def __init__(self, deviceId):
        self.deviceId = deviceId
        super().__init__(f"Thiết bị '{deviceId}' đã tồn tại trong phiếu mượn này.")

class DeviceNotInSlipException(BorrowingException):
    def __init__(self, deviceId):
        self.deviceId = deviceId
        super().__init__(f"Thiết bị '{deviceId}' không thuộc phiếu mượn này.")

class DeviceAlreadyReturnedException(BorrowingException):
    def __init__(self, deviceId):
        self.deviceId = deviceId
        super().__init__(f"Thiết bị '{deviceId}' đã được trả trước đó.")

class InvalidReturnDateException(BorrowingException):
    def __init__(self, deviceId):
        self.deviceId = deviceId
        super().__init__(f"Ngày trả thiết bị '{deviceId}' không hợp lệ (trước ngày mượn).")

# =============================================================================================
#  CÁC LỚP THIẾT BỊ CỤ THỂ
# =============================================================================================
class AirConditionerRemote(Device):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, maxBorrowDays=1, status=DeviceStatus.Available):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, maxBorrowDays, status)

    def calculateAnnualMaintenanceCost(self):
        return self.purchasePrice * 0.05

class Microphone(Device):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, maxBorrowDays=1, status=DeviceStatus.Available):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, maxBorrowDays, status)

    def calculateAnnualMaintenanceCost(self):
        return self.purchasePrice * 0.08

class ProjectorRemote(Device):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, maxBorrowDays=1, status=DeviceStatus.Available):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, maxBorrowDays, status)

    def calculateAnnualMaintenanceCost(self):
        return self.purchasePrice * 0.03

# =============================================================================================
#  KỊCH BẢN KIỂM THỬ
# =============================================================================================
def runTests():
    print("============= KHỞI TẠO DỮ LIỆU =============")
    # 1. Tạo Giảng viên và Trợ giảng
    lecturer = Lecturer("GV01", "PGS.TS Lê Mai Trang")
    ta = TeachingAssistant("TA01", "Trợ giảng Bùi Thu Huyền")

    # 2. Tạo thiết bị
    d_air = AirConditionerRemote("AC01", "ĐK Điều hòa 01", 2022, 500000)
    d_mic = Microphone("MIC01", "Micro Không Dây", 2023, 1500000)
    d_proj = ProjectorRemote("PRJ01", "ĐK Máy chiếu", 2021, 300000)
    d_air_broken = AirConditionerRemote("AC02", "ĐK Điều hòa Hỏng", 2020, 500000, status=DeviceStatus.UnderMaintenance)

    today = datetime.datetime.now()

    print("\n--- 11.1. LUỒNG THÀNH CÔNG ---")
    try:
        # 3. Tạo phiếu mượn cho một phòng dạy
        slip1 = BorrowingSlip("S001", lecturer, "Phòng 302-D3", today)
        
        # 4. Thêm điều khiển máy chiếu và micro vào phiếu
        slip1.addDevice(d_proj, 1)
        slip1.addDevice(d_mic, 1)
        
        # 5. Trả điều khiển máy chiếu đúng hạn
        slip1.returnDevice("PRJ01", today)
        
        # 6. Trả micro muộn 2 ngày
        slip1.returnDevice("MIC01", today + datetime.timedelta(days=3)) # Muộn 2 ngày so với hạn (hạn là +1)
        
        # 7. Hiển thị
        slip1.printSlipInfo()
        
    except Exception as e:
        print(f"  [!] Lỗi bất thường trong luồng thành công: {e}")

    print("\n--- 11.2. LUỒNG PHÁT SINH NGOẠI LỆ ---")
    slip2 = BorrowingSlip("S002", ta, "Phòng 101-D9", today)
    
    def runExceptionTest(testName, func, *args):
        print(f"\n  > {testName}")
        try:
            func(*args)
            print("    [!] Thất bại")
        except BorrowingException as e:
            print(f"    [OK] Bắt được Custom Exception: {e}")
        except Exception as e:
            print(f"    [OK] Bắt được Exception cơ bản: {e}")

    # 1. Mượn điều khiển điều hòa đang UnderMaintenance
    runExceptionTest("Test 1: Mượn thiết bị đang bảo trì", slip2.addDevice, d_air_broken, 1)

    # 2. Trợ giảng mượn thiết bị thứ ba (giới hạn 2)
    slip2.addDevice(d_air, 1)
    d_mic2 = Microphone("MIC02", "Micro 02", 2023, 1500000)
    slip2.addDevice(d_mic2, 1)
    d_proj2 = ProjectorRemote("PRJ02", "ĐK Máy chiếu 02", 2023, 300000)
    runExceptionTest("Test 2: Trợ giảng mượn thiết bị thứ 3 (vượt giới hạn)", slip2.addDevice, d_proj2, 1)

    # 3. Thêm cùng một thiết bị hai lần
    runExceptionTest("Test 3: Thêm cùng một thiết bị hai lần", slip2.addDevice, d_air, 1)

    # 4. Mượn micro trong 3 ngày dù giới hạn là 1 ngày
    d_mic3 = Microphone("MIC03", "Micro 03", 2023, 1500000, maxBorrowDays=1)
    slip3 = BorrowingSlip("S003", lecturer, "Phòng 205-D7", today)
    runExceptionTest("Test 4: Mượn quá thời hạn giới hạn thiết bị (3 ngày)", slip3.addDevice, d_mic3, 3)

    # 5. Trả một điều khiển máy chiếu không thuộc phiếu
    runExceptionTest("Test 5: Trả thiết bị không thuộc phiếu", slip2.returnDevice, "PRJ99", today)

    # 6. Trả cùng một thiết bị hai lần
    slip2.returnDevice("AC01", today) # Trả lần 1 thành công
    runExceptionTest("Test 6: Trả cùng một thiết bị hai lần", slip2.returnDevice, "AC01", today)

    # 7. Trả thiết bị với ngày trả trước ngày mượn
    d_proj3 = ProjectorRemote("PRJ03", "ĐK Máy chiếu 03", 2023, 300000)
    slip3.addDevice(d_proj3, 1)
    runExceptionTest("Test 7: Ngày trả trước ngày mượn", slip3.returnDevice, "PRJ03", today - datetime.timedelta(days=5))

    print("\n================== HOÀN TẤT KIỂM THỬ ==================")

if __name__ == "__main__":
    runTests()
