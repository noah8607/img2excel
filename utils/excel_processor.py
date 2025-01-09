import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ExcelProcessor:
    def __init__(self):
        """初始化 Excel 处理器"""
        self.columns = [
            '报销单号', '日期', '报销人', '部门', '项目名称', '金额', '总金额'
        ]

    def _format_date(self, date_str: str) -> str:
        """格式化日期字符串为标准格式"""
        try:
            # 尝试解析不同格式的日期
            date_formats = [
                '%Y年%m月%d日',
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%Y.%m.%d'
            ]
            
            for fmt in date_formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            raise ValueError(f"无法解析日期格式: {date_str}")
            
        except Exception as e:
            logger.error(f"日期格式化失败: {str(e)}")
            return date_str

    def create_excel(self, results: list, output_path: str) -> None:
        """
        根据解析结果创建 Excel 文件
        
        Args:
            results: 包含所有报销单数据的列表
            output_path: 输出文件路径
        """
        try:
            # 创建空的 DataFrame
            df = pd.DataFrame(columns=self.columns)
            
            # 处理每个报销单的数据
            for result in results:
                # 获取基本信息
                base_info = {
                    '报销单号': result['报销单号'],
                    '日期': self._format_date(result['日期']),
                    '报销人': result['报销人'],
                    '部门': result['部门']
                }
                
                # 处理每个费用项目
                for item in result['项目']:
                    row = base_info.copy()
                    row.update({
                        '项目名称': item['名称'],
                        '金额': float(item['金额']),
                        '总金额': float(result['总金额'])
                    })
                    # 添加行到 DataFrame
                    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            
            # 保存到 Excel 文件
            df.to_excel(output_path, index=False, engine='openpyxl')
            logger.info(f"Excel 文件已保存到: {output_path}")
            
        except Exception as e:
            logger.error(f"创建 Excel 文件失败: {str(e)}")
            raise
