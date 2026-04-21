#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
知识库模块
负责存储和管理问题与答案，以及根据用户的问题检索答案
"""

import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBase:
    """知识库"""
    
    def __init__(self, knowledge_file="data/knowledge_base.json"):
        """初始化知识库
        
        Args:
            knowledge_file: 知识库文件路径
        """
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.update_vectors()
    
    def load_knowledge(self):
        """加载知识库
        
        Returns:
            list: 知识库中的问题和答案列表
        """
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 默认知识库
            default_knowledge = [
                {"question": "如何注册账号？", "answer": "您可以通过点击网站右上角的注册按钮，按照提示填写相关信息完成注册。"},
                {"question": "如何重置密码？", "answer": "您可以在登录页面点击忘记密码，然后按照提示操作重置密码。"},
                {"question": "客服工作时间是什么时候？", "answer": "我们的客服工作时间是周一至周五，9:00-18:00。"},
                {"question": "如何联系客服？", "answer": "您可以通过电话400-123-4567或发送邮件至service@example.com联系我们。"},
                {"question": "产品的退换货政策是什么？", "answer": "在收到产品7天内，如产品无损坏且不影响二次销售，您可以申请退换货。"}
            ]
            # 保存默认知识库
            self.save_knowledge(default_knowledge)
            return default_knowledge
    
    def save_knowledge(self, knowledge):
        """保存知识库
        
        Args:
            knowledge: 知识库内容
        """
        # 创建目录
        os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
        # 保存到文件
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge, f, ensure_ascii=False, indent=2)
    
    def update_vectors(self):
        """更新文本向量"""
        questions = [item["question"] for item in self.knowledge]
        if questions:
            self.question_vectors = self.vectorizer.fit_transform(questions)
        else:
            self.question_vectors = None
    
    def query(self, question):
        """根据问题检索答案
        
        Args:
            question: 用户的问题
            
        Returns:
            str: 检索到的答案
        """
        if not self.knowledge or not self.question_vectors:
            return None
        
        # 计算用户问题与知识库中问题的相似度
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.question_vectors)[0]
        
        # 找到相似度最高的问题
        max_index = similarities.argmax()
        max_similarity = similarities[max_index]
        
        # 如果相似度高于阈值，返回对应的答案
        if max_similarity > 0.3:
            return self.knowledge[max_index]["answer"]
        else:
            return None
    
    def add_knowledge(self, question, answer):
        """添加新的知识到知识库
        
        Args:
            question: 问题
            answer: 答案
        """
        self.knowledge.append({"question": question, "answer": answer})
        self.save_knowledge(self.knowledge)
        self.update_vectors()
    
    def get_knowledge(self):
        """获取知识库内容
        
        Returns:
            list: 知识库内容
        """
        return self.knowledge