import os

os.environ["ERNIE_TOKEN"] = "*************"

from Tools.gen_new_readme import *

work_dir = "F:\\PythonCodes\\PaddleSpeech\\examples\\librispeech\\asr1" # 待生成README.md的目录
target_file = "README.md" # 生成的README.md文件名
target_sh = "run.sh" # 生成的run.sh文件名

example_dir = "F:\\PythonCodes\\PaddleSpeech\\examples\\aishell\\asr0" # 参考的README.md文件路径
example_file = "README.md" # 参考的README.md文件名
example_sh = "run.sh" # 参考的run.sh文件名

target_path = os.path.join(work_dir, target_file)
example_path = os.path.join(example_dir, example_file)
target_sh_path = os.path.join(work_dir, target_sh)
example_sh_path = os.path.join(example_dir, example_sh)
new_md_path = "README.md" # 可以直接替换为 target_path

# def prepare_data(target_path, example_path, target_sh_path, example_sh_path, save_flag=True, save_path="log.json"):
#     return example_blocks, target_blocks, example_sh_titles, target_sh_titles

# 数据预处理
print("正在准备数据...")
example_blocks, target_blocks, example_sh_titles, target_sh_titles = prepare_data(target_path, example_path, target_sh_path, example_sh_path)
print("数据准备完成.")

# 生成新的README.md文件标题
print("正在生成新的标题...")
new_titles = get_new_titles(example_blocks, example_sh_titles, target_blocks, target_sh_titles)
print("标题生成完成.")

# 将新的标题和原有信息对齐
print("正在对齐新旧标题和内容...")
merged_blocks = align_titles(new_titles, target_blocks, example_blocks)
print("标题对齐完成.")

# 生成新的内容
print("正在生成新的内容...")
sh_content = open(target_sh_path, 'r', encoding='utf-8').read()
merged_blocks = generate_content(merged_blocks, sh_content)
print("内容生成完成.")

# 保存到目标文件夹下
print("正在保存到目标文件夹...")
generate_new_md(merged_blocks, new_md_path)
print("保存完成.")
