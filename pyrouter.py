from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/list', methods=['GET'])
def list_forward():
    # 从请求的URL中获取参数
    original_url = request.url
    print("Received URL:", original_url)

    # 提取参数部分
    if 'list=' in original_url:
        params = original_url.split('list=')[1]
        params = params.split(',')
        params_str = ','.join(params)
        
        headers = {
            'Referer': 'https://finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # 转发请求到目标URL
        response = requests.get(f'https://hq.sinajs.cn/list={params_str}', headers=headers)
        
        # 将GBK编码转换为UTF-8
        content = response.content.decode('gbk').encode('utf-8')
        
        # 添加CORS头部
        cors_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'text/plain; charset=utf-8'
        }
        
        # 返回转换后的内容
        return content, response.status_code, cors_headers
    else:
        return jsonify({"error": "Invalid request format"}), 400

# 添加OPTIONS请求处理
@app.route('/list', methods=['OPTIONS'])
def handle_options():
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return '', 204, cors_headers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55123)