import json
from config import AI_PROVIDER, AI_API_KEY, AI_MODEL, AI_BASE_URL


def _call_chat_api(messages):
    if not AI_API_KEY:
        print("AI API Key 未配置，跳过 AI 分析")
        return None
    try:
        if AI_PROVIDER.lower() in ("openai", "deepseek", "volcengine", "tongyi", "qwen"):
            import requests
            url = f"{AI_BASE_URL}/chat/completions"
            headers = {
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": AI_MODEL,
                "messages": messages,
                "temperature": 0.3,
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"调用 AI API 失败: {e}")
    return None


def analyze_company_profile(stock_name, raw_info=""):
    result = {
        "主营业务": "暂无法判断",
        "商业模式": "暂无法判断",
        "核心护城河": "暂无法判断",
    }
    system_prompt = """你是一位专业的A股研究员，擅长从公开资料中提取公司核心信息。
请严格区分：事实、分析、推测。资料不足时输出"暂无法判断"，不得编造。

请输出 JSON 格式：
{
  "主营业务": "用通俗易懂的语言概述公司做什么、主要产品/服务是什么",
  "商业模式": "回答这家公司靠什么赚钱，识别收入类型（产品销售/服务收费/加盟/广告/平台抽佣/授权/一次性收入/持续性收入等）",
  "核心护城河": "从技术、成本、规模、品牌、渠道、客户关系、牌照、资源、网络效应、供应链等维度分析竞争优势"
}"""
    user_prompt = f"请分析A股上市公司「{stock_name}」的公司资料。\n\n可参考的公开信息：\n{raw_info}\n\n请直接输出JSON，不要额外文字。"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    content = _call_chat_api(messages)
    if not content:
        return result
    try:
        text = content.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.strip()
        parsed = json.loads(text)
        for k in result.keys():
            if k in parsed and parsed[k]:
                result[k] = parsed[k]
    except Exception as e:
        print(f"解析 AI 返回结果失败: {e}")
    return result
