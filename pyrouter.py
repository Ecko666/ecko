from flask import Flask, request, jsonify
import requests
import logging
import traceback

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        
        try:
            # 转发请求到目标URL
            response = requests.get(f'https://hq.sinajs.cn/list={params_str}', headers=headers, timeout=10)
            response.raise_for_status()
            
            # 将GBK编码转换为UTF-8
            content = response.content.decode('gbk').encode('utf-8')
            
        except requests.exceptions.RequestException as e:
            logging.error(f"请求失败: {str(e)} - 参数: {params_str}")
            return jsonify({"error": "上游服务不可用"}), 502
        except UnicodeDecodeError as e:
            logging.error(f"解码失败: {str(e)} - 原始内容: {response.content[:100]}")
            return jsonify({"error": "数据格式错误"}), 500
        except Exception as e:
            logging.error(f"未知错误: {str(e)}\n{traceback.format_exc()}")
            return jsonify({"error": "服务器内部错误"}), 500

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
