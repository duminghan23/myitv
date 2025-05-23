# myitv
一款支持键盘操作、简单易用的 IPTV 播放器  
本项目通过python_vlc控制vlc播放器进行播放，可以使用数字键盘区的+-/*进行频道加减、音量加减操作，数字进行节目的选择。较为完整地模仿了传统遥控器的使用方法。  


## 特色
支持启动后，播放全屏。   
使用小键盘区进行控制。  
更换频道、更改音量、输入的内容等会在右上角进行同步显示。  

## 键盘操作方法及对应功能
|  键盘   | 功能  |
|  ----  | ----  |
| +  | 频道号向后 |
| -  | 频道号向前 |
| /  | 音量减少5% |
| *  | 音量增加5% |
| 1  | 调整成1号频道 |
| 2  | 调整成2号频道 |
| 36  | 调整成36号频道 |
| Enter  | 静音 |
| esc  | 退出程序 |

## 项目文件介绍
arrange_url.py 是将传统的iptv.m3u文件解析成python中的数组，方便程序操作。  
myitv_main.py 是项目的主文件，使用 python myitv_main.py 即可运行此项目。  
requirements.txt 是项目源码的依赖库文件。  


## iptv.m3u文件内容格式
```
#EXTM3U\
#EXTINF:-1,CCTV1
http://192.168.2.1:4022/rtp/239.255.2.2:8000

#EXTINF:-1,CCTV2
http://192.168.2.1:4022/rtp/239.255.2.3:8006

#EXTINF:-1,CCTV3
http://192.168.2.1:4022/rtp/239.255.5.92:8364

#EXTINF:-1,CCTV3
http://192.168.2.1:4022/rtp/239.255.2.4:8012

#EXTINF:-1,CCTV4
http://192.168.2.1:4022/rtp/239.255.2.5:8018
```



## 项目使用方法
以windows为例：   
1、打开vlc官网 https://www.videolan.org/vlc/download-windows.html ，下载压缩包版本的程序，并解压到一个目录。  
![image](https://github.com/user-attachments/assets/741cc939-d37c-477d-9945-f5886b94c89f)
2、将本项目程序myitv_main.exe放置到vlc解压的目录中。  
3、将自己的iptv.m3u文件也放置到vlc解压的目录中。
![image](https://github.com/user-attachments/assets/28e40465-8278-40d4-9d4c-f5ab0d239701)
4、双击myitv_main.exe程序运行即可。


## 声明
其他第三方任何平台、任何人均不得搬运此项目到任何平台、任何文件，仅用于个人的技术交流、测试。

