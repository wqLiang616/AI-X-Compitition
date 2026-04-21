#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
对话管理模块测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from dialogue.dialogue_manager import DialogueManager


class TestDialogueManager(unittest.TestCase):
    """对话管理模块测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.dialogue_manager = DialogueManager()
    
    def test_greeting(self):
        """测试问候意图"""
        response = self.dialogue_manager.process_input("你好")
        self.assertIn("您好", response)
    
    def test_thanks(self):
        """测试感谢意图"""
        response = self.dialogue_manager.process_input("谢谢")
        self.assertIn("不客气", response)
    
    def test_goodbye(self):
        """测试告别意图"""
        response = self.dialogue_manager.process_input("再见")
        self.assertIn("再见", response)
    
    def test_faq(self):
        """测试FAQ意图"""
        response = self.dialogue_manager.process_input("如何注册账号？")
        self.assertIn("注册", response)
    
    def test_dialogue_history(self):
        """测试对话历史"""
        self.dialogue_manager.process_input("你好")
        history = self.dialogue_manager.get_dialogue_history()
        self.assertEqual(len(history), 2)  # 用户输入和系统响应
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")


if __name__ == "__main__":
    unittest.main()