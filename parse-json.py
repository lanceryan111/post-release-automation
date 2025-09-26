import json
import os
from typing import Dict, Any, Optional

class MetadataParser:
    def __init__(self):
        self.version_code: Optional[str] = None
        self.version_name: Optional[str] = None
        self.package_name: Optional[str] = None
        self.symbolization: Dict[str, Any] = {}
        self.group_id: Optional[str] = None
        self.artifact_id: Optional[str] = None
        self.version_id: Optional[str] = None
        self.dynatrace: Dict[str, Any] = {}
        self.application_id: Optional[str] = None
        self.platform: Optional[str] = None  # 重命名 'as' 为 'platform'

    def deep_get(self, dictionary: Dict, path: str, default: Any = None) -> Any:
        """
        安全地获取嵌套字典中的值
        """
        keys = path.split('.')
        current = dictionary
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key)
            if current is None:
                return default
        return current if current is not None else default

    def parse_metadata_to_map(self, metadata_file_path: str = './metadata.json') -> bool:
        """
        解析metadata.json文件并存储为实例变量
        
        Args:
            metadata_file_path: metadata.json文件路径
            
        Returns:
            bool: 解析是否成功
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(metadata_file_path):
                print(f"Error: Metadata file not found at {metadata_file_path}")
                return False

            # 读取JSON文件
            with open(metadata_file_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            # 使用安全的方式提取值
            self.version_code = metadata.get("versionCode")
            self.version_name = metadata.get("versionName")
            self.package_name = metadata.get("packageName")
            self.symbolization = metadata.get("symbolization", {})
            
            # 从symbolization中提取嵌套值
            self.group_id = self.symbolization.get("groupId")
            self.artifact_id = self.symbolization.get("artifactId")
            self.version_id = self.symbolization.get("versionId")
            
            # 使用deep_get方法处理更复杂的嵌套结构
            self.group_id = self.group_id or self.deep_get(metadata, "symbolization.environment.groupId")
            self.artifact_id = self.artifact_id or self.deep_get(metadata, "symbolization.environment.artifactId")
            
            self.dynatrace = metadata.get("dynatrace", {})
            self.application_id = self.dynatrace.get("applicationId")
            self.platform = self.dynatrace.get("as")  # 使用更有意义的变量名
            
            # 如果platform为空，尝试从其他位置获取
            if not self.platform:
                self.platform = metadata.get("os", "ANDROID")  # 默认值

            # 检查必需字段
            required_fields = [
                self.version_code, 
                self.version_name, 
                self.package_name, 
                self.group_id
            ]
            
            if not all(required_fields):
                missing_fields = []
                field_names = ["version_code", "version_name", "package_name", "group_id"]
                for field, name in zip(required_fields, field_names):
                    if not field:
                        missing_fields.append(name)
                
                raise ValueError(f"One or more required metadata fields are missing: {', '.join(missing_fields)}")

            print("Successfully parsed metadata and stored as instance variables")
            
            # 打印解析结果用于调试
            self.print_parsed_data()
            
            return True

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON metadata: {e}")
            return False
        except ValueError as e:
            print(f"Validation error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error parsing metadata: {e}")
            return False

    def print_parsed_data(self) -> None:
        """打印解析后的数据用于调试"""
        print("\n=== Parsed Metadata ===")
        print(f"Version Code: {self.version_code}")
        print(f"Version Name: {self.version_name}")
        print(f"Package Name: {self.package_name}")
        print(f"Group ID: {self.group_id}")
        print(f"Artifact ID: {self.artifact_id}")
        print(f"Version ID: {self.version_id}")
        print(f"Application