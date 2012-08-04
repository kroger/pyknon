import math
from pyknon.simplemusic import inversion
import Tkinter as Tk


MARGIN = 30

def x_y_points(tick, number_points, radius):
    angle = tick * (360.0 / number_points)
    rad_angle = math.radians(angle)
    x = radius * math.sin(rad_angle)
    y = radius * math.cos(rad_angle)
    return int(round(x)), int(round(y))


def points_in_a_circle(n_points, radius):
    return [x_y_points(n, n_points, radius) for n, p in enumerate(range(n_points))]


def scaled_points(radius):
    points = points_in_a_circle(12, radius)
    return [(x + radius + MARGIN, radius - y + MARGIN) for x, y in points]


def plot_circle(canvas, width, points):
    canvas.create_oval(MARGIN, width, width, MARGIN)


def plot_points(canvas, points):
    for x, y in points:
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")


def plot_numbers(canvas, points):
    for n, (x, y) in enumerate(points):
        canvas.create_text(x, y-10, text=str(n), font=("Helvetica Bold", 14))


def plot_notes(notes, canvas, points, color="black", dash=None):
    p = points
    for n1, n2 in zip(notes, notes[1:]):
        p = points[n1] + points[n2]
        canvas.create_line(*p, width=3, fill=color, dash=dash)


def canvas_notes(notes_list, width=400, is_black_and_white=False):
    canvas = Tk.Canvas(width=width, height=width)
    canvas.pack(side=Tk.TOP)
    radius = (width / 2) - MARGIN
    points = scaled_points(radius)
    plot_points(canvas, points)
    plot_numbers(canvas, points)
    plot_circle(canvas, width - MARGIN, points)
    if is_black_and_white:
        for notes, dash in notes_list:
            plot_notes(notes, canvas, points, dash=dash)
    else:
        for notes, color in notes_list:
            plot_notes(notes, canvas, points, color)
    return canvas


def view(notes_list, width=400):
    canvas = canvas_notes(notes_list, width)


def notes_ps(notes_list, filename, width=400, is_black_and_white=False):
    canvas = canvas_notes(notes_list, width, is_black_and_white=is_black_and_white)
    L, T, R, B = canvas.bbox(Tk.ALL)
    canvas.postscript(file=filename, height=B, width=R,
                      pageheight=B, pagewidth=R, x=0, y=0)


def plot2(notes1, notes2, filename):
    notes_list = [(notes1, "black"), (notes2, "red")]
    notes_ps(notes_list, filename)


def plot2_bw(notes1, notes2, filename):
    notes_list = [(notes1, None), (notes2, (4, 4))]
    notes_ps(notes_list, filename, is_black_and_white=True)
