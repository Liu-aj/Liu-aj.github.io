---
layout: post
title: Java线程与并发编程完全指南
date: 2018-07-13 13:46:05
forType: Java
category: 线程
tag: [Java, 线程, 并发编程, 多线程]
---

* content
{:toc}

# Java线程与并发编程完全指南

本文档详细介绍Java线程的创建、管理、同步机制以及高级并发编程技术，帮助开发者掌握多线程编程的核心概念和最佳实践。

## 一、线程基础

Java中创建线程的三种方式：

### 1. 继承Thread类
### 1. ConcurrentHashMap
线程安全的HashMap实现，比Hashtable更高效：
```java
import java.util.concurrent.ConcurrentHashMap;

ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 添加元素
map.put("key1", 1);

// 原子操作
map.putIfAbsent("key2", 2); // 如果key不存在则添加
map.computeIfAbsent("key3", k -> 3); // 计算并添加
map.computeIfPresent("key1", (k, v) -> v + 1); // 计算并更新

// 批量操作
map.forEach((k, v) -> System.out.println(k + ": " + v));```

### 2. CopyOnWriteArrayList
读操作无锁，写操作需要复制整个数组：
```java
import java.util.concurrent.CopyOnWriteArrayList;

CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

// 添加元素
list.add("element1");
list.add("element2");

// 读取元素（无需同步）
for (String element : list) {
    System.out.println(element);
}```

### 3. BlockingQueue
支持阻塞操作的队列，常用于生产者-消费者模式：
```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

// 创建容量为10的阻塞队列
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);

// 生产者线程
new Thread(() -> {
    try {
        for (int i = 0; i < 20; i++) {
            queue.put("Task " + i); // 如果队列满则阻塞
            System.out.println("Produced: Task " + i + ", queue size: " + queue.size());
            Thread.sleep(100);
        }
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();

// 消费者线程
new Thread(() -> {
    try {
        while (true) {
            String task = queue.take(); // 如果队列空则阻塞
            System.out.println("Consumed: " + task + ", queue size: " + queue.size());
            Thread.sleep(1000);
        }
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();```

## 八、线程安全与并发问题

### 1. 线程安全的概念
线程安全是指多线程环境下，共享的可变状态能够被正确地访问而不会导致数据不一致或其他异常情况。

### 2. 常见的并发问题
- **竞态条件**：多个线程同时访问和修改共享数据
- **死锁**：两个或多个线程互相等待对方释放资源
- **活锁**：线程不断重试一个永远失败的操作
- **饥饿**：某些线程长期无法获得资源

### 3. 避免并发问题的方法
- **不可变对象**：创建后不可修改的对象天然线程安全
- **线程局部变量**：使用ThreadLocal存储线程特定数据
- **同步机制**：使用synchronized或ReentrantLock
- **原子变量**：使用java.util.concurrent.atomic包中的类

## 九、并发性能优化

### 1. 减少锁的范围
尽量减小同步代码块的范围，只同步必要的代码：
```java
// 不好的做法
public synchronized void method() {
    // 非同步操作
    // 同步操作
    // 非同步操作
}

// 好的做法
public void method() {
    // 非同步操作
    synchronized(this) {
        // 同步操作
    }
    // 非同步操作
}```

### 2. 使用细粒度锁
将大对象分解为多个小对象，每个对象使用独立的锁：
```java
public class FineGrainedLockExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    private int field1;
    private int field2;
    
    public void updateField1(int value) {
        synchronized(lock1) {
            field1 = value;
        }
    }
    
    public void updateField2(int value) {
        synchronized(lock2) {
            field2 = value;
        }
    }
}```

### 3. 使用并发集合
优先使用java.util.concurrent包中的并发集合，而不是自己实现同步：
- ConcurrentHashMap代替Collections.synchronizedMap
- CopyOnWriteArrayList代替Collections.synchronizedList
- BlockingQueue用于生产者-消费者模式

### 4. 避免不必要的同步
- 对于只读数据，不需要同步
- 对于局部变量，不需要同步
- 对于不可变对象，不需要同步

### 5. 使用原子操作
对于简单的原子操作，使用java.util.concurrent.atomic包中的原子类：
```java
import java.util.concurrent.atomic.AtomicInteger;

AtomicInteger counter = new AtomicInteger(0);

// 原子递增
int newValue = counter.incrementAndGet();

// 原子递减
int oldValue = counter.getAndDecrement();

// 原子比较并交换
counter.compareAndSet(expectedValue, newValue);```

## 十、Java并发编程最佳实践

1. **优先使用Executor框架**：使用线程池管理线程，而不是直接创建线程
2. **使用线程安全的集合**：优先使用java.util.concurrent包中的集合类
3. **避免共享可变状态**：尽量减少共享可变数据，使用不可变对象或线程局部变量
4. **正确处理异常**：在线程的run()方法中捕获所有异常，避免线程意外终止
5. **使用高级并发工具**：利用CountDownLatch、CyclicBarrier等工具简化并发编程
6. **合理设置线程优先级**：只在必要时使用优先级，避免过度依赖
7. **避免使用Thread.stop()**：此方法已被废弃，使用interrupt()代替
8. **正确关闭线程池**：使用shutdown()或shutdownNow()关闭线程池
9. **使用Lock接口代替synchronized**：在复杂场景下提供更灵活的锁定机制
10. **进行性能测试**：在高并发场景下测试应用程序的性能和稳定性

通过本文的介绍，您应该能够掌握Java线程和并发编程的核心概念和实用技巧。在实际开发中，合理使用多线程可以充分利用多核处理器的性能，提高应用程序的响应速度和吞吐量。但同时，并发编程也带来了复杂性，需要仔细设计和测试，以避免常见的并发问题。java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread is running");
    }
    
    public static void main(String[] args) {
        MyThread thread = new MyThread();
        thread.start(); // 启动线程
    }
}```
```

### 2. 实现Runnable接口
```java
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable is running");
    }
    
    public static void main(String[] args) {
        Thread thread = new Thread(new MyRunnable());
        thread.start();
    }
}```

**优点**：避免了单继承的限制，可以同时实现其他接口
```

### 3. 使用Callable和Future
```java
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        return "Callable result";
    }
    
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<String> futureTask = new FutureTask<>(new MyCallable());
        Thread thread = new Thread(futureTask);
        thread.start();
        
        String result = futureTask.get(); // 获取返回结果
        System.out.println(result);
    }
}```

**优点**：可以返回执行结果，可以抛出异常
```

## 二、线程堆栈与调试

获取当前线程堆栈状态，用于调试和问题排查：
```java
StackTraceElement[] trace = Thread.currentThread().getStackTrace();
for (StackTraceElement element : trace) {
    System.out.println(element.getClassName() + "." + element.getMethodName() + ":" + element.getLineNumber());
}

// 查看所有线程的堆栈信息
Thread.getAllStackTraces().forEach((thread, stackTrace) -> {
    System.out.println("Thread: " + thread.getName());
    for (StackTraceElement element : stackTrace) {
        System.out.println("  " + element);
    }
});```
```

## 三、线程状态与控制

Java线程的生命周期包含以下状态：
- **NEW**：新建状态，线程已创建但尚未启动
- **RUNNABLE**：运行状态，线程正在执行或等待CPU资源
- **BLOCKED**：阻塞状态，线程等待获取锁
- **WAITING**：等待状态，线程等待其他线程的特定操作
- **TIMED_WAITING**：超时等待状态，线程在指定时间内等待
- **TERMINATED**：终止状态，线程已完成执行

常用的线程控制方法：
```java
Thread thread = new Thread(runnable);
thread.start(); // 启动线程
thread.join(); // 等待线程结束
thread.join(1000); // 等待线程结束，最多等待1000毫秒
thread.interrupt(); // 中断线程
thread.isInterrupted(); // 检查线程是否被中断
Thread.interrupted(); // 检查并清除中断状态
thread.setDaemon(true); // 设置为守护线程（必须在start()前设置）
thread.setPriority(Thread.MAX_PRIORITY); // 设置线程优先级
thread.getName(); // 获取线程名称
thread.setName("MyThread"); // 设置线程名称
```

**线程状态转换图**：
NEW → RUNNABLE → BLOCKED/Waiting/Timed_Waiting → RUNNABLE → TERMINATED
```

## 四、线程同步机制

### 1. synchronized关键字
```java
// 同步方法
public synchronized void synchronizedMethod() {
    // 同步代码块
}

// 同步代码块
public void method() {
    synchronized(this) {
        // 同步代码块
    }
}

// 类锁
public void staticMethod() {
    synchronized(MyClass.class) {
        // 同步代码块
    }
}```

**注意**：synchronized是可重入锁，同一线程可以多次获取同一把锁
```

### 2. ReentrantLock锁
```java
import java.util.concurrent.locks.ReentrantLock;

private final ReentrantLock lock = new ReentrantLock();

public void method() {
    lock.lock();
    try {
        // 同步代码块
    } finally {
        lock.unlock(); // 确保释放锁
    }
}

// 可中断的获取锁
public void interruptibleLock() throws InterruptedException {
    if (lock.tryLock(5, TimeUnit.SECONDS)) {
        try {
            // 同步代码块
        } finally {
            lock.unlock();
        }
    }
}```

**ReentrantLock vs synchronized**：
- ReentrantLock提供了更灵活的锁定机制
- 支持公平锁、可中断锁、超时锁
- 可以实现更复杂的同步场景
- 需要手动释放锁（通常在finally块中）
```

## 五、线程池

使用线程池管理线程资源，可以减少线程创建和销毁的开销：
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

// 创建固定大小的线程池
ExecutorService fixedThreadPool = Executors.newFixedThreadPool(5);

// 创建单线程线程池
ExecutorService singleThreadExecutor = Executors.newSingleThreadExecutor();

// 创建可缓存的线程池
ExecutorService cachedThreadPool = Executors.newCachedThreadPool();

// 创建定时任务线程池
ScheduledExecutorService scheduledThreadPool = Executors.newScheduledThreadPool(3);

// 提交任务
for (int i = 0; i < 10; i++) {
    final int taskId = i;
    fixedThreadPool.submit(() -> {
        System.out.println("Task " + taskId + " is running in thread: " + Thread.currentThread().getName());
    });
}

// 延迟执行任务
scheduledThreadPool.schedule(() -> {
    System.out.println("Task executed after delay");
}, 5, TimeUnit.SECONDS);

// 周期性执行任务
scheduledThreadPool.scheduleAtFixedRate(() -> {
    System.out.println("Task executed periodically");
}, 1, 3, TimeUnit.SECONDS);

// 关闭线程池
fixedThreadPool.shutdown(); // 等待已提交的任务完成
// fixedThreadPool.shutdownNow(); // 立即关闭线程池

// 等待线程池终止
try {
    if (!fixedThreadPool.awaitTermination(60, TimeUnit.SECONDS)) {
        fixedThreadPool.shutdownNow();
    }
} catch (InterruptedException e) {
    fixedThreadPool.shutdownNow();
    Thread.currentThread().interrupt();
}```

**最佳实践**：
- 根据任务特性选择合适的线程池
- 避免使用无界队列
- 合理设置线程池大小
- 不要忘记关闭线程池
```

## 六、高级并发工具类

Java并发包中提供了许多有用的工具类，用于处理复杂的并发场景：

### 1. CountDownLatch
用于等待多个线程完成任务后再继续执行：
```java
import java.util.concurrent.CountDownLatch;

// 等待多个线程完成
CountDownLatch latch = new CountDownLatch(3);

for (int i = 0; i < 3; i++) {
    final int taskId = i;
    new Thread(() -> {
        System.out.println("Task " + taskId + " is running");
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Task " + taskId + " is completed");
        latch.countDown(); // 计数减1
    }).start();
}

try {
    latch.await(); // 等待计数为0
} catch (InterruptedException e) {
    e.printStackTrace();
}
System.out.println("All tasks are completed");```

**注意**：CountDownLatch的计数只能使用一次，无法重置
```

### 2. CyclicBarrier
用于同步多个线程到达某个屏障点后再继续执行，可以重用：
```java
import java.util.concurrent.CyclicBarrier;

// 同步多个线程到达某个屏障点
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads have reached the barrier");
});

for (int i = 0; i < 3; i++) {
    final int taskId = i;
    new Thread(() -> {
        try {
            System.out.println("Thread " + taskId + " is working");
            Thread.sleep((long) (Math.random() * 2000));
            System.out.println("Thread " + taskId + " is waiting at the barrier");
            barrier.await(); // 等待其他线程
            System.out.println("Thread " + taskId + " has passed the barrier");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }).start();
}```

**CyclicBarrier vs CountDownLatch**：
- CyclicBarrier可以重用，CountDownLatch不能
- CyclicBarrier是所有线程互相等待，CountDownLatch是一组线程等待另一组线程
- CyclicBarrier可以提供一个屏障操作，在所有线程到达后执行
```

### 3. Semaphore
用于控制同时访问特定资源的线程数量：
```java
import java.util.concurrent.Semaphore;

// 创建最多允许3个线程同时访问的信号量
Semaphore semaphore = new Semaphore(3);

for (int i = 0; i < 10; i++) {
    final int taskId = i;
    new Thread(() -> {
        try {
            semaphore.acquire(); // 获取许可
            System.out.println("Task " + taskId + " is accessing the resource");
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            System.out.println("Task " + taskId + " has released the resource");
            semaphore.release(); // 释放许可
        }
    }).start();
}```

### 4. Exchanger
用于两个线程之间交换数据：
```java
import java.util.concurrent.Exchanger;
import java.util.concurrent.TimeUnit;

Exchanger<String> exchanger = new Exchanger<>();

new Thread(() -> {
    try {
        String data1 = "Data from Thread 1";
        System.out.println("Thread 1 is sending: " + data1);
        String receivedData = exchanger.exchange(data1);
        System.out.println("Thread 1 received: " + receivedData);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();

new Thread(() -> {
    try {
        // 模拟处理时间
        TimeUnit.SECONDS.sleep(2);
        String data2 = "Data from Thread 2";
        System.out.println("Thread 2 is sending: " + data2);
        String receivedData = exchanger.exchange(data2);
        System.out.println("Thread 2 received: " + receivedData);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
}).start();```

## 七、线程安全集合

Java提供了多种线程安全的集合类，用于在多线程环境下安全地操作数据：

```java
// ConcurrentHashMap: 线程安全的HashMap实现
import java.util.concurrent.ConcurrentHashMap;
ConcurrentHashMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();
concurrentMap.put("key1", 1);
Integer value = concurrentMap.get("key1");

// CopyOnWriteArrayList: 适用于读多写少场景的ArrayList实现
import java.util.concurrent.CopyOnWriteArrayList;
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("element1");

// BlockingQueue: 支持阻塞操作的队列
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
BlockingQueue<String> queue = new LinkedBlockingQueue<>();
queue.put("item"); // 可能阻塞
String item = queue.take(); // 可能阻塞

// ConcurrentLinkedQueue: 线程安全的队列实现
import java.util.concurrent.ConcurrentLinkedQueue;
ConcurrentLinkedQueue<String> concurrentLinkedQueue = new ConcurrentLinkedQueue<>();
concurrentLinkedQueue.add("element");
String head = concurrentLinkedQueue.poll();
```

线程优化建议
---
1. 尽量使用线程池，避免频繁创建和销毁线程
2. 减少锁的持有时间，避免死锁
3. 优先使用并发工具类，而不是手动实现同步机制
4. 使用ThreadLocal存储线程局部变量
5. 避免使用stop()方法强制终止线程，应该使用interrupt()
6. 合理设置线程优先级，避免滥用高优先级线程
