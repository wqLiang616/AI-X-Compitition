#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
上下文管理器模块
负责管理对话上下文信息
"""


class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        """初始化上下文管理器"""
        self.context = {}
        self.reset()
    
    def reset(self):
        """重置上下文"""
        self.context = {
            "last_intent": None,
            "last_utterance": None,
            "conversation_history": [],
            "user_info": {},
            "session_start_time": None
        }
    
    def update_context(self, user_input, intent):
        """更新上下文
        
        Args:
            user_input: 用户输入的文本
            intent: 识别出的意图
        """
        # 更新最后一个意图
        self.context["last_intent"] = intent
        # 更新最后一个 utterance
        self.context["last_utterance"] = user_input
        # 添加到对话历史
        self.context["conversation_history"].append({
            "utterance": user_input,
            "intent": intent
        })
        # 限制对话历史长度，避免内存占用过大
        if len(self.context["conversation_history"]) > 10:
            self.context["conversation_history"] = self.context["conversation_history"][-10:]
    
    def get_context(self):
        """获取当前上下文
        
        Returns:
            dict: 当前上下文信息
        """
        return self.context
    
    def get_last_intent(self):
        """获取最后一个意图
        
        Returns:
            str: 最后一个意图
        """
        return self.context["last_intent"]
    
    def get_last_utterance(self):
        """获取最后一个 utterance
        
        Returns:
            str: 最后一个 utterance
        """
        return self.context["last_utterance"]
    
    def get_conversation_history(self):
        """获取对话历史
        
        Returns:
            list: 对话历史列表
        """
        return self.context["conversation_history"]