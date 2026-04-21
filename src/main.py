#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
智能客服对话系统主入口
"""

from dialogue.dialogue_manager import DialogueManager
from ui.web_ui import WebUI
import argparse


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='智能客服对话系统')
    parser.add_argument('--mode', type=str, default='web', choices=['web', 'cli'],
                        help='运行模式: web (网页界面) 或 cli (命令行界面)')
    parser.add_argument('--port', type=int, default=5000, help='网页服务端口')
    
    args = parser.parse_args()
    
    # 初始化对话管理器
    dialogue_manager = DialogueManager()
    
    if args.mode == 'web':
        # 启动网页界面
        web_ui = WebUI(dialogue_manager, port=args.port)
        web_ui.run()
    else:
        # 启动命令行界面
        print("智能客服对话系统 (命令行模式)")
        print("输入 'exit' 退出系统")
        
        while True:
            user_input = input("用户: ")
            if user_input.lower() == 'exit':
                break
            
            response = dialogue_manager.process_input(user_input)
            print(f"客服: {response}")


if __name__ == "__main__":
    main()