import numpy as np


# Aluminium
al = {'alpha': 0.9975, 'rho': 2.698, 'masse_ato': 4.48e-22, 'vol': 58.58, 'G':1.759,
      'Kt':0.2, 'Kp': 0.043, 'f': 1, 'N_gamma': 3340, 't_mes': 6.967, 'sigma': 0.23e-24, 'lam': 0.309}

van = {'alpha': 1, 'm': 42.32, 'masse_ato': 0.846e-21, 'G': 3.393,
      'Kt': 0.2, 'Kp': 0.05, 'f': 1, 'N_gamma': 33381, 't_mes': 9.4, 'lam': 0.185}

cu_63 = {'alpha': 0.6917, 'rho': 8.96, 'vol': 37.235, 'masse_ato': 1.04e-21, 'G': 2.765,
       'Kt': 0.2, 'Kp': 0.35, 'f': 0.61, 'N_gamma': 7505, 't_mes': 6.067, 'lam': 9.096e-4}

cu_65 = {'alpha': 0.3083, 'rho': 8.98, 'vol': 37.235, 'masse_ato': 1.08e-21, 'G': 2.765,
         'Kt': 0.2, 'Kp': 0.15, 'f': 1, 'N_gamma': 843, 't_mes': 6.067, 'lam': 0.135}


def get_Nc(alpha, masse_ato, m=None, rho=None, vol=None):
    if m==None:
        res = alpha * rho * vol / masse_ato
    else:
        res = alpha * m / masse_ato

    return res

def get_K(G, Kt, Kp, f):
    return G*Kt*Kp*f

def get_phi(lam, N_gamma, sigma, K, Nc, t_mes):
    return (lam*N_gamma/(sigma*K*Nc))*1/(1- np.exp(-lam*t_mes))

def get_Q(lam, N_gamma, K, t_mes):
    return (lam * N_gamma / K )*(1/(1 - np.exp(-lam * t_mes)))

def get_sigma(phi, Q, Nc):
    return Q/(phi*Nc)

Nc_al = get_Nc(al['alpha'], al['masse_ato'], rho=al['rho'], vol=al['vol'])
#print('Aluminium')
#print(Nc_al)
K_al  = get_K(al['G'], al['Kt'], al['Kp'], al['f'])
#print(K_al)
phi = get_phi(al['lam'], al['N_gamma'], al['sigma'], K_al, Nc_al, al['t_mes'])
phi = phi/60
print(phi)

Nc_van = get_Nc(van['alpha'], van['masse_ato'],  m=van['m'])

K_van = get_K(van['G'], van['Kt'], van['Kp'], van['f'])

Q_van = get_Q(van['lam'], van['N_gamma'], K_van, van['t_mes'])
Q_van = Q_van/60 # minutes -> secondes
sigma_van = get_sigma(phi,Q_van, Nc_van)


print('Vanadium')
#print(Nc_van)
#print(K_van)
#print(Q_van)
print(sigma_van)

print('Cu_63')

G_cu = 0.0358

Nc_cu_63 = get_Nc(cu_63['alpha'], cu_63['masse_ato'], rho=cu_63['rho'], vol=cu_63['vol'])

K_cu_63 = get_K(G_cu, cu_63['Kt'], cu_63['Kp'], cu_63['f'])
Q_cu_63 = get_Q(cu_63['lam'], cu_63['N_gamma'], K_cu_63, cu_63['t_mes'])
Q_cu_63 = Q_cu_63/60 # minutes -> secondes
sigma_cu_63 = get_sigma(phi,Q_cu_63, Nc_cu_63)
print(sigma_cu_63)

print('Cu_65')

Nc_cu_65 = get_Nc(cu_65['alpha'], cu_65['masse_ato'], rho=cu_65['rho'], vol=cu_65['vol'])
print(Nc_cu_65)
K_cu_65 = get_K(G_cu, cu_65['Kt'], cu_65['Kp'], cu_65['f'])
Q_cu_65 = get_Q(cu_65['lam'], cu_65['N_gamma'], K_cu_65, cu_65['t_mes'])
Q_cu_65 = Q_cu_65/60 # minutes -> secondes
sigma_cu_65 = get_sigma(phi,Q_cu_65, Nc_cu_65)
print(sigma_cu_65)
