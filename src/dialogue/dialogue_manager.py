#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
对话管理模块
负责处理用户输入、管理对话状态和生成响应
"""

from intent.intent_classifier import IntentClassifier
from knowledge.knowledge_base import KnowledgeBase
from utils.context_manager import ContextManager


class DialogueManager:
    """对话管理器"""
    
    def __init__(self):
        """初始化对话管理器"""
        # 初始化意图分类器
        self.intent_classifier = IntentClassifier()
        # 初始化知识库
        self.knowledge_base = KnowledgeBase()
        # 初始化上下文管理器
        self.context_manager = ContextManager()
        # 初始化对话状态
        self.reset_dialogue()
    
    def reset_dialogue(self):
        """重置对话状态"""
        self.context_manager.reset()
        self.current_intent = None
        self.dialogue_history = []
    
    def process_input(self, user_input):
        """处理用户输入并生成响应
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            str: 系统生成的响应
        """
        # 记录用户输入到对话历史
        self.dialogue_history.append({"role": "user", "content": user_input})
        
        # 分类用户意图
        intent = self.intent_classifier.classify(user_input)
        self.current_intent = intent
        
        # 更新上下文
        self.context_manager.update_context(user_input, intent)
        
        # 根据意图生成响应
        response = self.generate_response(user_input, intent)
        
        # 记录系统响应到对话历史
        self.dialogue_history.append({"role": "assistant", "content": response})
        
        return response
    
    def generate_response(self, user_input, intent):
        """根据用户输入和意图生成响应
        
        Args:
            user_input: 用户输入的文本
            intent: 识别出的意图
            
        Returns:
            str: 生成的响应
        """
        # 处理不同的意图
        if intent == "greeting":
            return "您好！我是智能客服助手，有什么可以帮助您的吗？"
        elif intent == "thanks":
            return "不客气，很高兴能帮到您！"
        elif intent == "goodbye":
            self.reset_dialogue()
            return "再见！祝您有愉快的一天！"
        elif intent == "faq":
            # 从知识库中获取答案
            answer = self.knowledge_base.query(user_input)
            if answer:
                return answer
            else:
                return "抱歉，我暂时无法回答这个问题。您可以尝试用其他方式表述，或者联系人工客服。"
        else:
            # 默认响应
            return "我正在理解您的问题，请稍等..."
    
    def get_dialogue_history(self):
        """获取对话历史
        
        Returns:
            list: 对话历史列表
        """
        return self.dialogue_history