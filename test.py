import c_i
from main_eff import calc_simulation


N = 200         # nombre de particules
T = 4         # temps

R = 1           # rayon petite partiucle
m = 1          # masse petite particule
Temp = 300                  # Température en Kelvin


r_b_x = 200
r_b_y = 200


# # execution de la simulation
#

#
# N = 50
# T = 1/1
#
# R = 1
# m = 1
# Temp = 300                  # Température en Kelvin
#
R_grosse = 50
#
# initialisation du système
parts, x_max, y_max = c_i.broooown(N, 10, 10, Temp, R, m, R_grosse)
# parts, dt, x_max, y_max = c_i.equilibre_homog(N, R, 50, 50, m, Temp)

# execution simulation avec extraction données grosse part
data = calc_simulation(x_max, y_max, T, N, parts)


