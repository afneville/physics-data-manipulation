from math import pi

diameter = 0.0284
abs_unc_diameter = 0.0001
area = pi*(diameter/2)**2
perc_unc_area = (abs_unc_diameter/diameter * 100)*2

abs_unc_mass = 0.0001
abs_unc_volume = 2/(1E6)
gravity_acceleration = 9.81
