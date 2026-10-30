"""
/****************/
Mã sinh viên: 202418837
Họ tên: Đinh Thị Lan Anh
/****************/
"""

# =============================================================================================
#  HỆ THỐNG QUẢN LÝ THIẾT BỊ DẠY HỌC
#  – Áp dụng Event-Driven Architecture (Publisher - Subscriber)
#  – Áp dụng Delegate/Callback cho cơ chế lọc cảnh báo (Alert Filter)
# =============================================================================================

from enum import Enum
from datetime import datetime
from typing import List, Callable, Any, Optional

# =============================================================================================
#  1. ENUMS
# =============================================================================================
class DeviceStatus(Enum):
    Available = "Available"
    Borrowed = "Borrowed"
    UnderMaintenance = "Under Maintenance"

class AlertSeverity(Enum):
    Information = "Information"
    Warning = "Warning"
    Critical = "Critical"

# =============================================================================================
#  2. CLASSES DỮ LIỆU SỰ KIỆN (EVENT ARGS)
# =============================================================================================
class EventArgs:
    pass

class DeviceStatusChangedEventArgs(EventArgs):
    def __init__(self, deviceId: str, oldStatus: DeviceStatus, newStatus: DeviceStatus, changedAt: datetime):
        self.deviceId = deviceId
        self.oldStatus = oldStatus
        self.newStatus = newStatus
        self.changedAt = changedAt

class DeviceAlertEventArgs(EventArgs):
    def __init__(self, deviceId: str, message: str, severity: AlertSeverity, occurredAt: datetime):
        self.deviceId = deviceId
        self.message = message
        self.severity = severity
        self.occurredAt = occurredAt

# =============================================================================================
#  3. EXCEPTION
# =============================================================================================
class InvalidDeviceReadingException(Exception):
    def __init__(self, deviceId: str, invalidValue: int):
        self.deviceId = deviceId
        self.invalidValue = invalidValue
        super().__init__(f"Lỗi: Giá trị {invalidValue} không hợp lệ cho thiết bị {deviceId} (Phải từ 0-100).")

# =============================================================================================
#  4. GIẢ LẬP EVENT
# =============================================================================================
class Event:
    def __init__(self):
        self._handlers: List[Callable[[Any, Any], None]] = []

    def __iadd__(self, handler: Callable[[Any, Any], None]):
        if handler not in self._handlers:
            self._handlers.append(handler)
        return self

    def __isub__(self, handler: Callable[[Any, Any], None]):
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def invoke(self, sender: Any, args: Any):
        for handler in self._handlers:
            handler(sender, args)

# =============================================================================================
#  5. LỚP TRỪU TƯỢNG TEACHING DEVICE (PUBLISHER)
# =============================================================================================
class TeachingDevice:
    def __init__(self, deviceId: str, name: str):
        self._id = deviceId.strip()
        self._name = name.strip()
        self._status = DeviceStatus.Available
        
        # Events
        self.statusChanged = Event()
        self.alertRaised = Event()

    @property
    def id(self) -> str: return self._id

    @property
    def name(self) -> str: return self._name

    @property
    def status(self) -> DeviceStatus: return self._status

    def changeStatus(self, newStatus: DeviceStatus):
        if self._status == newStatus:
            return  # Không phát sinh event nếu trạng thái không đổi
            
        oldStatus = self._status
        self._status = newStatus  # Cập nhật trạng thái trước
        
        # Phát sinh event sau khi cập nhật
        self._onStatusChanged(DeviceStatusChangedEventArgs(self.id, oldStatus, newStatus, datetime.now()))

    def _raiseAlert(self, message: str, severity: AlertSeverity):
        self._onAlertRaised(DeviceAlertEventArgs(self.id, message, severity, datetime.now()))

    def _onStatusChanged(self, e: DeviceStatusChangedEventArgs):
        self.statusChanged.invoke(self, e)

    def _onAlertRaised(self, e: DeviceAlertEventArgs):
        self.alertRaised.invoke(self, e)

# =============================================================================================
#  6. CÁC LỚP THIẾT BỊ CỤ THỂ
# =============================================================================================
class ProjectorRemote(TeachingDevice):
    def __init__(self, deviceId: str, name: str):
        super().__init__(deviceId, name)
        self.batteryLevel = 100

    def updateBatteryLevel(self, newLevel: int):
        if newLevel < 0 or newLevel > 100:
            raise InvalidDeviceReadingException(self.id, newLevel)
            
        self.batteryLevel = newLevel
        if self.batteryLevel == 0:
            self._raiseAlert("Pin cạn kiệt (0%).", AlertSeverity.Critical)
        elif self.batteryLevel < 20:
            self._raiseAlert("Pin yếu dưới 20%.", AlertSeverity.Warning)

class AirConditionerRemote(TeachingDevice):
    def __init__(self, deviceId: str, name: str, assignedRoom: str):
        super().__init__(deviceId, name)
        self.assignedRoom = assignedRoom
        self.isResponsive = True

    def updateResponseState(self, isResponsive: bool):
        if self.isResponsive and not isResponsive:
            self.isResponsive = False
            self._raiseAlert(f"Mất kết nối với phòng {self.assignedRoom}.", AlertSeverity.Critical)
        elif not self.isResponsive and isResponsive:
            self.isResponsive = True
            self._raiseAlert("Đã khôi phục kết nối.", AlertSeverity.Information)

class WirelessMicrophone(TeachingDevice):
    def __init__(self, deviceId: str, name: str):
        super().__init__(deviceId, name)
        self.batteryLevel = 100
        self.signalQuality = 100

    def updateBatteryLevel(self, newLevel: int):
        if newLevel < 0 or newLevel > 100:
            raise InvalidDeviceReadingException(self.id, newLevel)
            
        self.batteryLevel = newLevel
        if self.batteryLevel == 0:
            self._raiseAlert("Micro hết sạch pin.", AlertSeverity.Critical)
        elif self.batteryLevel < 30:
            self._raiseAlert("Pin Micro yếu (< 30%).", AlertSeverity.Warning)

    def updateSignalQuality(self, newQuality: int):
        if newQuality < 0 or newQuality > 100:
            raise InvalidDeviceReadingException(self.id, newQuality)
            
        self.signalQuality = newQuality
        if self.signalQuality == 0:
            self._raiseAlert("Mất hoàn toàn tín hiệu.", AlertSeverity.Critical)
        elif self.signalQuality < 40:
            self._raiseAlert("Chất lượng tín hiệu kém (< 40%).", AlertSeverity.Warning)

# =============================================================================================
#  7. CÁC SUBSCRIBERS
# =============================================================================================
class ConsoleNotificationService:
    def handleAlert(self, sender: Any, e: DeviceAlertEventArgs):
        print(f"  [NOTIFY] [{e.severity.value}] {e.deviceId}: {e.message}")

class DeviceAuditLogger:
    def __init__(self):
        self.entries: List[str] = []

    def handleStatusChanged(self, sender: Any, e: DeviceStatusChangedEventArgs):
        logMsg = f"{e.changedAt.strftime('%H:%M:%S')} - {e.deviceId}: {e.oldStatus.value} -> {e.newStatus.value}"
        self.entries.append(logMsg)
        print(f"  [LOG] {logMsg}")

class MaintenanceService:
    def __init__(self):
        self.requests: List[str] = []

    def handleCriticalAlert(self, sender: Any, e: DeviceAlertEventArgs):
        if e.severity != AlertSeverity.Critical:
            return
        reqMsg = f"Maintenance request cho {e.deviceId}: {e.message}"
        self.requests.append(reqMsg)
        print(f"  [MAINTENANCE] {reqMsg}")

# =============================================================================================
#  8. DELEGATE/CALLBACK VÀ CHÍNH SÁCH LỌC THÔNG BÁO
# =============================================================================================
# Delegate tự định nghĩa trong Python bằng Type Hinting
AlertFilter = Callable[[DeviceAlertEventArgs], bool]
AlertAction = Callable[[DeviceAlertEventArgs], None]

class FilteredAlertSubscriber:
    def __init__(self, filterFunc: AlertFilter, actionFunc: AlertAction):
        self.filterFunc = filterFunc
        self.actionFunc = actionFunc

    def handleAlert(self, sender: Any, e: DeviceAlertEventArgs):
        if self.filterFunc(e):
            self.actionFunc(e)

# =============================================================================================
#  9. ĐIỀU PHỐI ĐĂNG KÝ (COORDINATOR)
# =============================================================================================
class DeviceMonitoringCoordinator:
    def __init__(self, devices: List[TeachingDevice], notif: ConsoleNotificationService, logger: DeviceAuditLogger, maint: MaintenanceService):
        self.devices = devices
        self.notificationService = notif
        self.auditLogger = logger
        self.maintenanceService = maint
        self._isSubscribed = False

    def subscribe(self):
        if self._isSubscribed: return
        for dev in self.devices:
            dev.statusChanged += self.auditLogger.handleStatusChanged
            dev.alertRaised += self.notificationService.handleAlert
            dev.alertRaised += self.maintenanceService.handleCriticalAlert
        self._isSubscribed = True
        print("[*] Coordinator: Đã Subscribe thành công.")

    def unsubscribe(self):
        if not self._isSubscribed: return
        for dev in self.devices:
            dev.statusChanged -= self.auditLogger.handleStatusChanged
            dev.alertRaised -= self.notificationService.handleAlert
            dev.alertRaised -= self.maintenanceService.handleCriticalAlert
        self._isSubscribed = False
        print("[*] Coordinator: Đã Unsubscribe thành công.")

    def dispose(self):
        self.unsubscribe()

# =============================================================================================
#  KIỂM THỬ
# =============================================================================================
def runTests():
    print("============= KHỞI TẠO HỆ THỐNG =============")
    proj = ProjectorRemote("PRJ-01", "Máy chiếu Sony")
    ac = AirConditionerRemote("AC-01", "Điều hòa LG", "D3-301")
    mic = WirelessMicrophone("MIC-01", "Micro Shure")
    devices = [proj, ac, mic]

    notifSvc = ConsoleNotificationService()
    loggerSvc = DeviceAuditLogger()
    maintSvc = MaintenanceService()

    coordinator = DeviceMonitoringCoordinator(devices, notifSvc, loggerSvc, maintSvc)
    coordinator.subscribe()

    print("\n1. TEST THAY ĐỔI TRẠNG THÁI (Ghi Log)")
    proj.changeStatus(DeviceStatus.Borrowed)
    proj.changeStatus(DeviceStatus.Borrowed) # Trạng thái không đổi => Không log
    ac.changeStatus(DeviceStatus.UnderMaintenance)

    print("\n2. TEST CẢNH BÁO WARNING (Chỉ Console Notif xử lý)")
    proj.updateBatteryLevel(15) 
    mic.updateBatteryLevel(25)
    mic.updateSignalQuality(35)

    print("\n3. TEST CẢNH BÁO CRITICAL (Cả Console và Maintenance xử lý)")
    proj.updateBatteryLevel(0)
    ac.updateResponseState(False) 

    print("\n4. TEST BỘ LỌC DELEGATE ĐỘC LẬP (FilteredAlertSubscriber)")
    def myFilter(e: DeviceAlertEventArgs): return e.severity == AlertSeverity.Critical
    def myAction(e: DeviceAlertEventArgs): print(f"  [FILTERED ALERT] Thiết bị {e.deviceId} cần sửa ngay!")
    
    customSubscriber = FilteredAlertSubscriber(myFilter, myAction)
    mic.alertRaised += customSubscriber.handleAlert # Đăng ký thêm
    mic.updateSignalQuality(0) # Mất sóng -> Kích hoạt Critical

    print("\n5. TEST NGOẠI LỆ GIÁ TRỊ KHÔNG HỢP LỆ")
    try:
        proj.updateBatteryLevel(-5)
    except InvalidDeviceReadingException as e:
        print(f"  [OK] Bắt lỗi: {e}")

    print("\n6. TEST HỦY ĐĂNG KÝ (UNSUBSCRIBE)")
    coordinator.dispose()
    proj.changeStatus(DeviceStatus.Available) # Sẽ không có Log nào hiện ra

if __name__ == "__main__":
    runTests()
