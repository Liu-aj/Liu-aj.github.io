---
layout: post
title: Java线程详解
date: 2018-07-13 13:46:05
forType: Java
category: 线程
tag: [Java, 线程, 并发编程]
---

* content
{:toc}

线程基础
---
Java中创建线程的三种方式：

### 1. 继承Thread类
```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread is running");
    }
    
    public static void main(String[] args) {
        MyThread thread = new MyThread();
        thread.start(); // 启动线程
    }
}
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
}
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
}
```

线程堆栈
---
获取当前线程堆栈状态：
```java
StackTraceElement[] trace = Thread.currentThread().getStackTrace();
for (StackTraceElement element : trace) {
    System.out.println(element.getClassName() + "." + element.getMethodName() + ":" + element.getLineNumber());
}
```

线程状态与控制
---
Java线程的生命周期包含以下状态：
- NEW：新建状态
- RUNNABLE：运行状态
- BLOCKED：阻塞状态
- WAITING：等待状态
- TIMED_WAITING：超时等待状态
- TERMINATED：终止状态

常用的线程控制方法：
```java
Thread thread = new Thread(runnable);
thread.start(); // 启动线程
thread.join(); // 等待线程结束
thread.interrupt(); // 中断线程
thread.setDaemon(true); // 设置为守护线程
thread.setPriority(Thread.MAX_PRIORITY); // 设置线程优先级
```

线程同步机制
---
### 1. synchronized关键字
```java
public synchronized void synchronizedMethod() {
    // 同步代码块
}

public void method() {
    synchronized(this) {
        // 同步代码块
    }
}
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
```

线程池
---
使用线程池管理线程资源：
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

// 创建固定大小的线程池
ExecutorService executor = Executors.newFixedThreadPool(5);

// 提交任务
for (int i = 0; i < 10; i++) {
    final int taskId = i;
    executor.submit(() -> {
        System.out.println("Task " + taskId + " is running");
    });
}

// 关闭线程池
// executor.shutdown(); // 等待已提交的任务完成
// executor.shutdownNow(); // 立即关闭线程池
```

并发工具类
---
Java并发包中提供了许多有用的工具类：

### 1. CountDownLatch
```java
import java.util.concurrent.CountDownLatch;

// 等待多个线程完成
CountDownLatch latch = new CountDownLatch(3);

for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        // 执行任务
        latch.countDown(); // 计数减1
    }).start();
}

latch.await(); // 等待计数为0
System.out.println("All tasks are completed");
```

### 2. CyclicBarrier
```java
import java.util.concurrent.CyclicBarrier;

// 同步多个线程到达某个屏障点
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All threads have reached the barrier");
});

for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        // 执行任务
        try {
            barrier.await(); // 等待其他线程
        } catch (Exception e) {
            e.printStackTrace();
        }
    }).start();
}
```

线程安全集合
---
Java提供了多种线程安全的集合类：
```java
// ConcurrentHashMap - 线程安全的HashMap实现
ConcurrentHashMap<String, String> concurrentHashMap = new ConcurrentHashMap<>();

// CopyOnWriteArrayList - 线程安全的ArrayList实现
CopyOnWriteArrayList<String> copyOnWriteArrayList = new CopyOnWriteArrayList<>();

// ConcurrentLinkedQueue - 线程安全的队列实现
ConcurrentLinkedQueue<String> concurrentLinkedQueue = new ConcurrentLinkedQueue<>();
```

线程优化建议
---
1. 尽量使用线程池，避免频繁创建和销毁线程
2. 减少锁的持有时间，避免死锁
3. 优先使用并发工具类，而不是手动实现同步机制
4. 使用ThreadLocal存储线程局部变量
5. 避免使用stop()方法强制终止线程，应该使用interrupt()
6. 合理设置线程优先级，避免滥用高优先级线程
