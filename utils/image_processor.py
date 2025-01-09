from PIL import Image
import io
import numpy as np

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_data: bytes) -> bytes:
        """
        预处理图像，包括调整大小、增强对比度等
        """
        # 从字节数据创建图像
        image = Image.open(io.BytesIO(image_data))
        
        # 转换为RGB模式（如果不是的话）
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 调整图像大小，保持宽高比
        max_size = 1600
        ratio = min(max_size/image.width, max_size/image.height)
        if ratio < 1:
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # 转换回字节
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', quality=95)
        return img_byte_arr.getvalue()

    @staticmethod
    def enhance_image(image_data: bytes) -> bytes:
        """
        增强图像质量
        """
        image = Image.open(io.BytesIO(image_data))
        
        # 转换为灰度图像
        gray_image = image.convert('L')
        
        # 增加对比度
        enhanced_image = Image.fromarray(np.uint8(np.clip((np.array(gray_image) - 128) * 1.2 + 128, 0, 255)))
        
        # 转换回字节
        img_byte_arr = io.BytesIO()
        enhanced_image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
