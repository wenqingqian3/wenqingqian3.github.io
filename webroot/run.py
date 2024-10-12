import os
import re

html_file_path = './assets/download.html'

download_folder = './assets/download'

new_content = ""

# 遍历download目录下的子文件夹
for subdir in os.listdir(download_folder):
    subdir_path = os.path.join(download_folder, subdir)
    if os.path.isdir(subdir_path):
        # 生成 <section> 和 <h1> 标题
        new_content += f'<section>\n\t<h1>{subdir}</h1>\n\t<ul>\n'
        
        # 遍历子文件夹中的文件
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            if os.path.isfile(file_path):
                # 生成 <li> 列表项和下载链接
                new_content += f'\t\t<li><a href="./{download_folder}/{subdir}/{file}" download>{file}</a></li>\n'
        
        # 关闭 <ul> 和 <section>
        new_content += '\t</ul>\n</section>\n'


# 定义正则模式匹配 <!-- autogen --> 包围的内容
pattern = re.compile(r'(<!-- autogen -->)(.*?)(<!-- autogen -->)', re.DOTALL)

# 读取现有HTML文件
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用正则替换掉 <!-- autogen --> 包围的内容
new_html_content = re.sub(pattern, rf'\1\n{new_content}\n\3', html_content)

# 将新的内容写回HTML文件
with open(html_file_path, 'w', encoding='utf-8') as file:
    file.write(new_html_content)
