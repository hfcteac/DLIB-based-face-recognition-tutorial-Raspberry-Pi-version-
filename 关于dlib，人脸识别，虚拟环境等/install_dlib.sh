#!/bin/bash
# 树莓派安装dlib脚本

echo "开始安装dlib及其依赖项..."

# 更新系统包
echo "正在更新系统包..."
sudo apt-get update
sudo apt-get upgrade -y

# 安装必要的依赖项
echo "正在安装依赖项..."
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev
sudo apt-get install -y python3-dev python3-pip

# 增加交换空间大小（编译dlib需要大量内存）
echo "正在增加交换空间大小..."
sudo cp /etc/dphys-swapfile /etc/dphys-swapfile.bak
sudo sed -i 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=2048/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

# 安装dlib
echo "正在安装dlib（这可能需要很长时间，请耐心等待）..."
pip3 install dlib

# 检查安装结果
if python3 -c "import dlib; print('dlib 安装成功！')" &> /dev/null; then
    echo "dlib 已成功安装！"
else
    echo "标准安装方法失败，尝试使用预编译wheel..."
    # 尝试安装预编译的wheel文件
    pip3 install https://github.com/eclecticitguy/dlib-wheels/releases/download/v19.21.99/dlib-19.21.99-cp37-cp37m-linux_armv7l.whl
    
    if python3 -c "import dlib; print('dlib 安装成功！')" &> /dev/null; then
        echo "使用预编译wheel成功安装dlib！"
    else
        echo "安装失败。请考虑手动编译安装dlib。"
    fi
fi

# 恢复交换空间设置
echo "正在恢复交换空间设置..."
sudo sed -i 's/CONF_SWAPSIZE=.*/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile restart

echo "安装过程完成。"
