---
title: Omini_Controller
category: SOF
author: DynAis
tags: OMIC
---

## Omini_Controller()

Omini_Controller()的初衷是



## FAQs



## 1.我就想使用默认配置，我要怎么用？（一般用户）

### 提示！阅读一下指南你应该拥有基础的Unity知识和基础的Python知识, 

**1.检查你的外设**

**2.**

## 2.更多自由度？看这里（具有一些Python经验的用户）

解释1.中不明确的地方

### 2.1配置按钮



### 2.2为按钮配置滤镜



### 2.3 添加自己的滤镜



### 2.4分层



### 2.5 函数和接口



### 2.6 Update 一个周期内发生了什么



## 3.二次开发（具有丰富Python经验的人）

更多可能的玩法



### 3.1 调试器

如何构造debuug数据

### 3.2 软件架构

上图！



#### 3.2.1 Layer 0 - Rawdata

Layer 0 负责从控制器获取数据并转换坐标顺序到自身坐标空间

##### Class State

这个类是控制器数据的抽象，提供了用于获取控制器数据的方法

**Attributes:**

| 值                 | 数据类型   | 数据范围 | 描述 |
| ------------------ | ---------- | -------- | ---- |
| `pos_diff`         | `float[3]` |          |      |
| `rot_diff`         | `float[3]` |          |      |
| `pre_pos_diff`     | `float[3]` |          |      |
| `pre_rot_diff`     | `float[3]` |          |      |
| `t`                | `float`    |          |      |
| `l_button_pressed` | `int`      |          |      |
| `r_button_pressed` | `int`      |          |      |
| `raw`              |            |          |      |
| `raw.x`            | `float`    |          |      |
| `raw.y`            | `float`    |          |      |
| `raw.z`            | `float`    |          |      |
| `raw.roll`         | `float`    |          |      |
| `raw.yaw`          | `float`    |          |      |
| `raw.pitch`        | `float`    |          |      |
| `raw.buttons`      | `int[2]`   |          |      |



**Methods:**

**update_raw_data()**

**描述**：从控制器读取一次原始数据，更新`raw`对象.

**参数**：无

**返回**：无



**update()**

**描述**：使用得到的`raw`对象更新自身数据，控制器的三维坐标(y向前，z向上)会被转换到程序内部坐标系顺序(z向前，y向上)

**参数**：无

**返回**：无





#### 3.2.2 Layer 1 - Event

Layer 1 负责判断和记录控制器上的按钮事件，并且可以抽像每一个按钮事件为一个开关

##### Class Event

这个类继承了Layer 0 中的 `State` 类

**Attributes:**

| 值                 | 数据类型       | 数据范围 | 描述                                                         |
| ------------------ | -------------- | -------- | ------------------------------------------------------------ |
| `event_dict`       | `diction`      |          | 按钮事件枚举字典，对应每一个状态到一个整数                   |
| `event_state_dict` | `diction`      |          | 按钮事件状态字典，一个按钮状态激活为`1`，没激活为`0`         |
| `is_toggle_dict`   | `diction`      |          | 按钮事件是否为开关字典，一个事件如果被视为开关则为`True`，否则为`False` |
| `event`            | `int`          |          | 当前时刻被触发的按钮状态对应的数值                           |
| `t_diff`           | `float`        |          | 距离上一次update过去的时间，既一次loop所花费的时间           |
| `l_button`         | `Event.Button` |          |                                                              |
| `r_button`         | `Event.Button` |          |                                                              |

**Methods:**

**register_toggle(event_name)**

**描述**：

注册一个按钮事件为开关，只对瞬间事件有效，既Click类型的事件，对Hold类型的事件无效. 一个按钮事件被注册为开关之后，每次事件被触发不再只生效一次，而是反转事件状态，就像一个开关一样.

**参数**：

`event_name`：字符串，应该是给出的事件列表中的一个，这个事件会被注册为开关

**返回**：

无



**get_event_state(event_name)**

**描述**：

返回给定按钮事件在`event_state_dict`中的值，既按钮事件是否被激活

**参数**：

`event_name`：字符串，应该是给出的事件列表中的一个

**返回**：

 `1`或者`0`



**get_active_event_state_list()**

**描述**：

返回一个数组，数组包含了所有当前被激活的按钮事件，数值为这个事件在`event_dict`中对应的数字

**参数**：

无

**返回**：

一个`list`，包含了所有当前被激活的按钮事件



**update()**

**描述**：

**参数**：无

**返回**：无





#### 3.2.3 Layer 2 - Process

Layer 2 负责在每个周期计算程序内部摄像机的位姿. 计算会根据按钮事件而改变. 具体根据用户定义的Filter而定.

##### Class Process

这个类继承了Layer 1 中的 `Evene` 类

**Attributes:**

| 值                   | 数据类型   | 数据范围 | 描述 |
| -------------------- | ---------- | -------- | ---- |
| `STOP_EVALUATE_FLAG` | `bool`     |          |      |
| `AS_VARIABLE_TUNNER` | `bool`     |          |      |
| `pre_pos`            | `float[3]` |          |      |
| `pre_rot`            | `float[3]` |          |      |
| `pos`                | `float[3]` |          |      |
| `rot`                | `float[3]` |          |      |

**Methods:**

**stop_evaluate()**

**描述**：

停止继续计算位姿

**参数**：

无

**返回**：

无



**start_evaluate()**

**描述**：

开始继续计算位姿

**参数**：

无

**返回**：

无



**toggle_evaluate()**

**描述**：

转换开始/停止继续计算位姿

**参数**：

无

**返回**：

无



**start_variable_tunner()**

**描述**：

使用这个函数以改变设备进入参数调整状态，位姿计算将会停止，但是设备传感器信息将会继续读取，这个信息可以被继续使用.

**参数**：

无

**返回**：

无



**stop_variable_tunner()**

**描述**：

使用这个函数以结束参数调整状态

**参数**：

无

**返回**：

无



**add_pre_pos_filter_list(event_name, func_list)**

**描述**：

使用这个函数向指定按钮事件添加函数列表, 函数结构应该形如：

```python
def foo(pre_vec3: np.ndarray, vec3: np.ndarray) -> np.ndarray:
    return np.zeros(3)
```

函数接收两个1*3的向量, 第二个变量为当前位移差(既这个变量结合上一个瞬间的位移计算下一个事件的位移)，第一个变量为前一次的位移差.

这个函数应该返回一个1*3的变量, 这个变量会替代当前位移差.

**参数**：

`event_name`:字符串, 按钮事件名称

`func_list`:一个list, 包含函数句柄

**返回**：

无



**add_pre_rot_filter_list(event_name, func_list)**

使用这个函数向指定按钮事件添加函数列表, 函数结构应该形如：

```python
def foo(pre_vec3: np.ndarray, vec3: np.ndarray) -> np.ndarray:
    return np.zeros(3)
```

函数接收两个1*3的向量, 第二个变量为当前旋转差(既这个变量结合上一个瞬间的位移计算下一个事件的旋转)，第一个变量为前一次的旋转差.

这个函数应该返回一个1*3的变量, 这个变量会替代当前旋转差.

**描述**：

使用这个函数向指定按钮事件添加函数列表

**参数**：

`event_name`:字符串, 按钮事件名称

`func_list`:一个list, 包含函数句柄

**返回**：

无



**add_after_pos_filter_list(event_name, func_list)**

使用这个函数向指定按钮事件添加函数列表, 函数结构应该形如：

```python
def foo(pre_vec3: np.ndarray, vec3: np.ndarray) -> np.ndarray:
    return np.zeros(3)
```

函数接收两个1*3的向量, 第二个变量为当前位置结果(既经过计算之后即将输出的位置结果)，第一个变量为前一次的位置结果.

这个函数应该返回一个1*3的变量, 这个变量会替代当前位置结果.

**描述**：

使用这个函数向指定按钮事件添加函数列表

**参数**：

`event_name`:字符串, 按钮事件名称

`func_list`:一个list, 包含函数句柄

**返回**：

无



**add_after_rot_filter_list(event_name, func_list)**

使用这个函数向指定按钮事件添加函数列表, 函数结构应该形如：

```python
def foo(pre_vec3: np.ndarray, vec3: np.ndarray) -> np.ndarray:
    return np.zeros(3)
```

函数接收两个1*3的向量, 第二个变量为当前旋转结果(既经过计算之后即将输出的旋转结果)，第一个变量为前一次的旋转结果.

这个函数应该返回一个1*3的变量, 这个变量会替代当前旋转结果.

**描述**：

使用这个函数向指定按钮事件添加函数列表

**参数**：

`event_name`:字符串, 按钮事件名称

`func_list`:一个list, 包含函数句柄

**返回**：

无



**add_func_list(event_name, func_list)**

**描述**：

使用这个函数向指定按钮事件添加函数列表, 按钮事件被激活时, 这个函数将会执行

**参数**：

`event_name`:字符串, 按钮事件名称

`func_list`:一个list, 包含函数句柄

**返回**：

无



**update()**

**描述**：



**参数**：

无

**返回**：

无





#### 3.2.4 Layer 3 - System

Layer 3 整合了一些常用的摄影机模式提供调用.

##### Class Camera

这个类继承了Layer 2 中的 `Process` 类

**Attributes:**

无

**Methods:**

**register_start_stop_toggle(bind_key_name)**

**描述**：

注册给定按钮事件为开关机按钮

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**register_reset_button(bind_key_name)**

**描述**：

注册给定按钮事件为位姿重置按钮

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**mode_fpv(bind_key_name)**

**描述**：

给定按钮事件激活时进入fpv模式

FPV模式:无限制

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**mode_drone(bind_key_name)**

**描述**：

给定按钮事件激活时进入航拍模式

无人机模式:锁定z轴旋转

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**mode_tripod(bind_key_name)**

**描述**：

给定按钮事件激活时进入三脚架模式

三脚架模式:固定在当前位置, 并且锁定z轴旋转

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**mode_cruise(bind_key_name)**

**描述**：

给定按钮事件激活时进入定速巡航模式

定速巡航模式:保持进入状态时的速度不变

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**mode_slide(bind_key_name)**

**描述**：

给定按钮事件激活时进入滑轨模式

滑轨模式:固定在当前高度平面, 并且锁定z轴旋转

**参数**：

`bind_key_name`:需要绑定的按钮事件的名称

**返回**：

无



**update()**

**描述**：



**参数**：

无

**返回**：

无



