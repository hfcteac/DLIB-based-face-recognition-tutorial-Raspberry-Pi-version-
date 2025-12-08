#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸编码脚本
Face Encoding Script for Raspberry Pi
生成和保存人脸特征编码
"""

import dlib
import cv2
import numpy as np
import pickle
import os


class FaceEncoder:
    """人脸编码器类"""
    
    def __init__(self, predictor_path, face_rec_model_path):
        """
        初始化人脸编码器
        
        Args:
            predictor_path: 68点人脸特征点检测器模型路径
            face_rec_model_path: 人脸识别模型路径
        """
        # 加载人脸检测器
        self.detector = dlib.get_frontal_face_detector()
        
        # 加载特征点检测器
        self.predictor = dlib.shape_predictor(predictor_path)
        
        # 加载人脸识别模型
        self.face_encoder = dlib.face_recognition_model_v1(face_rec_model_path)
        
    def get_face_encoding(self, image, face_location):
        """
        获取人脸编码
        
        Args:
            image: 输入图像
            face_location: 人脸位置
            
        Returns:
            128维人脸特征向量
        """
        # 获取人脸特征点
        shape = self.predictor(image, face_location)
        
        # 计算人脸编码
        face_encoding = self.face_encoder.compute_face_descriptor(image, shape)
        
        return np.array(face_encoding)
    
    def encode_faces_from_folder(self, folder_path):
        """
        从文件夹中的图片提取人脸编码
        
        Args:
            folder_path: 包含人脸图片的文件夹路径
            
        Returns:
            字典 {姓名: [编码列表]}
        """
        encodings = {}
        
        # 遍历文件夹
        for person_name in os.listdir(folder_path):
            person_path = os.path.join(folder_path, person_name)
            
            if not os.path.isdir(person_path):
                continue
            
            encodings[person_name] = []
            
            # 遍历该人的所有图片
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                
                # 读取图像
                image = cv2.imread(image_path)
                if image is None:
                    continue
                
                # 转换为RGB
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # 检测人脸
                faces = self.detector(rgb_image, 1)
                
                if len(faces) > 0:
                    # 获取第一个人脸的编码
                    encoding = self.get_face_encoding(rgb_image, faces[0])
                    encodings[person_name].append(encoding)
                    print(f"已编码: {person_name}/{image_name}")
        
        return encodings
    
    def save_encodings(self, encodings, output_path):
        """
        保存编码到文件
        
        Args:
            encodings: 编码字典
            output_path: 输出文件路径
        """
        with open(output_path, 'wb') as f:
            pickle.dump(encodings, f)
        print(f"编码已保存到: {output_path}")
    
    def load_encodings(self, input_path):
        """
        从文件加载编码
        
        Args:
            input_path: 编码文件路径
            
        Returns:
            编码字典
        """
        with open(input_path, 'rb') as f:
            encodings = pickle.load(f)
        return encodings


def main():
    """主函数"""
    print("人脸编码程序")
    print("=" * 50)
    
    # 模型文件路径（需要根据实际情况修改）
    predictor_path = "models/shape_predictor_68_face_landmarks.dat"
    face_rec_model_path = "models/dlib_face_recognition_resnet_model_v1.dat"
    
    # 检查模型文件是否存在
    if not os.path.exists(predictor_path):
        print(f"错误: 找不到模型文件 {predictor_path}")
        print("请下载模型文件并放置在正确的位置")
        return
    
    if not os.path.exists(face_rec_model_path):
        print(f"错误: 找不到模型文件 {face_rec_model_path}")
        print("请下载模型文件并放置在正确的位置")
        return
    
    # 初始化编码器
    encoder = FaceEncoder(predictor_path, face_rec_model_path)
    
    # 从文件夹提取编码
    faces_folder = "faces"
    
    if not os.path.exists(faces_folder):
        print(f"错误: 找不到人脸文件夹 {faces_folder}")
        print("请创建文件夹并按照以下结构组织图片:")
        print("  faces/")
        print("    ├── person1/")
        print("    │   ├── image1.jpg")
        print("    │   └── image2.jpg")
        print("    └── person2/")
        print("        └── image1.jpg")
        return
    
    print(f"从 {faces_folder} 提取人脸编码...")
    encodings = encoder.encode_faces_from_folder(faces_folder)
    
    # 保存编码
    output_path = "encodings.pkl"
    encoder.save_encodings(encodings, output_path)
    
    print("\n编码统计:")
    for name, encs in encodings.items():
        print(f"  {name}: {len(encs)} 张图片")
    
    print("\n完成!")


if __name__ == "__main__":
    main()
