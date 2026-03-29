# algorithm/app.py
from flask import Flask, jsonify, request
import sys
sys.path.append('./channel_model')
from thorp_model import UnderwaterAcousticChannel

app = Flask(__name__)
# 初始化信道模型（贴合深海小型水声设备）
channel = UnderwaterAcousticChannel(frequency=10)

# API1：获取指定距离的信道参数（传播损失+多径时延）
@app.route('/api/channel/params', methods=['GET'])
def get_channel_params():
    distance = float(request.args.get('distance', 10))  # 默认10km
    depth_tx = float(request.args.get('depth_tx', 100)) # 发射端深度
    depth_rx = float(request.args.get('depth_rx', 100)) # 接收端深度
    # 调用核心算法
    pl = channel.calc_propagation_loss(distance)
    multipath = channel.calc_multipath_delay(distance, depth_tx, depth_rx)
    # 计算误码率（简化版，贴合通信性能）
    ber = 0.001 * pl / 100  # 传播损失越大，误码率越高
    return jsonify({
        "code": 200,
        "data": {
            "propagation_loss": round(pl, 2),
            "direct_delay": round(multipath['direct_delay'], 4),
            "delay_diff": round(multipath['surface_delay_diff']*1000, 2), # 转ms
            "ber": round(ber, 4)
        }
    })

# API2：生成设备仿真状态（电压、温度、深度）
@app.route('/api/device/status', methods=['GET'])
def get_device_status():
    import random
    voltage = round(220 + random.uniform(-5, 5), 2)
    temperature = round(30 + random.uniform(-2, 2), 2)
    depth = round(100 + random.uniform(-10, 10), 2)
    # 模拟异常状态（随机触发，用于告警）
    status = "normal" if voltage > 215 else "abnormal"
    return jsonify({
        "code": 200,
        "data": {
            "voltage": voltage,
            "temperature": temperature,
            "depth": depth,
            "status": status
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)