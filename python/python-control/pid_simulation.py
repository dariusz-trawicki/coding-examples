import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# --- 1) Plant: G(s) = 1 / (s^2 + 2s + 1)
G = ctrl.tf([1], [1, 2, 1])

# --- 2) PID with derivative filter (PIDF) to make it proper
Kp, Ki, Kd = 3.0, 1.0, 0.4
N = 50.0  # derivative filter factor

s = ctrl.tf([1, 0], [1])
C = Kp + Ki/s + (Kd*s) / (1 + s/N)

# --- 3) Closed-loop transfer function
T = ctrl.feedback(C * G, 1)

# --- 4) Step response of output y(t)
t = np.linspace(0, 10, 2000)
t, y = ctrl.step_response(T, t)

# --- 5) Control effort u(t) for r(t)=1: u = C * (1 - T) * r, r = step
S = 1 - T
t, u = ctrl.step_response(C * S, t)

# --- 6) Plots
plt.figure()
plt.plot(t, y)
plt.axhline(1.0, linestyle="--")
plt.xlabel("t [s]")
plt.ylabel("y(t)")
plt.title("Closed-loop step response with PIDF")
plt.grid(True)

plt.figure()
plt.plot(t, u)
plt.xlabel("t [s]")
plt.ylabel("u(t)")
plt.title("Control effort u(t) for unit step reference")
plt.grid(True)

plt.show()

print("Plant G(s) =", G)
print("Controller C(s) =", C)
print("Closed-loop T(s) =", T)
