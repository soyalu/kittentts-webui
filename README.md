# KittenTTS Web界面

这是一个基于KittenTTS的文字转语音Web应用，提供了现代化的用户界面，支持多种语音风格选择，在线预览和下载功能。

## 功能特点

- 🎯 **智能TTS转换**: 基于KittenML/kitten-tts-nano-0.1模型
- 🎨 **现代化UI**: 响应式设计，支持移动端和桌面端
- 🎭 **多种语音风格**: 支持8种不同的语音风格（男声/女声）
- 🔊 **在线预览**: 生成后可直接在浏览器中播放
- 💾 **文件下载**: 支持下载生成的WAV音频文件
- ⌨️ **键盘快捷键**: Ctrl+Enter快速生成，Esc隐藏错误信息
- 📱 **响应式设计**: 完美适配各种设备尺寸
- 📝 **完整日志系统**: 应用日志、访问日志、错误日志分离管理

## 安装说明

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd kittentts
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行应用
```bash
python app.py
```

应用将在 `http://localhost:5050` 启动

## 使用方法

1. **输入文字**: 在文本框中输入要转换的文字（最多500字符）
2. **选择语音**: 从下拉菜单中选择喜欢的语音风格
3. **生成语音**: 点击"生成语音"按钮
4. **预览播放**: 使用内置音频播放器预览生成的语音
5. **下载文件**: 点击"下载音频文件"保存到本地

## 语音风格选项

- `expr-voice-2-m`: 语音2 (男声)
- `expr-voice-2-f`: 语音2 (女声) - 默认
- `expr-voice-3-m`: 语音3 (男声)
- `expr-voice-3-f`: 语音3 (女声)
- `expr-voice-4-m`: 语音4 (男声)
- `expr-voice-4-f`: 语音4 (女声)
- `expr-voice-5-m`: 语音5 (男声)
- `expr-voice-5-f`: 语音5 (女声)

## 日志管理

### 日志文件位置
- **应用日志**: `logs/app.log` - 记录应用运行状态和TTS操作
- **访问日志**: `logs/access.log` - 记录所有HTTP请求和响应
- **错误日志**: `logs/error.log` - 记录错误和异常信息

### 日志查看工具
使用内置的日志查看工具管理日志：

```bash
# 列出所有日志文件
python view_logs.py list

# 查看应用日志（最后50行）
python view_logs.py view --file logs/app.log

# 查看访问日志（最后100行）
python view_logs.py view --file logs/access.log --lines 100

# 实时跟踪日志
python view_logs.py view --file logs/app.log --follow

# 清理所有日志文件
python view_logs.py clear
```

### 日志轮转
- 每个日志文件最大10MB
- 自动保留5个备份文件
- 支持UTF-8编码，完美显示中文

## 技术架构

- **后端**: Flask (Python)
- **前端**: HTML5 + CSS3 + JavaScript (ES6+)
- **TTS引擎**: KittenTTS
- **音频处理**: soundfile
- **UI框架**: 原生CSS + Font Awesome图标
- **日志系统**: Python logging + RotatingFileHandler

## 项目结构

```
kittentts/
├── app.py              # Flask主应用
├── logging_config.py   # 日志配置模块
├── view_logs.py        # 日志查看工具
├── templates/          # HTML模板
│   └── index.html     # 主页面
├── static/            # 静态资源
│   ├── css/          # 样式文件
│   │   └── style.css
│   ├── js/           # JavaScript文件
│   │   └── app.js
│   └── audio/        # 生成的音频文件
├── logs/              # 日志文件目录
│   ├── app.log       # 应用日志
│   ├── access.log    # 访问日志
│   └── error.log     # 错误日志
├── requirements.txt   # Python依赖
├── test.py           # 原始测试文件
└── README.md         # 项目说明
```

## 键盘快捷键

- `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac): 快速生成语音
- `Esc`: 隐藏错误信息

## 注意事项

- 首次运行时会自动下载TTS模型，请确保网络连接正常
- 生成的音频文件保存在 `static/audio/` 目录中
- 支持最大500字符的文本输入
- 音频采样率为24kHz，格式为WAV
- 日志文件会自动轮转，避免占用过多磁盘空间

## 故障排除

### 模型加载失败
- 检查网络连接
- 确认kittentts包安装正确
- 查看控制台错误信息
- 检查 `logs/app.log` 日志文件

### 音频生成失败
- 检查输入文本是否为空
- 确认文本长度不超过500字符
- 查看浏览器控制台错误信息
- 检查 `logs/error.log` 日志文件

### 日志相关问题
- 确保logs目录有写入权限
- 检查磁盘空间是否充足
- 使用 `python view_logs.py list` 查看日志文件状态

## 许可证

本项目基于MIT许可证开源。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！
