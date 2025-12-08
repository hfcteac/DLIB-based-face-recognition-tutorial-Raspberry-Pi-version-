# DIB-based Face Recognition Tutorial - Raspberry Pi Version

基于 dlib 的人脸识别教程 - 树莓派版本

毕业设计关于 dlib 人脸识别的部分教程和代码备份

---

## 📖 项目简介 / Project Overview

本项目提供了一套完整的基于 dlib 的人脸识别系统，专门针对树莓派平台优化。包含详细的教程文档和可直接运行的代码。

This project provides a complete dlib-based face recognition system optimized for Raspberry Pi, including detailed tutorials and ready-to-run code.

### 主要特性 / Key Features

- ✅ 实时人脸检测与识别
- ✅ 适配树莓派性能优化
- ✅ 详细的中英文教程
- ✅ 完整的代码注释
- ✅ 易于扩展和定制

- ✅ Real-time face detection and recognition
- ✅ Optimized for Raspberry Pi performance
- ✅ Detailed bilingual tutorials
- ✅ Fully commented code
- ✅ Easy to extend and customize

---

## 📂 项目结构 / Project Structure

```
.
├── code/                       # 代码备份 / Code Backup
│   ├── face_detection.py      # 人脸检测脚本
│   ├── face_encoding.py       # 人脸编码脚本
│   ├── face_recognition.py    # 人脸识别主程序
│   ├── requirements.txt       # Python依赖
│   └── README.md             # 代码说明
│
├── tutorials/                  # 教程备份 / Tutorials Backup
│   ├── installation_guide.md  # 安装指南
│   ├── usage_tutorial.md      # 使用教程
│   ├── configuration_guide.md # 配置指南
│   ├── images/               # 教程图片
│   └── README.md             # 教程索引
│
└── README.md                  # 本文件
```

---

## 🚀 快速开始 / Quick Start

### 1. 克隆项目 / Clone Repository

```bash
git clone https://github.com/hfcteac/DIB-based-face-recognition-tutorial-Raspberry-Pi-version-.git
cd DIB-based-face-recognition-tutorial-Raspberry-Pi-version-
```

### 2. 安装依赖 / Install Dependencies

```bash
cd code
pip install -r requirements.txt
```

详细安装步骤请查看 [安装指南](tutorials/installation_guide.md)

For detailed installation steps, see [Installation Guide](tutorials/installation_guide.md)

### 3. 下载模型 / Download Models

```bash
mkdir models
cd models
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
wget http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
bunzip2 dlib_face_recognition_resnet_model_v1.dat.bz2
```

### 4. 准备人脸数据 / Prepare Face Data

```bash
mkdir faces
# 在 faces/ 目录下为每个人创建文件夹并添加照片
# Create a folder for each person in faces/ and add photos
```

### 5. 生成编码 / Generate Encodings

```bash
python face_encoding.py
```

### 6. 运行识别 / Run Recognition

```bash
python face_recognition.py
```

---

## 📚 文档 / Documentation

### 代码文档 / Code Documentation

- [代码说明](code/README.md) - 代码结构和使用方法
- [Code Documentation](code/README.md) - Code structure and usage

### 教程文档 / Tutorial Documentation

1. **[安装指南](tutorials/installation_guide.md)** - 系统安装步骤
   - [Installation Guide](tutorials/installation_guide.md) - System setup steps

2. **[使用教程](tutorials/usage_tutorial.md)** - 详细使用说明
   - [Usage Tutorial](tutorials/usage_tutorial.md) - Detailed usage instructions

3. **[配置指南](tutorials/configuration_guide.md)** - 参数配置详解
   - [Configuration Guide](tutorials/configuration_guide.md) - Parameter configuration

---

## 💡 功能说明 / Features

### 人脸检测 / Face Detection
实时检测摄像头画面中的人脸，绘制边界框。

Real-time detection of faces in camera feed with bounding boxes.

### 人脸编码 / Face Encoding
从图片中提取人脸特征，生成128维特征向量。

Extract face features from images, generate 128-dimensional feature vectors.

### 人脸识别 / Face Recognition
匹配检测到的人脸与已知人脸，显示识别结果。

Match detected faces with known faces and display recognition results.

---

## 🔧 系统要求 / System Requirements

### 硬件 / Hardware
- 树莓派 3B+ / 4B (推荐 4B)
- 摄像头模块或 USB 摄像头
- 至少 1GB RAM (推荐 2GB+)

- Raspberry Pi 3B+ / 4B (4B recommended)
- Camera module or USB camera
- At least 1GB RAM (2GB+ recommended)

### 软件 / Software
- Raspberry Pi OS (Debian-based)
- Python 3.7+
- OpenCV
- dlib
- numpy

---

## 📝 使用示例 / Usage Examples

### 仅检测人脸 / Face Detection Only

```bash
python code/face_detection.py
```

### 生成人脸编码 / Generate Face Encodings

```bash
python code/face_encoding.py
```

### 实时人脸识别 / Real-time Face Recognition

```bash
python code/face_recognition.py
```

---

## ⚙️ 配置建议 / Configuration Recommendations

### 树莓派 3B/3B+
- 分辨率: 320x240
- 处理间隔: 每10帧
- 识别容差: 0.6

- Resolution: 320x240
- Process interval: Every 10 frames
- Tolerance: 0.6

### 树莓派 4B
- 分辨率: 640x480
- 处理间隔: 每5帧
- 识别容差: 0.6

- Resolution: 640x480
- Process interval: Every 5 frames
- Tolerance: 0.6

详细配置请参考 [配置指南](tutorials/configuration_guide.md)

For detailed configuration, see [Configuration Guide](tutorials/configuration_guide.md)

---

## 🐛 故障排除 / Troubleshooting

遇到问题？查看：

Having issues? Check:

1. [安装指南 - 故障排除](tutorials/installation_guide.md#故障排除--troubleshooting)
2. [使用教程 - 常见问题](tutorials/usage_tutorial.md#常见问题--faq)
3. 项目 Issues 页面

---

## 🤝 贡献 / Contributing

欢迎贡献！如果您有改进建议或发现问题：

Contributions welcome! If you have improvements or find issues:

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 许可证 / License

本项目用于教育和学习目的。

This project is for educational and learning purposes.

---

## 👨‍💻 作者 / Author

毕业设计项目 - 基于 dlib 的人脸识别系统

Graduation Project - dlib-based Face Recognition System

---

## 🙏 致谢 / Acknowledgments

- [dlib](http://dlib.net/) - 人脸识别库
- [OpenCV](https://opencv.org/) - 计算机视觉库
- [Raspberry Pi Foundation](https://www.raspberrypi.org/) - 树莓派平台

---

## 📮 联系方式 / Contact

有问题或建议？欢迎：
- 提交 Issue
- 发起 Discussion
- 查看教程文档

Questions or suggestions? Feel free to:
- Submit an Issue
- Start a Discussion
- Check tutorial documentation

---

## 🌟 支持项目 / Support

如果这个项目对您有帮助，请给个 Star ⭐

If this project helps you, please give it a Star ⭐
