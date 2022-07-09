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

![image-20220704214405298](D:/Workspace/.Typora%20Images%20Hub/image-20220704214405298.png)