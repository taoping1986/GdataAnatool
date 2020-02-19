import matplotlib.pyplot as plt
import numpy as np


def Show(x, y, z):
    # 参数为一个list

    len_y = len(x)
    # x = range(len_y)
    _y = [y[-1]] * len_y

    fig = plt.figure(figsize=(960 / 72, 360 / 72))
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(x, y, z, color='blue')
    line_x = ax1.plot(x, _y, color='red')[0]
    line_y = ax1.axvline(x=len_y - 1, color='red')

    ax1.set_title('aaa')
    # 标签
    text0 = plt.text(len_y - 1, y[-1], str(y[-1]), fontsize=10)

    def scroll(event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        fanwei_x = (x_max - x_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + fanwei_x, x_max - fanwei_x))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - fanwei_x, x_max + fanwei_x))
        fig.canvas.draw_idle()

    # 这个函数实时更新图片的显示内容
    def motion(event):
        try:
            temp = y[int(np.round(event.xdata))]
            for i in range(len_y):
                _y[i] = temp
            line_x.set_ydata(_y)
            line_y.set_xdata(event.xdata)
            ######
            text0.set_position((event.xdata, temp))
            text0.set_text(str(temp))

            fig.canvas.draw_idle()  # 绘图动作实时反映在图像上
        except:
            pass

    fig.canvas.mpl_connect('scroll_event', scroll)
    fig.canvas.mpl_connect('motion_notify_event', motion)

    plt.show()


dat = [i for i in range(10000)]
dat2 = [i * 2 for i in dat]
Show(dat[:], dat, dat[:])