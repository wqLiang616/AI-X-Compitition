#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
知识库模块测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import json
from knowledge.knowledge_base import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):
    """知识库模块测试"""
    
    def setUp(self):
        """设置测试环境"""
        # 创建临时知识库文件
        self.test_file = "data/test_knowledge_base.json"
        # 确保目录存在
        os.makedirs(os.path.dirname(self.test_file), exist_ok=True)
        # 初始化知识库
        self.knowledge_base = KnowledgeBase(self.test_file)
    
    def tearDown(self):
        """清理测试环境"""
        # 删除测试文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_query(self):
        """测试查询功能"""
        # 添加测试知识
        self.knowledge_base.add_knowledge("如何注册账号？", "您可以通过点击网站右上角的注册按钮，按照提示填写相关信息完成注册。")
        
        # 测试精确匹配
        answer = self.knowledge_base.query("如何注册账号？")
        self.assertIn("注册按钮", answer)
        
        # 测试相似问题
        answer = self.knowledge_base.query("怎么注册账号？")
        self.assertIn("注册按钮", answer)
        
        # 测试不匹配的问题
        answer = self.knowledge_base.query("这是一个无关的问题")
        self.assertIsNone(answer)
    
    def test_add_knowledge(self):
        """测试添加知识功能"""
        # 添加知识
        self.knowledge_base.add_knowledge("测试问题", "测试答案")
        
        # 验证知识是否添加成功
        knowledge = self.knowledge_base.get_knowledge()
        self.assertEqual(len(knowledge), 6)  # 默认5条 + 1条新添加的
        self.assertEqual(knowledge[-1]["question"], "测试问题")
        self.assertEqual(knowledge[-1]["answer"], "测试答案")
    
    def test_load_knowledge(self):
        """测试加载知识库功能"""
        # 保存测试数据
        test_data = [
            {"question": "测试问题1", "answer": "测试答案1"},
            {"question": "测试问题2", "answer": "测试答案2"}
        ]
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
        
        # 重新初始化知识库
        knowledge_base = KnowledgeBase(self.test_file)
        knowledge = knowledge_base.get_knowledge()
        self.assertEqual(len(knowledge), 2)
        self.assertEqual(knowledge[0]["question"], "测试问题1")


if __name__ == "__main__":
    unittest.main()