# /****************/  
# Mã sinh viên: 202418837  
# Họ tên: Đinh Thị Lan Anh  
# /****************/  

import threading
from abc import ABC, abstractmethod

# ==========================================
# INTERFACES & CLASSES
# ==========================================

class IDevice(ABC):
    """Abstraction chung cho mọi thiết bị thông minh."""
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

class ILockable(ABC):
    """Hành vi riêng dành cho thiết bị có thể khóa (cửa)."""
    @abstractmethod
    def lock(self):
        pass

    @abstractmethod
    def unlock(self):
        pass

class SmartLight(IDevice):
    def __init__(self, name: str):
        self.name = name

    def turn_on(self):
        print(f"{self.name}: ON")

    def turn_off(self):
        print(f"{self.name}: OFF")

class SmartFan(IDevice):
    def __init__(self, name: str):
        self.name = name

    def turn_on(self):
        print(f"{self.name}: ON")

    def turn_off(self):
        print(f"{self.name}: OFF")

class SmartDoor(IDevice, ILockable):
    def __init__(self, name: str):
        self.name = name

    def turn_on(self):
        print(f"{self.name}: OPEN")

    def turn_off(self):
        print(f"{self.name}: CLOSED")

    def lock(self):
        print(f"{self.name}: LOCKED")

    def unlock(self):
        print(f"{self.name}: UNLOCKED")

# ==========================================
# DEVICE FACTORY
# ==========================================

class DeviceFactory:
    """Tách việc tạo đối tượng cụ thể khỏi client."""
    @staticmethod
    def create(device_type: str, name: str) -> IDevice:
        # Không phân biệt chữ hoa, chữ thường, loại bỏ khoảng trắng thừa
        device_type = device_type.strip().lower()
        
        if device_type == "light":
            return SmartLight(name)
        elif device_type == "fan":
            return SmartFan(name)
        elif device_type == "door":
            return SmartDoor(name)
        else:
            raise ValueError(f"Unsupported device type: {device_type}")

# ==========================================
# HOME CONFIGURATION
# ==========================================

class HomeConfiguration:
    """Chia sẻ cấu hình ứng dụng một cách an toàn luồng (Thread-safe)."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(HomeConfiguration, cls).__new__(cls)
                # Khởi tạo giá trị mặc định
                cls._instance.home_name = "My Home"
                cls._instance.night_light_level = 30
        return cls._instance
