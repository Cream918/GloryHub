from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)
DEEPSEEK_API_KEY = "自己去申请个api ， apply deepseek api by yourself"  # 替换为你的DeepSeek API密钥


def aigc_rewrite(text):
    """调用DeepSeek API进行专业改写"""
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{
            "role": "user",
            "content": f"请对以下AI生成内容进行专业降重改写：\n1.彻底改变原句结构\n2.替换所有模板化表达\n3.增加个性化表述\n4.保持专业准确\n\n原文：{text}"
        }],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        raise ValueError(f"API请求失败: {str(e)}")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/rewrite', methods=['POST'])
def rewrite():
    text = request.json.get('text', '')
    if not text.strip():
        return jsonify({"error": "输入内容不能为空"}), 400

    try:
        rewritten = aigc_rewrite(text)
        return jsonify({
            "original": text,
            "rewritten": rewritten,
            "success": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


if __name__ == '__main__':
    # 确保模板目录存在
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
