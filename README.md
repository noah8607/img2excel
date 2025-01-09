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

### [2025-01-09]: [1.2.5]
- 优化Docker镜像标签，使用阿里云容器镜像服务
- 更新Docker使用说明，确保国内环境可用
- 添加本地构建脚本 local_build_image.sh

### [2025-01-09]: [1.2.4]
- 优化Docker构建配置，使用国内镜像源
- 简化系统依赖安装过程

### [2025-01-09]: [1.2.3]
- 使用阿里云Python镜像
- 优化基础镜像选择

### [2025-01-09]: [1.2.2]
- 将 .windsurfrules 加入 gitignore
- 优化项目配置文件管理

### [2025-01-09]: [1.2.1]
- 优化Excel文件命名格式为"报销人_单号_时间戳"
- 改进空值处理逻辑，使用空字符串代替默认值

### [2025-01-09]: [1.2.0]
- 优化项目结构，移除无关文件到dist目录
- 修改Excel文件命名格式为"报销人_时间戳"
- 更新.gitignore配置
- 优化Docker构建，使用阿里云镜像源

### [2025-01-09]: [1.1.0]
- 优化服务初始化逻辑，实现按需加载
- 注释掉总金额验证逻辑
- 优化代码结构，提高性能
- 改进清除结果功能，确保完全重置系统状态

### [2025-01-08]: [1.0.0]
- 初始版本发布
- 实现基本的报销单识别功能
- 支持Excel导出和MinIO存储

## Docker 使用说明

### 方式一：从阿里云镜像仓库拉取（推荐）
```bash
# 拉取最新版本
docker pull registry.cn-hangzhou.aliyuncs.com/img2excel/expense-report:latest

# 运行容器
docker run -p 8501:8501 --env-file .env registry.cn-hangzhou.aliyuncs.com/img2excel/expense-report:latest
```

### 方式二：本地构建
```bash
# 使用构建脚本（推荐）
chmod +x local_build_image.sh
./local_build_image.sh 1.2.5  # 指定版本号

# 或手动构建
docker build -t registry.cn-hangzhou.aliyuncs.com/img2excel/expense-report:latest .
docker run -p 8501:8501 --env-file .env registry.cn-hangzhou.aliyuncs.com/img2excel/expense-report:latest
```

### 方式三：直接运行
```bash
chmod +x start.sh
./start.sh
```

## 注意事项

1. 确保环境变量配置正确
2. 启动前确保MinIO服务器正常运行
3. 上传的图片格式支持：jpg、jpeg、png
4. Excel文件下载链接有效期为7天
5. 使用Docker时，建议优先使用阿里云镜像源以提高下载速度

## 许可证

MIT License
