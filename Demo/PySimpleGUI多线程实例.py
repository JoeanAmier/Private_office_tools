import threading
import time

import PySimpleGUI as sg

"""
    设计模式-使用共享全局变量的多线程长任务GUI提供了一种在PySimpleGUI环境中运行长时间运行操作的方法。
    PySimpleGUI代码，以及底层GUI框架，作为主主线程运行。
    正在启动的线程中包含“长时间工作”。使用全局变量（小心地）进行通信有两种向用户报告“进度”的方式。
    您可以模拟工作线程发生的两种不同场景。
    1.如果提前知道时间量，或者可以将工作分解为可计数的单位，则使用进度条。
    2.如果任务是一段很长的时间，不能分解为更小的单位，则会显示一个动画GIF，只要任务在运行，它就会旋转。
"""

total = 100  # 与进度条一起使用的单位数
message = ''  # 线程用于将消息发送回主线程
progress = 0  # 当前进度最大为“总计”


def long_operation_thread(seconds):
    """
    通过全局消息变量与GUI通信的工作线程此线程可以阻塞任意长的时间，GUI不会受到影响：
    param seconds：（int）睡眠时间，最终阻塞调用
    """

    global message, progress

    print('Thread started - will sleep for {} seconds'.format(seconds))
    for _ in range(int(seconds * 10)):
        time.sleep(.1)  # sleep for a while
        progress += total / (seconds * 10)

    message = '*** The thread says.... "I am finished" ***'


def the_gui():
    """
    启动并执行GUI从全局变量读取数据，并在用户退出关闭窗口时显示返回值
    """
    global message, progress

    sg.theme('Light Brown 3')

    layout = [[sg.Text('Long task to perform example')],
              [sg.Output(size=(80, 12))],
              [sg.Text('Number of seconds your task will take'),
               sg.Input(key='-SECONDS-', size=(5, 1)),
               sg.Button('Do Long Task', bind_return_key=True),
               sg.CBox('ONE chunk, cannot break apart', key='-ONE CHUNK-')],
              [sg.Text('Work progress'), sg.ProgressBar(total, size=(20, 20), orientation='h', key='-PROG-')],
              [sg.Button('Click Me'), sg.Button('Exit')], ]

    window = sg.Window('Multithreaded Demonstration Window', layout)

    thread = None

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break
        elif event.startswith('Do') and not thread:
            print(
                'Thread Starting! Long work....sending value of {} seconds'.format(
                    float(
                        values['-SECONDS-'])))
            thread = threading.Thread(
                target=long_operation_thread,
                args=(
                    float(
                        values['-SECONDS-']),
                ),
                daemon=True)
            thread.start()
        elif event == 'Click Me':
            print('Your GUI is alive and well')

        if thread:  # 如果线程正在运行
            if values['-ONE CHUNK-']:  # 如果是一个大操作，则显示动画GIF
                sg.popup_animated(
                    sg.DEFAULT_BASE64_LOADING_GIF,
                    background_color='white',
                    transparent_color='white',
                    time_between_frames=100)
            else:  # 不是一个大的操作，所以更新一个进度条
                window['-PROG-'].update_bar(progress, total)
            thread.join(timeout=0)
            if not thread.is_alive():  # 线程完成
                print(f'message = {message}')
                # stop animination in case one is running
                sg.popup_animated(None)
                thread, message, progress = None, '', 0  # reset variables for next run
                window['-PROG-'].update_bar(0, 0)  # clear the progress bar

    window.close()


if __name__ == '__main__':
    the_gui()
