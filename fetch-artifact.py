import requests
import urllib.parse

def download_from_nexus3(nexus_url, repository, group_id, artifact_id, version, packaging=None, classifier=None, username=None, password=None, download_path="."):
    """
    从Nexus 3下载文件
    
    参数:
    nexus_url: Nexus 3服务器URL (例如: http://localhost:8081)
    repository: 仓库名称
    group_id: 组ID (例如: com.example)
    artifact_id: 构件ID (例如: my-artifact)
    version: 版本号
    packaging: 文件类型 (例如: jar, war, pom, 默认为jar)
    classifier: 分类器 (例如: sources, javadoc)
    username: Nexus用户名 (可选)
    password: Nexus密码 (可选)
    download_path: 下载目录 (默认为当前目录)
    """
    
    # 设置默认值
    if packaging is None:
        packaging = "jar"
    
    # 构建搜索URL
    search_url = f"{nexus_url}/service/rest/v1/search/assets"
    
    # 构建查询参数
    params = {
        "repository": repository,
        "group": group_id,
        "name": artifact_id,
        "version": version
    }
    
    if classifier:
        params["maven.classifier"] = classifier
    
    # 认证信息
    auth = None
    if username and password:
        auth = (username, password)
    
    try:
        # 搜索构件
        response = requests.get(search_url, params=params, auth=auth)
        response.raise_for_status()
        
        data = response.json()
        
        if not data["items"]:
            print(f"未找到构件: {group_id}:{artifact_id}:{version}")
            return False
        
        # 查找匹配的构件
        for item in data["items"]:
            download_url = item["downloadUrl"]
            
            # 检查是否匹配packaging和classifier
            if packaging and packaging not in download_url:
                
import requests
import os

def download_from_nexus(base_url, repository, group_id, artifact_id, version, packaging="jar", classifier=None, username=None, password=None, output_dir="."):
    """
    从 Nexus3 下载 artifact 文件

    :param base_url: Nexus3 服务地址，例如 "http://nexus.example.com:8081"
    :param repository: Nexus 仓库名，例如 "maven-releases"
    :param group_id: Maven groupId，例如 "com.example"
    :param artifact_id: Maven artifactId，例如 "demo-app"
    :param version: 版本号，例如 "1.0.0"
    :param packaging: 文件类型，例如 "jar", "zip" (默认 jar)
    :param classifier: 可选的 classifier，例如 "sources"
    :param username: Nexus 用户名（如需要认证）
    :param password: Nexus 密码（如需要认证）
    :param output_dir: 下载目录，默认当前目录
    :return: 下载文件的本地路径
    """
    
    # groupId 转路径形式
    group_path = group_id.replace(".", "/")
    
    # 构造文件名
    if classifier:
        filename = f"{artifact_id}-{version}-{classifier}.{packaging}"
    else:
        filename = f"{artifact_id}-{version}.{packaging}"
    
    # 拼接下载 URL
    url = f"{base_url}/repository/{repository}/{group_path}/{artifact_id}/{version}/{filename}"

    # 下载
    auth = (username, password) if username and password else None
    response = requests.get(url, auth=auth, stream=True)

    if response.status_code == 200:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ 下载成功: {file_path}")
        return file_path
    else:
        raise Exception(f"❌ 下载失败: {response.status_code} - {response.text}")


# 示例调用
if __name__ == "__main__":
    download_from_nexus(
        base_url="http://nexus.example.com:8081",
        repository="maven-releases",
        group_id="com.example",
        artifact_id="demo-app",
        version="1.0.0",
        packaging="jar",
        username="admin",
        password="admin123"
    )