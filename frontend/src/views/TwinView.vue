<template>
  <div style="width: 100%; height: 100%; display: flex;">
    <!-- 左侧3D可视化区域（80%） -->
    <div style="flex: 8; height: 100%;">
      <Twin3D ref="twin3dRef" />
    </div>
    <!-- 右侧科技风数据面板（20%） -->
    <div style="flex: 2; height: 100%; padding: 16px; display: flex; flex-direction: column; gap: 16px;">
      <!-- 设备状态面板 -->
      <div class="twin-panel">
        <div class="twin-title">设备运行状态</div>
        <div class="param-item">
          <div class="param-name">工作电压 (V)</div>
          <div class="param-value">{{ deviceData.voltage || 220.00 }}</div>
        </div>
        <div class="param-item">
          <div class="param-name">工作温度 (℃)</div>
          <div class="param-value">{{ deviceData.temperature || 30.00 }}</div>
        </div>
        <div class="param-item">
          <div class="param-name">水下深度 (m)</div>
          <div class="param-value">{{ deviceData.depth || 100.00 }}</div>
        </div>
        <div class="param-item">
          <div class="param-name">设备状态</div>
          <div class="param-value" :style="{color: deviceData.status === 'normal' ? '#00FF00' : '#FF0000'}">
            {{ deviceData.status === 'normal' ? '正常' : '异常' }}
          </div>
        </div>
      </div>

      <!-- 信道参数面板 -->
      <div class="twin-panel">
        <div class="twin-title">水声信道参数</div>
        <div class="param-item">
          <div class="param-name">传播距离 (km)</div>
          <div class="param-value">{{ distance || 10.00 }}</div>
        </div>
        <div class="param-item">
          <div class="param-name">传播损失 (dB)</div>
          <div class="param-value">{{ channelData.propagation_loss || 81.25 }}</div>
        </div>
        <div class="param-item">
          <div class="param-name">多径时延差 (ms)</div>
          <div class="param-value">{{ channelData.delay_diff || 0.85 }}</div>
        </div>
        <div class="param-item">
          <div class="param-name">通信误码率</div>
          <div class="param-value">{{ channelData.ber || 0.0025 }}</div>
        </div>
      </div>

      <!-- 实时曲线面板 -->
      <div class="twin-panel" style="flex: 1; display: flex; flex-direction: column; gap: 8px;">
        <div class="twin-title">仿真数据曲线</div>
        <div ref="plChartRef" style="width: 100%; height: 45%;"></div>
        <div ref="berChartRef" style="width: 100%; height: 45%;"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import Twin3D from '@/components/Twin3D.vue'
import { twinApi } from '@/api/request.js'

// 3D组件引用
const twin3dRef = ref(null)
// 数据存储
const deviceData = ref({})
const channelData = ref({})
const distance = ref(10) // 初始传播距离10km
const historyData = ref([])
// ECharts实例
const plChartRef = ref(null)
const berChartRef = ref(null)
let plChart, berChart;
// 定时器（实时请求数据）
let timer = null;

// 获取实时融合数据
const getRealTimeData = async () => {
  try {
    const res = await twinApi.getRealTimeData(distance.value);
    if (res.data.code === 200) {
      deviceData.value = res.data.data.device;
      channelData.value = res.data.data.channel;
      distance.value = res.data.data.distance;
      // 更新3D设备状态（异常变红）
      twin3dRef.value.updateDeviceStatus(deviceData.value.status);
      // 获取历史数据更新曲线
      getHistoryData();
    }
  } catch (err) {
    console.error('获取实时数据失败：', err);
  }
}

// 获取历史数据（绘制曲线）
const getHistoryData = async () => {
  try {
    const res = await twinApi.getHistoryData(30);
    if (res.data.code === 200) {
      historyData.value = res.data.data;
      updateECharts();
    }
  } catch (err) {
    console.error('获取历史数据失败：', err);
  }
}

// 初始化ECharts
const initECharts = () => {
  // 传播损失曲线
  plChart = echarts.init(plChartRef.value);
  plChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { top: 10, right: 10, bottom: 30, left: 30 },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: '#87CEEB' } },
      axisLabel: { color: '#fff' }
    },
    yAxis: {
      type: 'value',
      name: '传播损失 (dB)',
      nameTextStyle: { color: '#00FFFF' },
      axisLine: { lineStyle: { color: '#87CEEB' } },
      axisLabel: { color: '#fff' }
    },
    series: [{
      name: '传播损失',
      type: 'line',
      data: [],
      lineStyle: { color: '#00FFFF' },
      itemStyle: { color: '#00FFFF' },
      smooth: true
    }]
  });

  // 误码率曲线
  berChart = echarts.init(berChartRef.value);
  berChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { top: 10, right: 10, bottom: 30, left: 30 },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: '#87CEEB' } },
      axisLabel: { color: '#fff' }
    },
    yAxis: {
      type: 'value',
      name: '误码率',
      nameTextStyle: { color: '#FF6666' },
      axisLine: { lineStyle: { color: '#87CEEB' } },
      axisLabel: { color: '#fff' }
    },
    series: [{
      name: '通信误码率',
      type: 'line',
      data: [],
      lineStyle: { color: '#FF6666' },
      itemStyle: { color: '#FF6666' },
      smooth: true
    }]
  });
}

// 更新ECharts数据
const updateECharts = () => {
  if (!plChart || !berChart || historyData.value.length === 0) return;
  // 处理x轴数据（时间戳简化）
  const xData = historyData.value.map(item => {
    return item.time.split(' ')[1].substring(0, 8);
  });
  // 传播损失数据
  const plData = historyData.value.map(item => item.propagation_loss);
  // 误码率数据
  const berData = historyData.value.map(item => item.ber);

  // 更新配置
  plChart.setOption({ xAxis: { data: xData }, series: [{ data: plData }] });
  berChart.setOption({ xAxis: { data: xData }, series: [{ data: berData }] });
}

// 窗口自适应ECharts
const onEChartsResize = () => {
  plChart?.resize();
  berChart?.resize();
}

// 挂载时初始化
onMounted(() => {
  initECharts();
  getRealTimeData();
  // 每3秒请求一次实时数据，模拟实时更新
  timer = setInterval(getRealTimeData, 3000);
  window.addEventListener('resize', onEChartsResize);
})

// 卸载时销毁
onUnmounted(() => {
  clearInterval(timer);
  window.removeEventListener('resize', onEChartsResize);
  plChart?.dispose();
  berChart?.dispose();
})
</script>