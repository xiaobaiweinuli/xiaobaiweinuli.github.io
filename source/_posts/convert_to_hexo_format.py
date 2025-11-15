import os
import re
import yaml
from datetime import datetime

# 定义posts目录路径
POSTS_DIR = "d:\\15268\\Desktop\\Gridea\\posts"

def convert_gridea_to_hexo(file_path):
    """
    将Gridea格式的Markdown文件转换为Hexo格式
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 查找YAML front matter
            match = re.search(r'^---\s*(.*?)\s*---(.*)$', content, re.DOTALL)
            if match:
                front_matter = match.group(1)
                body_content = match.group(2)
                
                # 解析YAML
                data = yaml.safe_load(front_matter)
                if not data:
                    return None
                
                # 创建Hexo格式的front matter
                hexo_front_matter = {}
                
                # 必需字段
                if 'title' in data:
                    hexo_front_matter['title'] = data['title']
                else:
                    # 如果没有title，使用文件名
                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    hexo_front_matter['title'] = base_name
                
                # 日期字段处理
                if 'date' in data:
                    # 确保日期格式正确
                    if isinstance(data['date'], str):
                        try:
                            # 尝试解析日期字符串
                            date_obj = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
                            hexo_front_matter['date'] = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            # 如果解析失败，使用当前时间
                            hexo_front_matter['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        hexo_front_matter['date'] = str(data['date'])
                else:
                    hexo_front_matter['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # 标签字段处理
                if 'tags' in data:
                    tags = data['tags']
                    # 确保tags是字符串列表格式
                    if isinstance(tags, str):
                        # 如果tags是字符串，尝试分割
                        hexo_front_matter['tags'] = [tag.strip() for tag in tags.split(',')]
                    elif isinstance(tags, list):
                        hexo_front_matter['tags'] = tags
                    else:
                        hexo_front_matter['tags'] = []
                else:
                    hexo_front_matter['tags'] = []
                
                # 可选字段转换
                # 分类（可以根据需要从其他字段映射或设置默认值）
                hexo_front_matter['categories'] = ['默认分类']  # 默认分类
                
                # 描述（可选，可以留空）
                hexo_front_matter['description'] = ''
                
                # 是否显示目录（可选）
                hexo_front_matter['toc'] = True
                
                # 生成新的front matter字符串
                new_front_matter = "---\n"
                for key, value in hexo_front_matter.items():
                    if isinstance(value, list):
                        # 处理数组类型（tags和categories）
                        new_front_matter += f"{key}: {value}\n"
                    else:
                        new_front_matter += f"{key}: '{value}'\n"
                new_front_matter += "---"
                
                # 组合新的文件内容
                new_content = new_front_matter + body_content
                
                return new_content
            return None
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return None

def batch_convert_files():
    """
    批量转换目录下的所有Markdown文件
    """
    converted_count = 0
    failed_count = 0
    
    # 遍历目录下的所有.md文件
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md') and filename != 'README.md':  # 排除README文件
            file_path = os.path.join(POSTS_DIR, filename)
            
            # 转换文件格式
            new_content = convert_gridea_to_hexo(file_path)
            
            if new_content:
                # 写回原文件
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"已转换: {filename}")
                    converted_count += 1
                except Exception as e:
                    print(f"写入文件 {filename} 失败: {e}")
                    failed_count += 1
            else:
                print(f"转换失败: {filename}")
                failed_count += 1
    
    print(f"\n批量转换完成!")
    print(f"成功转换: {converted_count} 个文件")
    print(f"失败: {failed_count} 个文件")

if __name__ == "__main__":
    print("开始将Gridea格式Markdown文件转换为Hexo格式...")
    print(f"处理目录: {POSTS_DIR}")
    print("=" * 50)
    batch_convert_files()