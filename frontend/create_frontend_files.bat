@echo off
chcp 65001 > nul
echo ======================================
echo 正在一键创建前端Vue3项目所有文件...
echo ======================================
echo.

:: 1. 创建根目录下的核心文件
type nul > package.json
type nul > vite.config.js
echo 已创建：package.json、vite.config.js

:: 2. 创建public文件夹+文件
mkdir public
type nul > public/index.html
echo 已创建：public/ + public/index.html

:: 3. 创建src目录及子文件夹
mkdir src
mkdir src\api
mkdir src\components
mkdir src\views
echo 已创建：src/ + api/ + components/ + views/

:: 4. 创建src下的核心文件
type nul > src\main.js
type nul > src\App.vue
type nul > src\style.css
type nul > src\api\request.js
type nul > src\components\Twin3D.vue
type nul > src\views\TwinView.vue
echo 已创建：src下所有.vue/.js/.css文件

echo.
echo ======================================
echo 前端文件全部创建完成！直接粘贴代码即可！
echo ======================================
pause