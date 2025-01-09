from minio import Minio
from minio.error import S3Error
import os
import logging
from datetime import datetime, timedelta
import io

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, host: str, access_key: str, secret_key: str):
        """初始化 MinIO 客户端"""
        try:
            # 移除可能存在的协议前缀
            host = host.replace('http://', '').replace('https://', '')
            
            self.client = Minio(
                host,
                access_key=access_key,
                secret_key=secret_key,
                secure=False,  # 如果使用 HTTPS，设置为 True
            )
            self.bucket_name = "expense-reports"
            self._ensure_bucket_exists()
            logger.info("MinIO 客户端初始化成功")
        except Exception as e:
            logger.error(f"MinIO 客户端初始化失败: {str(e)}")
            raise

    def _ensure_bucket_exists(self):
        """确保存储桶存在"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"创建存储桶: {self.bucket_name}")
            else:
                logger.info(f"存储桶已存在: {self.bucket_name}")
        except S3Error as e:
            logger.error(f"存储桶操作失败: {str(e)}")
            raise

    def _get_object_name(self, expense_user: str, expense_id: str, file_type: str) -> str:
        """生成对象名称，使用时间戳避免重复"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{file_type}/{expense_user}_{expense_id}_{timestamp}.xlsx"

    def save_excel(self, excel_data: bytes, expense_user: str = "未知", expense_id: str = "") -> str:
        """
        保存Excel文件到MinIO
        返回文件的URL
        """
        try:
            # 生成文件名
            object_name = self._get_object_name(expense_user, expense_id, "excel")
            
            # 将数据转换为流
            data_stream = io.BytesIO(excel_data)
            
            # 上传文件
            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                len(excel_data),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # 获取文件URL（7天有效）
            expiry = timedelta(days=7)
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expiry
            )
            
            logger.info(f"Excel文件已保存: {object_name}")
            return url
            
        except S3Error as e:
            logger.error(f"保存Excel文件失败: {str(e)}")
            raise

    def list_files(self, prefix: str = "excel/") -> list:
        """列出指定前缀的所有文件"""
        try:
            objects = self.client.list_objects(
                self.bucket_name,
                prefix=prefix,
                recursive=True
            )
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"列出文件失败: {str(e)}")
            raise
