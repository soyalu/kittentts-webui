document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const textInput = document.getElementById('text-input');
    const voiceSelect = document.getElementById('voice-select');
    const generateBtn = document.getElementById('generate-btn');
    const outputSection = document.getElementById('output-section');
    const loadingSection = document.getElementById('loading-section');
    const errorSection = document.getElementById('error-section');
    const audioPlayer = document.getElementById('audio-player');
    const downloadBtn = document.getElementById('download-btn');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const charCount = document.getElementById('char-count');
    const errorMessage = document.getElementById('error-message');

    let currentAudioUrl = '';
    let currentFilename = '';

    // 字符计数
    textInput.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count;
        
        // 如果超过限制，显示警告色
        if (count > 450) {
            charCount.style.color = '#dc3545';
        } else if (count > 400) {
            charCount.style.color = '#ffc107';
        } else {
            charCount.style.color = '#888';
        }
    });

    // 生成语音按钮点击事件
    generateBtn.addEventListener('click', function() {
        const text = textInput.value.trim();
        const voice = voiceSelect.value;

        if (!text) {
            showError('请输入要转换的文字');
            return;
        }

        if (text.length > 500) {
            showError('文字长度不能超过500个字符');
            return;
        }

        generateSpeech(text, voice);
    });

    // 下载按钮点击事件
    downloadBtn.addEventListener('click', function() {
        if (currentFilename) {
            window.open(`/download/${currentFilename}`, '_blank');
        }
    });

    // 播放/暂停按钮点击事件
    playPauseBtn.addEventListener('click', function() {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>暂停';
        } else {
            audioPlayer.pause();
            playPauseBtn.innerHTML = '<i class="fas fa-play"></i>播放';
        }
    });

    // 音频播放状态变化监听
    audioPlayer.addEventListener('play', function() {
        playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>暂停';
    });

    audioPlayer.addEventListener('pause', function() {
        playPauseBtn.innerHTML = '<i class="fas fa-play"></i>播放';
    });

    // 音频播放结束监听
    audioPlayer.addEventListener('ended', function() {
        playPauseBtn.innerHTML = '<i class="fas fa-play"></i>播放';
    });

    // 生成语音函数
    async function generateSpeech(text, voice) {
        try {
            // 显示加载状态
            showLoading();
            hideError();
            hideOutput();

            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    voice: voice
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // 成功生成语音
                currentAudioUrl = data.audio_url;
                currentFilename = data.filename;
                
                // 设置音频源
                audioPlayer.src = currentAudioUrl;
                
                // 显示输出区域
                showOutput();
                
                // 显示成功消息
                showSuccessMessage(data.message);
                
                // 自动播放（可选）
                // audioPlayer.play();
                
            } else {
                // 显示错误信息
                showError(data.error || '生成语音失败');
            }

        } catch (error) {
            console.error('生成语音时出错:', error);
            showError('网络错误，请检查连接后重试');
        } finally {
            hideLoading();
        }
    }

    // 显示加载状态
    function showLoading() {
        loadingSection.style.display = 'block';
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>生成中...';
    }

    // 隐藏加载状态
    function hideLoading() {
        loadingSection.style.display = 'none';
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic"></i>生成语音';
    }

    // 显示输出区域
    function showOutput() {
        outputSection.style.display = 'block';
        outputSection.scrollIntoView({ behavior: 'smooth' });
    }

    // 隐藏输出区域
    function hideOutput() {
        outputSection.style.display = 'none';
    }

    // 显示错误信息
    function showError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        errorSection.scrollIntoView({ behavior: 'smooth' });
    }

    // 隐藏错误信息
    function hideError() {
        errorSection.style.display = 'none';
    }

    // 显示成功消息（临时提示）
    function showSuccessMessage(message) {
        // 创建一个临时的成功提示
        const successToast = document.createElement('div');
        successToast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            font-weight: 500;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        successToast.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
        
        document.body.appendChild(successToast);
        
        // 显示动画
        setTimeout(() => {
            successToast.style.transform = 'translateX(0)';
        }, 100);
        
        // 自动隐藏
        setTimeout(() => {
            successToast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(successToast);
            }, 300);
        }, 3000);
    }

    // 键盘快捷键支持
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter 或 Cmd+Enter 生成语音
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            generateBtn.click();
        }
        
        // Esc 键隐藏错误信息
        if (e.key === 'Escape') {
            hideError();
        }
    });

    // 页面加载完成后的初始化
    console.log('KittenTTS Web界面已加载完成');
});
