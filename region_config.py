#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@description: use gemini for generate json from natural language
@file_name: region_config.py
@project: workplace
@version: 1.0
@date: 2026/4/14 21:02
@author: air
"""

import pandas as pd
import json

# ==========================================
# 第一步：解析 Excel 生成 JSON 文件
# ==========================================
def process_excel_to_json(excel_path, json_path):
    """
    读取 Excel 并转换为以地区名称为 key 的 JSON 配置文件。
    使用 dtype 强制指定字符串类型，防止 region_id (如 165) 被解析为浮点数 (165.0)
    """
    try:
        df = pd.read_excel(excel_path, dtype={'marketRegion': str, 'SiteID': str, '地区二字码': str})
    except Exception as e:
        print(f"读取 Excel 失败: {e}")
        return None

    country_dict = {}
    for _, row in df.iterrows():
        # 忽略地区名称为空的异常行
        if pd.isna(row['地区名称']):
            continue

        region_name = str(row['地区名称']).strip()

        # 提取并重命名所需的属性，处理 NaN
        country_dict[region_name] = {
            "deploy_site": str(row['部署区']).strip() if not pd.isna(row['部署区']) else "",
            "region_id": str(row['marketRegion']).strip() if not pd.isna(row['marketRegion']) else "",
            "name": str(row['地区英文名']).strip() if not pd.isna(row['地区英文名']) else "",
            "site_id": str(row['SiteID']).strip() if not pd.isna(row['SiteID']) else ""
        }

    # 保存为 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(country_dict, f, ensure_ascii=False, indent=4)

    print(f"✅ 第一步完成：Excel 已成功转化为 {json_path}")
    return country_dict


# ==========================================
# 第二步：读取 JSON 并解析多行杂乱文本
# ==========================================
def parse_text_to_structure(text_input, json_path):
    """
    读取 JSON 字典，解析输入的杂乱文本，输出层级嵌套的部署字典
    包含对以“斯坦”结尾的国家名称的自动简称兼容（如“哈萨克斯坦”兼容“哈萨克”）
    """
    counties = []
    with open(json_path, 'r', encoding='utf-8') as f:
        country_data = json.load(f)

    # ==========================================
    # 新增优化：建立国家名称别名映射表
    # ==========================================
    alias_map = { '沙特': '沙特阿拉伯' }
    for country in country_data.keys():
        # 1. 存入标准全称
        alias_map[country] = country

        # 2. 如果国家以“斯坦”结尾，自动生成去掉“斯坦”的简称作为别名
        if country.endswith("斯坦"):
            short_name = country[:-2]  # 截断最后两个字
            alias_map[short_name] = country

    # 提取所有用来匹配的名称（包括全称和简称），按长度降序排序，优先匹配全称和长名
    search_keys = sorted(list(alias_map.keys()), key=len, reverse=True)

    result = {}
    tokens = text_input.split()
    current_country = None

    for token in tokens:
        # 明确跳过以“语”结尾的语言类干扰项
        if token.endswith("语"):
            continue

        # ==========================================
        # 1. 尝试在当前词中匹配国家名称（包括简称）
        # ==========================================
        matched_country = False
        for search_key in search_keys:
            if search_key in token:
                # 无论匹配到的是“哈萨克斯坦”还是“哈萨克”，都映射回标准全称
                current_country = alias_map[search_key]
                matched_country = True
                break

        # 如果当前 token 是国家名，处理完直接进入下一个 token
        if matched_country:
            continue

        # 2. 尝试在当前词中匹配支付方式关键字
        method_match = None
        token_lower = token.lower()
        if "credit" in token_lower:
            method_match = "0"
        elif "cash" in token_lower:
            method_match = "1"
        elif "paypay" in token_lower:
            method_match = "2"

        # 3. 如果找到了支付方式，且当前已经锁定了一个国家 -> 组合数据
        if method_match is not None and current_country is not None:
            # 判断流程状态
            if "+" in token or "和" in token:
                flow = 2
            elif "非全流程" in token:
                flow = 0
            elif "全流程" in token:
                flow = 1
            else:
                flow = 2

            # 获取该标准全称国家的基础信息
            c_data = country_data[current_country]
            deploy_site = c_data.get("deploy_site")
            region_id = c_data.get("region_id")

            if deploy_site and region_id:
                # 动态初始化嵌套字典
                if deploy_site not in result:
                    result[deploy_site] = {}
                if region_id not in result[deploy_site]:
                    result[deploy_site][region_id] = {}

                # 赋值写入结果
                result[deploy_site][region_id][method_match] = flow

            # 处理完当前国家的支付信息后，重置状态
            counties.append(current_country)
            current_country = None
    print('/'.join(counties))
    return result

# ==========================================
# 测试与运行示例
# ==========================================
if __name__ == "__main__":
    # 假设你已经准备好了一个名为 data.xlsx 的文件
    # excel_file = "data.xlsx"
    # json_file = "region_config.json"
    # process_excel_to_json(excel_file, json_file)

    # ---- 以下为模拟数据测试环节 ----

    # 模拟第一步生成的 json 数据（确保测试能跑通）
    # mock_json_file = "mock_config.json"
    # mock_data = {
    #     "卡塔尔": {"deploy_site": "eu", "region_id": "165", "name": "Qatar", "site_id": "QA"},
    #     "墨西哥": {"deploy_site": "na", "region_id": "101", "name": "Mexico", "site_id": "MX"},
    #     "日本": {"deploy_site": "ap", "region_id": "201", "name": "Japan", "site_id": "JP"}
    # }
    # with open(mock_json_file, 'w', encoding='utf-8') as f:
    #     json.dump(mock_data, f, ensure_ascii=False)

    # 你的杂乱输入样本
    test_input = """
德国 英语、德语， cash全流程
    """

    # 执行第二步解析
    json_file = "region_config.json"
    final_output = parse_text_to_structure(test_input, json_file)

    print("\n✅ 第二步完成：文本解析结果如下：")
    print(json.dumps(final_output, ensure_ascii=False, indent=4))
