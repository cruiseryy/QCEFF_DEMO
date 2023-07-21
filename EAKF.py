import numpy as np
from matplotlib import pyplot as plt

H = np.array([1, np.sqrt(3)])
H.shape = [1, 2]

sigma = 0.2
T = 100
N = 1000

xx = np.zeros([T, 2, N])
yy = np.zeros([])
xa = np.random.randn(2, N)
xx[0, :, :] = xa 

y_obs = np.random.rand(T, 1) * 2

M = np.array([[0.25, 0.75],[0.65, 0.35]])
bins = np.linspace(-3, 3, 60)
for i in range(1, T):
    xp = M @ xa + sigma * np.random.randn(2, N)
    yp = H @ xp

    # Fitting and merging the prior and likelihood 
    # closed here since both are Gaussian
    mu_yp = np.mean(yp)
    sigma_yp = np.std(yp, ddof = 1)
    mu_yo = y_obs[i]
    sigma_yo = sigma
    mu_ya = (mu_yp/sigma_yp**2 + mu_yo/sigma_yo**2) / (1/sigma_yp**2 + 1/sigma_yo**2)
    sigma_ya = np.sqrt(1 / (1/sigma_yp**2 + 1/sigma_yo**2))
    ya = (yp - mu_yp) / sigma_yp * sigma_ya + mu_ya

    Si = np.cov(xp, ddof = 1)
    Ki = Si @ H.T * 1 / ( H @ Si @ H.T + sigma**2)
    xa = xp + Ki @ (ya - yp)
    
    xx[i, :, :] = xa 
    fig, ax = plt.subplots()
    hyp, hxp, _ = ax.hist(yp[0, :], bins, alpha=0.5, label='prior')
    hya, hxa, _ = ax.hist(ya[0, :], bins ,alpha=0.5, label='analysis')
    ax.plot([y_obs[i], y_obs[i]], [0, np.max([hyp, hya])], color = 'black', linestyle = 'dashed')
    ax.set_ylabel('freq')
    ax.set_xlabel('y')
    ax.legend()
    pause = 1
    plt.close(fig)
    
pause = 1