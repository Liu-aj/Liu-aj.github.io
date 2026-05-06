---
title: 设计模式
description: 常用设计模式
---

# 设计模式 🎨

> 常见设计模式

---

## 单例模式

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## 工厂模式

```python
class Factory:
    def create(self, type):
        if type == 'A':
            return ProductA()
        elif type == 'B':
            return ProductB()
```

## 观察者模式

```python
class Observer:
    def update(self, state):
        pass

class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
```

---

*设计模式是经验的积累*
