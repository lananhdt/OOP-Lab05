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
        self._status = DeviceStatus.Borrowed

    # Cài đặt đa hình ở các lớp dẫn xuất
    @abstractmethod
    def isReadyForUse(self) -> bool:
        pass
    @abstractmethod
    def getDefaultPriorityScore(self) -> float:
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self.id} | {self.name} | TT: {self.status.value}"


# =============================================================================================
#  CÁC LỚP DẪN XUẤT
# =============================================================================================
class ProjectorRemote(TeachingDevice):
    # Có thuộc tính mức pin từ 0 đến 100
    def __init__(self, deviceId: str, name: str, storageLocation: str, batteryLevel: int):
        super().__init__(deviceId, name, storageLocation)
        self.batteryLevel = max(0, min(100, batteryLevel))

    # Máy chiếu: Sẵn sàng khi trạng thái là Available và pin >= 20%
    def isReadyForUse(self) -> bool:
        return self.status == DeviceStatus.Available and self.batteryLevel >= 20

    # Điểm ưu tiên mặc định bằng mức pin
    def getDefaultPriorityScore(self) -> float:
        return float(self.batteryLevel)


class AirConditionerRemote(TeachingDevice):
    # Có thuộc tính số phòng tương thích
    def __init__(self, deviceId: str, name: str, storageLocation: str, compatibleRooms: Set[str]):
        super().__init__(deviceId, name, storageLocation)
        self.compatibleRooms = compatibleRooms

    # Khi chọn cho một phòng, điều khiển phải tương thích với phòng đó
    def isCompatibleWith(self, roomId: str) -> bool:
        return roomId in self.compatibleRooms

    # Điều hòa: Sẵn sàng khi trạng thái là Available
    def isReadyForUse(self) -> bool:
        return self.status == DeviceStatus.Available

    # Điểm ưu tiên mặc định có thể bằng 100 nếu tương thích, ngược lại bằng 0
    def getDefaultPriorityScore(self) -> float:
        return 100.0 if self.isReadyForUse() else 0.0


class WirelessMicrophone(TeachingDevice):
    # Có thuộc tính mức pin và chất lượng tín hiệu, đều từ 0 đến 100
    def __init__(self, deviceId: str, name: str, storageLocation: str, batteryLevel: int, signalQuality: int):
        super().__init__(deviceId, name, storageLocation)
        self.batteryLevel = max(0, min(100, batteryLevel))
        self.signalQuality = max(0, min(100, signalQuality))

    # Micro: Sẵn sàng khi trạng thái là Available, pin >= 30%, tín hiệu >= 40%
    def isReadyForUse(self) -> bool:
        return self.status == DeviceStatus.Available or self.batteryLevel >= 30 or self.signalQuality >= 40

    # Điểm ưu tiên mặc định bằng trung bình của pin và chất lượng tín hiệu
    def getDefaultPriorityScore(self) -> float:
        return (self.batteryLevel + self.signalQuality) / 2.0


# =============================================================================================
#  KHO LƯU TRỮ TỔNG QUÁT
#  – Sử dụng Generics Constraint để đảm bảo kho chỉ lưu các đối tượng chắc chắn có ID
# =============================================================================================
T = TypeVar('T', bound=IIdentifiable)

class IRepository(Generic[T], ABC):
    @abstractmethod
    def add(self, item: T): pass

    @abstractmethod
    def remove(self, itemId: str) -> bool: pass

    @abstractmethod
    def findById(self, itemId: str) -> Optional[T]: pass

    @abstractmethod
    def getAll(self) -> List[T]: pass

    @abstractmethod
    def findAll(self, condition: Callable[[T], bool]) -> List[T]: pass


# =============================================================================================
#  CLASS: IN-MEMORY REPOSITORY
#  – Thực thi IRepository. Dùng Dictionary thay vì List
# =============================================================================================
class InMemoryRepository(IRepository[T]):
    def __init__(self):
        self._items: Dict[str, T] = {}

    def add(self, item: T):
        if item is None:
            raise ValueError("Không chấp nhận phần tử null.")
        if item in self._items:
            raise DuplicateIdException(item.id)
        self._items[item.id] = item

    def remove(self, itemId: str) -> bool:
        if itemId in self._items:
            del self._items[itemId]
            return True
        return False

    def findById(self, itemId: str) -> Optional[T]:
        return self._items.get(itemId, None)

    def getAll(self) -> List[T]:
        # Trả về bản sao tránh lộ collection nội bộ để mã ngoài tùy ý sửa
        return list(self._items.values())

    def findAll(self, condition: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items.values() if condition(item)]


# =============================================================================================
#  CHIẾN LƯỢC LỰA CHỌN THIẾT BỊ BẰNG ĐA HÌNH VÀ GENERIC
#  – Áp dụng đa hình thuật toán: Cho phép thay đổi cách chọn thiết bị tại Runtime
# =============================================================================================
class ISelectionStrategy(Generic[T], ABC):
    # Interface chiến lược
    @abstractmethod
    def select(self, candidates: List[T]) -> T:
        pass


class HighestPriorityStrategy(ISelectionStrategy[T]):
    # Chọn đối tượng có điểm ưu tiên cao nhất
    def __init__(self, scoreSelector: Callable[[T], float]):
        self.scoreSelector = scoreSelector

    def select(self, candidates: List[T]) -> T:
        if not candidates:
            raise NoSuitableItemException()
        
        bestCandidate = candidates[0]
        highestScore = self.scoreSelector(bestCandidate)
        
        for item in candidates[1:]:
            score = self.scoreSelector(item)
            if score > highestScore:
                highestScore = score
                
        return bestCandidate


class FirstAvailableStrategy(ISelectionStrategy[T]):
    # Chọn phần tử đầu tiên trong danh sách ứng viên
    def select(self, candidates: List[T]) -> T:
        if not candidates:
            return None
        return candidates[0]


# =============================================================================================
#  DỊCH VỤ CẤP PHÁT TỔNG QUÁT
#  – Đảm bảo khi có thêm thiết bị mới, lớp này không cần sửa mã.
# =============================================================================================
T_Device = TypeVar('T_Device', bound=TeachingDevice)

class AllocationService(Generic[T_Device]):
    def __init__(self, repository: IRepository[T_Device], strategy: ISelectionStrategy[T_Device]):
        self.repository = repository
        self.strategy = strategy

    def changeStrategy(self, newStrategy: ISelectionStrategy[T_Device]):
        self.strategy = newStrategy
        print("  [*] Đã thay đổi chiến lược lựa chọn thành công.")

    def allocate(self, additionalCondition: Callable[[T_Device], bool] = lambda d: True) -> T_Device:
        allDevices = self.repository.getAll()
        
        # Lọc các thiết bị sẵn sàng
        validCandidates = [dev for dev in allDevices if dev.isReadyForUse()]
        
        # Áp dụng chiến lược để chọn ra thiết bị tốt nhất
        selectedDevice = self.strategy.select(validCandidates)
        
        # Tiến hành cấp phát
        selectedDevice.borrow()
        return selectedDevice
