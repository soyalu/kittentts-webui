from flask import Flask, render_template, request, jsonify, send_file
import soundfile as sf
import os
import uuid
from datetime import datetime
from logging_config import setup_logging, log_startup_info, log_shutdown_info

app = Flask(__name__)

# 设置日志
app_logger, access_logger, error_logger = setup_logging()

# 初始化KittenTTS模型
tts_model = None
available_voices = [
    'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f'
]

def load_tts_model():
    """尝试加载TTS模型"""
    global tts_model
    try:
        from kittentts import KittenTTS
        tts_model = KittenTTS("KittenML/kitten-tts-nano-0.1")
        app_logger.info("✅ TTS模型加载成功！")
        return True
    except ImportError as e:
        app_logger.error(f"❌ 导入KittenTTS失败: {e}")
        app_logger.info("请确保已安装kittentts包: pip install kittentts")
        return False
    except Exception as e:
        app_logger.error(f"❌ 模型加载失败: {e}")
        if "espeak" in str(e).lower():
            app_logger.info("💡 提示: 请安装espeak语音合成器:")
            app_logger.info("  macOS: brew install espeak")
            app_logger.info("  Ubuntu/Debian: sudo apt-get install espeak-ng")
            app_logger.info("  Windows: 下载espeak安装包")
        return False

# 尝试加载模型
model_loaded = load_tts_model()

# 创建输出目录
os.makedirs('static/audio', exist_ok=True)

# 请求日志中间件
@app.before_request
def log_request():
    """记录每个请求"""
    access_logger.info(f"请求: {request.method} {request.path} - IP: {request.remote_addr}")

@app.after_request
def log_response(response):
    """记录每个响应"""
    access_logger.info(f"响应: {request.method} {request.path} - 状态: {response.status_code}")
    return response

@app.route('/')
def index():
    app_logger.info(f"访问主页 - IP: {request.remote_addr}")
    return render_template('index.html', 
                         voices=available_voices, 
                         model_loaded=model_loaded)

@app.route('/generate', methods=['POST'])
def generate_speech():
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice = data.get('voice', 'expr-voice-2-f')
        
        app_logger.info(f"生成语音请求 - 文本长度: {len(text)}, 语音: {voice}, IP: {request.remote_addr}")
        
        if not text:
            app_logger.warning(f"生成语音失败 - 文本为空, IP: {request.remote_addr}")
            return jsonify({'error': '请输入要转换的文字'}), 400
        
        if not model_loaded:
            app_logger.error(f"生成语音失败 - 模型未加载, IP: {request.remote_addr}")
            return jsonify({'error': 'TTS模型未加载，请检查模型配置。可能需要安装espeak语音合成器。'}), 500
        
        if tts_model is None:
            app_logger.error(f"生成语音失败 - 模型未初始化, IP: {request.remote_addr}")
            return jsonify({'error': 'TTS模型未初始化，请重启应用'}), 500
        
        # 生成语音
        app_logger.info(f"开始生成语音 - 文本: {text[:50]}..., 语音: {voice}")
        audio = tts_model.generate(text, voice=voice)
        
        # 生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"speech_{timestamp}_{uuid.uuid4().hex[:8]}.wav"
        filepath = os.path.join('static/audio', filename)
        
        # 保存音频文件
        sf.write(filepath, audio, 24000)
        
        app_logger.info(f"语音生成成功 - 文件: {filename}, 大小: {os.path.getsize(filepath)} bytes")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'audio_url': f'/static/audio/{filename}',
            'message': '语音生成成功！'
        })
        
    except Exception as e:
        error_msg = str(e)
        app_logger.error(f"生成语音异常 - 错误: {error_msg}, IP: {request.remote_addr}")
        error_logger.error(f"生成语音异常详情 - 错误: {error_msg}, IP: {request.remote_addr}")
        
        if "espeak" in error_msg.lower():
            error_msg = "语音生成失败：需要安装espeak语音合成器。请查看控制台提示。"
        
        return jsonify({'error': f'生成语音时出错: {error_msg}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join('static/audio', filename)
        if os.path.exists(filepath):
            app_logger.info(f"文件下载 - 文件: {filename}, IP: {request.remote_addr}")
            return send_file(filepath, as_attachment=True)
        else:
            app_logger.warning(f"文件下载失败 - 文件不存在: {filename}, IP: {request.remote_addr}")
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        app_logger.error(f"文件下载异常 - 文件: {filename}, 错误: {str(e)}, IP: {request.remote_addr}")
        error_logger.error(f"文件下载异常详情 - 文件: {filename}, 错误: {str(e)}, IP: {request.remote_addr}")
        return jsonify({'error': f'下载文件时出错: {str(e)}'}), 500

@app.route('/voices')
def get_voices():
    app_logger.info(f"获取语音列表 - IP: {request.remote_addr}")
    return jsonify({'voices': available_voices})

@app.route('/model-status')
def model_status():
    """获取模型状态"""
    app_logger.info(f"获取模型状态 - IP: {request.remote_addr}")
    return jsonify({
        'model_loaded': model_loaded,
        'voices_available': len(available_voices),
        'voices': available_voices
    })

if __name__ == '__main__':
    # 记录启动信息
    log_startup_info(app_logger)
    
    app_logger.info(f"📊 模型状态: {'✅ 已加载' if model_loaded else '❌ 未加载'}")
    app_logger.info(f"🎭 可用语音: {len(available_voices)} 种")
    
    if not model_loaded:
        app_logger.warning("🔧 故障排除:")
        app_logger.warning("1. 确保已安装kittentts: pip install kittentts")
        app_logger.warning("2. 安装espeak语音合成器:")
        app_logger.warning("   macOS: brew install espeak")
        app_logger.warning("   Ubuntu/Debian: sudo apt-get install espeak-ng")
        app_logger.warning("   Windows: 下载espeak安装包")
        app_logger.warning("3. 重启应用")
    
    app_logger.info(f"🌐 应用将在 http://localhost:5050 启动")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5050)
    except KeyboardInterrupt:
        app_logger.info("收到中断信号，正在关闭应用...")
    finally:
        log_shutdown_info(app_logger)
