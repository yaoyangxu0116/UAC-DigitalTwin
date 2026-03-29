import { createApp } from 'vue'

const App = {
  mounted() {
    document.body.style.background = '#051929'
    document.body.style.color = '#fff'
    document.body.style.padding = '30px'
    document.body.style.margin = '0'
    document.body.style.fontFamily = 'Microsoft YaHei, sans-serif'

    document.getElementById('app').innerHTML = `
      <div class="container">
        <h1 style="color: #00ffff; font-size: 26px; margin-bottom: 30px;">
          深海小型水声通信设备数字孪生系统
        </h1>

        <div style="display: flex; gap: 24px; flex-wrap: wrap;">
          <!-- 设备状态 -->
          <div style="background-color: #092a47; border: 1px solid #00ffff; border-radius: 12px; padding: 24px; width: 340px;">
            <h2 style="color: #00ffff; margin-top: 0; font-size: 20px;">设备运行状态</h2>
            <p style="font-size: 16px; margin: 12px 0;">工作电压：220.6 V</p>
            <p style="font-size: 16px; margin: 12px 0;">设备温度：27.3 ℃</p>
            <p style="font-size: 16px; margin: 12px 0;">水下深度：122.4 m</p>
            <p style="font-size: 16px; margin: 12px 0;">运行状态：正常运行</p>
          </div>

          <!-- 水声信道参数 -->
          <div style="background-color: #092a47; border: 1px solid #00ffff; border-radius: 12px; padding: 24px; width: 340px;">
            <h2 style="color: #00ffff; margin-top: 0; font-size: 20px;">水声通信信道参数</h2>
            <p style="font-size: 16px; margin: 12px 0;">传播损失：186.8 dB</p>
            <p style="font-size: 16px; margin: 12px 0;">多径时延差：1.28 ms</p>
            <p style="font-size: 16px; margin: 12px 0;">系统误码率：0.00021</p>
            <p style="font-size: 16px; margin: 12px 0;">通信距离：10 km</p>
          </div>
        </div>
      </div>
    `
  }
}

createApp(App).mount('#app')