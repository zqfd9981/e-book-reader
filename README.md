运行过程：
1、首先解压缩后在命令行cmd进入相关路径；

2、然后首先输入python run_server.py运行服务器。

3、然后再打开一个命令行输入python run_client.py运行客户端。

4、此时会显示登录窗口，可以打开，用server/user.txt里面的用户和密码进行登录。从而进入到书籍列表窗口。
（如果要验证多线程，则需要再打开一个命令行窗口运行客户端，输入用户名密码登录）

5、进入书籍列表窗口后选择需要进行阅读的书籍，会进入到上一次退出的书页进行阅读。可以进行下一页，下一章等定位操作
退出后自动保存，书签更新为退出时的页面。

6、也可以在书籍列表选择对应的书籍选择路径进行下载

整个项目主要分为3个部分：client   server   typechange

client部分: __init__.py 初始化文件，当你运行run_client.py时就进入到这个模块就开始运行。client下还有forms子目录，子目录下四个.py文件分别写着不同情况下的运行前端界面（书架，登录，阅读器，注册界面）；memory.py存储着当前用户的信息。

server部分:
__init__.py初始化文件 ，当你运行run_server.py时进入到该模块。
server下有event子文件夹，这个子文件夹的运行时初始化工作的代码是在__init__.py中。这个函数中定义了一个handle函数，这个函数根据消息类型选择调用不同功能的函数以实现功能。这些不同功能函数的实现实在event中定义的：
download.py:下载功能
login.py:登录功能
read_one_page.py:读一页功能
reading.py：根据书签打开书签页阅读的功能
register.py: 注册的功能
send_list.py: 发送书籍列表的功能
updata_bookmark.py:更新书签的功能
books文件夹下面存放的是书籍的txt文件，相当于书籍的数据库。
bookmarks_database.txt和users.txt存放的是用户的书签列表和用户的登录信息，是两个数据库。


typechange部分：
此部分是完成类型的转化，bytetotype.py是将byte类型转换为相应的原始数据类型，typetobyte反之

Extendedsocket是对原始socket的一种扩展，它将原始的消息流进行封装，发送和接受消息。



 