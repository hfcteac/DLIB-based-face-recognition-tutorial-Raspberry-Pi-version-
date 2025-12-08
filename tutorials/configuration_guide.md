# 配置指南 / Configuration Guide

## 系统配置详解

本指南详细介绍系统的各项配置选项和参数调整方法。

This guide details system configuration options and parameter tuning methods.

---

## 目录 / Table of Contents

1. [摄像头配置](#摄像头配置--camera-configuration)
2. [识别参数配置](#识别参数配置--recognition-parameters)
3. [性能优化配置](#性能优化配置--performance-optimization)
4. [模型配置](#模型配置--model-configuration)
5. [日志配置](#日志配置--logging-configuration)

---

## 摄像头配置 / Camera Configuration

### 基本设置

在 `face_recognition.py` 或 `face_detection.py` 中配置摄像头：

```python
# 打开默认摄像头（索引0）
cap = cv2.VideoCapture(0)

# 如果有多个摄像头，可以指定索引
cap = cv2.VideoCapture(1)  # 第二个摄像头
```

### 分辨率设置

```python
# 标准分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 低分辨率（提高性能）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 高分辨率（更好的质量）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
```

### 帧率设置

```python
# 设置帧率
cap.set(cv2.CAP_PROP_FPS, 30)

# 对于树莓派，建议使用较低帧率
cap.set(cv2.CAP_PROP_FPS, 15)
```

### 其他摄像头参数

```python
# 亮度
cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)  # 0-255

# 对比度
cap.set(cv2.CAP_PROP_CONTRAST, 128)    # 0-255

# 饱和度
cap.set(cv2.CAP_PROP_SATURATION, 128)  # 0-255

# 自动曝光
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
```

### 树莓派摄像头模块配置

使用 picamera 库的配置示例：

```python
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# 让摄像头预热
time.sleep(0.1)

# 捕获连续帧
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    # 处理图像...
    
    rawCapture.truncate(0)
```

---

## 识别参数配置 / Recognition Parameters

### 识别容差 (Tolerance)

容差值决定了识别的严格程度：

```python
# 在 face_recognition.py 中
tolerance = 0.6  # 默认值

# 严格模式（减少误识别）
tolerance = 0.4  # 建议范围: 0.3-0.5

# 宽松模式（提高识别率）
tolerance = 0.8  # 建议范围: 0.7-0.9
```

**推荐设置**:
- **安全场景**: 0.4-0.5
- **一般场景**: 0.5-0.6
- **便利场景**: 0.6-0.7

### 人脸检测参数

```python
# 在 FaceDetector 或 FaceEncoder 中
# 第二个参数是上采样次数，影响检测精度和速度
faces = self.detector(gray, 1)

# 不上采样（更快，但可能漏检小脸）
faces = self.detector(gray, 0)

# 上采样1次（默认，平衡性能和准确度）
faces = self.detector(gray, 1)

# 上采样2次（更准确，但更慢）
faces = self.detector(gray, 2)
```

### 处理间隔

控制每隔多少帧进行一次识别：

```python
# 在 face_recognition.py 主循环中
if frame_count % 5 == 0:  # 每5帧处理一次
    faces, names = recognizer.recognize_faces_in_frame(frame)

# 更频繁（更流畅，但更耗资源）
if frame_count % 2 == 0:  # 每2帧处理一次

# 更少频繁（节省资源）
if frame_count % 10 == 0:  # 每10帧处理一次
```

---

## 性能优化配置 / Performance Optimization

### 树莓派优化配置

创建配置文件 `config.py`:

```python
# config.py

# 树莓派 3B/3B+ 配置
RASPBERRY_PI_3_CONFIG = {
    'camera_width': 320,
    'camera_height': 240,
    'camera_fps': 15,
    'process_interval': 10,  # 每10帧处理一次
    'upsample_times': 0,     # 不上采样
    'tolerance': 0.6,
}

# 树莓派 4B 配置
RASPBERRY_PI_4_CONFIG = {
    'camera_width': 640,
    'camera_height': 480,
    'camera_fps': 20,
    'process_interval': 5,   # 每5帧处理一次
    'upsample_times': 1,     # 上采样1次
    'tolerance': 0.6,
}

# 高性能配置
HIGH_PERFORMANCE_CONFIG = {
    'camera_width': 1280,
    'camera_height': 720,
    'camera_fps': 30,
    'process_interval': 2,   # 每2帧处理一次
    'upsample_times': 1,
    'tolerance': 0.5,
}

# 选择配置
CURRENT_CONFIG = RASPBERRY_PI_3_CONFIG
```

使用配置：

```python
from config import CURRENT_CONFIG

# 在代码中使用
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CURRENT_CONFIG['camera_width'])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CURRENT_CONFIG['camera_height'])
# ...
```

### 图像预处理优化

```python
def preprocess_image(image, resize_factor=0.5):
    """
    预处理图像以提高性能
    
    Args:
        image: 输入图像
        resize_factor: 缩放因子（0-1）
    """
    # 缩小图像
    if resize_factor < 1.0:
        width = int(image.shape[1] * resize_factor)
        height = int(image.shape[0] * resize_factor)
        image = cv2.resize(image, (width, height))
    
    # 可选：直方图均衡化（改善光线条件）
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.equalizeHist(gray)
    # image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    return image
```

### 多线程优化

使用线程分离捕获和处理：

```python
import threading
import queue

frame_queue = queue.Queue(maxsize=10)

def capture_frames(cap):
    """摄像头捕获线程"""
    while True:
        ret, frame = cap.read()
        if ret:
            if not frame_queue.full():
                frame_queue.put(frame)

def process_frames(recognizer):
    """处理线程"""
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            # 处理帧...

# 启动线程
capture_thread = threading.Thread(target=capture_frames, args=(cap,))
process_thread = threading.Thread(target=process_frames, args=(recognizer,))

capture_thread.start()
process_thread.start()
```

---

## 模型配置 / Model Configuration

### 模型文件路径

在代码开头定义模型路径：

```python
# 模型文件路径配置
MODEL_CONFIG = {
    'predictor': 'models/shape_predictor_68_face_landmarks.dat',
    'face_rec': 'models/dlib_face_recognition_resnet_model_v1.dat',
    'encodings': 'encodings.pkl',
}

# 使用绝对路径
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CONFIG = {
    'predictor': os.path.join(BASE_DIR, 'models/shape_predictor_68_face_landmarks.dat'),
    'face_rec': os.path.join(BASE_DIR, 'models/dlib_face_recognition_resnet_model_v1.dat'),
    'encodings': os.path.join(BASE_DIR, 'encodings.pkl'),
}
```

### 使用不同的特征点模型

dlib 提供不同的特征点检测器：

```python
# 5点模型（更快，但精度略低）
predictor = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')

# 68点模型（标准，平衡性能和精度）
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
```

---

## 日志配置 / Logging Configuration

### 基本日志记录

```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('face_recognition.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 使用日志
logger.info("系统启动")
logger.warning("检测到陌生人")
logger.error("摄像头错误")
```

### 识别结果日志

```python
def log_recognition(name, timestamp=None):
    """记录识别结果"""
    if timestamp is None:
        timestamp = datetime.now()
    
    with open('recognition_log.csv', 'a') as f:
        f.write(f"{timestamp},{name}\n")

# 在识别循环中
for name in names:
    if name != "Unknown":
        log_recognition(name)
```

### 性能监控日志

```python
import time

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.frame_times = []
        self.start_time = None
    
    def start_frame(self):
        """开始计时"""
        self.start_time = time.time()
    
    def end_frame(self):
        """结束计时并记录"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.frame_times.append(elapsed)
            
            # 保留最近100帧的数据
            if len(self.frame_times) > 100:
                self.frame_times.pop(0)
    
    def get_fps(self):
        """获取平均FPS"""
        if not self.frame_times:
            return 0
        avg_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_time if avg_time > 0 else 0
    
    def log_stats(self):
        """记录统计信息"""
        logger.info(f"Average FPS: {self.get_fps():.2f}")

# 使用
monitor = PerformanceMonitor()

while True:
    monitor.start_frame()
    # 处理帧...
    monitor.end_frame()
    
    # 每100帧记录一次
    if frame_count % 100 == 0:
        monitor.log_stats()
```

---

## 高级配置示例

### 完整的配置文件

创建 `settings.py`:

```python
# settings.py
import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 模型配置
MODELS = {
    'predictor': os.path.join(BASE_DIR, 'models/shape_predictor_68_face_landmarks.dat'),
    'face_recognition': os.path.join(BASE_DIR, 'models/dlib_face_recognition_resnet_model_v1.dat'),
}

# 数据配置
DATA = {
    'faces_dir': os.path.join(BASE_DIR, 'faces'),
    'encodings_file': os.path.join(BASE_DIR, 'encodings.pkl'),
}

# 摄像头配置
CAMERA = {
    'device_id': 0,
    'width': 640,
    'height': 480,
    'fps': 20,
}

# 识别配置
RECOGNITION = {
    'tolerance': 0.6,
    'upsample_times': 1,
    'process_interval': 5,
}

# 显示配置
DISPLAY = {
    'show_fps': True,
    'show_confidence': False,
    'box_thickness': 2,
    'font_scale': 0.6,
}

# 日志配置
LOGGING = {
    'level': 'INFO',
    'file': 'face_recognition.log',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
}

# 性能配置
PERFORMANCE = {
    'enable_threading': False,
    'resize_factor': 1.0,
    'enable_gpu': False,
}
```

---

## 环境变量配置

使用环境变量覆盖配置：

```python
import os

# 从环境变量读取配置
TOLERANCE = float(os.getenv('FACE_RECOGNITION_TOLERANCE', '0.6'))
CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', '640'))
CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', '480'))
```

在启动程序前设置环境变量：

```bash
# Linux/Mac
export FACE_RECOGNITION_TOLERANCE=0.5
export CAMERA_WIDTH=320
export CAMERA_HEIGHT=240
python face_recognition.py

# Windows
set FACE_RECOGNITION_TOLERANCE=0.5
set CAMERA_WIDTH=320
set CAMERA_HEIGHT=240
python face_recognition.py
```

---

## 配置建议总结

### 低性能设备（树莓派 3B/3B+）
```python
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
PROCESS_INTERVAL = 10
UPSAMPLE_TIMES = 0
TOLERANCE = 0.6
```

### 中等性能设备（树莓派 4B）
```python
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
PROCESS_INTERVAL = 5
UPSAMPLE_TIMES = 1
TOLERANCE = 0.6
```

### 高性能设备
```python
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
PROCESS_INTERVAL = 2
UPSAMPLE_TIMES = 1
TOLERANCE = 0.5
```

---

## 故障排除

### 性能问题
- 降低分辨率
- 增加处理间隔
- 减少上采样次数
- 关闭不必要的功能

### 识别问题
- 调整容差值
- 增加训练样本
- 改善光线条件
- 使用更高质量的照片

---

## 参考资料

- [dlib 官方配置文档](http://dlib.net/python/index.html)
- [OpenCV 参数说明](https://docs.opencv.org/master/d4/d15/group__videoio__flags__base.html)
- [树莓派优化指南](https://www.raspberrypi.org/documentation/)
