import axios from 'axios'

// 创建axios实例，对接后端Node.js服务
const request = axios.create({
  baseURL: 'http://localhost:3000/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 数字孪生相关接口
export const twinApi = {
  // 获取实时融合数据（设备+信道）
  getRealTimeData: (distance = 10) => request.get('/twin/data', { params: { distance } }),
  // 获取历史仿真数据（用于绘制曲线）
  getHistoryData: (limit = 30) => request.get('/twin/history', { params: { limit } })
}

export default request