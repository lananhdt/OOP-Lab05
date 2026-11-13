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
