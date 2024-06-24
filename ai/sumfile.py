import os
import pygame
import time

mp3_id = 0


def play_music(file):
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(file)
    # 获取音乐时间长度
    sone_length = pygame.mixer.Sound(file).get_length()
    print("2音乐长度：{:.0f}".format(sone_length))
    pygame.mixer.music.play()
    # 等待音乐播放完毕

    while pygame.mixer.music.get_busy():
        time.sleep(1)
        sone_length = sone_length - 1
        clock.tick(30)
        print("2音乐长度：{:.0f}".format(sone_length))



def count_mp3_files(folder_path):
    mp3_count = 0
    for file in os.listdir(folder_path):
        if file.endswith(".mp3"):
            mp3_count += 1
            print(mp3_count,file) # 打印文件名
            # print("mp3_id",mp3_id)
            # print(type(mp3_id),type(mp3_count))
            if mp3_id == mp3_count:
                # print("播放第{}首歌曲".format(mp3_id))
                play_music(os.path.join(folder_path, file))
                # print("音乐长度2：", sone_length)
        else:
            pass
            # os.remove(os.path.join(folder_path, file))
    # return mp3_count

# 示例
folder_path = "F:/mp3"  # 替换为你要统计的文件夹路径
mp3_count = count_mp3_files(folder_path)
print("指定目录中包含 {} 个MP3文件。".format(mp3_count))
mp3_id = int(input("输入播放歌曲的ID:"))
count_mp3_files(folder_path)

