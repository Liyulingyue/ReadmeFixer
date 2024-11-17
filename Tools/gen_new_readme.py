import json
from .helper import mdpath2blocks, shpath2text, get_new_titles, merge_new_titles, get_informative_content, \
    get_new_content

def prepare_data(target_path, example_path, target_sh_path, example_sh_path, save_flag=True, save_path="log.json"):
    example_blocks = mdpath2blocks(example_path)
    target_blocks = mdpath2blocks(target_path)
    example_sh_titles = shpath2text(example_sh_path)
    target_sh_titles = shpath2text(target_sh_path)

    if save_flag:
        save_dict = {
            "example_blocks": example_blocks,
            "target_blocks": target_blocks,
            "example_sh_titles": example_sh_titles,
            "target_sh_titles": target_sh_titles
        }
        json.dump(save_dict, open(save_path, "w", encoding="utf-8"), indent=4)
    return example_blocks, target_blocks, example_sh_titles, target_sh_titles

def generate_titles(example_blocks, target_blocks, example_sh_titles, target_sh_titles, save_flag=True, save_path="log.json"):
    new_titles = get_new_titles(example_blocks, example_sh_titles, target_blocks, target_sh_titles)

    if save_flag:
        save_dict = {
            "example_blocks": example_blocks,
            "target_blocks": target_blocks,
            "example_sh_titles": example_sh_titles,
            "target_sh_titles": target_sh_titles,
            "new_titles": new_titles
        }
    json.dump(save_dict, open(save_path, "w", encoding="utf-8"), indent=4)

    return new_titles

def align_titles(new_titles, target_blocks, example_blocks, save_flag=True, save_path="log.json"):
    merged_blocks = merge_new_titles(new_titles, target_blocks)

    for i in range(len(merged_blocks)):
        block = merged_blocks[i]
        # def get_informative_content(title, example_blocks):
        # return informative_content
        new_title = block['new_title']
        informative_content = get_informative_content(new_title, example_blocks)
        merged_blocks[i]['informative_content'] = informative_content

    if save_flag:
        save_dict = {
            "example_blocks": example_blocks,
            "target_blocks": target_blocks,
            "new_titles": new_titles,
            "merged_blocks": merged_blocks
        }
        json.dump(save_dict, open(save_path, "w", encoding="utf-8"), indent=4)

    return merged_blocks

def generate_content(merged_blocks, sh_content, save_flag=True, save_path="log.json"):
    for i in range(len(merged_blocks)):
        block = merged_blocks[i]
        new_title = block['new_title']
        informative_content = block['informative_content']
        old_content = block['content']
        new_content = get_new_content(new_title, old_content, informative_content, sh_content)
        merged_blocks[i]['new_content'] = new_content

    if save_flag:
        save_dict = {
            "merged_blocks": merged_blocks,
            "sh_content": sh_content
        }
        json.dump(save_dict, open(save_path, "w", encoding="utf-8"), indent=4)

    return merged_blocks

def generate_new_md(merged_blocks, new_md_path):
    error_words = "这个链接可能存在安全风险，为了保护您的设备和数据安全，请避免访问此链接。"

    full_markdown = ""

    for block in merged_blocks:
        new_title = block['new_title']
        new_content = block['new_content']
        content = block['content']
        if error_words in new_content and content != "":
            full_markdown += content
        else:
            full_markdown += new_content

        full_markdown += "\n"

    with open(new_md_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown)

