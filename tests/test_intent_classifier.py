#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
意图识别模块测试
"""

import unittest
from intent.intent_classifier import IntentClassifier


class TestIntentClassifier(unittest.TestCase):
    """意图识别模块测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.intent_classifier = IntentClassifier()
    
    def test_greeting(self):
        """测试问候意图识别"""
        intent = self.intent_classifier.classify("你好")
        self.assertEqual(intent, "greeting")
        
        intent = self.intent_classifier.classify("早上好")
        self.assertEqual(intent, "greeting")
    
    def test_thanks(self):
        """测试感谢意图识别"""
        intent = self.intent_classifier.classify("谢谢")
        self.assertEqual(intent, "thanks")
        
        intent = self.intent_classifier.classify("感谢")
        self.assertEqual(intent, "thanks")
    
    def test_goodbye(self):
        """测试告别意图识别"""
        intent = self.intent_classifier.classify("再见")
        self.assertEqual(intent, "goodbye")
        
        intent = self.intent_classifier.classify("拜拜")
        self.assertEqual(intent, "goodbye")
    
    def test_faq(self):
        """测试FAQ意图识别"""
        intent = self.intent_classifier.classify("如何注册账号？")
        self.assertEqual(intent, "faq")
        
        intent = self.intent_classifier.classify("价格是多少？")
        self.assertEqual(intent, "faq")
    
    def test_add_intent(self):
        """测试添加新意图"""
        self.intent_classifier.add_intent("complaint", ["投诉", "抱怨", "不满"])
        intent = self.intent_classifier.classify("我要投诉")
        self.assertEqual(intent, "complaint")


if __name__ == "__main__":
    unittest.main()