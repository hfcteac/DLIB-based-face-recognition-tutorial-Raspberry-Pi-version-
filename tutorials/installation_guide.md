# 安装指南 / Installation Guide

## 树莓派人脸识别系统安装教程

本教程将指导您在树莓派上安装和配置基于 dlib 的人脸识别系统。

This guide will help you install and configure a dlib-based face recognition system on Raspberry Pi.

---

## 系统要求 / System Requirements

### 硬件要求 / Hardware Requirements

- **树莓派** Raspberry Pi 3B+ 或更高版本 (推荐 4B)
- **内存** 至少 1GB RAM (推荐 2GB+)
- **存储** 至少 8GB microSD 卡 (推荐 16GB+)
- **摄像头** 树莓派摄像头模块或 USB 摄像头
- **电源** 5V 2.5A+ 电源适配器

### 软件要求 / Software Requirements

- **操作系统** Raspberry Pi OS (Debian-based)
- **Python** 3.7 或更高版本
- **网络连接** 用于下载依赖包

---

## 第一步：更新系统 / Step 1: Update System

首先，更新系统包列表和已安装的包：

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

---

## 第二步：安装系统依赖 / Step 2: Install System Dependencies

安装必要的系统库和工具：

```bash
# 安装编译工具
sudo apt-get install -y build-essential cmake pkg-config

# 安装图像处理库
sudo apt-get install -y libjpeg-dev libtiff5-dev libpng-dev

# 安装视频处理库
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev

# 安装 GTK 开发库（用于 OpenCV GUI）
sudo apt-get install -y libgtk-3-dev libcanberra-gtk3-dev

# 安装数值计算库
sudo apt-get install -y libatlas-base-dev gfortran

# 安装 Python 开发包
sudo apt-get install -y python3-dev python3-pip
```

---

## 第三步：安装 Python 虚拟环境 / Step 3: Install Python Virtual Environment

创建和激活虚拟环境（推荐）：

```bash
# 安装虚拟环境工具
sudo pip3 install virtualenv

# 创建虚拟环境
python3 -m venv ~/face-recognition-env

# 激活虚拟环境
source ~/face-recognition-env/bin/activate
```

---

## 第四步：升级 pip / Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

---

## 第五步：安装 Python 依赖 / Step 5: Install Python Dependencies

### 安装 NumPy

```bash
pip install numpy
```

### 安装 OpenCV

```bash
pip install opencv-python
```

如果遇到问题，可以尝试安装预编译版本：

```bash
sudo apt-get install -y python3-opencv
```

### 安装 dlib

dlib 的安装可能需要较长时间（30分钟到1小时），因为需要从源代码编译：

```bash
# 方法1：使用 pip 安装（推荐）
pip install dlib

# 方法2：如果方法1失败，从源码安装
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake ..
cmake --build .
cd ..
python setup.py install
```

**注意**: 在树莓派 3B+ 上编译 dlib 可能需要增加交换空间：

```bash
# 临时增加交换空间
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

编译完成后可以关闭临时交换空间：

```bash
sudo swapoff /swapfile
sudo rm /swapfile
```

---

## 第六步：安装其他依赖 / Step 6: Install Other Dependencies

```bash
pip install -r requirements.txt
```

---

## 第七步：下载模型文件 / Step 7: Download Model Files

下载 dlib 预训练模型：

```bash
# 创建模型目录
mkdir -p models
cd models

# 下载 68 点人脸特征点检测器
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2

# 下载人脸识别模型
wget http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
bunzip2 dlib_face_recognition_resnet_model_v1.dat.bz2

cd ..
```

---

## 第八步：配置摄像头 / Step 8: Configure Camera

### 对于树莓派摄像头模块

启用摄像头接口：

```bash
sudo raspi-config
```

选择 `Interface Options` -> `Camera` -> `Enable`

重启树莓派：

```bash
sudo reboot
```

### 对于 USB 摄像头

USB 摄像头通常即插即用，无需额外配置。

测试摄像头：

```bash
# 列出视频设备
ls /dev/video*

# 使用 v4l2 工具测试（可选）
sudo apt-get install -y v4l-utils
v4l2-ctl --list-devices
```

---

## 第九步：验证安装 / Step 9: Verify Installation

创建测试脚本验证安装：

```python
# test_installation.py
import cv2
import dlib
import numpy as np

print("OpenCV 版本:", cv2.__version__)
print("NumPy 版本:", np.__version__)
print("dlib 版本:", dlib.__version__ if hasattr(dlib, '__version__') else "已安装")

# 测试摄像头
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✓ 摄像头可用")
    cap.release()
else:
    print("✗ 摄像头不可用")

print("\n安装验证完成!")
```

运行测试：

```bash
python test_installation.py
```

---

## 故障排除 / Troubleshooting

### 问题 1: dlib 编译失败

**解决方案**:
- 确保已安装所有编译工具
- 增加交换空间（见第五步）
- 尝试使用预编译的 wheel 文件

### 问题 2: OpenCV 无法打开摄像头

**解决方案**:
- 检查摄像头连接
- 确认摄像头权限: `sudo usermod -a -G video $USER`
- 重启系统

### 问题 3: 内存不足

**解决方案**:
- 关闭不必要的程序
- 增加交换空间
- 考虑升级到内存更大的树莓派型号

### 问题 4: 导入模块失败

**解决方案**:
- 确认虚拟环境已激活
- 重新安装相关包
- 检查 Python 版本兼容性

---

## 下一步 / Next Steps

安装完成后，请查看：
- [使用教程](usage_tutorial.md) - 学习如何使用系统
- [配置指南](configuration_guide.md) - 了解配置选项

---

## 参考资源 / References

- [dlib 官方文档](http://dlib.net/)
- [OpenCV 文档](https://docs.opencv.org/)
- [树莓派官方文档](https://www.raspberrypi.org/documentation/)
