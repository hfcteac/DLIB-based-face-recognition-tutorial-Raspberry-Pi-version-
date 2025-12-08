# 使用教程 / Usage Tutorial

## 树莓派人脸识别系统使用指南

本教程详细介绍如何使用基于 dlib 的人脸识别系统。

This tutorial provides detailed instructions on using the dlib-based face recognition system.

---

## 目录 / Table of Contents

1. [快速开始](#快速开始--quick-start)
2. [准备训练数据](#准备训练数据--prepare-training-data)
3. [生成人脸编码](#生成人脸编码--generate-face-encodings)
4. [运行人脸识别](#运行人脸识别--run-face-recognition)
5. [高级功能](#高级功能--advanced-features)
6. [常见问题](#常见问题--faq)

---

## 快速开始 / Quick Start

### 步骤概览

1. 准备人脸图片
2. 生成人脸编码
3. 运行识别系统

---

## 准备训练数据 / Prepare Training Data

### 1. 创建数据目录

```bash
mkdir -p faces
```

### 2. 组织人脸图片

为每个需要识别的人创建一个文件夹，文件夹名称即为该人的姓名：

```
faces/
├── 张三/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── 李四/
│   ├── photo1.jpg
│   └── photo2.jpg
└── 王五/
    ├── photo1.jpg
    ├── photo2.jpg
    └── photo3.jpg
```

### 3. 图片要求

为了获得最佳识别效果，请确保：

- ✅ **清晰度**: 图片清晰，不模糊
- ✅ **光线**: 光线充足，避免过暗或过亮
- ✅ **正面照**: 主要使用正面照片
- ✅ **单人**: 每张图片只包含一个人脸
- ✅ **分辨率**: 至少 640x480 像素
- ✅ **数量**: 每人至少 3-5 张不同角度的照片
- ❌ **避免**: 戴墨镜、口罩等遮挡物

### 4. 图片采集建议

**方法一：使用现有照片**
- 从手机或电脑中选择合适的照片
- 确保照片符合上述要求

**方法二：使用摄像头拍摄**

创建简单的拍照脚本：

```python
# capture_photos.py
import cv2
import os

def capture_photos(name, num_photos=5):
    """拍摄指定数量的照片"""
    # 创建目录
    person_dir = f"faces/{name}"
    os.makedirs(person_dir, exist_ok=True)
    
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    
    print(f"开始为 {name} 拍照")
    print(f"需要拍摄 {num_photos} 张照片")
    print("按 SPACE 键拍照，按 Q 键退出")
    
    count = 0
    
    while count < num_photos:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 显示画面
        cv2.putText(frame, f"Photos: {count}/{num_photos}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Capture Photos - Press SPACE', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # 按空格键拍照
        if key == ord(' '):
            photo_path = f"{person_dir}/photo_{count+1}.jpg"
            cv2.imwrite(photo_path, frame)
            print(f"已保存: {photo_path}")
            count += 1
        
        # 按 Q 键退出
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"完成! 共拍摄 {count} 张照片")

if __name__ == "__main__":
    name = input("请输入姓名: ")
    capture_photos(name)
```

使用方法：

```bash
python capture_photos.py
```

---

## 生成人脸编码 / Generate Face Encodings

### 1. 运行编码脚本

```bash
python code/face_encoding.py
```

### 2. 过程说明

脚本会执行以下操作：

1. 扫描 `faces/` 目录
2. 检测每张图片中的人脸
3. 提取人脸特征（128维向量）
4. 保存编码到 `encodings.pkl` 文件

### 3. 输出示例

```
人脸编码程序
==================================================
从 faces 提取人脸编码...
已编码: 张三/photo1.jpg
已编码: 张三/photo2.jpg
已编码: 张三/photo3.jpg
已编码: 李四/photo1.jpg
已编码: 李四/photo2.jpg
编码已保存到: encodings.pkl

编码统计:
  张三: 3 张图片
  李四: 2 张图片

完成!
```

### 4. 验证编码

可以使用以下脚本验证编码文件：

```python
# verify_encodings.py
import pickle

with open('encodings.pkl', 'rb') as f:
    encodings = pickle.load(f)

print("已编码的人员:")
for name, encs in encodings.items():
    print(f"  - {name}: {len(encs)} 个编码")
```

---

## 运行人脸识别 / Run Face Recognition

### 1. 启动识别系统

```bash
python code/face_recognition.py
```

### 2. 系统界面

程序启动后会显示：

- 实时摄像头画面
- 检测到的人脸边界框
- 识别结果（姓名标签）
- 帧数信息

### 3. 颜色含义

- **绿色边框**: 成功识别的已知人脸
- **红色边框**: 未识别的陌生人脸

### 4. 退出程序

按键盘上的 `Q` 键退出程序。

### 5. 性能优化

如果在树莓派上运行较慢，可以调整以下参数：

**降低摄像头分辨率**（在 `face_recognition.py` 中）:

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # 从 640 降低到 320
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # 从 480 降低到 240
```

**增加处理间隔**（在 `face_recognition.py` 中）:

```python
if frame_count % 10 == 0:  # 从 5 改为 10，每10帧处理一次
```

---

## 高级功能 / Advanced Features

### 仅进行人脸检测

如果只需要检测人脸而不需要识别：

```bash
python code/face_detection.py
```

这个脚本会：
- 实时检测人脸
- 显示检测到的人脸数量
- 绘制人脸边界框

### 调整识别容差

在 `face_recognition.py` 中修改 `tolerance` 参数：

```python
# 更严格的识别（减少误识别，但可能漏识别）
names = recognizer.recognize_faces_in_frame(frame, tolerance=0.5)

# 更宽松的识别（提高识别率，但可能增加误识别）
names = recognizer.recognize_faces_in_frame(frame, tolerance=0.7)
```

**默认值**: 0.6
- 值越小：识别越严格
- 值越大：识别越宽松

### 批量处理图片

创建批处理脚本识别照片中的人脸：

```python
# batch_recognize.py
import cv2
from face_recognition import FaceRecognizer

recognizer = FaceRecognizer(
    "models/shape_predictor_68_face_landmarks.dat",
    "models/dlib_face_recognition_resnet_model_v1.dat",
    "encodings.pkl"
)

image_path = "test_photo.jpg"
image = cv2.imread(image_path)

faces, names = recognizer.recognize_faces_in_frame(image)

for face, name in zip(faces, names):
    print(f"检测到: {name}")
    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imwrite("result.jpg", image)
print("结果已保存到 result.jpg")
```

---

## 常见问题 / FAQ

### Q1: 为什么识别率不高？

**A**: 可能的原因和解决方案：

1. **光线问题**: 确保环境光线充足
2. **照片质量**: 使用高质量的训练照片
3. **训练样本**: 增加每人的照片数量（建议5张以上）
4. **容差设置**: 调整 tolerance 参数
5. **角度问题**: 确保摄像头角度与训练照片相似

### Q2: 程序运行很慢怎么办？

**A**: 优化建议：

1. 降低摄像头分辨率
2. 增加处理帧间隔
3. 使用更强大的树莓派型号（如 4B）
4. 考虑使用 GPU 加速（需要额外配置）

### Q3: 如何添加新的人脸？

**A**: 步骤：

1. 在 `faces/` 目录创建新文件夹
2. 添加该人的照片
3. 重新运行 `face_encoding.py`
4. 新的编码会自动添加到系统中

### Q4: 可以同时识别多个人吗？

**A**: 可以！系统会自动检测和识别画面中的所有人脸。

### Q5: 识别结果可以保存吗？

**A**: 可以修改代码添加日志功能：

```python
# 在识别循环中添加
with open('recognition_log.txt', 'a') as f:
    for name in names:
        if name != "Unknown":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - 识别到: {name}\n")
```

### Q6: 如何删除某个人的数据？

**A**: 步骤：

1. 删除 `faces/` 目录中对应的文件夹
2. 重新运行 `face_encoding.py` 生成新的编码文件

---

## 使用技巧 / Tips

### 提高识别准确度

1. **多样化训练照片**: 包含不同表情、角度和光线条件
2. **定期更新**: 随着时间推移，定期添加新照片
3. **保持环境一致**: 识别环境与训练照片环境相似
4. **清理数据**: 删除模糊或质量差的训练照片

### 最佳实践

1. **定期备份**: 定期备份 `encodings.pkl` 文件
2. **测试验证**: 添加新人后进行充分测试
3. **性能监控**: 注意系统资源使用情况
4. **安全考虑**: 妥善保管人脸数据

---

## 下一步 / Next Steps

- 查看 [配置指南](configuration_guide.md) 了解高级配置
- 阅读代码注释学习实现细节
- 尝试修改和扩展功能

---

## 获取帮助 / Get Help

如遇问题，请：
1. 查看本教程的常见问题部分
2. 检查代码中的注释
3. 查阅官方文档
4. 提交 Issue 到项目仓库
