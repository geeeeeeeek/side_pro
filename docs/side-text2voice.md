# 从零搭建一个免费的文本转语音在线工具（基于 Flask + Edge TTS）

> 项目在线体验地址：[https://text2voice.cc](https://text2voice.cc)

> GitHub 源码：文末附完整代码

## 前言

最近有个需求，需要把一段文字转换成语音，找了几个在线工具，要么收费，要么有水印，要么音质惨不忍睹。后来发现微软 Edge 浏览器的 TTS（Text-to-Speech）服务音质非常好，而且免费开放使用。于是动手写了一个在线工具，分享给大家。

## 效果预览
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/83daf5cceb3f47ccbb24206fab010bb0.jpeg#pic_center)



主要功能：
- 支持中文、英文、日文、韩文等多种语言
- 多种语音角色可选（男声/女声）
- 可调节语速和音调
- 支持在线播放和 MP3 下载
- 响应式设计，手机也能用

## 技术选型

为什么选择 Edge TTS？

| 方案 | 音质 | 免费额度 | 下载支持 |
|------|------|----------|----------|
| 百度语音合成 | 一般 | 有限制 | 支持 |
| 讯飞语音 | 较好 | 有限制 | 支持 |
| Web Speech API | 取决于系统 | 免费 | 不支持 |
| **Edge TTS** | **优秀** | **免费** | **支持** |

Edge TTS 使用微软 Neural TTS 技术，生成的语音接近真人，而且完全免费，没有调用次数限制。

## 项目架构

```
浏览器 (HTML/CSS/JS)
    │
    │  POST /api/tts
    ▼
Flask 服务端 (server.py)
    │
    │  WebSocket
    ▼
Microsoft Edge TTS 服务
    │
    │  MP3 音频流
    ▼
浏览器播放/下载
```

- **前端**：原生 HTML + CSS + JavaScript，无框架依赖
- **后端**：Flask 提供静态文件服务和 TTS API 代理
- **语音合成**：通过 edge-tts Python 包调用微软服务

## 核心代码实现

### 1. 后端服务 (server.py)

```python
#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
import edge_tts
import asyncio
import io

app = Flask(__name__, static_folder="web")

@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "").strip()
    voice = data.get("voice", "zh-CN-XiaoxiaoNeural")
    rate = data.get("rate", "+0%")
    pitch = data.get("pitch", "+0Hz")
    
    if not text:
        return jsonify(error="文本内容不能为空"), 400
    
    try:
        audio_data = asyncio.run(synthesize(text, voice, rate, pitch))
        return audio_data, 200, {"Content-Type": "audio/mpeg"}
    except Exception as e:
        return jsonify(error=f"语音合成失败: {e}"), 500

async def synthesize(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])
    return buffer.getvalue()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

核心逻辑很简单：
1. 接收前端传来的文本和语音参数
2. 调用 edge-tts 进行语音合成
3. 将音频流返回给前端

### 2. 前端调用 (app.js)

```javascript
// 调用后端 TTS API
async function callEdgeTTS(text, voice, rate, pitch) {
    const ratePercent = Math.round((rate - 1) * 100);
    const rateStr = (ratePercent >= 0 ? '+' : '') + ratePercent + '%';
    const pitchStr = (pitch >= 0 ? '+' : '') + pitch + 'Hz';

    const response = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: text,
            voice: voice,
            rate: rateStr,
            pitch: pitchStr
        })
    });

    if (!response.ok) {
        throw new Error('语音合成请求失败');
    }

    return await response.blob();
}

// 播放音频
function playAudioBlob(blob) {
    const url = URL.createObjectURL(blob);
    const audio = document.getElementById('audioPlayer');
    audio.src = url;
    audio.play();
}

// 下载 MP3
function downloadAudio(blob) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tts_audio.mp3';
    a.click();
}
```

### 3. 支持的语音列表

```javascript
const VOICES = {
    'zh-CN': {
        label: '中文(普通话)',
        voices: [
            { name: 'zh-CN-XiaoxiaoNeural', label: '晓晓', gender: '女' },
            { name: 'zh-CN-YunxiNeural', label: '云希', gender: '男' },
            { name: 'zh-CN-XiaoyiNeural', label: '晓伊', gender: '女' },
            { name: 'zh-CN-YunjianNeural', label: '云健', gender: '男' },
        ]
    },
    'en-US': {
        label: '英文(美国)',
        voices: [
            { name: 'en-US-JennyNeural', label: 'Jenny', gender: '女' },
            { name: 'en-US-GuyNeural', label: 'Guy', gender: '男' },
        ]
    },
    // ... 更多语言
};
```

## 双引擎备用机制

考虑到用户可能没有启动后端服务，我加了一个备用方案：当 Edge TTS 不可用时，自动切换到浏览器内置的 Web Speech API。

```javascript
async function synthesize() {
    try {
        // 优先使用 Edge TTS
        const blob = await callEdgeTTS(text, voice, rate, pitch);
        playAudioBlob(blob);
        enableDownload(); // 支持下载
    } catch (edgeError) {
        // 备用方案：Web Speech API
        console.warn('Edge TTS 不可用，切换到浏览器内置语音');
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = rate;
        speechSynthesis.speak(utterance);
        disableDownload(); // 不支持下载
    }
}
```

这样即使没有后端，用户也能听到语音，只是不能下载 MP3。

## 安全与限流

为了防止滥用，加了几个保护措施：

```python
# 限制单次文本长度
MAX_TEXT_LENGTH = 1000

# 限制每小时请求次数
MAX_REQUESTS_PER_HOUR = 10

# 按 IP 记录请求
request_log = {}

def check_rate_limit(ip):
    now = time.time()
    timestamps = request_log.get(ip, [])
    timestamps = [t for t in timestamps if t > now - 3600]
    request_log[ip] = timestamps
    return len(timestamps) < MAX_REQUESTS_PER_HOUR
```

## 部署上线

### 本地运行

```bash
# 安装依赖
pip install flask edge-tts

# 启动服务
python server.py

# 访问 http://localhost:8000
```

### 生产环境部署

使用 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name text2voice.cc;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

后台启动：

```bash
nohup python3 server.py > server.log 2>&1 &
```

## 项目结构

```
web_text2voice/
├── web/
│   ├── index.html      # 主页面
│   ├── about.html      # 关于页面
│   ├── privacy.html    # 隐私政策
│   ├── css/
│   │   └── style.css   # 样式文件
│   └── js/
│       └── app.js      # 前端逻辑
├── server.py           # Flask 后端服务
└── README.md           # 项目文档
```

## 遇到的问题与解决

### 问题1：edge-tts 是异步的，Flask 是同步的

edge-tts 使用 asyncio，而 Flask 默认是同步的。解决方法是用 `asyncio.run()` 包装：

```python
audio_data = asyncio.run(synthesize(text, voice, rate, pitch))
```

### 问题2：音频流如何返回给前端

edge-tts 返回的是异步生成器，需要收集所有 chunk：

```python
async def synthesize(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])
    return buffer.getvalue()
```

### 问题3：跨域问题

开发时可能遇到 CORS 问题，可以加个简单的 CORS 头：

```python
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
```

## 总结

这个项目虽然简单，但涵盖了前后端交互、异步处理、文件下载等常见场景。Edge TTS 的音质确实不错，适合做语音播报、有声书、视频配音等应用。

项目已开源，欢迎大家 Star 和 Fork！

---

**相关链接：**
- 在线体验：https://text2voice.cc
- 源码：https://github.com/geeeeeeeek/text2voice
- Flask 官方文档：https://flask.palletsprojects.com/


