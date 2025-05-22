import keyboard
import queue
import threading
import vlc

from arrange_url import channel_url_list


# 更新 OSD 显示
def update_osd(custom_text=None):
    osd_time_out = 0 if globals_audio_volume == 0 else 6000    # 音量为0时，osd显示时间为永久，否则显示时间为6秒
    if player.video_get_marquee_int(vlc.VideoMarqueeOption.Timeout) != osd_time_out:
        player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, osd_time_out)

    if custom_text is None:    # 没有传输内容时，默认显示内容
        custom_text = f"频道号：{globals_channel_num}    频道: {channel_list[globals_channel_num - 1][0]}    音量: {globals_audio_volume}"
    player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, custom_text)


# 控制播放的频道操作、音量操作
def play_vlc(event_all: str):
    print("接收到输入的频道操作：", event_all, end='  ')

    global globals_channel_num
    global globals_audio_volume
    global globals_audio_volume_before

    if event_all == '+':    # 频道列表向后移动
        globals_channel_num += 1
    elif event_all == '-':    # 频道列表向前移动
        globals_channel_num -= 1
    elif event_all == '/':    # 声音减小
        if globals_audio_volume-5 >= 0:
            globals_audio_volume -= 5
            player.audio_set_volume(globals_audio_volume)
            print('变更后：globals_audio_volume', globals_audio_volume)
            update_osd()
        else:
            print("音量已最小，无法再减小")
            update_osd("音量已最小，无法再减小")
        return
    elif event_all == '*':    # 声音增大
        if globals_audio_volume+5 <= 120:
            globals_audio_volume += 5
            player.audio_set_volume(globals_audio_volume)
            print('变更后：globals_audio_volume', globals_audio_volume)
            update_osd()
        else:
            print("音量已最大，无法再增加")
            update_osd("音量已最大，无法再增加")
        return
    elif event_all == 'enter':    # 静音
        if globals_audio_volume == 0:    # 此时就属于静音的状态，需要还原音量
            globals_audio_volume = globals_audio_volume_before
            update_osd()
        else:    # 此时需要进行静音，需要记录一下音量
            globals_audio_volume_before = globals_audio_volume
            globals_audio_volume = 0
            update_osd("静音")
        player.audio_set_volume(globals_audio_volume)
        print('变更后：globals_audio_volume', globals_audio_volume)
        return
    else:
        try:
            globals_channel_num = int(event_all)
        except Exception as ee:
            print("输入错误，请重新输入", ee)
            update_osd("输入错误，请重新输入")
            return
    try:
        channel_name = channel_list[globals_channel_num - 1][0]
        channel_url = channel_list[globals_channel_num - 1][1]
        print("正在播放：", channel_name, channel_url)
        player.set_mrl(channel_url)
        player.play()
        update_osd()  # 更新 OSD 显示
    except Exception as ee:
        print("输入错误，请重新输入", ee)
        return

# 处理输入频道数字的操作
def process_events():
    global processing_flag
    if not processing_flag:
        processing_flag = True
        # 处理队列中的所有事件
        event_all: str = ''
        while not event_queue.empty():
            event = event_queue.get()
            # print(f"Processed key: {event.name}")
            event_all += event.name
            event_queue.task_done()
        play_vlc(event_all)
        processing_flag = False


# 监听键盘的操作
def on_key_event(event: keyboard.KeyboardEvent):
    if event.name in ('+', '-', '*', '/', 'enter'):    # 音量控制、频道控制，立即响应
        print("立即响应", end='')
        play_vlc(event_all=event.name)
    else:
        # 将按键事件放入队列中
        event_queue.put(event)

        # 显示当前队列中的按键
        current_keys = list(event_queue.queue)  # 获取当前队列中所有事件对象
        key_names = [e.name for e in current_keys]
        combined_text = "输入: " + "".join(key_names)
        player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, combined_text)

        # 每次有按键事件时，取消之前的定时器（如果有）
        global timer
        if 'timer' in globals() and timer is not None:
            timer.cancel()

        # 设置一个新的定时器，等待2秒如果没有新的按键，则处理队列
        timer = threading.Timer(1.0, process_events)
        timer.start()


if __name__ == '__main__':
    globals_channel_num: int = 1    # 全局变量：频道号
    globals_audio_volume: int = 60     # 全局变量：音量
    globals_audio_volume_before: int = 60      # 全局变量，记录静音前的音量

    # 获取所有的频道
    channel_list: list = channel_url_list()

    # 创建一个线程安全的队列对象
    event_queue = queue.Queue()

    # 用来控制是否应该处理队列的标志
    processing_flag: bool = False

    # 创建一个 VLC 播放器
    player = vlc.MediaPlayer()
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)  # 启用 OSD
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, 6)  # 0居中，1左侧，2右侧，4顶部，8底部，5左上，6右上，9底左，10底右
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 6000)  # 单位是毫秒，6秒=6000ms

    # 将vlc播放器全屏
    player.set_fullscreen(True)
    player.audio_set_volume(globals_audio_volume)  # 设置默认音量
    player.set_mrl(channel_list[globals_channel_num-1][1])    # 设置默认播放的频道
    update_osd()
    player.play()

    # 设置键盘监听器，当有按键按下时调用 on_key_event 函数
    keyboard.on_press(on_key_event)

    print("开始程序。在两秒内没有进一步按键后，将会打印所有按下的按键。")
    # keyboard.wait('decimal')  # 等待直到用户按下 ESC 键结束程序
    keyboard.wait('esc')  # 等待直到用户按下 ESC 键结束程序

    # 如果程序退出前还有未处理的事件，确保它们被处理
    # 实际不用处理，直接丢弃
    # if 'timer' in globals() and timer is not None:
    #     timer.cancel()
    # process_events()

    print("程序已退出。")
