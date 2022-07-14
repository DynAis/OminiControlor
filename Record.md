## socket

```
import socket
  UDP_IP = "127.0.0.1"
  UDP_PORT = 1347
  MESSAGE = "{0},{1},{2},{3},{4},{5}\n".format(pos[0], pos[1], pos[2], rot[0], rot[1], rot[2])
  # change message to byte
  MESSAGE = MESSAGE.encode('utf-8')
    
  print("UDP target IP: %s" % UDP_IP)
  print("UDP target port: %s" % UDP_PORT)
  print("message: %s" % MESSAGE)
  sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
  sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
```



## wrapper

https://www.youtube.com/watch?v=r7Dtus7N4pI

```python
def send_to_vofa(func):
    def wrapper(*args, **kwargs):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 1347  # vofa local port
        MESSAGE = func(*args, **kwargs)
        print("Debug Message: %s" % MESSAGE)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
        sock.sendto(MESSAGE.encode("utf-8"), (UDP_IP, UDP_PORT))

    return wrapper
```

https://foofish.net/python-decorator.html

```python
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args)
        return wrapper

    return decorator

@use_logging(level="warn")
def foo(name='foo'):
    print("i am %s" % name)

foo()
```



## *args **kwargs

https://zhuanlan.zhihu.com/p/149532177



## async

https://www.youtube.com/watch?v=t5Bo1Je9EmE&t=1380s

两个Task, 一个0,5s, 一个1s

现在让他们执行的总和时间为1s

- await 用在 async 里执行其他 async 函数
- asyncio.run(func()) 启动
- asyncio
- 定义了task的函数可以并行计算
- 从定义了task的那一刻函数就开始运行
- await表示在这里停住等待



## Archtech

![image-20220711132826933](D:/Workspace/.Typora%20Images%20Hub/image-20220711132826933.png)



## 按钮状态图

![image-20220711184012110](D:/Workspace/.Typora%20Images%20Hub/image-20220711184012110.png)



## 精彩语句

```python
# 向量转csv字符串
",".join(map(str, vec3))
```

```python
next_event = self.event_dict["none"]
        if self.event == self.event_dict["none"]:
            if (
                self.l_button_pressed
                and self.r_button_pressed
                and self.l_button_hold_time < self.BUTTON_HOLD_THRESHOLD
                and self.r_button_hold_time < self.BUTTON_HOLD_THRESHOLD
            ):
                next_event = self.event_dict["all_button_click"]
            elif (
                self.l_button_pressed
                and self.l_button_hold_time < self.BUTTON_HOLD_THRESHOLD
            ):
                next_event = self.event_dict["left_button_click"]
            elif (
                self.r_button_pressed
                and self.r_button_hold_time < self.BUTTON_HOLD_THRESHOLD
            ):
                next_event = self.event_dict["right_button_click"]

        if (
            self.event == self.event_dict["left_button_click"]
            or self.event == self.event_dict["right_button_click"]
            or self.event == self.event_dict["all_button_click"]
        ):
            if (
                not self.l_button_pressed
                and not self.r_button_pressed
                and self.l_button_hold_time < self.BUTTON_HOLD_THRESHOLD
                and self.r_button_hold_time < self.BUTTON_HOLD_THRESHOLD
            ):
                next_event = self.event_dict["all_wait"]
            elif (
                not self.l_button_pressed
                and self.l_button_hold_time > self.BUTTON_HOLD_THRESHOLD
            ):
                next_event = self.event_dict["left_button_wait"]
            elif (
                not self.r_button_pressed
                and self.r_button_hold_time > self.BUTTON_HOLD_THRESHOLD
            ):
                next_event = self.event_dict["right_button_wait"]
                return next_event
```

## FSM

```
from transitions import Machine
```

https://runnerliu.github.io/2017/05/26/transitionstranslate/

https://github.com/pytransitions/transitions#hsm