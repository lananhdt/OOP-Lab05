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
