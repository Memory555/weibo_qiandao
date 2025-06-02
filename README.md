# window实现自动每天定时指定目标超话签到

**注意：如果为黄子弘凡的官方超话，可直接操作完步骤一后跳转到步骤五添加auto_signin_lars.exe到任务计划程序即可）**

作者本人是在anaconda配置的实验虚拟环境，这里提供一下自己的环境创建过程以供参考用于步骤二，三，四：

创建虚拟环境：

```
conda create -n file python==3.6
```

激活虚拟环境:

```
conda activate file
```

安装库：

```
pip install requests selenium pyinstaller
```

## ✅ 一、获取自己的cookie

**！！！注意由于cookie作为网络身份证，需要定期更新，所以要定期运行save_cookie.exe更新最新的自己的cookie。**

### 1. 运行save_cookie.exe进入主界面：

![image-20250602123549361](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602123549361.png)

### 2. 选择你的浏览器驱动位置

![image-20250602123559790](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602123559790.png)

### 3. 登录微博账号（60秒内）

点击`启动浏览器并保存 Cookie`，跳转到浏览器页面（注意不要挂梯子），登录自己的微博账号

![image-20250602123757707](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602123757707.png)

### 4.等待保存pkl文件（60秒后）

60秒后会跳出保存成功，在此之前请不要关闭主界面。

![image-20250602123913131](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602123913131.png)

得到cookie文件：

![image-20250602124007009](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602124007009.png)

## ✅ 二、配置目标超话id

### 1. 查找目标超话id

浏览器打开目标超话（这里以黄子弘凡超话为例）得到超话网址：

```bash
https://weibo.com/p/100808c98f988ea22d7b40caed47951f8eb507/super_index
```

此时`100808c98f988ea22d7b40caed47951f8eb507`即为目标超话

### 2. 修改auto_signin.py目标超话id

打开`auto_signin.py`修改`topic_id`部分：

![7034de8ab6cb3cf1e92e78b6f7b5724](https://gitee.com/Memory578/picgo/raw/master/img/7034de8ab6cb3cf1e92e78b6f7b5724.png)

------

**【注】下面三和四二选一操作即可**

## ✅ 三、打包成 `.exe` 文件

### 1. 安装打包工具 `pyinstaller`

打开 CMD 或 PowerShell：

```bash
pip install pyinstaller
```

------

### 2. 使用 `pyinstaller` 打包

确保你的 `weibo_cookies.pkl` 文件在和 `auto_signin.py` 同一目录下。

```bash
pyinstaller --onefile --noconsole auto_signin.py
```

#### 参数解释：

- `--onefile`：打包成一个单独的 `.exe` 文件。
- `--noconsole`：不弹出控制台窗口（适合后台运行）。如需调试，建议先不加该参数。

打包完成后，会在：

```
dist/auto_signin.exe
```

生成最终的可执行文件。

------

### 3. 搬运文件

将以下内容放到一个文件夹中（例如 `WeiboSignInTask/`）：

```
WeiboSignInTask/
├── auto_signin.exe          # 打包后生成
├── save_cookie.exe          # 打包后生成
└── weibo_cookies.pkl        # 必须放在相同目录，供程序加载
```

------

## ✅ 四、编写bat文件

### 1. 创建bat文件

创建一个txt文件，将后缀改为bat即可

------

### 2. 编写bat程序

将下面程序写入程序写入：

```bash
@echo off
REM 初始化 Conda 环境变量（第一次运行 Conda）
CALL E:\Anaconda\Scripts\activate.bat

REM 激活你的虚拟环境
CALL conda activate file

REM 切换到脚本所在目录
cd /d C:\Lars

REM 执行脚本
python auto_signin.py

REM 可选：保存日志
REM python auto_signin.py >> signin_log.txt 2>&1
```

#### 参数解释：

- E:\Anaconda\Scripts\activate.bat:修改为自己的conda环境地址
- conda activate file：修改为自己的conda虚拟环境
- C:\Lars：修改为你程序的放置文件夹

------

### 3. 搬运文件

将以下内容放到一个文件夹中（例如 `WeiboSignInTask/`）：

## ✅ 五、添加到 Windows 任务计划程序

### 1. 打开“任务计划程序”

按下 Win 键 → 搜索并打开「任务计划程序」 → 右侧点击“创建基本任务”。

### 2. 配置任务

- **名称**：微博超话签到
- **触发器**：每天，时间设为 `08:00`；以及开机启动时

![image-20250602124139611](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602124139611.png)

- **操作**：选择「启动程序」，然后点击“浏览”：
  - 选择你打包后的 `auto_signin.exe`或者run_signin.bat

------

### 3. 确保权限

- 勾选 **“使用最高权限运行”**（避免 Cookie 读写权限问题）
- 勾选**“不管用户是否登录都运行”**

![image-20250602124232209](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602124232209.png)

- 需要网络，所以请确保电脑始终联网

------

## ✅ 五、验证运行效果

你可以：

1. 手动右键 `.exe` → 以管理员身份运行，测试是否能成功签到，查看同目录底下的日志查看签到情况：signin_log.txt。

![image-20250602125746242](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602125746242.png)

2或者在任务计划程序中右键任务 → 选择“运行”，测试是否生效。

![image-20250602124329412](https://gitee.com/Memory578/picgo/raw/master/img/image-20250602124329412.png)