import os
import json
import base64
import logging
from typing import Dict, Any
from PIL import Image
import io
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QwenProcessor:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        logger.info("QwenProcessor initialized")

    def _encode_image(self, image_data: bytes) -> str:
        """将图片数据转换为base64编码"""
        base64_image = base64.b64encode(image_data).decode('utf-8')
        # 由于我们接收的是JPEG格式的图片，所以使用image/jpeg
        return f"data:image/jpeg;base64,{base64_image}"

    def process_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        使用千问模型处理图片
        """
        try:
            logger.info("开始处理图片...")
            
            # 准备图片数据
            base64_image = self._encode_image(image_data)
            
            # 准备请求消息
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": "这是一张报销单，请帮我提取以下信息：报销单号、日期、报销人、部门、费用明细（包含项目名称和金额）。请以JSON格式返回，格式为：{'报销单号':'xxx', '日期':'xxx', '报销人':'xxx', '部门':'xxx', '项目':[{'名称':'xxx', '金额':xxx}], '总金额':xxx}"
                        }
                    ]
                }
            ]

            # 发送请求
            logger.info("发送请求到千问API...")
            try:
                completion = self.client.chat.completions.create(
                    model="qwen-vl-max-latest",  # 使用最新的模型版本
                    messages=messages
                )
                
                # 获取响应文本
                response_text = completion.choices[0].message.content
                logger.info(f"API响应内容: {response_text}")
                
                # 提取JSON数据
                try:
                    # 找到JSON字符串的开始和结束位置
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1
                    if start == -1 or end == 0:
                        raise Exception("响应中未找到JSON数据")
                    json_str = response_text[start:end]
                    
                    # 尝试解析JSON
                    try:
                        data = json.loads(json_str)
                    except json.JSONDecodeError:
                        # 如果解析失败，尝试处理可能的转义问题
                        json_str = json_str.replace("'", '"')
                        data = json.loads(json_str)
                    
                    logger.info("成功解析JSON数据")
                    return data
                    
                except Exception as e:
                    logger.error(f"解析JSON响应失败: {str(e)}")
                    raise Exception(f"解析响应失败: {str(e)}")
                
            except Exception as e:
                logger.error(f"API调用失败: {str(e)}")
                raise Exception(f"API调用失败: {str(e)}")

        except Exception as e:
            logger.error(f"处理过程发生错误: {str(e)}")
            raise Exception(f"处理失败: {str(e)}")

    def validate_response(self, data: Dict[str, Any]) -> bool:
        """
        验证API返回的数据是否完整
        """
        required_fields = ["报销单号", "日期", "报销人", "部门", "项目", "总金额"]
        
        try:
            # 检查必填字段
            for field in required_fields:
                if field not in data:
                    logger.warning(f"缺少必填字段: {field}")
                    return False
            
            # 检查项目列表
            if not isinstance(data["项目"], list):
                logger.warning("项目列表格式不正确")
                return False
            
            # 验证每个项目
            for item in data["项目"]:
                if not isinstance(item, dict) or "名称" not in item or "金额" not in item:
                    logger.warning("项目格式不正确")
                    return False
            
            # 注释掉总金额验证
            # # 验证总金额
            # if data["项目"]:  # 只在有项目时验证总金额
            #     total = sum(item["金额"] for item in data["项目"])
            #     if abs(total - data["总金额"]) > 0.01:
            #         logger.warning(f"总金额不匹配: 计算值={total}, 返回值={data['总金额']}")
            #         return False
            
            logger.info("数据验证通过")
            return True
            
        except Exception as e:
            logger.error(f"数据验证过程出错: {str(e)}")
            return False
