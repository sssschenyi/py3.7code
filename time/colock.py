"""
# author: chenyi
# ide: notepad++
# date: 16:46 2022年11月28日
# version: 1.0.0
# 闹钟程序，定时播放MP3
"""
import pygame
import time
# 多线程模块
import _thread

MP3 = r'F:\mp3\Unchained Melody.mp3' # 全局变量地址

# 获得本机时间函数
def showTime():
    """显示时间""" 
    t = time.localtime() # 实例化本机时间
    global get_hour, get_minute, get_second 
    get_hour = t.tm_hour # 获得本机小时时间
    get_minute = t.tm_min # 获得本机分钟时间
    get_second = t.tm_sec # 获得本机秒种时间
    return '%02d:%02d:%02d' %(get_hour, get_minute, get_second)


# 播放函数
def playMp3(playLen = 10):
    # 播放MP3
    pygame.mixer.init()  # 初始化音频函数
    pygame.mixer.music.load(MP3) # 载入文件
    pygame.mixer.music.play() # 播放文件
    #  开始播放倒计时
    time.sleep(playLen) # 播放 playLen 长度 
    pygame.mixer.music.stop() # playLen 参数时间到 mp3 就停止播放


# 监控时间函数
def monitorTime(h, m, s=0):
        setClockHour = h
        setClockMin = m
        setClocksecond = s
        mp3_play_len = 10
        # 监控时间，时间到就调用播放 playMp3() 函数
        if get_hour == setClockHour and get_minute == setClockMin and get_second==setClocksecond:
            print('%02d:%02d:%02d,clock 1, start mp3' %(get_hour, get_minute, get_second))
            # playMp3() # 调用播放函数
            _thread.start_new_thread( playMp3, (mp3_play_len,) ) # 多线程调用 playmp3 函数
        elif setClockHour == -1 and get_minute == setClockMin and get_second==setClocksecond: # 每个小时的第 setClockMin 分种运行一次 playMp3 函数
            print('>>>%2d:%02d,clock minute, start mp3' %( get_minute, get_second))
            _thread.start_new_thread( playMp3, (mp3_play_len,) ) # 多线程调用 playmp3 函数
        elif setClockHour == -1 and setClockMin == -1 and get_second==setClocksecond: # 每分钟的 setClocksecond 秒时间点运行 playMp3 函数
            print('>>>%02d,clock second, start mp3' %(get_second))
            _thread.start_new_thread( playMp3, (mp3_play_len,) ) # 多线程调用 playmp3 函数
        
        """
            # 本函数的参数使用方法    
            monitorTime(12,30,30) # 12:30:30  每天的12:30:30开始闹钟   
            monitorTime(-1,30,30) # -1,30,0  每小时的30分:30秒开始闹钟   
            monitorTime(-1,-1,30) # -1,-1,30  每分钟的第30秒开始闹钟 
            monitorTime(-1,-1,-1) # -1,-1,-1  取消闹钟该时间段的闹钟 
            """
   
if __name__ == '__main__':
    # 用二维列表的数据结构设置闹钟的时间 [时, 分, 秒]
    setColock = [[16, 28, 20], [20, 2, 0], [-1, -1, 30], [-1, -1, -1], [-1, -1, -1]] 
    # setColock = [[13, 15, 0], [14, 30, 0], [-1, 57, 1], [-1, -1, -1], [-1, -1, -1]] 
    # setColock = [[-1, -1, 'd']] # 也可以单独设置一维数组
    while True:
        print(showTime())
        time.sleep(1)
        # showTime()
        for i in setColock: #遍历列表使 monitorTime 函数获得参数
            monitorTime(i[0], i[1], i[2])
