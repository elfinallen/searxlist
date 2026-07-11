import requests
import json
import re
import sys

def fetch_instances():
    """从 searx.space 获取所有实例数据"""
    url = "https://searx.space/data/instances.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

def parse_version(version_str):
    """
    解析 SearXNG 版本号（通常是日期格式），提取年月日并转换为元组以便正确比较大小。
    """
    match = re.search(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', str(version_str))
    if match:
        return tuple(map(int, match.groups()))
    # 无法解析的版本排在最后
    return (0, 0, 0)

def main():
    data = fetch_instances()
    instances = data.get('instances', {})
    
    instance_list = []
    for url, info in instances.items():
        url = url.strip()
        # 过滤掉非 HTTPS 的 URL
        if not url.startswith('https'):
            continue
        version = info.get('version', 'unknown')
        instance_list.append((url, version))
        
    # 按版本号降序排序（最新版在前）
    instance_list.sort(key=lambda x: parse_version(x[1]), reverse=True)
    
    output_file = 'searx.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for url, version in instance_list:
            f.write(f"{url}\n")
            
    print(f"Successfully wrote {len(instance_list)} instances to {output_file}")

if __name__ == "__main__":
    main()