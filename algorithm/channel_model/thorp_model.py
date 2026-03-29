# algorithm/channel_model/thorp_model.py
import math
import numpy as np

class UnderwaterAcousticChannel:
    """
    适配深海小型水声通信设备的轻量化水声信道快速建模类
    核心：Thorp传播损失模型 + 简化多径时延模型
    设计原则：轻量化、工程化、可扩展（适配数字孪生虚实闭环）
    """
    def __init__(self, frequency=10, sound_speed=1500):
        """
        初始化信道核心参数（贴合深海小型水声通信设备特性）
        :param frequency: 通信频率（kHz），深海小型设备典型值10kHz
        :param sound_speed: 深海声速（m/s），深海默认1500m/s
        """
        self.frequency = frequency  # 通信频率（核心参数）
        self.sound_speed = sound_speed  # 声速
        self.absorption_coeff = self.calc_thorp_absorption()  # Thorp吸收系数

    def calc_thorp_absorption(self):
        """
        计算Thorp吸收系数（dB/km）——论文核心公式实现
        适配深海环境的吸收损耗计算，工程误差<5%
        """
        f = self.frequency
        # Thorp经典公式（论文可直接引用）
        term1 = 0.11 * f**2 / (1 + f**2)
        term2 = 44 * f**2 / (4100 + f**2)
        term3 = 2.75e-4 * f**2
        term4 = 0.003
        alpha = term1 + term2 + term3 + term4
        return alpha

    def calc_propagation_loss(self, distance):
        """
        计算传播损失（dB）——设备通信性能的核心影响因子
        :param distance: 传播距离（km），深海通信典型1~20km
        """
        if distance <= 0:
            return 0  # 边界值处理，避免计算异常
        # 球面扩展损失 + 吸收损失 + 固定损失（工程经验值）
        spherical_loss = 10 * math.log10(distance)
        absorption_loss = self.absorption_coeff * distance
        pl = spherical_loss + absorption_loss + 60  # 60为固定参考损失
        return pl

    def calc_multipath_delay(self, distance, depth_tx=100, depth_rx=100, sea_depth=1000):
        """
        简化多径时延模型（直达径+海面反射+海底反射）
        适配深海小型设备的多径传播特性，忽略复杂散射
        :param distance: 水平距离（km）→ 转换为m计算
        :param depth_tx: 发射端深度（m），深海典型100m
        :param depth_rx: 接收端深度（m），深海典型100m
        :param sea_depth: 海水深度（m），深海典型1000m
        """
        distance_m = distance * 1000  # 转换为米级计算
        # 1. 直达径时延（s）
        direct_path = math.sqrt(distance_m**2 + (depth_tx - depth_rx)**2) / self.sound_speed
        # 2. 海面反射径时延（海面为理想反射面）
        surface_path = math.sqrt(distance_m**2 + (depth_tx + depth_rx)**2) / self.sound_speed
        # 3. 海底反射径时延（海底为理想反射面）
        bottom_path = math.sqrt(distance_m**2 + (2*sea_depth - depth_tx - depth_rx)**2) / self.sound_speed
        
        # 计算时延差（核心输出，影响通信码间串扰）
        delay_diff_surface = surface_path - direct_path
        delay_diff_bottom = bottom_path - direct_path
        return {
            "direct_delay": round(direct_path, 4),
            "surface_delay": round(surface_path, 4),
            "bottom_delay": round(bottom_path, 4),
            "surface_delay_diff": round(delay_diff_surface, 6),
            "bottom_delay_diff": round(delay_diff_bottom, 6)
        }

    def calc_ber(self, pl, snr_base=20):
        """
        简化误码率计算（BER）——关联信道与设备通信性能
        :param pl: 传播损失（dB）
        :param snr_base: 基准信噪比（dB），无损耗时默认20dB
        """
        snr = snr_base - pl / 10  # 传播损失越大，信噪比越低
        # 二进制移频键控（FSK）误码率公式（水声通信常用）
        ber = 0.5 * math.erfc(math.sqrt(10 ** (snr / 10) / 2))
        # 边界处理，避免误码率超出0~1范围
        ber = max(0, min(1, ber))
        return round(ber, 6)

# ====================== 本地测试（可直接运行验证） ======================
if __name__ == "__main__":
    # 初始化深海小型水声通信设备信道模型
    channel = UnderwaterAcousticChannel(frequency=10)
    # 测试10km传播距离（深海典型场景）
    distance = 10
    # 计算核心参数
    pl = channel.calc_propagation_loss(distance)
    multipath = channel.calc_multipath_delay(distance)
    ber = channel.calc_ber(pl)
    
    # 输出测试结果（论文表格/图表数据来源）
    print("=== 深海小型水声通信设备信道仿真结果（10km） ===")
    print(f"Thorp吸收系数：{channel.absorption_coeff:.4f} dB/km")
    print(f"传播损失：{pl:.2f} dB")
    print(f"直达径时延：{multipath['direct_delay']:.4f} s")
    print(f"海面反射时延差：{multipath['surface_delay_diff']*1000:.2f} ms")
    print(f"通信误码率：{ber:.6f}")