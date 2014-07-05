# Splat - splat/interpol.py
#
# Copyright (C) 2014 Guillaume Tucker <guillaume@mangoz.org>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Tkinter import *

def spline(spline, n=100, w=400, h=400):
    if (n < 2) or (w < 2) or (h < 2):
        raise ValueError("Invalid view parameters")

    step = (spline.end - spline.start) / float(n - 1)
    pts = list()
    ymin = ymax = None
    for i in range(n):
        x = spline.start + (i * step)
        y = spline.value(x)
        if ymin is None or y < ymin:
            ymin = y
        elif ymax is None or y > ymax:
            ymax = y
        pts.append(spline.value(x))

    master = Tk()
    c = Canvas(master, width=w, height=h)
    c.pack()
    c.create_rectangle(0, 0, w, h, fill="white")
    xratio = float(w) / float(n - 1)
    yratio = float(h) / (ymax - ymin)
    y0 = (pts[0] - ymin) * yratio
    for x, y in enumerate(pts[1:]):
        y = (y - ymin) * yratio
        x1 = (x + 1) * xratio
        x = x * xratio
        c.create_line(x, (h - y0), x1, (h - y))
        y0 = y
    mainloop()

def frag(frag, w=400, h=200):
    if (w < 2) or (h < 2):
        raise ValueError("Invalid view parameters")

    width = w
    height = h * frag.channels
    scale = h / 2
    master = Tk()
    c = Canvas(master, width=width, height=height)
    c.pack()
    c.create_rectangle(0, 0, width, height, fill="white")

    axes = list()
    for n in range(frag.channels):
        y0 = h * (n + 0.5)
        c.create_line(0, y0, width, y0)
        axes.append(y0)

    i = 0
    y0 = tuple(0.0 for n in range(frag.channels))
    for x in range(w):
        j = frag.s2n((x + 1)* frag.duration / w)
        y1 = tuple(0.0 for n in range(frag.channels))
        l = j - i
        for n in range(i, j):
            y1 = tuple((a + b) for a, b in zip(y1, frag[n]))
        y1 = tuple(y * scale / l for y in y1)
        for axis, a, b in zip(axes, y0, y1):
            c.create_line(x, (axis - a), (x + 1), (axis - b))
        i = j
        y0 = y1

    mainloop()
