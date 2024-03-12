
# DoxBox - ⚡️比特币闪电网络照片盒

<p align="center">
<img src="https://raw.githubusercontent.com/j0sh21/DoxBox/main/docs/images/Box.jpeg" width="200">
</p>

DoxBox 通过其 [LNbits](https://github.com/lnbits/lnbits) 钱包接收比特币闪电支付来打印捕获的照片。
你可以在任何婚礼、会议、聚会或节日上设置它。我们以模块化的方式构建它，以便你可以轻松地随身携带。


## 硬件要求

- **Raspberry Pi 4** 运行基于 Debian 的操作系统 [可从 Raspberry Pi 官方软件页面获取](https://www.raspberrypi.com/software/operating-systems/)。
- **DSLR 相机**：Canon EOS 450D，至少需要 1GB 的 SD 卡。如果使用其他相机，请[确保在官网上与 gphoto2 兼容](http://www.gphoto.org/proj/libgphoto2/support.php)。
- **显示器**：Waveshare 10.4 英寸 QLED 量子点电容显示屏（1600 x 720）。
- **打印机**：Xiaomi Instant Photo Printer 1S，支持 CUPS 打印系统，6 英寸照片纸。
- **LED**：4 通道 RGB LED 条，包括面包板、连接电缆和 4 个 Mosfets 控制器。
- **建筑材料**：三块 80x80cm 的胶合板；如果可能，使用激光切割器会更好。
- **组装硬件**：20 套角落磁铁（每套 2 个），40 个 4mm 直径的螺丝和 120 个 4mm 直径的螺帽来固定组件。
- **喷涂颜色**：1 罐底漆，4 罐实际颜色。


  
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/384280e0-cc6e-4bd0-9953-c318b5e12f15" height="200">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/e446af16-d840-4cbc-87f9-3d5f67b3a15d" height="200">
<img src="https://github.com/j0sh21/DoxBox/assets/63317640/4bcc6965-a1fa-41e5-8d07-cc7e3280bc58" height="200">

  
## 示例程序流程：

<img src="docs/images/flowchart.JPG" height="1100">

## 设置说明

### 关键组件

- **main.py**：作为应用程序的入口点，根据操作模式协调各个组件的执行。
- **app.py**：管理应用程序的图形用户界面 (GUI)，促进用户互动和信息显示。
- **switch.py**：处理外部 API 交互并基于接收到的数据执行特定操作，如触发其他应用程序组件。
- **img_capture.py**：与相机交互以捕获图像，下载图像并管理文件存储，利用 gphoto2。
- **print.py (进行中)**：使用 CUPS 与打印机接口打印图像，具有选择打印机和管理打印任务的功能。
- **config.py**：包含整个应用程序使用的配置设置，如 API 密钥、设备名称和文件路径。

### 安装

1. **克隆仓库**：首先克隆此仓库。

   ```sh
   git clone https://github.com/j0sh21/DoxBox.git
    ```
2. **安装依赖**：确保系统上安装了 Python，安装所需的 Python 包。

    ```sh

    pip install -r requirements.txt
    ```
    **注意**：某些组件可能需要额外的系统级依赖（例如，gphoto2, CUPS）。
   

   - 如果你想自动安装额外的系统级依赖，请运行 install.sh：
      ```sh
      cd DoxBox/install
      chmod u+x install.sh
      ./install.sh

3. **配置**：查看并更新 config/cfg.ini 中的特定设置，例如设备名称、API 密钥和文件路径。
   ```sh
   nano cfg.ini
## 使用方法

要运行应用程序，请导航到项目目录并执行 main.py：

 ```sh
python3 main.py
 ```
对于特定功能，例如捕获图像或打印，你可以运行相应的脚本（例如，对于图像捕获运行 python img_capture.py）。
示例用法

**捕获图像** 确保你的相机已连接并被系统识别，然后运行：

 ```sh
python3 img_capture.py
 ```
**打印图像**：使用打印机的名称和图像文件路径更新 print.py，然后执行：
 ```sh
 python print.py
 ```
## 许可证
该项目根据 MIT 许可证授权 - 详情见 LICENSE 文件。
欢迎为该项目做出贡献！

## 致谢
特别感谢 [Ben Arc](https://github.com/arcbtc) 的 [LNbits](https://github.com/lnbits/lnbits) 以及本项目中也使用的所有外部库和工具的维护者。

 ⚡️ 如果你喜欢 DoxBox，请 [打赏该项目](https://legend.lnbits.com/lnurlp/link/4Wc7ZE) ⚡️

