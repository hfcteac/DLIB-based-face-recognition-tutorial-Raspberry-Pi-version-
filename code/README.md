# 代码备份 / Code Backup

## 概述 / Overview

这个目录包含了基于 dlib 的人脸识别系统的 Python 代码，适用于树莓派。

This directory contains Python code for a dlib-based face recognition system, optimized for Raspberry Pi.

## 文件说明 / File Description

### 核心脚本 / Core Scripts

- **face_detection.py** - 人脸检测脚本
  - 实时检测摄像头中的人脸
  - 绘制人脸边界框
  - Real-time face detection from camera
  - Draw bounding boxes around faces

- **face_encoding.py** - 人脸编码脚本
  - 从图片中提取人脸特征
  - 生成128维人脸特征向量
  - 保存编码供识别使用
  - Extract face features from images
  - Generate 128-dimensional face feature vectors
  - Save encodings for recognition

- **face_recognition.py** - 人脸识别主程序
  - 实时人脸识别
  - 匹配检测到的人脸与已知人脸
  - 显示识别结果
  - Real-time face recognition
  - Match detected faces with known faces
  - Display recognition results

### 配置文件 / Configuration Files

- **requirements.txt** - Python依赖包列表
  - Python dependencies list

## 使用方法 / Usage

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 下载模型文件 / Download Model Files

需要下载以下 dlib 模型文件并放置在 `models/` 目录中:

You need to download the following dlib model files and place them in the `models/` directory:

- `shape_predictor_68_face_landmarks.dat`
- `dlib_face_recognition_resnet_model_v1.dat`

### 3. 准备人脸数据 / Prepare Face Data

创建 `faces/` 目录并按以下结构组织图片:

Create a `faces/` directory and organize images as follows:

```
faces/
├── person1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
├── person2/
│   ├── image1.jpg
│   └── image2.jpg
└── person3/
    └── image1.jpg
```

### 4. 生成人脸编码 / Generate Face Encodings

```bash
python face_encoding.py
```

这将生成 `encodings.pkl` 文件。

This will generate an `encodings.pkl` file.

### 5. 运行人脸识别 / Run Face Recognition

```bash
python face_recognition.py
```

按 'q' 键退出程序。

Press 'q' to quit the program.

## 测试人脸检测 / Test Face Detection

如果只想测试人脸检测功能:

If you just want to test face detection:

```bash
python face_detection.py
```

## 注意事项 / Notes

- 确保摄像头已正确连接 / Ensure camera is properly connected
- 首次运行可能需要一些时间来加载模型 / First run may take time to load models
- 树莓派上运行速度可能较慢，建议降低处理帧率 / May run slowly on Raspberry Pi, consider reducing frame rate
- 确保光线充足以获得更好的识别效果 / Ensure good lighting for better recognition

## 系统要求 / System Requirements

- Python 3.7+
- OpenCV
- dlib
- numpy
- Raspberry Pi 3B+ 或更高版本 (推荐) / Raspberry Pi 3B+ or higher (recommended)
- 摄像头模块或 USB 摄像头 / Camera module or USB camera
