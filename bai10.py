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

# ==========================================
# SMART HOME FACADE
# ==========================================

class SmartHomeFacade:
    """Cung cấp các thao tác mức cao (GoToWork, GoToSleep) cho nhiều thiết bị."""
    def __init__(self, light: IDevice, fan: IDevice, door: ILockable):
        self.light = light
        self.fan = fan
        self.door = door

    def go_to_work(self):
        print("\n--- Activating Go To Work Mode ---")
        self.light.turn_off()
        self.fan.turn_off()
        self.door.lock()

    def go_to_sleep(self):
        print("\n--- Activating Go To Sleep Mode ---")
        self.fan.turn_off()
        self.door.lock()
        self.light.turn_on()
        
        # Đọc cấu hình độ sáng từ Singleton
        level = HomeConfiguration().night_light_level
        print(f"Night light level: {level}%")

# ==========================================
# KIỂM THỬ
# ==========================================

def main():
    print("=== BẮT ĐẦU KIỂM THỬ T1 - T5 ===")
    
    # T1: Tạo light, fan, door - Kỳ vọng: Factory trả đúng kiểu đối tượng
    print("\n[T1] Khởi tạo thiết bị hợp lệ:")
    light = DeviceFactory.create("light", "Living room light")
    fan = DeviceFactory.create("fan", "Living room fan")
    door = DeviceFactory.create("door", "Main door")
    print(f"Đã tạo: {light.name}, {fan.name}, {door.name}")
    
    # T2: Tạo loại camera khi chưa hỗ trợ - Kỳ vọng: ValueError (tương đương ArgumentException)
    print("\n[T2] Khởi tạo thiết bị không hỗ trợ (camera):")
    try:
        camera = DeviceFactory.create("camera", "Security Camera")
    except ValueError as e:
        print(f"Bắt được ngoại lệ thành công: {e}")
        
    # T3: Lấy HomeConfiguration 2 lần - Kỳ vọng: Cùng một tham chiếu đối tượng
    print("\n[T3] Kiểm tra tính duy nhất của Singleton:")
    config1 = HomeConfiguration()
    config2 = HomeConfiguration()
    is_same = config1 is config2
    print(f"config1 và config2 có cùng tham chiếu không? -> {is_same}")
    if not is_same:
        raise Exception("Singleton implementation is incorrect.")
        
    # Chuẩn bị Facade
    facade = SmartHomeFacade(light, fan, door)
    
    # T4: Gọi GoToWork() - Kỳ vọng: Đèn tắt, quạt tắt, cửa khóa
    print("\n[T4] Kiểm tra Facade - GoToWork():")
    facade.go_to_work()
    
    # T5: Gọi GoToSleep() - Kỳ vọng: Quạt tắt, cửa khóa, đèn bật, hiện mức sáng
    print("\n[T5] Kiểm tra Facade - GoToSleep():")
    facade.go_to_sleep()

if __name__ == "__main__":
    main()
