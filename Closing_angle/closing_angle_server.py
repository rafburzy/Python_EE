#importing all required modules
import numpy as np
import scipy as sp
from math import *


#bokeh
from bokeh.plotting import Figure, curdoc
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.layouts import column, row

# RMS value of voltage
u = 230 

#time vector
t = np.linspace(0,0.08, 100)

#frequency & angular frequency
f = 50
omega = 2 * pi * f

#Resitance
R = 5

#Inductance
L = 0.1
XL = 2*pi*f*L

#Phase angle
phi=atan(XL/R)

#closing angle [rad]
alpha = 0

#Phase A
#Current response
ia = [(sqrt(2)*u/(sqrt(R**2+XL**2))*(sin(omega*k+alpha-phi)-sin(alpha-phi)*exp(-R/L*k))) for k in t]

#DC component of the current
iadc = [(sqrt(2)*u/(sqrt(R**2+XL**2))*-sin(alpha-phi)*(exp(-R/L*k))) for k in t]

#AC steady state current
iau = [(sqrt(2)*u/(sqrt(R**2+XL**2))*sin(omega*k+alpha-phi)) for k in t]

#Plotting part

source = ColumnDataSource(data={'t': t, 'ia': ia, 'iadc': iadc, 'iau': iau})

plot = Figure(plot_width=800, plot_height=400, title = "Influence of a voltage closing angle on the current in a R-L circuit")
plot.title.text_font_size = '12pt'
plot.xaxis.axis_label="Time [s]"
plot.xaxis.axis_label_text_font_size = '10pt'
plot.yaxis.axis_label="Current [A]"
plot.yaxis.axis_label_text_font_size = '10pt'
plot.line('t', 'ia', source=source, line_width=3, line_alpha=0.6, legend="Circuit current")
plot.line('t', 'iadc', source=source, line_width=2, line_alpha=0.6, color="orange", legend="DC component")
plot.line('t', 'iau', source=source, line_width=2, line_alpha=0.6, color="green", legend="AC component")

# slider
slider = Slider(start=0, end=phi, value=0, step=.1, title="Voltage closing angle [rad]", name="slider")

#callback part

def callback(attr, old, new):
    new_alpha = slider.value
    #Current response
    ia = [(sqrt(2)*u/(sqrt(R**2+XL**2))*(sin(omega*k+new_alpha-phi)-sin(new_alpha-phi)*exp(-R/L*k))) for k in t]

    #DC component of the current
    iadc = [(sqrt(2)*u/(sqrt(R**2+XL**2))*-sin(new_alpha-phi)*(exp(-R/L*k))) for k in t]

    #AC steady state current
    iau = [(sqrt(2)*u/(sqrt(R**2+XL**2))*sin(omega*k+new_alpha-phi)) for k in t]
    
    # source data update
    source.data = {'t': t, 'ia': ia, 'iadc': iadc, 'iau': iau}

slider.on_change('value', callback)
    
layout = row(slider, plot)

curdoc().add_root(layout)