import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import time


# Lecture des fichiers

def read_params(params_path="params.txt"):
    with open(params_path, "r") as f:
        params = f.read().strip().split()
        
    x_max = float(params[0])
    y_max = float(params[1])
    dt = float(params[2])
    T = float(params[3])
    N = int(params[4])
    R = [float(x) for x in params [5:]]
    
    return x_max, y_max, R, dt, T, N

def read_data(excel_path="data.xlsx"):
    df = pd.read_excel(excel_path)
    
    x_col = sorted([c for c in df.columns if str(c).startswith("X")], key=lambda s: int(str(s)[1:]))
    y_col = sorted([c for c in df.columns if str(c).startswith("Y")], key=lambda s: int(str(s)[1:]))
    
    N = len(x_col)
    
    position = np.zeros((len(df), N, 2), dtype=float)
    position[:,:,0] = df[x_col].to_numpy()
    position[:,:,1] = df[y_col].to_numpy()
    
    return position, N


# Animation

def anim(excel_path="data.xlsx", params_path="params.txt"):
    global ani
    x_max, y_max, R, dt, T, N_params = read_params(params_path)
    data, N_data = read_data(excel_path)
    
    if N_params != N_data:
        print(f"Y'a un problème chef, c'est pas les mêmes N")
        N = min(N_params, N_data)
    else :
        N = N_params

    
    n_frames = data.shape[0]
    times = np.arange(n_frames) * dt
    

    # Figure
    
    fig, ax = plt.subplots(figsize=(13,13))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-x_max/10,x_max*11/10)
    ax.set_ylim(-y_max/10,y_max*11/10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Particules de gaz dures en 2D")
    
    ax.plot([0, x_max, x_max, 0, 0], [0, 0, y_max, y_max,0], lw=2)
    
    # Particules
    
    circles = []
    
    spec_col = 0
    for i in range(N):
        if i == spec_col :
            color = "red"
        else:
            color="blue"
        circ = plt.Circle((data[0, i, 0], data[0, i, 1]), R[i], color=color, fill=True,)
        ax.add_patch(circ)
        circles.append(circ)
        

    # Temps
    start_real_time = time.perf_counter()
    # time_text = ax.text(-0.02, 1.02, "", transform=ax.transAxes)
    # real_time_text = ax.text(0.75, 1.02, "", transform=ax.transAxes)
    
    def t_init():
        for i, circ in enumerate(circles):
            circ.center = (data[0, i, 0], data[0, i, 1])
        # time_text.set_text(f"t = {times[0]:.2f} s")
        # real_time_text.set_text("vrai temps = 0.00s")
        return circles
    
    def t_update(frame):
        for i, circ in enumerate(circles):
            x, y = data[frame, i, 0], data[frame, i, 1]
            circ.center = (x, y)
        # time_text.set_text(f"t = {times[frame]:.2f} s")
        # clock = time.perf_counter() -  start_real_time
        # real_time_text.set_text(f"vrai temps = {clock:.2f}")
        return circles
    
    epsilon = dt*1000
    ani = FuncAnimation(fig, t_update, frames=n_frames, init_func=t_init, interval=epsilon, blit=True)
    plt.show()



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

"""

anim.py nous permet d'animer la simulation.

"""

def anim_direct(x_max, y_max, R, dt, T, N_params, data_pos):
    global ani

    data = pd.DataFrame(data_pos)
    N_data = data.shape[1]//2

    if N_params != N_data:
        print(f"ERREUR:: N correspond pas au nombre de particules")
        N = min(N_params, N_data)
    else :
        N = N_params

    n_frames = data.shape[0]
    print(f"frames: {n_frames}")
    times = np.arange(n_frames) * dt

    # Figure
    fig, ax = plt.subplots(figsize=(13,13))
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Particules de gaz dures en 2D")
    
    
    # ax.set_xlim(0, x_max/(10**7))
    # ax.set_ylim(0, y_max/(10**7))
    ax.plot([0, x_max, x_max, 0, 0], [0, 0, y_max, y_max,0], lw=2)

    # Particules
    circles = []

    spec_col = 0
    for i in range(N):
        if i == spec_col :
            color = "red"
        else:
            color="blue"
        circ = plt.Circle((data.loc[0, f"X{i}"], data.loc[0, f"Y{i}"]), R[i], color=color, fill=True,)
        ax.add_patch(circ)
        circles.append(circ)
        

    def t_init():
        for i, circ in enumerate(circles):
            circ.center = (data.loc[0, f"X{i}"], data.loc[0, f"Y{i}"])
        return circles
    
    def t_update(frame):
        for i, circ in enumerate(circles):
            x, y = data.loc[frame, f"X{i}"], data.loc[frame, f"Y{i}"]
            circ.center = (x, y)
        return circles
    
    epsilon = dt*1000
    ani = FuncAnimation(fig, t_update, frames=n_frames, init_func=t_init, interval=epsilon, blit=True)
    ani.save("animation.gif", writer=PillowWriter(fps=20))
    plt.show()


