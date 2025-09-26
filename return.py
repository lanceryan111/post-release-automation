def parse_metadata_to_map(self, metadata_file_path: str = './metadata.json') -> 'MetadataParser':
    """
    解析metadata.json文件并返回self实例
    """
    try:
        # ... 解析逻辑 ...
        
        if not all([self.version_code, self.version_name, self.package_name, self.group_id]):
            raise ValueError("Required fields are missing")
            
        print("Successfully parsed metadata")
        return self  # 返回实例本身

    except Exception as e:
        print(f"Error parsing metadata: {e}")
        return None

# 使用示例
def process_metadata():
    parser = MetadataParser()
    result = parser.parse_metadata_to_map("./metadata.json")
    
    if result:
        # 直接使用解析器实例
        next_function(result)
    else:
        print("解析失败!")

def next_function(parser: MetadataParser):
    """下一个处理函数"""
    print(f"版本号: {parser.version_code}")
    print(f"包名: {parser.package_name}")
    print(f"Group ID: {parser.group_id}")
    # ... 其他处理逻辑