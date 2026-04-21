#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
意图识别模块
负责识别用户的意图
"""

import numpy as np
from transformers import pipeline


class IntentClassifier:
    """意图分类器"""
    
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """初始化意图分类器
        
        Args:
            model_name: 使用的预训练模型名称
        """
        # 初始化情感分析管道
        self.classifier = pipeline("sentiment-analysis", model=model_name)
        # 定义意图映射
        self.intent_map = {
            "greeting": ["你好", "您好", "嗨", "早上好", "下午好", "晚上好"],
            "thanks": ["谢谢", "感谢", "多谢", "谢了"],
            "goodbye": ["再见", "拜拜", "下次见"],
            "faq": ["如何", "怎样", "什么", "为什么", "哪里", "什么时候", "价格", "费用", "收费"]
        }
    
    def classify(self, text):
        """分类用户意图
        
        Args:
            text: 用户输入的文本
            
        Returns:
            str: 识别出的意图
        """
        # 简单的基于关键词的意图识别
        for intent, keywords in self.intent_map.items():
            for keyword in keywords:
                if keyword in text:
                    return intent
        
        # 如果没有匹配到关键词，使用情感分析作为默认意图
        result = self.classifier(text)[0]
        if result["label"] == "POSITIVE":
            return "thanks"
        else:
            return "faq"
    
    def add_intent(self, intent_name, keywords):
        """添加新的意图和关键词
        
        Args:
            intent_name: 意图名称
            keywords: 关键词列表
        """
        self.intent_map[intent_name] = keywords
    
    def get_intents(self):
        """获取所有意图
        
        Returns:
            list: 意图列表
        """
        return list(self.intent_map.keys())