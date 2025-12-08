#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸检测脚本
Face Detection Script for Raspberry Pi
使用dlib进行人脸检测
"""

import dlib
import cv2
import numpy as np


class FaceDetector:
    """人脸检测器类"""
    
    def __init__(self):
        """初始化人脸检测器"""
        # 加载dlib的人脸检测器
        self.detector = dlib.get_frontal_face_detector()
        
    def detect_faces(self, image):
        """
        检测图像中的人脸
        
        Args:
            image: 输入图像 (BGR格式)
            
        Returns:
            检测到的人脸位置列表
        """
        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = self.detector(gray, 1)
        
        return faces
    
    def draw_faces(self, image, faces):
        """
        在图像上绘制人脸框
        
        Args:
            image: 输入图像
            faces: 人脸位置列表
            
        Returns:
            绘制了人脸框的图像
        """
        output = image.copy()
        
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()
            
            # 绘制矩形框
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
        return output


def main():
    """主函数"""
    print("启动人脸检测程序...")
    
    # 初始化检测器
    detector = FaceDetector()
    
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("无法打开摄像头")
        return
    
    print("按 'q' 键退出程序")
    
    while True:
        # 读取帧
        ret, frame = cap.read()
        
        if not ret:
            print("无法读取摄像头画面")
            break
        
        # 检测人脸
        faces = detector.detect_faces(frame)
        
        # 绘制人脸框
        output = detector.draw_faces(frame, faces)
        
        # 显示结果
        cv2.putText(output, f"Faces: {len(faces)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Face Detection', output)
        
        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("程序已退出")


if __name__ == "__main__":
    main()
