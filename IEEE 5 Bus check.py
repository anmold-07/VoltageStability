from GridCal.Engine import *
import networkx as nx
from GridCal.Engine.Simulations.ContinuationPowerFlow.voltage_collapse_driver import VoltageCollapseOptions, \
    VoltageCollapseInput, VoltageCollapse

from GridCal.Engine.Core.snapshot_static_inputs import StaticSnapshotIslandInputs

np.set_printoptions(precision=4)
grid = MultiCircuit()


bus0 = Bus('Bus 0', vnom=230)       # creating an object
grid.add_bus(bus0)                  # appending an object to the list
gen00 = Generator(name='gen00', active_power=40.0, power_factor=0.8, voltage_module=1.0, is_controlled=True,
                 Qmin=-30, Qmax=30, Snom=9999, power_prof=None, power_factor_prof=None, vset_prof=None,
                 Cost_prof=None, active=True)
grid.add_generator(bus0, gen00)
gen01 = Generator(name='gen01', active_power=170.0, power_factor=0.8, voltage_module=1.0, is_controlled=True,
                 Qmin=0, Qmax=127.5, Snom=9999, power_prof=None, power_factor_prof=None, vset_prof=None,
                 Cost_prof=None, active=True)
grid.add_generator(bus0, gen01)


bus1 = Bus('Bus 1', vnom=230)
grid.add_bus(bus1)
grid.add_load(bus1, Load('load 1', P=300, Q=98.61))

bus2 = Bus('Bus 2', vnom=230)
grid.add_bus(bus2)
gen2 = Generator(name='gen2', active_power=323.49, power_factor=0.8, voltage_module=1.0, is_controlled=True,
                 Qmin=-390, Qmax=390, Snom=9999, power_prof=None, power_factor_prof=None, vset_prof=None,
                 Cost_prof=None, active=True)
grid.add_generator(bus2, gen2)
grid.add_load(bus2, Load('load 2', P=300, Q=98.61))

bus3 = Bus('Bus 3', vnom=230, is_slack=True)
bus3.is_slack = True
grid.add_bus(bus3)
gen3 = Generator(name='gen3', active_power=0.0, power_factor=0.8, voltage_module=1.0, is_controlled=True,
                 Qmin=0, Qmax=150, Snom=9999, power_prof=None, power_factor_prof=None, vset_prof=None,
                 Cost_prof=None, active=True)
grid.add_generator(bus3, gen3)
grid.add_load(bus3, Load('load 3', P=99.99, Q=99.99))


bus4 = Bus('Bus 4', vnom=230)
grid.add_bus(bus4)
gen4 = Generator(name='gen4', active_power=466.51, power_factor=0.8, voltage_module=1.0, is_controlled=True,
                 Qmin=-450, Qmax=450, Snom=9999, power_prof=None, power_factor_prof=None, vset_prof=None,
                 Cost_prof=None, active=True)
grid.add_generator(bus4, gen4)


grid.add_branch(Branch(bus0, bus1, 'line 0-1', r=0.00281, x=0.0281, b=0.00712, rate=400.0))
br2 = Branch(bus0, bus3, 'line 0-3', r=0.00304, x=0.0304, b=0.00658, rate=224.4)
grid.add_branch(br2)
grid.add_branch(Branch(bus0, bus4, 'line 0-4', r=0.00064, x=0.0064, b=0.03126, rate=273.3))
grid.add_branch(Branch(bus1, bus2, 'line 1-2', r=0.00108, x=0.0108, b=0.01852, rate=128.3))
grid.add_branch(Branch(bus2, bus3, 'line 2-3', r=0.0029, x=0.0297, b=0.0067, rate=34.6))
br5 = Branch(bus3, bus4, 'line 3-4', r=0.00297, x=0.0297, b=0.00674, rate=240.0)
grid.add_branch(br5)
#-----------------------------------------Power Flow Code--------------------------------------------
'''
options = PowerFlowOptions(SolverType.NR, initialize_with_existing_solution=False, control_p=True, multi_core=False, dispatch_storage=True, control_q=ReactivePowerControlMode.Direct)
power_flow = PowerFlowDriver(grid, options)
power_flow.run()
vm = np.abs(power_flow.results.voltage)
va = np.angle(power_flow.results.voltage)

for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name

bus_list = list(grid.bus_dictionary.values())

result_type = ResultTypes.BusVoltageAngle
mdl = power_flow.results.mdl(result_type, None, np.array(bus_list))
mdl.plot()

result_type = ResultTypes.BusVoltageModule
mdl = power_flow.results.mdl(result_type, None, np.array(bus_list))
mdl.plot()

#result_type = ResultTypes.BusActivePower
#mdl = power_flow.results.mdl(result_type, None, np.array(["Bus 1", "Bus 2", "Bus 3", "Bus 4", "Bus 5"]))
#mdl.plot()
#f1 = plt.figure()
#plt.plot(vm)
#f2 = plt.figure()
#plt.plot(va)
print('\n\n', grid.name)
print('\t|V|:', abs(power_flow.results.voltage))
print('\t|Theta|:', np.angle(power_flow.results.voltage))
print('\t|Sbranch|:', abs(power_flow.results.Sbranch))
print('\t|loading|:', abs(power_flow.results.loading) * 100)
print('\terr:', power_flow.results.error)
print('\tConv:', power_flow.results.converged)

print(power_flow.results.voltage)
v_r = power_flow.results.voltage.real   # splitting the real and imaginary
v_i = power_flow.results.voltage.imag
print(v_r)
print(v_i)

numeric_circuit = grid.compile_snapshot()
numeric_inputs = numeric_circuit.compute()
ybus_1 = numeric_inputs[0].Ybus      # computing the Y bus of the matrix;
R = ybus_1.A.real                    # Scipy sparse matrix to normal matrix;
I = ybus_1.A.imag
print(R)
print(-I)
eigenValues_r, eigenVectors_r = linalg.eig(R)
eigenValues_i, eigenVectors_i = linalg.eig(-I)
idx_r = eigenValues_r.argsort()
idx_i = eigenValues_i.argsort()
eigenValues_r = eigenValues_r[idx_r]        # sorting (in increasing order) the corresponding eigenvalues and the corresponding vectors
eigenVectors_r = eigenVectors_r[:,idx_r]

eigenValues_i = eigenValues_i[idx_i]        # sorting (in increasing order) the corresponding eigenvalues and the corresponding vectors
eigenVectors_i = eigenVectors_i[:,idx_i]

print(eigenValues_r)
print(eigenVectors_r)

print(eigenValues_i)
print(eigenVectors_i)

v_r_hat = (eigenVectors_r.T).dot(v_r)   # finding the graph fourier transform of the real part
v_i_hat = (eigenVectors_i.T).dot(v_i)   # finding the graph fourier transform of the imaginary part

print(v_r_hat)
print(v_i_hat)

fig, ax = plt.subplots()
ax.stem(eigenValues_r, v_r_hat, use_line_collection=True)
fig, ax = plt.subplots()
ax.stem(eigenValues_i, v_i_hat, use_line_collection=True)

plt.show()
'''

'''
v = np.array([1, 2])
A = np.array([[4, 1],
              [6, 3]])
eigenValues, eigenVectors = linalg.eig(A)
idx = eigenValues.argsort()
eigenValues = eigenValues[idx]        # sorting (in increasing order) the corresponding eigenvalues and the corresponding vectors
eigenVectors = eigenVectors[:,idx]
print(eigenValues)
print(eigenVectors)
print(A.dot(v))
'''

numeric_circuit = grid.compile_snapshot()
numeric_inputs = numeric_circuit.compute()
ybus_1 = numeric_inputs[0].Ybus      # computing the Y bus of the matrix;
R = ybus_1.A.real                    # Scipy sparse matrix to normal matrix;
I = ybus_1.A.imag

#-----------------------------------------Voltage Collapse Code------------------------------------------------------------------------------------
vc_options = VoltageCollapseOptions(step=0.001, adapt_step=True, step_min=0.00001, step_max=0.2, error_tol=1e-3, tol=1e-6, max_it=20, verbose=False)
numeric_circuit = grid.compile()
numeric_inputs = numeric_circuit.compute()
Sbase = np.zeros(len(grid.buses), dtype=complex)
Vbase = np.zeros(len(grid.buses), dtype=complex)
for c in numeric_inputs:
    Sbase[c.original_bus_idx] = c.Sbus
    Vbase[c.original_bus_idx] = c.Vbus
unitary_vector = -1 + 2 * np.random.random(len(grid.buses))
print(unitary_vector)

vc_inputs = VoltageCollapseInput(Sbase=Sbase, Vbase=Vbase, Starget=Sbase * (10 + unitary_vector))
vc = VoltageCollapse(circuit=grid, options=vc_options, inputs=vc_inputs)
vc.run()

smoothness_r = []
smoothness_i = []
data = vc.results.voltages
print(data)                # extracting the graph signals in cartesian coordinates

for a in range(data.shape[0]):
    vv = data[a,:]
    vv_r = vv.real
    vv_i = vv.imag
    smoothness_r.append(vv_r.T.dot(R).dot(vv_r))
    smoothness_i.append(vv_i.T.dot(-I).dot(vv_i))

q = [a for a in range(data.shape[0]) if a%6==0]
fig, ax = plt.subplots()
ax.stem(q, np.absolute(smoothness_r[0:data.shape[0]:6]), use_line_collection=True)
ax.set_title('IEEE 5 system', fontsize=20)
ax.set_ylabel('Test Statistic (Real Part)', fontsize=20)
ax.set_xlabel('Number of Iterations of Continuation Power Flow', fontsize=20)

fig, ax = plt.subplots()
ax.stem(q, np.absolute(smoothness_i[0:data.shape[0]:6]), use_line_collection=True)
ax.set_title('IEEE 5 system', fontsize=20)
ax.set_ylabel('Test Statistic (Imaginary Part)', fontsize=20)
ax.set_xlabel('Number of Iterations of Continuation Power Flow', fontsize=20)

print(smoothness_r)
print(smoothness_i)

data = abs(data)  # extracting the graph signals magnitudes


mdl = vc.results.mdl()
fig = plt.figure(figsize=(20, 20))
index, columns, data = mdl.get_data()
indices = [1, 3]                                             # selecting the required buses you want to plot
A = [[sublist[x] for x in indices] for sublist in data]
#print(data)
#print(A)
columns = [columns[x] for x in indices]
df1 = pd.DataFrame(data=A, index=index, columns=columns)
ax = df1.plot()
ax.set_title(mdl.title, fontsize=25)
ax.set_ylabel(mdl.ylabel, fontsize=25)
#mdl.plot()

plt.show()
'''
grid.delete_branch(br5)
vc_options = VoltageCollapseOptions(step=0.001, adapt_step=True, step_min=0.00001, step_max=0.2, error_tol=1e-3, tol=1e-6, max_it=20, verbose=False)
numeric_circuit = grid.compile()
numeric_inputs = numeric_circuit.compute()
Sbase = np.zeros(len(grid.buses), dtype=complex)
Vbase = np.zeros(len(grid.buses), dtype=complex)
for c in numeric_inputs:
    Sbase[c.original_bus_idx] = c.Sbus
    Vbase[c.original_bus_idx] = c.Vbus
unitary_vector = -1 + 2 * np.random.random(len(grid.buses))
vc_inputs = VoltageCollapseInput(Sbase=Sbase, Vbase=Vbase, Starget=Sbase * (10 + unitary_vector))
vc = VoltageCollapse(circuit=grid, options=vc_options, inputs=vc_inputs)
vc.run()

mdl = vc.results.mdl()
index, columns, data = mdl.get_data()
B = [[sublist[x] for x in indices] for sublist in data]
columns = [columns[x] for x in indices]
df2 = pd.DataFrame(data=B, index=index, columns=columns)
df2.plot(ax=ax, ls="--")
'''
'''
#-----------------------------------------NetworkX grid plotting properties--------------------------------------------
#plt.figure()
#g1 = grid.build_Di_graph()
#nx.draw(g1)
plt.figure()
g2 = grid.build_multi_graph()
pos = nx.circular_layout(g2)
nx.draw_networkx(g2,pos,edge_color='black',width=1,linewidths=1,node_size=2000,node_color='pink',alpha=0.9,with_labels = True)
edge_labels = {}
for i, branch in enumerate(grid.branches):
    f = grid.bus_dictionary[branch.bus_from]
    t = grid.bus_dictionary[branch.bus_to]
    edge_labels[(f,t)] = branch.name
#print(edge_labels)
nx.draw_networkx_edge_labels(g2, pos, edge_labels = edge_labels, font_color='red')
#print(type(grid.bus_dictionary) )       # grid.bus_dictionary is a dictionary of
#print(type(grid.buses))                 # grid.buses is a list of objects(buses)

grid.delete_branch(br2)
plt.figure()
g3 = grid.build_multi_graph()
pos = nx.circular_layout(g3)
nx.draw_networkx(g3,pos,edge_color='black',width=1,linewidths=1,node_size=2000,node_color='pink',alpha=0.9,with_labels = True)
edge_labels = {}
for i, branch in enumerate(grid.branches):
    f = grid.bus_dictionary[branch.bus_from]
    t = grid.bus_dictionary[branch.bus_to]
    edge_labels[(f,t)] = branch.name
#print(edge_labels)
nx.draw_networkx_edge_labels(g3, pos, edge_labels = edge_labels, font_color='red')
'''


#-----------------------------------------Power Flow Code--------------------------------------------
'''
options = PowerFlowOptions(SolverType.NR,
                           initialize_with_existing_solution=False,
                           control_p=True,
                           multi_core=False, dispatch_storage=True,
                           control_q=ReactivePowerControlMode.Direct
                           )
power_flow = PowerFlowDriver(grid, options)
power_flow.run()
vm = np.abs(power_flow.results.voltage)
va = np.angle(power_flow.results.voltage)

for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name

bus_list = list(grid.bus_dictionary.values())

result_type = ResultTypes.BusVoltageAngle
mdl = power_flow.results.mdl(result_type, None, np.array(bus_list))
mdl.plot()

result_type = ResultTypes.BusVoltageModule
mdl = power_flow.results.mdl(result_type, None, np.array(bus_list))
mdl.plot()

#result_type = ResultTypes.BusActivePower
#mdl = power_flow.results.mdl(result_type, None, np.array(["Bus 1", "Bus 2", "Bus 3", "Bus 4", "Bus 5"]))
#mdl.plot()
#f1 = plt.figure()
#plt.plot(vm)
#f2 = plt.figure()
#plt.plot(va)
print('\n\n', grid.name)
print('\t|V|:', abs(power_flow.results.voltage))
print('\t|Theta|:', np.angle(power_flow.results.voltage))
print('\t|Sbranch|:', abs(power_flow.results.Sbranch))
print('\t|loading|:', abs(power_flow.results.loading) * 100)
print('\terr:', power_flow.results.error)
print('\tConv:', power_flow.results.converged)
#--------------------------------------------------------------------------------------

#grid.plot_graph()
#plt.show()
'''
