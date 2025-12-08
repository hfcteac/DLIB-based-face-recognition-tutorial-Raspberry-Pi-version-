#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸识别主程序
Face Recognition Main Script for Raspberry Pi
实时人脸识别
"""

import dlib
import cv2
import numpy as np
import pickle
import os
from face_encoding import FaceEncoder


class FaceRecognizer:
    """人脸识别器类"""
    
    def __init__(self, predictor_path, face_rec_model_path, encodings_path):
        """
        初始化人脸识别器
        
        Args:
            predictor_path: 特征点检测器模型路径
            face_rec_model_path: 人脸识别模型路径
            encodings_path: 已保存的人脸编码文件路径
        """
        # 初始化编码器
        self.encoder = FaceEncoder(predictor_path, face_rec_model_path)
        
        # 加载已保存的编码
        self.known_encodings = self.encoder.load_encodings(encodings_path)
        
        # 准备编码和标签
        self.prepare_encodings()
        
    def prepare_encodings(self):
        """准备编码数据用于识别"""
        self.encoding_list = []
        self.name_list = []
        
        for name, encodings in self.known_encodings.items():
            for encoding in encodings:
                self.encoding_list.append(encoding)
                self.name_list.append(name)
        
        print(f"加载了 {len(self.name_list)} 个人脸编码")
        
    def recognize_face(self, face_encoding, tolerance=0.6):
        """
        识别人脸
        
        Args:
            face_encoding: 待识别的人脸编码
            tolerance: 识别容差（越小越严格）
            
        Returns:
            识别出的姓名，如果未识别返回 "Unknown"
        """
        if len(self.encoding_list) == 0:
            return "Unknown"
        
        # 计算与所有已知人脸的距离
        distances = []
        for known_encoding in self.encoding_list:
            distance = np.linalg.norm(known_encoding - face_encoding)
            distances.append(distance)
        
        # 找到最小距离
        min_distance_idx = np.argmin(distances)
        min_distance = distances[min_distance_idx]
        
        # 判断是否在容差范围内
        if min_distance < tolerance:
            return self.name_list[min_distance_idx]
        else:
            return "Unknown"
    
    def recognize_faces_in_frame(self, frame, tolerance=0.6):
        """
        识别视频帧中的所有人脸
        
        Args:
            frame: 输入视频帧
            tolerance: 识别容差
            
        Returns:
            (faces, names) 元组
        """
        # 转换为RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 检测人脸
        faces = self.encoder.detector(rgb_frame, 1)
        
        # 识别每个人脸
        names = []
        for face in faces:
            encoding = self.encoder.get_face_encoding(rgb_frame, face)
            name = self.recognize_face(encoding, tolerance)
            names.append(name)
        
        return faces, names


def main():
    """主函数"""
    print("=" * 60)
    print("人脸识别系统 - Raspberry Pi 版本")
    print("=" * 60)
    
    # 模型文件路径
    predictor_path = "models/shape_predictor_68_face_landmarks.dat"
    face_rec_model_path = "models/dlib_face_recognition_resnet_model_v1.dat"
    encodings_path = "encodings.pkl"
    
    # 检查必要文件
    if not os.path.exists(predictor_path):
        print(f"错误: 找不到模型文件 {predictor_path}")
        return
    
    if not os.path.exists(face_rec_model_path):
        print(f"错误: 找不到模型文件 {face_rec_model_path}")
        return
    
    if not os.path.exists(encodings_path):
        print(f"错误: 找不到编码文件 {encodings_path}")
        print("请先运行 face_encoding.py 生成人脸编码")
        return
    
    # 初始化识别器
    print("\n初始化人脸识别器...")
    recognizer = FaceRecognizer(predictor_path, face_rec_model_path, encodings_path)
    
    # 打开摄像头
    print("打开摄像头...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("错误: 无法打开摄像头")
        return
    
    # 设置摄像头分辨率（适合树莓派）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("\n系统已启动!")
    print("按 'q' 键退出程序")
    print("=" * 60)
    
    frame_count = 0
    
    while True:
        # 读取帧
        ret, frame = cap.read()
        
        if not ret:
            print("错误: 无法读取摄像头画面")
            break
        
        # 每隔几帧进行一次识别（减少计算量）
        if frame_count % 5 == 0:
            # 识别人脸
            faces, names = recognizer.recognize_faces_in_frame(frame)
            
            # 绘制结果
            for face, name in zip(faces, names):
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()
                
                # 根据识别结果选择颜色
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                
                # 绘制矩形框
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # 绘制姓名
                cv2.rectangle(frame, (x1, y2), (x2, y2 + 30), color, -1)
                cv2.putText(frame, name, (x1 + 6, y2 + 22),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # 显示FPS信息
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # 显示结果
        cv2.imshow('Face Recognition - Press Q to quit', frame)
        
        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("\n程序已退出")


if __name__ == "__main__":
    main()
