<template>
  <div ref="twin3dRef" class="twin-3d" style="width: 100%; height: 100%;"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'

const twin3dRef = ref(null)
let scene, camera, renderer, controls, deviceMesh;

// 初始化3D场景
const init3D = () => {
  // 1. 场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x051929); // 深海蓝背景

  // 2. 相机
  camera = new THREE.PerspectiveCamera(75, twin3dRef.value.clientWidth / twin3dRef.value.clientHeight, 0.1, 1000);
  camera.position.set(20, 20, 30);
  camera.lookAt(0, 0, 0);

  // 3. 渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(twin3dRef.value.clientWidth, twin3dRef.value.clientHeight);
  renderer.setClearColor(0x051929, 1);
  twin3dRef.value.appendChild(renderer.domElement);

  // 4. 控制器（鼠标拖拽/滚轮缩放）
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; // 阻尼效果，更丝滑
  controls.dampingFactor = 0.05;

  // 5. 灯光
  // 环境光
  const ambientLight = new THREE.AmbientLight(0x404040, 1.2);
  scene.add(ambientLight);
  // 平行光（科技蓝）
  const dirLight1 = new THREE.DirectionalLight(0x00FFFF, 1.5);
  dirLight1.position.set(10, 20, 30);
  scene.add(dirLight1);
  const dirLight2 = new THREE.DirectionalLight(0x1E90FF, 1);
  dirLight2.position.set(-10, -20, -30);
  scene.add(dirLight2);

  // 6. 绘制深海小型水声通信设备（圆柱形换能器基阵，贴合论文）
  createDevice();

  // 7. 绘制水下环境（海底平面+网格辅助）
  createEnv();

  // 8. 动画循环
  animate();
}

// 创建水声通信设备（核心孪生体）
const createDevice = () => {
  // 设备主体：圆柱形换能器基阵
  const deviceGeo = new THREE.CylinderGeometry(2, 2, 5, 32);
  // 科技蓝自发光材质
  const deviceMat = new THREE.MeshPhongMaterial({
    color: 0x00FFFF,
    emissive: 0x002244,
    emissiveIntensity: 0.8,
    shininess: 100
  });
  deviceMesh = new THREE.Mesh(deviceGeo, deviceMat);
  deviceMesh.position.set(0, 2.5, 0);
  scene.add(deviceMesh);

  // 设备底座
  const baseGeo = new THREE.CylinderGeometry(3, 3, 1, 32);
  const baseMat = new THREE.MeshPhongMaterial({ color: 0x1E90FF });
  const baseMesh = new THREE.Mesh(baseGeo, baseMat);
  baseMesh.position.set(0, 0.5, 0);
  scene.add(baseMesh);

  // 设备波束指示（扇形，体现通信方向）
  const beamGeo = new THREE.ConeGeometry(8, 20, 32, 1, true);
  const beamMat = new THREE.MeshPhongMaterial({
    color: 0x00FFFF,
    transparent: true,
    opacity: 0.2,
    side: THREE.DoubleSide
  });
  const beamMesh = new THREE.Mesh(beamGeo, beamMat);
  beamMesh.rotation.x = -Math.PI/2;
  beamMesh.position.set(0, 2.5, 0);
  scene.add(beamMesh);
}

// 创建水下环境
const createEnv = () => {
  // 海底平面
  const seaGeo = new THREE.PlaneGeometry(100, 100);
  const seaMat = new THREE.MeshPhongMaterial({ color: 0x001122, side: THREE.DoubleSide });
  const seaMesh = new THREE.Mesh(seaGeo, seaMat);
  seaMesh.rotation.x = -Math.PI/2;
  seaMesh.position.set(0, 0, 0);
  scene.add(seaMesh);

  // 网格辅助线（方便观察位置）
  const gridHelper = new THREE.GridHelper(100, 20, 0x004466, 0x002233);
  scene.add(gridHelper);

  // 坐标轴辅助线
  const axesHelper = new THREE.AxesHelper(10);
  scene.add(axesHelper);
}

// 设备状态更新（异常时变红，贴合告警逻辑）
const updateDeviceStatus = (status) => {
  if (!deviceMesh) return;
  if (status === 'abnormal') {
    deviceMesh.material.color.set(0xFF0000);
    deviceMesh.material.emissive.set(0x440000);
  } else {
    deviceMesh.material.color.set(0x00FFFF);
    deviceMesh.material.emissive.set(0x002244);
  }
}

// 动画循环
const animate = () => {
  requestAnimationFrame(animate);
  controls.update(); // 更新控制器
  if (deviceMesh) {
    deviceMesh.rotation.y += 0.01; // 设备缓慢旋转，科技感
  }
  renderer.render(scene, camera);
}

// 窗口自适应
const onWindowResize = () => {
  camera.aspect = twin3dRef.value.clientWidth / twin3dRef.value.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(twin3dRef.value.clientWidth, twin3dRef.value.clientHeight);
}

// 挂载时初始化
onMounted(() => {
  init3D();
  window.addEventListener('resize', onWindowResize);
})

// 卸载时销毁
onUnmounted(() => {
  window.removeEventListener('resize', onWindowResize);
  renderer.dispose();
  scene.clear();
})

// 暴露设备状态更新方法
defineExpose({
  updateDeviceStatus
})
</script>