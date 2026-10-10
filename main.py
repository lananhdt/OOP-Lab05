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

# =============================================================================================
#  CLASS: COMPUTER (Kế thừa Device, Thực thi INetworkable)
#  – Quản lý máy tính, bổ sung RAM, CPU và GPU
# =============================================================================================
class Computer(Device, INetworkable):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, ram, cpu, hasGpu, status=DeviceStatus.Active):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, status)
        self.ram = ram
        self.cpu = cpu
        self.hasGpu = bool(hasGpu)
        
        # Biến phục vụ cho interface kết nối mạng
        self._ipAddress = ""
        self._isConnected = False

    # =============================================================================================
    #  TÍNH CHI PHÍ BẢO TRÌ
    #  – Cơ bản: 5% giá mua
    #  – Phụ thu 1: Thêm 2% nếu có GPU rời
    #  – Phụ thu 2: Thêm 1% nếu thiết bị đã dùng trên 5 năm
    # =============================================================================================
    def calculateAnnualMaintenanceCost(self):
        totalCost = self.purchasePrice * 0.5
        if self.hasGpu:
            totalCost += self.purchasePrice * 0.2
        if self.getYearsUsed() > 5:
            totalCost += self.purchasePrice * 0.1
        return totalCost

    # =============================================================================================
    #  TRIỂN KHAI CÁC HÀM CỦA INETWORKABLE
    #  – Xử lý logic kết nối và ngắt kết nối IP
    # =============================================================================================
    @property
    def ipAddress(self): return self._ipAddress
    
    @property
    def isConnected(self): return self._isConnected

    def connect(self, ipAddress):
        # Tránh việc thiết bị đang online lại gọi kết nối đè lên
        if self._isConnected:
            print(f"  [!] {self._deviceId} Đã kết nối, không thể kết nối lại.")
            return
        if not ipAddress.strip():
            raise ValueError("Địa chỉ IP không được rỗng.")
            
        self._ipAddress = ipAddress
        self._isConnected = True
        print(f"  [OK] {self._deviceId} Đã kết nối mạng tới IP: {self._ipAddress}")

    def disconnect(self):
        self._ipAddress = ""
        self._isConnected = False
        print(f"  [OK] {self._deviceId} Đã ngắt kết nối mạng.")

# =============================================================================================
#  CLASS: PRINTER (Kế thừa Device)
#  – Quản lý máy in chung (Chưa có tính năng mạng)
# =============================================================================================
class Printer(Device):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, printerType, printedPages, isColor, status=DeviceStatus.Active):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, status)
        self.printerType = printerType
        self.printedPages = int(printedPages)
        self.isColor = bool(isColor)

    # =============================================================================================
    #  TÍNH CHI PHÍ BẢO TRÌ
    #  – Cơ bản: 4% giá mua
    #  – Phụ thu 1: +500,000 VND nếu số trang in vượt 100,000
    #  – Phụ thu 2: +300,000 VND nếu là máy in màu
    # =============================================================================================
    def calculateAnnualMaintenanceCost(self):
        totalCost = self.purchasePrice * 0.4
        if self.printedPages > 100000:
            totalCost += 500000
        if self.isColor:
            totalCost += 300000
        return totalCost

# =============================================================================================
#  CLASS: NETWORK PRINTER (Kế thừa Printer, Thực thi INetworkable)
#  – Yêu cầu "chỉ một số máy in mới có mạng"
# =============================================================================================
class NetworkPrinter(Printer, INetworkable):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, printerType, printedPages, isColor, status=DeviceStatus.Active):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, printerType, printedPages, isColor, status)
        self._ipAddress = ""
        self._isConnected = False

    @property
    def ipAddress(self): return self._ipAddress
    
    @property
    def isConnected(self): return self._isConnected

    def connect(self, ipAddress):
        if self._isConnected:
            return
        if not ipAddress.strip(): raise ValueError("IP rỗng.")
        self._ipAddress = ipAddress
        self._isConnected = True
        print(f"  [OK] {self._deviceId} (Máy in mạng) đã kết nối IP: {self._ipAddress}")

    def disconnect(self):
        self._ipAddress = ""
        self._isConnected = False

# =============================================================================================
#  CLASS: PROJECTOR (Kế thừa Device)
#  – Máy chiếu, tính bảo trì dựa trên độ sáng và số giờ chiếu bóng đèn
# =============================================================================================
class Projector(Device):
    def __init__(self, deviceId, name, yearOfUse, purchasePrice, brightness, lampHours, status=DeviceStatus.Active):
        super().__init__(deviceId, name, yearOfUse, purchasePrice, status)
        self.brightness = brightness
        self.lampHours = lampHours

    # =============================================================================================
    #  TÍNH CHI PHÍ BẢO TRÌ
    #  – Cơ bản: 3% giá mua
    #  – Phụ thu: +1,500,000 VND nếu bóng đèn đã sử dụng trên 3000 giờ
    # =============================================================================================
    def calculateAnnualMaintenanceCost(self):
        totalCost = self.purchasePrice * 0.03
        if self.lampHours > 3000:
            totalCost += 1500000
        return totalCost

# =============================================================================================
#  CLASS: LAB ROOM (Quan hệ Kết tập với Device)
#  – Quản lý danh sách thiết bị trong một phòng thực hành
# =============================================================================================
class LabRoom:
    def __init__(self, roomId, name, capacity):
        self.roomId = roomId
        self.name = name
        self.capacity = capacity
        self.deviceList = []

    # =============================================================================================
    #  THÊM THIẾT BỊ VÀO PHÒNG
    #  – Không thêm hai thiết bị có cùng mã (ID) vào một phòng
    #  – Không chấp nhận đối tượng thiết bị null
    # =============================================================================================
    def addDevice(self, device):
        if device is None:
            raise ValueError("Thiết bị không được null.")
            
        if self.findDevice(device.deviceId):
            print(f"  [!] Lỗi: Thiết bị mã {device.deviceId} đã tồn tại trong phòng {self.name}.")
            return
            
        self.deviceList.append(device)
        print(f"  [OK] Đã thêm thiết bị {device.deviceId} vào phòng {self.name}.")

    # =============================================================================================
    #  XÓA THIẾT BỊ KHỎI PHÒNG
    #  – Tìm kiếm thiết bị bằng ID, nếu thấy thì gỡ khỏi mảng và trả về True
    #  – Nếu không tồn tại trả về False
    # =============================================================================================
    def removeDevice(self, deviceId):
        device = self.findDevice(deviceId)
        if device is not None:
            self.deviceList.remove(device)
            return True
        return False

    # =============================================================================================
    #  TÌM KIẾM THIẾT BỊ
    #  – Duyệt mảng và trả về tham chiếu đến đối tượng Device nếu khớp ID, ngược lại trả về None
    # =============================================================================================
    def findDevice(self, deviceId):
        for dev in self.deviceList:
            if dev.deviceId == deviceId:
                return dev
        return None

    # =============================================================================================
    #  TÍNH TỔNG CHI PHÍ BẢO TRÌ TOÀN PHÒNG
    #  – Tự động gọi đúng hàm tính phí của từng lớp con mà không cần if/else ép kiểu
    # =============================================================================================
    def calculateAnnualMaintenanceCost(self):
        totalRoomCost = 0
        for dev in self.deviceList:
            totalRoomCost += dev.calculateAnnualMaintenanceCost()
        return totalRoomCost

    # =============================================================================================
    #  LỌC DANH SÁCH THIẾT BỊ CẦN BẢO TRÌ
    #  – Lọc các thiết bị đang ở trạng thái UnderMaintenance hoặc có thời gian sử dụng trên 5 năm
    # =============================================================================================
    def getDevicesRequiringMaintenance(self):
        maintenanceList = []
        for dev in self.deviceList:
            if dev.status == DeviceStatus.UnderMaintenance and dev.getYearsUsed() > 5:
                maintenanceList.append(dev)
        return maintenanceList

    # =============================================================================================
    #  IN DANH SÁCH THIẾT BỊ
    # =============================================================================================
    def printDevices(self):
        print(f"\n--- DANH SÁCH THIẾT BỊ PHÒNG: {self.name} ---")
        for dev in self.deviceList:
            cost = dev.calculateAnnualMaintenanceCost()
            print(f"  {dev} | Phí bảo trì dự kiến: {cost:,.0f} VNĐ")
        print("-" * 50)
