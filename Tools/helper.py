import os

from Tools.ernie import ErnieClass
from .lcs_similarity_index import lcs_similarity_index

ernie_token = os.environ.get("ERNIE_TOKEN")
llm = ErnieClass(ernie_token)

def mdpath2blocks(file_path):
    if os.path.exists(file_path) == False:
        md_lines = []
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            md_lines = f.readlines()

    # 将markdown 内容，进行拆分，如果以 "# " 或 "## " 开头，认为是一个 块 的起点
    blocks = []
    content = None
    title = None
    in_code_block = False
    for line in md_lines:
        if (line.startswith("# ") or line.startswith("## ")) and not in_code_block:
            if content is not None:
                blocks.append({
                    "title": title,
                    "content": content
                })
            content = line
            title = line
        else:
            content += line
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
    blocks.append({
        "title": title,
        "content": content
    })

    # for block in blocks:
    #     print(block)

    return blocks

def shpath2text(file_path):
    sh_content = open(file_path, "r").read()
    md_text = llm.get_llm_markdown_answer(
f"""
请帮我描述sh脚本的内容， 你不需要详细地进行说明，只是给出总结性地语句。
以Markdown格式输出。

sh文件内容是{sh_content}
一个简单的输出内容样例如下，你可以根据实际情况适当增加描述：
1. 配置环境变量等信息
2. 步骤0，进行数据预处理
3. 步骤1，进行模型训练
4. 步骤2，对模型进行均值化
5. 步骤3，对模型进行评估
6. 步骤4，导出静态模型
7. 步骤5，测试导出模型

请加上markdown文本块标识。

"""
    )
    return md_text

def get_new_titles(example_blocks, example_sh_titles, target_blocks, target_sh_titles):
    new_titles = llm.get_llm_json_answer(
f"""
请结合示例和我当前的sh文本，给出新的章节标题。
示例README.md文件和示例sh内容是对应的，你需要根据当我当前的sh文件内容，给出新的标题。
以json格式输出。

示例的README.md文件的标题是{[block["title"] for block in example_blocks]}
示例的sh文件内容是{example_sh_titles}
我当前的README.md文件的标题是{[block["title"] for block in target_blocks]}
我当前的sh文件内容是{target_sh_titles}

请以json格式返回判断结果，输出是一个列表，列表按照顺序描述了新的标题，样例格式如下：
{[
    {
        "new_title": "str，第一个新的标题，可以和原有标题保持一致",
        "old_title": "str，第一个旧的标题，如果没有，则为空字符串"
    }, {
        "new_title": "str，第二个新的标题，可以和原有标题保持一致",
        "old_title": "str，第二个旧的标题，如果没有，则为空字符串"
    }, {
        "new_title": "str，第三个新的标题，可以和原有标题保持一致",
        "old_title": "str，第三个旧的标题，如果没有，则为空字符串"
    },
]}

"""
    )

    # print(new_titles)
    return new_titles

def merge_new_titles(new_titles, blocks):
    merged_blocks = []
    for i in range(len(new_titles)):
        new_title = new_titles[i]["new_title"]
        old_title = new_titles[i]["old_title"]
        # 如果new_title不以 # 开头，不以\n结尾，则添加对应元素
        if not new_title.startswith('#'):
            new_title = '# ' + new_title
        if not new_title.endswith('\n'):
            new_title = new_title + '\n'

        content = ""
        for j in range(len(blocks)):
            similarity_index, difference_number = lcs_similarity_index(old_title.strip(), blocks[j]["title"].strip())
            if difference_number <= 3:
                content = blocks[j]["content"]
                break
        merged_blocks.append({
            "new_title": new_title,
            "title": old_title,
            "content": content
        })
    return merged_blocks

def get_informative_content(title, example_blocks):
    informative_dict = llm.get_llm_json_answer(
f"""
请帮我找到和当前章节标题关联最紧密的样例章节标题，如果没有关联紧密的参考章节标题，请帮我找到文字表述方面最具有参考性的章节的标题。
以json格式输出。

我当前的标题是{title}。
样例文档中的标题是{[block["title"] for block in example_blocks]}

请以json格式返回判断结果，输出给是如下
{{
    "informative_title": "str，样例文档中，用于参考的章节的标题"
}}

"""
    )
    informative_title = informative_dict.get("informative_title", None)
    informative_content = example_blocks[5]["content"]
    if informative_title is not None:
        for block in example_blocks:
            similarity_index, difference_number = lcs_similarity_index(informative_title.strip(), block["title"].strip())
            if difference_number <= 3:
                informative_content = block["content"]
                break
    return informative_content

def get_new_content(new_title, old_content, informative_content, sh_content):
    new_content = llm.get_llm_markdown_answer(
f"""
请帮我给一个README.md文档的一个章节补充内容。
我会提供给你一个章节名称，你需要参考原有的章节内容（可能原来的章节内容写的非常潦草，甚至为空，也有可能写的已经很完美了）、bash脚本，初次之外，我还会给你提供一个样例文字，你可以参考样例文本的表达风格进行行文。
特别的，你可能会有一些表述涉及到bash脚本的调用，请注意不要出错（原有的章节内容中可能还有一些其他的错误，请注意修改）。

需要补充的章节名称是{new_title}
原有的章节内容是{old_content}
需要补充的章节对应的bash脚本是{sh_content}
样例文本是{informative_content}

以markdown格式输出。

输出内容样例如下：

标题
章节内容

不需要添加markdown文本块标识。
"""
    , raw_flag=True)
    return new_content