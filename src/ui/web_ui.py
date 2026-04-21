#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web界面模块
负责处理Web请求和响应，提供用户与智能客服的交互界面
"""

from flask import Flask, render_template, request, jsonify


class WebUI:
    """Web界面"""
    
    def __init__(self, dialogue_manager, port=5000):
        """初始化Web界面
        
        Args:
            dialogue_manager: 对话管理器
            port: 服务端口
        """
        self.app = Flask(__name__)
        self.dialogue_manager = dialogue_manager
        self.port = port
        
        # 注册路由
        self.register_routes()
    
    def register_routes(self):
        """注册路由"""
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            data = request.json
            user_input = data.get('message', '')
            if not user_input:
                return jsonify({'error': 'No message provided'}), 400
            
            # 处理用户输入
            response = self.dialogue_manager.process_input(user_input)
            
            return jsonify({'response': response})
    
    def run(self):
        """运行Web服务"""
        # 创建templates目录
        import os
        os.makedirs('templates', exist_ok=True)
        
        # 创建index.html文件
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能客服对话系统</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .chat-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
            height: 500px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }
        .user-message {
            background-color: #e3f2fd;
            align-self: flex-end;
            margin-left: auto;
        }
        .bot-message {
            background-color: #f1f1f1;
            align-self: flex-start;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>智能客服对话系统</h1>
        <div class="chat-container" id="chat-container">
            <div class="message bot-message">
                您好！我是智能客服助手，有什么可以帮助您的吗？
            </div>
        </div>
        <div class="input-container">
            <input type="text" id="message-input" placeholder="请输入您的问题...">
            <button id="send-button">发送</button>
        </div>
    </div>
    <script>
        const chatContainer = document.getElementById('chat-container');
        const messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        
        function addMessage(message, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function sendMessage() {
            const message = messageInput.value.trim();
            if (message) {
                addMessage(message, true);
                messageInput.value = '';
                
                // 发送请求到服务器
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.response) {
                        addMessage(data.response, false);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('抱歉，系统暂时无法响应，请稍后再试。', false);
                });
            }
        }
        
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
            ''')
        
        print(f"Web服务启动在 http://localhost:{self.port}")
        self.app.run(host='0.0.0.0', port=self.port, debug=True)
