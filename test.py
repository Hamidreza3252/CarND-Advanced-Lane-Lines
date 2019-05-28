import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.widgets as widgets
import cv2

def onselect(eclick, erelease):
    if eclick.ydata>erelease.ydata:
        eclick.ydata,erelease.ydata=erelease.ydata,eclick.ydata
    if eclick.xdata>erelease.xdata:
        eclick.xdata,erelease.xdata=erelease.xdata,eclick.xdata
    ax.set_ylim(erelease.ydata,eclick.ydata)
    ax.set_xlim(eclick.xdata,erelease.xdata)
    fig.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
filename = "test_images/straight_lines1.jpg"
filename = "test_images/undistorted-01.jpg"

# im = Image.open(filename)
im = mpimg.imread(filename)
arr = np.asarray(im)
plt_image = plt.imshow(arr)

rs = widgets.RectangleSelector(
    ax, onselect, drawtype='box',
    rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.5, fill=True))

plt.show()
