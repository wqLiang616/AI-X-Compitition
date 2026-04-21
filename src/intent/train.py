#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
意图识别模型训练脚本
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os


def load_data(data_path):
    """加载训练数据
    
    Args:
        data_path: 数据文件路径
        
    Returns:
        tuple: (X, y) 特征和标签
    """
    df = pd.read_csv(data_path)
    X = df['text'].values
    y = df['intent'].values
    return X, y


def train_model(X_train, y_train):
    """训练意图识别模型
    
    Args:
        X_train: 训练数据特征
        y_train: 训练数据标签
        
    Returns:
        tuple: (vectorizer, model) 向量化器和训练好的模型
    """
    # 文本向量化
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    
    # 训练SVM模型
    model = SVC(kernel='linear', C=1.0, probability=True)
    model.fit(X_train_vec, y_train)
    
    return vectorizer, model


def evaluate_model(model, vectorizer, X_test, y_test):
    """评估模型性能
    
    Args:
        model: 训练好的模型
        vectorizer: 向量化器
        X_test: 测试数据特征
        y_test: 测试数据标签
    """
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型准确率: {accuracy:.4f}")
    print("\n分类报告:")
    print(classification_report(y_test, y_pred))


def save_model(model, vectorizer, model_path, vectorizer_path):
    """保存模型和向量化器
    
    Args:
        model: 训练好的模型
        vectorizer: 向量化器
        model_path: 模型保存路径
        vectorizer_path: 向量化器保存路径
    """
    # 创建保存目录
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # 保存模型
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # 保存向量化器
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print(f"模型保存到: {model_path}")
    print(f"向量化器保存到: {vectorizer_path}")


def main():
    """主函数"""
    # 数据路径
    data_path = 'data/intent_data.csv'
    model_path = 'models/intent_classifier.pkl'
    vectorizer_path = 'models/vectorizer.pkl'
    
    # 加载数据
    print("加载数据...")
    X, y = load_data(data_path)
    
    # 分割数据
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"训练数据: {len(X_train)} 条, 测试数据: {len(X_test)} 条")
    
    # 训练模型
    print("训练模型...")
    vectorizer, model = train_model(X_train, y_train)
    
    # 评估模型
    print("评估模型...")
    evaluate_model(model, vectorizer, X_test, y_test)
    
    # 保存模型
    print("保存模型...")
    save_model(model, vectorizer, model_path, vectorizer_path)


if __name__ == "__main__":
    main()