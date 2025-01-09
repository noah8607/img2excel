# 报销单处理系统

基于千问大模型的智能报销单处理系统，可以自动识别报销单图片中的关键信息，生成标准化的Excel报表，并将数据持久化到MinIO存储服务。

## 功能特点

- 支持多张报销单图片批量上传
- 自动识别报销单中的关键信息：
  - 报销单号
  - 日期
  - 报销人
  - 部门
  - 费用明细（项目名称和金额）
- 生成标准格式的Excel报表（REI sheet）
- 支持日期格式自动转换
- 实时显示处理结果
- 数据持久化到MinIO存储服务
  - 自动生成带有时间戳的文件名
  - 提供7天有效的下载链接
- 提供导出和清除功能

## 技术栈

- Web框架：Streamlit
- 图像处理：Pillow
- AI模型：千问API
- 存储服务：MinIO
- Excel处理：Pandas, OpenPyXL
- 其他：Python-dotenv, Requests

## 环境要求

- Python 3.11+
- MinIO服务器
- 依赖包：见 requirements.txt

## 安装说明

1. 克隆项目：
```bash
git clone [项目地址]
cd project_a
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 .env 文件并设置以下变量：
```
# API Keys
DASHSCOPE_API_KEY=your_api_key_here

# MinIO Configuration
MINIO_HOST=localhost:9000
MINIO_ACCESS_KEY=your_access_key_here
MINIO_SECRET_KEY=your_secret_key_here
```

## 使用说明

1. 启动MinIO服务器（如果是本地开发）：
```bash
docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"
```

2. 启动应用：
```bash
streamlit run streamlit_app.py
```

3. 在浏览器中访问应用（默认地址：http://localhost:8501）

4. 使用步骤：
   - 点击"上传报销单图片"选择一张或多张报销单图片
   - 系统会自动处理每张图片并显示识别结果
   - 确认所有图片处理完成后，点击"导出Excel"
   - Excel文件会自动保存到MinIO服务器，并提供下载链接
   - 如果MinIO保存失败，系统会提供本地下载选项
   - 如需清除已处理的结果，点击"清除所有结果"

## 项目结构

```
project_a/
├── streamlit_app.py    # 主应用程序
├── requirements.txt    # 项目依赖
├── .env               # 环境变量配置
└── utils/
    ├── qwen_processor.py    # 千问API处理模块
    ├── image_processor.py   # 图片处理模块
    ├── excel_processor.py   # Excel处理模块
    └── storage.py          # MinIO存储模块
```

## 更新日志

[2025-01-09]: [1.0.0] 初始版本发布
- 支持报销单图片识别
- 支持批量处理
- 支持Excel导出
- 支持MinIO存储
- 优化用户界面

[2025-01-09]: [1.1.0]
- 优化服务初始化逻辑，实现按需加载
- 注释掉总金额验证逻辑
- 优化代码结构，提高性能
- 改进清除结果功能，确保完全重置系统状态
