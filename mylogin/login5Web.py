import hashlib
import time
import random
import atexit
import win32api
import redis



# 远程连接 redis 数据库
# 官方网站 https://app.redislabs.com/
# redis 免费远程地址 redis-13349.c60.us-west-1-2.ec2.cloud.redislabs.com
"""

# 连接远程的地址
def con_redis():
    remoteAddress = 'redis-13349.c60.us-west-1-2.ec2.cloud.redislabs.com'
    remotePort   = '13349'
    passwd = 'dMEMaBSh9Uq1D5WfpcIfV6rhIitg15LA'
    # 使用连接池 连接数据库
    pool = redis.ConnectionPool(host=remoteAddress, port=remotePort, password=passwd, decode_responses=True)
    r = redis.Redis(connection_pool=pool, charset='UTF-8', encoding='UTF-8')    
    return r
""" 

# 连接本地的
def con_redis():
    remoteAddress = '127.0.0.1'
    remotePort   = '6379'
    passwd = ''
    # 使用连接池 连接数据库
    pool = redis.ConnectionPool(host=remoteAddress, port=remotePort, password=passwd, decode_responses=True)
    r = redis.Redis(connection_pool=pool, charset='UTF-8', encoding='UTF-8')    
    return r
    
##  web 版, 使用 redis 数据库
inputusername = "用户名："
inputpassword = "密  码："
bakUserFile = 0
usernameYesNo = 0
userName = '' 
userPawd = ''
userRegistTime = ''
loginname = ''
loginppwd = ''
loginok = False
# 首次安装默认管理员用户和密码
# 密码保存模式是 用户名+密码
default_user_pwd = "admin"

# userInfoList 用户信息列表名,也可以看成是数据库名
# key 名设计 数据库名:表名:ID
userInfoList = "login:userinfo:1" 
# onLineUserList 在线的用户名列表
onLineUserList = "login:onlineuser:1"
# 备份用户信息数据列表名  
bakuserInfoList = "bak:userinfo:1"

"""
check user_db is exist
"""
def userdb_exist():
    start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # start_date = 等于首次安装使用的时间
    rs=con_redis()
    user_db = rs.scan()
    onLineUserList_db = user_db[1].count(onLineUserList)
    userInfoList_db = user_db[1].count(userInfoList)
    if userInfoList_db != 1:
        # default_admin_user
        rs.rpush(userInfoList,default_user_pwd,strMd5(default_user_pwd*2),start_date)
        # print("创建管理用户 ok")
    elif userInfoList_db:
        pass
        # print("管理用户数据库存在")
    
    if onLineUserList_db != 1:
        rs.rpush(onLineUserList,"null_user",start_date)
        # print("创建默认在线用户 ok")
    elif onLineUserList_db:
        pass
        # print("在线用户数据库存在")

'''
MD5加密字符串
'''
def strMd5(str):
    a = hashlib.md5() #初始化MD5
    a.update(str.encode(encoding='utf-8'))
    newstr = a.hexdigest()[0:16]#截取md5 前16位数字
    return newstr
'''
check username is exist
# 检测用户名 是否存在
'''  
def checkUserInfo(usernameStr):
    global usernameYesNo
    global userName, userPawd, userRegistTime
    allUserName      = []
    allUserPass      = []
    alluserRegistTime = []
    
    # 查询数据
    rs = con_redis()
    userinfo = rs.lrange(userInfoList, 0 , -1)
    # load user info        
    for i in range(0, len(userinfo), 3):    
        # 生成用户信息列表 
        # print(user)
        n = userinfo[i:i+3] # 把全部信息分割成单个列表
        allUserName.append(n[0]) # 全部用户名列表
        allUserPass.append(n[1]) # 全部用户密码列表
        alluserRegistTime.append(n[2]) # 全部用户注册时间的列表     
   
    # 查找用户名是否在用户名列表里面
    if (usernameStr in allUserName):
        infoIndex = allUserName.index(usernameStr) 
        # infoIndex 得到用户名列表索引号
        userName = allUserName[infoIndex]
        # userName 得到用户名
        userPawd = allUserPass[infoIndex]
        # userPawd 得到用户密码
        userRegistTime =  alluserRegistTime[infoIndex]
        # userRegistTime 得到用户注册时间        
        usernameYesNo = 1
        # 如果用户名存在，就设置 usernameYesNo 变量等于 1
    elif (usernameStr not in allUserName) :
        usernameYesNo = 0

'''
    注册用户代码
'''
def regist(): 
    registTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("regist in...")
    # print(os.path.realpath(fo.name))
    getUsername = input(inputusername)
    getPassword = input(inputpassword)
    # strip 移除字符串头尾指定的空格。
    getUsername = getUsername.strip()
    getPassword = getPassword.strip()
    
    if len(getUsername) == 0:
        print("用户名不能填空白")
    elif len(getPassword) == 0:
        print("密码不能填空白")
    elif len(getUsername) > 0 or len(getPassword) > 0:
        checkUserInfo(getUsername)# 用函数检查 getUsername 是否存在
        if usernameYesNo == 1:
            print("！！！用户名  %s  已经被注册！！！"%getUsername)
            # 返回一个 1 到 9 之间的数字
            r = random.randint(1, 9)
            # proposal 翻译:建议
            proposalName = getUsername+str(r)
            print("！！！建议使用  %s  来注册！！！"%proposalName)
        elif usernameYesNo == 0:
            # 把用户名和密码连接起来加密,主要是为了使密码是唯一的字符串
            userANDpwd = getUsername+getPassword
            # 插入信息到数据库
            rs = con_redis()
            rs.rpush(userInfoList,getUsername,strMd5(userANDpwd),registTime)
            print("regist ok(注册成功)...")
    else:
        print("regist info error 注册失败")

'''
用户登录验证
'''
def login():
    loginTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("login...")
    global loginname
    global loginppwd
    global loginok
    loginname = input(inputusername)
    loginppwd = input(inputpassword)
    loginname = loginname.strip() # 去掉空格字符
    loginppwd = loginppwd.strip() # 去掉空格字符   
    
    # check user is exist 
    checkUserInfo(loginname)# 用函数检查 username 是否存在
    # 把用户名和密码连接起来加密
    userANDpwd = loginname+loginppwd
    if len(loginname) == 0:
        print("用户名不能是空")
    elif len(loginppwd) == 0:
        print("密码不能是空")
    elif loginname != userName:
        print("用户名 %s 还未注册..."%loginname)
    elif strMd5(userANDpwd) != userPawd:
        # print("userPawd",userPawd)
        print("密码填写错误...")
    elif loginname == userName and strMd5(userANDpwd) == userPawd:                
        # print("loginppwd:",loginppwd)
        # print("userPawd:",userPawd)
        loginok = True
        print("登录成功,欢迎(%s)"%userName)
        # 登录成功后，把用户写入到登录的数据库  
        # onLineUserList 是登录成功的数据库列表名
        # 插入信息到数据库
        rs = con_redis()
        rs.rpush(onLineUserList,loginname,loginTime)
    else:
        print("登录失败!!!")

#  显示在线的用户
def showallUserName():
    rs = con_redis()
    userinfo = rs.lrange(onLineUserList,0 ,-1)

    print("在线用户:")
    print("ID \t NAME \t loginTime")
    print("--------- ----------")
    id = 1
    # 把全部信息分割成 2位长度 的单个列表
    # range(2,) 从 2 开始截取，把2前面的默认用户不显示
    for i in range(2, len(userinfo), 2):
        n = userinfo[i:i+2]
        # print(n[1:])
        u = n[0]  # 在线的用户名  
        lt = n[1] # 登录的时间
        # print(id,"\t",u, p, t)
        print(id,"\t",u,"\t", lt)
        id += 1
    
# 备份用户数据的函数
def bakUserInfoFile():
    if loginok:
        if loginname == "admin":
            # 查询数据
            rs = con_redis()
            userinfo = rs.lrange(userInfoList, 0, -1)
            # print(userinfo)
            for i in userinfo:
                rs.rpush(bakuserInfoList, i)
            print("备份数据成功")
        else:
            print("备份数据失败...\n请登录管理员账户再进行备份")
    else:
        print("还没登录,不能使用这个功能")

# recovery 恢复用户数据函数
def recoveryUserInfoFile():
    pass

# updateFileStr 函数用来修改字符串，例如 修改用户密码
def updateFileStr(newStr):
    """
    替换文件中的字符串
    old_str:旧字符串
    new_str:新字符串
    """
    # 查询数据库
    rs = con_redis()
    userinfo = rs.lrange(userInfoList, 0, -1)
    # userPawd变量 等于用户名的密码
    # indexpwd 索引用户的密码
    indexpwd =userinfo.index(userPawd)
    #  Lset 通过索引来修改元素的值。
    rs.lset(userInfoList, indexpwd, newStr)

# 开启私聊,  7824
def char_one():
    import socket
    import threading
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '172.20.137.118'  # host 地址可以指定服务器地址
    port = 9999
    s.connect((host, port))  # 连接到服务器
    name = loginname
    s.send(name.encode("utf-8"))  # 给服务器发信息
    
    
    # receive_handle 接受处理数据
    def receive_handle(sock, addr):
        while True:
            data = sock.recv(1024)  # 接受数据
            msg = data.decode("utf-8")
            # msg = str(msg)
            index = msg.index(":")
            my_name = msg[0:index]
            if name == my_name:  # 跳过打印自己发送的信息
                continue
            print("\n消息来自于", msg)
    # 开启线程监听接收消息
    receive_thread = threading.Thread(target=receive_handle, args=(s, '1'))
    receive_thread.start()

    while True:
        re_data = input("\n输入消息>>>")
        if re_data == 'exit':
            break
        s.send(re_data.encode("utf-8"))



# 开启群聊  7825
def char_all():
    print("start all char")


# 显示菜单
def show_menu(login_status):
    if login_status:
        print("\t\t\t welcome %s ，您好！"%loginname,"\n")
        print("开启私聊(7824) \t\t 开启群聊(7825)\n")
        print("查看在线用户(7469)\t 备份用户数据(2225)\n")
        print("修改密码(8732)\t\t 恢复数据(7326)\n")           
        print("退出账号(886) \t\t 帮助(4357)")
    else:
        print("\t\t\t游客模式")
        print("\n注册(7343) \t\t 登录(4644) \t\t 帮助(4357)\n")
        
# 帮助
def help(login_status):
    show_menu(login_status)
    
# updatePass 函数用来修改用户密码
def updatePass():
    newPwd2  = input("输入新密码:")
    newPwd3  = input("确认新密码:")
    newPwd2.strip() # 去掉空格字符
    newPwd3.strip() # 去掉空格字符
    if len(newPwd2) > 0 and len(newPwd3) > 0 and newPwd2 == newPwd3:
        # 如果 2 次输入的密码相同,就调用 updateFileStr 函数
        # 把用户名和密码连接起来加密
        newpwd = userName+newPwd3
        updateFileStr(strMd5(newpwd))
        print("修改密码成功")
    else:
        print("两次输入密码不一样!")

# exit 退出在线状态
# @atexit.register  @ 埃特符号是一个装饰器函数
# atexit 模块用来退出处理器时，必须要执行的代码
# ctrl + c 终止程序后,下面这条函数会执行 
@atexit.register
def logout():
    # 开始调用 upDateOnlineFile函数
    upDateOnlineFile()
    global loginok
    loginok = False
   
    
    
# exit 退出在线状态
# window_cmd_exit函数功能: 触发控制台被关闭的事件,下面这条函数会执行 
def window_cmd_exit(sig):
    # 开始调用 upDateOnlineFile函数
    upDateOnlineFile()
    global loginok
    loginok = False
    
    
# upDateOnlineFile函数的功能：更新在线用户的配置文件
# upDateOnlineFile 这个函数主要给 logout函数 和 window_cmd_exit函数调用
def upDateOnlineFile():
    # 打开数据库
    rs = con_redis()
    # 读取 onLineUserList 列表的内容
    line = rs.lrange(onLineUserList, 0, -1)
    loginname_index = line.index(loginname)
    login_time_index = loginname_index + 1
    if loginname in line:
        #Lset 通过索引来删除元素的值。
        rs.lrem(onLineUserList, -1, line[loginname_index])
        rs.lrem(onLineUserList, -1, line[login_time_index])
    
# 程序入口
# __name__ == "__main__": 的意思是只有当前脚本能用。其他 import 会报错
if __name__ == "__main__":
    while True:
        userdb_exist()    
        # 登录成功后显示的 菜单
        if loginok:
            """
                win32api.SetConsoleCtrlHandler函数功能: 
                触发控制台被关闭的事件,如果控制台被概关闭
                下面这条函数会执行.
                并且调用 window_cmd_exit() 函数
             """
            win32api.SetConsoleCtrlHandler(window_cmd_exit, True)
            show_menu(loginok)
            inputMent = input("输入数字菜单:")
            # isdigit函数 检查 inputMent 变量是否由数字组成
            if inputMent.isdigit():
                if int(inputMent) == 7469:                
                    showallUserName()
                elif int(inputMent) == 7824:
                    char_one()
                elif int(inputMent) == 7825:
                    char_all()
                elif int(inputMent) == 2225:
                    # 2225 对应的是9键 backup 字母的相应键盘
                    bakUserInfoFile()
                elif int(inputMent) == 7326:
                    # 7326 对应的是9键 recovery 字母的相应键盘
                    recoveryUserInfoFile()
                elif int(inputMent) == 8732:
                    # 8732 对应的是9键 update 字母的相应键盘
                    updatePass()
                elif int(inputMent) == 886:
                    logout()            
                elif int(inputMent) == 4357:
                    help(loginok)                
                else:
                    print("命令不存在,请输入正确的命令")
            else:
                print("输入菜单错误")
        
        # 游客模式的菜单        
        if (not loginok):
            show_menu(loginok)
            inputMent = input("输入数字菜单:")
            if inputMent.isdigit():
                if int(inputMent) == 7343:
                    regist()
                elif int(inputMent) == 4644:
                    login()
                elif int(inputMent) == 4357:
                    help(loginok)
                else:
                    print("命令不存在,请输入正确的命令")
            else:
                print("输入菜单错误")
            
