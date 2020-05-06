from GridCal.Engine import *
import networkx as nx
from GridCal.Engine.Simulations.ContinuationPowerFlow.voltage_collapse_driver import VoltageCollapseOptions, \
    VoltageCollapseInput, VoltageCollapse

np.set_printoptions(precision=4)
grid = MultiCircuit()

#-----------------------------------------Start of modeling Nordi-32----------------------------------------------------
bus1 = Bus('Bus 1 HV', vnom=139.92, is_slack=True)    # creating an object
grid.add_bus(bus1)                                    # appending an object to the list
gen0 = Generator(name='gen0', active_power=232.4, power_factor=0.8, voltage_module=1.06, is_controlled=True, Qmin=0, Qmax=10)
grid.add_generator(bus1, gen0)

bus2 = Bus('Bus 2 HV', vnom=137.94)       # creating an object
grid.add_bus(bus2)                        # appending an object to the list
gen1 = Generator(name='gen1', active_power=40, voltage_module=1.045, is_controlled=True, Qmin=-40, Qmax=50)
grid.add_generator(bus2, gen1)
grid.add_load(bus2, Load('load@BUS2', P=21.7, Q=12.7))

bus3 = Bus('Bus 3 HV', vnom=133.32)       # creating an object
grid.add_bus(bus3)                        # appending an object to the list
gen2 = Generator(name='gen2', active_power=0, voltage_module=1.01, is_controlled=True, Qmin=0, Qmax=40)
grid.add_generator(bus2, gen2)
grid.add_load(bus3, Load('load@BUS3', P=94.2, Q=19))

bus4 = Bus('Bus 4 HV', vnom=134.46)       # creating an object
grid.add_bus(bus4)                        # appending an object to the list
grid.add_load(bus4, Load('load@BUS4', P=47.8, Q=-3.9))

bus5 = Bus('Bus 5 HV', vnom=134.67)       # creating an object
grid.add_bus(bus5)                        # appending an object to the list
grid.add_load(bus5, Load('load@BUS5', P=7.6, Q=1.6))

bus6 = Bus('Bus 6 LV', vnom=35.31)       # creating an object
grid.add_bus(bus6)                       # appending an object to the list
grid.add_load(bus6, Load('load@BUS6', P=11.2, Q=7.5))

bus7 = Bus('Bus 7 ZV', vnom=1.06)       # creating an object
grid.add_bus(bus7)                        # appending an object to the list

bus8 = Bus('Bus 8 TV', vnom=11.99)       # creating an object
grid.add_bus(bus8)                        # appending an object to the list

bus9 = Bus('Bus 9 LV', vnom=34.86)       # creating an object
grid.add_bus(bus9)                        # appending an object to the list
grid.add_load(bus9, Load('load@BUS9', P=29.5, Q=16.6))

bus10 = Bus('Bus 10 LV', vnom=34.69)       # creating an object
grid.add_bus(bus10)                        # appending an object to the list
grid.add_load(bus10, Load('load@BUS10', P=9.0, Q=5.8))

bus11 = Bus('Bus 11 LV', vnom=34.88)       # creating an object
grid.add_bus(bus11)                        # appending an object to the list
grid.add_load(bus11, Load('load@BUS11', P=3.5, Q=1.8))

bus12 = Bus('Bus 12 LV', vnom=34.82)       # creating an object
grid.add_bus(bus12)                        # appending an object to the list
grid.add_load(bus12, Load('load@BUS12', P=6.1, Q=1.6))

bus13 = Bus('Bus 13 LV', vnom=34.66)       # creating an object
grid.add_bus(bus13)                        # appending an object to the list
grid.add_load(bus13, Load('load@BUS13', P=13.5, Q=5.8))

bus14 = Bus('Bus 14 LV', vnom=34.18)       # creating an object
grid.add_bus(bus14)                        # appending an object to the list
grid.add_load(bus14, Load('load@BUS14', P=14.9, Q=5.0))

grid.add_branch(Branch(bus1, bus2, 'transformer branch 1-2', r=0.01938, x=0.0591, b=0.0528, rate=192.6, bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1, bus5, 'transformer branch 1-5', r=0.054, x=0.2230, b=0.0492, rate=93.94,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus2, bus3, 'transformer branch 2-3', r=0.046, x=0.197, b=0.0438, rate=88.9,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus2, bus4, 'transformer branch 2-4', r=0.058, x=0.1762, b=0.034, rate=88.9,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus2, bus5, 'transformer branch 2-5', r=0.056, x=0.173, b=0.034, rate=50.75,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus3, bus4, 'transformer branch 3-4', r=0.06, x=0.171, b=0.0128, rate=29.05,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus4, bus5, 'line 4-5', r=0.013, x=0.042, b=0.0, rate=73.7))
grid.add_branch(Branch(bus4, bus7, 'transformer branch 4-7', r=0.0, x=0.2, b=0.0, rate=33.6, tap = 0.978,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus4, bus9, 'transformer branch 4-9', r=0.0, x=0.5565, b=0.0, rate=19.88, tap = 0.96,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5, bus6, 'transformer branch 5-6', r=0.0, x=0.25, b=0.0, rate=58.77, tap = 0.932,bus_to_regulated=True, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus6, bus11, 'line 6-11', r=0.094, x=0.1989, b=0.0, rate=10.65))
grid.add_branch(Branch(bus6, bus12, 'line 6-12', r=0.122, x=0.255, b=0.0, rate=9.95))
grid.add_branch(Branch(bus6, bus13, 'line 6-13', r=0.06, x=0.13, b=0.0, rate=23.46))
grid.add_branch(Branch(bus7, bus8, 'line 7-8', r=0.0, x=0.176, b=0.0, rate=28, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus7, bus9, 'line 7-9', r=0.0, x=0.11, b=0.0, rate=33, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus9, bus10, 'line 9-10', r=0.03, x=0.084, b=0.0, rate=7.11))
grid.add_branch(Branch(bus9, bus14, 'line 9-14', r=0.12, x=0.27, b=0.0, rate=11.6))
grid.add_branch(Branch(bus10, bus11, 'line 10-11', r=0.08, x=0.192, b=0.0, rate=5.8))
grid.add_branch(Branch(bus12, bus13, 'line 12-13', r=0.22, x=0.192, b=0.0, rate=2.28))
grid.add_branch(Branch(bus13, bus14, 'line 13-14', r=0.170, x=0.34, b=0.0, rate=7.5))
grid.add_shunt(bus9, Shunt( name='shunt', B=19.0))
#-----------------------------------------End of modeling Nordic-32--------------


#-----------------------------------------Power Flow Code--------------------------------------------
'''
options = PowerFlowOptions(SolverType.NR,
                           initialize_with_existing_solution=True,
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
print('\t|Theta|:', np.degrees(np.angle(power_flow.results.voltage)))
print('\t|Sbranch|:', abs(power_flow.results.Sbranch))
print('\t|loading|:', abs(power_flow.results.loading) * 100)
print('\terr:', power_flow.results.error)
print('\tConv:', power_flow.results.converged)
'''

numeric_circuit = grid.compile_snapshot()
numeric_inputs = numeric_circuit.compute()
ybus_1 = numeric_inputs[0].Ybus      # computing the Y bus of the matrix;
R = ybus_1.A.real                    # Scipy sparse matrix to normal matrix;
I = ybus_1.A.imag


eigenValues_r, eigenVectors_r = linalg.eig(R)
eigenValues_i, eigenVectors_i = linalg.eig(-I)
idx_r = eigenValues_r.argsort()
idx_i = eigenValues_i.argsort()
eigenValues_r = eigenValues_r[idx_r]        # sorting (in increasing order) the corresponding eigenvalues and the corresponding vectors
eigenVectors_r = eigenVectors_r[:,idx_r]

eigenValues_i = eigenValues_i[idx_i]        # sorting (in increasing order) the corresponding eigenvalues and the corresponding vectors
eigenVectors_i = eigenVectors_i[:,idx_i]

#-----------------------------------------Voltage Collapse Code--------------------------------------------
vc_options = VoltageCollapseOptions()
numeric_circuit = grid.compile()
numeric_inputs = numeric_circuit.compute()
Sbase = np.zeros(len(grid.buses), dtype=complex)
Vbase = np.zeros(len(grid.buses), dtype=complex)
for c in numeric_inputs:
    Sbase[c.original_bus_idx] = c.Sbus
    Vbase[c.original_bus_idx] = c.Vbus
unitary_vector = -1 + 2 * np.random.random(len(grid.buses))
vc_inputs = VoltageCollapseInput(Sbase=Sbase,
                                 Vbase=Vbase,
                                 Starget=Sbase * (15 + unitary_vector))
vc = VoltageCollapse(circuit=grid, options=vc_options,
                     inputs=vc_inputs)
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

q = [a for a in range(data.shape[0]) if a%4==0]
fig, ax = plt.subplots()
ax.stem(q, np.absolute(smoothness_r[0:data.shape[0]:4]), use_line_collection=True)
ax.set_title('IEEE 14 system', fontsize=20)
ax.set_ylabel('Test Statistic (Real Part)', fontsize=20)
ax.set_xlabel('Number of Iterations of Continuation Power Flow', fontsize=20)

fig, ax = plt.subplots()
ax.stem(q, np.absolute(smoothness_i[0:data.shape[0]:4]), use_line_collection=True)
ax.set_title('IEEE 14 system', fontsize=20)
ax.set_ylabel('Test Statistic (Imaginary Part)', fontsize=20)
ax.set_xlabel('Number of Iterations of Continuation Power Flow', fontsize=20)

print(smoothness_r)
print(smoothness_i)


v_r_hat = (eigenVectors_r.T).dot(data[2,:].real)   # finding the graph fourier transform of the real part
fig, ax = plt.subplots()
ax.stem(eigenValues_r, v_r_hat, use_line_collection=True)

v_r_hat = (eigenVectors_r.T).dot(data[ data.shape[0]-10, :].real)   # finding the graph fourier transform of the real part
fig, ax = plt.subplots()
ax.stem(eigenValues_r, v_r_hat, use_line_collection=True)


v_i_hat = (eigenVectors_i.T).dot(data[2,:].imag)   # finding the graph fourier transform of the real part
fig, ax = plt.subplots()
ax.stem(eigenValues_i, v_i_hat, use_line_collection=True)

v_i_hat = (eigenVectors_i.T).dot(data[ data.shape[0]-10, :].imag)   # finding the graph fourier transform of the real part
fig, ax = plt.subplots()
ax.stem(eigenValues_i, v_i_hat, use_line_collection=True)


data = abs(data)  # extracting the graph signals magnitudes
mdl = vc.results.mdl()
mdl.plot()


#-----------------------------------------NetworkX grid plotting properties--------------------------------------------
'''
plt.figure()
g2 = grid.build_multi_graph()
pos = nx.kamada_kawai_layout(g2)
nx.draw_networkx(g2,pos,edge_color='black',width=1,linewidths=1,node_size=2000,node_color='pink',alpha=0.9,with_labels = True)
edge_labels = {}
for i, branch in enumerate(grid.branches):
    f = grid.bus_dictionary[branch.bus_from]
    t = grid.bus_dictionary[branch.bus_to]
    edge_labels[(f,t)] = branch.name
#print(edge_labels)
nx.draw_networkx_edge_labels(g2, pos, edge_labels = edge_labels, font_color='red')
'''
plt.show()
