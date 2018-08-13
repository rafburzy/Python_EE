import numpy as np
import scipy as sp
from scipy.integrate import odeint, ode, romb, cumtrapz
from bokeh.plotting import figure, output_file, output_notebook, show, curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.layouts import column, row, widgetbox
from math import pi, sin, cos, atan, sqrt

# RMS value of voltage
u = 230 

#time vector
t = np.linspace(0,0.4, 1000)

#frequency & angular frequency
f = 50
omega = 2 * pi * f

def calRLCcir(R, L, C, alpha):
    #Resitance (values to consider 5 and 10 Ohms)
    R = R

    #Inductance 0.1
    L = L
    XL = 2*pi*f*L

    #Capacitance (worth to consider 0.01 - two inertia or 0.001 - oscillator)
    C = C
    XC = 1/(omega*C)

    #Phase angle
    phi=atan((XL-XC)/R)

    #closing angle [rad]
    alpha = alpha

    ub = [sqrt(2)*u*sin(omega*k + alpha) for k in t]

    # definition of the function dp/dt

    def di(y,t):
        #x = i, p = di/dt
        x, p = y[0], y[1]

        dx = p
        dp = 1/L*(omega*sqrt(2)*u*cos(omega*t + alpha)-R*p-(1/C)*x)

        return [dx, dp]

    #initial state

    #initial capacitor voltage
    uc0 = 0

    y0 = [0.0, 1/L*(u-uc0)]

    I = odeint(di, y0, t)

    ib = I[:,0]

    #Capacitor voltage derivative
    duc2 = ib/C

    uc2 = cumtrapz(duc2, dx=0.4/1000, initial=0)
    
    return ib, uc2, ub

ib, uc2, ub = calRLCcir(R=5, L=0.1, C=0.01, alpha=0)

source = ColumnDataSource(data={'t': t, 'i': ib, 'uc': uc2, 'usupp': ub})

p=figure(plot_width=600, plot_height=400, title='Current in RLC circuit')
p.line('t', 'i', source=source)
p.xaxis.axis_label='Time [s]'
p.yaxis.axis_label='Current [A]'

m=figure(plot_width=600, plot_height=400, title='Voltages')
m.line('t', 'usupp', source=source, legend='Line voltage', color='orange')
m.line('t', 'uc', source=source, legend='Capacitor voltage', color='green')
m.xaxis.axis_label='Time [s]'
m.yaxis.axis_label='Voltage[V]'
m.legend.location = "bottom_left"

# widgets
Slider_C = Slider(start=0.0001, end=0.01, value=0.01, step=.00001, title="Capacitance [F]")
Slider_R = Slider(start=1, end=50, value=5, step=1, title="Resistance [Ohm]")
Slider_L = Slider(start=0.001, end=1, value=0.1, step=0.001, title="Inductance [H]")
#Slider_Uo = Slider(start=10e3, end=100e3, value=20e3, step=10e3, title="Charging voltage [V]")

layout = row(widgetbox(Slider_C, Slider_R, Slider_L), column(p,m))

def callback(attr, old, new):
    new_C = Slider_C.value
    new_R = Slider_R.value
    new_L = Slider_L.value
    ib, uc2, ub = calRLCcir(R=new_R, L=new_L, C=new_C, alpha=0)
    source.data = {'t': t, 'i': ib, 'uc': uc2, 'usupp': ub}
    
Slider_C.on_change('value', callback)
Slider_R.on_change('value', callback)
Slider_L.on_change('value', callback)

curdoc().add_root(layout)