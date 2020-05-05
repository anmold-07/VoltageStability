from GridCal.Engine import *
import networkx as nx
import pandas
from matplotlib import pylab
from GridCal.Engine.Simulations.ContinuationPowerFlow.voltage_collapse_driver import VoltageCollapseOptions, \
    VoltageCollapseInput, VoltageCollapse

np.set_printoptions(precision=4)
grid = MultiCircuit()
#-----------------------------------------Graph Visualization for Nordic 68------------------------------------------------------------------------------------------------------------------
def save_graph(graph, file_name):
    plt.figure(num=None, figsize=(100, 100), dpi=300)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.kamada_kawai_layout(graph)

    non_gen_non_load = [a for a in graph.nodes() if len(a) > 1]           # collecting all nodes names
    load_nodes = [a for a in graph.nodes() if 'L' in a]                   # load buses list
    gen_nodes = [a for a in graph.nodes() if 'G' in a]                    # gen buses list
    load_gen = load_nodes + gen_nodes
    remain = [a for a in non_gen_non_load if a not in load_gen]
    one_hun_kv_nodes = [a for a in remain if a[0] == '1']       # 130kV nodes
    two_hun_kv_nodes = [a for a in remain if a[0] == '2']       # 220 kv nodes or buses
    three_hun_kv_nodes = [a for a in remain if a[0] == '3' ]    # 300 kv nodes or buses
    four_hun_kv_nodes = [a for a in remain if a[0] == '4']      # 400kV nodes

    nx.draw_networkx_nodes(graph, pos, nodelist=four_hun_kv_nodes, node_color='blue', node_size=20000, alpha=0.8, with_labels=True)
    nx.draw_networkx_nodes(graph, pos, nodelist=three_hun_kv_nodes, node_color='blue', node_size=20000, alpha=0.6, with_labels=True)
    nx.draw_networkx_nodes(graph, pos, nodelist=two_hun_kv_nodes, node_color='blue', node_size=20000, alpha=0.4, with_labels=True)
    nx.draw_networkx_nodes(graph, pos, nodelist=one_hun_kv_nodes, node_color='blue', node_size=30000, alpha=0.1, with_labels=True)
    nx.draw_networkx_nodes(graph, pos, nodelist=load_nodes, node_color='pink', node_size=20000, node_shape='d', alpha=0.8, with_labels=True)
    nx.draw_networkx_nodes(graph, pos, nodelist=gen_nodes, node_color='red', node_size=20000, alpha=0.6, with_labels=True)

    for key, value in grid.bus_dictionary.items():
        grid.bus_dictionary[key] = key.name             # bus_dictionary modified with key as objects and values as bus names: altering the names of the nodes

    labels = {key.name: val for key, val in grid.bus_dictionary.items()}
    node_names = [val for key, val in grid.bus_dictionary.items()]
    nx.draw_networkx_labels(graph, pos, labels=labels, font_family='serif', font_size=25)
    edge_labels = {}
    fro = []
    to = []
    for i, branch in enumerate(grid.branches):
        f = grid.bus_dictionary[branch.bus_from]
        t = grid.bus_dictionary[branch.bus_to]
        fro.append(f)
        to.append(t)
        edge_labels[(f, t)] = branch.name

    # print(edge_labels)
    four_hun_edges_dict = {key: val for key, val in edge_labels.items() if '400' in val}
    four_hun_edges_list = [key for key, val in four_hun_edges_dict.items()]

    three_hun_edges_dict = {key: val for key, val in edge_labels.items() if '300' in val}
    three_hun_edges_list = [key for key, val in three_hun_edges_dict.items()]

    two_hun_edges_dict = {key: val for key, val in edge_labels.items() if '220' in val}
    two_hun_edges_list = [key for key, val in two_hun_edges_dict.items()]

    one_hun_edges_dict = {key: val for key, val in edge_labels.items() if '130' in val}
    one_hun_edges_list = [key for key, val in one_hun_edges_dict.items()]

    transfomer_edges_dict = {key: val for key, val in edge_labels.items() if 'Transformer' in val}
    transfomer_edges_list = [key for key, val in transfomer_edges_dict.items()]

    DC_edges_dict = {key: val for key, val in edge_labels.items() if 'DC' in val}
    DC_edges_list = [key for key, val in DC_edges_dict.items()]


    nx.draw_networkx_edges(graph, pos, width=2.0, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, edgelist=four_hun_edges_list, edge_color='b', width=30.0, alpha=0.8, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=three_hun_edges_list, edge_color='b', width=30.0, alpha=0.6, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=two_hun_edges_list, edge_color='b', width=50.0, alpha=0.4, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=one_hun_edges_list, edge_color='b', width=50.0, alpha=0.1, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=transfomer_edges_list, edge_color='g', width=50.0, alpha=0.2, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=DC_edges_list, edge_color='g', width=50.0, alpha=0.8, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_weight='bold')

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig
# -----------------------------------------End of Visualizing code------------------------------------------------------------------------------------------------------------------





#-----------------------------------------Start of modeling Nordi-68------------------------------------------------------------------------------------------------------------------
bus41 = Bus('1_BUS 41 L', vnom=130)       # creating an object
grid.add_bus(bus41)                    # appending an object to the list
grid.add_load(bus41, Load('load@BUS 41', P=540, Q=128.28))

bus42 = Bus('1_BUS 42 L', vnom=130)    # creating an object
grid.add_bus(bus42)                    # appending an object to the list
grid.add_load(bus42, Load('load@BUS 42', P=400.0, Q=125.67))

bus43 = Bus('1_BUS 43 L', vnom=130)    # creating an object
grid.add_bus(bus43)                    # appending an object to the lis
grid.add_load(bus43, Load('load@BUS 43', P=900.0, Q=238.83))

bus46 = Bus('1_BUS 46 L', vnom=130)    # creating an object
grid.add_bus(bus46)                    # appending an object to the list
grid.add_load(bus46, Load('load@BUS 46', P=700.0, Q=193.72))

bus47 = Bus('1_BUS 47 L', vnom=130)    # creating an object
grid.add_bus(bus47)                    # appending an object to the list
grid.add_load(bus47, Load('load@BUS 47', P=100.0, Q=45.19))

bus51 = Bus('BUS 51 L', vnom=130)    # creating an object
grid.add_bus(bus51)                    # appending an object to the list
grid.add_load(bus51, Load('load@BUS 51', P=800.0, Q=253.22))

bus61 = Bus('1_BUS 61 L', vnom=130)    # creating an object
grid.add_bus(bus61)                    # appending an object to the list
grid.add_load(bus61, Load('load@BUS 61', P=500.0, Q=112.31))

bus62 = Bus('1_BUS 62 L', vnom=130)    # creating an object
grid.add_bus(bus62)
grid.add_load(bus62, Load('load@BUS 62', P=300.0, Q=80.02))

bus63 = Bus('1_BUS 63 L', vnom=130)    # creating an object
grid.add_bus(bus63)
grid.add_load(bus63, Load('load@BUS 63', P=590.0, Q=256.19))

bus1011 = Bus('1_BUS 1011 L', vnom=130)    # creating an object
grid.add_bus(bus1011)
grid.add_load(bus1011, Load('load@BUS 1011', P=200.0, Q=80.0))


bus1012 = Bus('1_BUS 1012 G', vnom=130)    # creating an object
grid.add_bus(bus1012)
grid.add_load(bus1012, Load('load@BUS 1012', P=300.0, Q=100.0))
gen1012 = Generator(name='G1012', active_power=419.168, Snom=800.0, voltage_module=1.13, Qmin=-80.0, Qmax=400.0)
grid.add_generator(bus1012, gen1012)


bus1013 = Bus('1_BUS 1013 G', vnom=130)    # creating an object
grid.add_bus(bus1013)
grid.add_load(bus1013, Load('load@BUS 1013', P=100.0, Q=40.0))
gen1013 = Generator(name='G1013', active_power=314.376, Snom=600, voltage_module=1.145, Qmin=-50.0, Qmax=300.0)
grid.add_generator(bus1013, gen1013)


bus1014 = Bus('1_BUS 1014 G', vnom=130)    # creating an object
grid.add_bus(bus1014)
gen1014 = Generator(name='G1014', active_power=576.355, Snom=700, voltage_module=1.16, Qmin=-100.0, Qmax=350.0)
grid.add_generator(bus1014, gen1014)

bus1021 = Bus('1_BUS 1021  G', vnom=130)    # creating an object
grid.add_bus(bus1021)
gen1021 = Generator(name='G1021', active_power=419.168, Snom=600, voltage_module=1.1, Qmin=-60.0, Qmax=300.0)
grid.add_generator(bus1021, gen1021)

bus1022 = Bus('1_BUS 1022  G', vnom=130)    # creating an object
grid.add_bus(bus1022)
grid.add_load(bus1022, Load('load@BUS 1022', P=280.0, Q=95.0))
gen1022 = Generator(name='G1022', active_power=209.584, Snom=250, voltage_module=1.07, Qmin=-25.0, Qmax=125.0)
grid.add_generator(bus1022, gen1022)

bus1041 = Bus('1_BUS 1041 L', vnom=130)    # creating an object
grid.add_bus(bus1041)
grid.add_load(bus1041, Load('load@BUS 1041', P=600.0, Q=200.0))


bus1042 = Bus('1_BUS 1042 G', vnom=130)    # creating an object
grid.add_bus(bus1042)
grid.add_load(bus1042, Load('load@BUS 1042', P=300.0, Q=80.0))
gen1042 = Generator(name='G1042', active_power=377.251, Snom=400, voltage_module=1.0, Qmin=-40.0, Qmax=200.0)
grid.add_generator(bus1042, gen1042)

bus1043 = Bus('1_BUS 1043 G', vnom=130)    # creating an object
grid.add_bus(bus1043)
grid.add_load(bus1043, Load('load@BUS 1043', P=230.0, Q=100.0))
gen1043 = Generator(name='G1043', active_power=188.625, Snom=200, voltage_module=1.0, Qmin=-20.0, Qmax=100.0)
grid.add_generator(bus1043, gen1043)

bus1044 = Bus('1_BUS 1044 L', vnom=130)    # creating an object
grid.add_bus(bus1044)
grid.add_load(bus1044, Load('load@BUS 1044', P=800.0, Q=300))

bus1045 = Bus('1_BUS 1045 L', vnom=130)    # creating an object
grid.add_bus(bus1045)
grid.add_load(bus1045, Load('load@BUS 1045', P=700.0, Q=250))



bus2031 = Bus('2_BUS 2031 L', vnom=220)    # creating an object
grid.add_bus(bus2031)
grid.add_load(bus2031, Load('load@BUS 2031', P=100.0, Q=30.0))

bus2032 = Bus('2_BUS 2032 G', vnom=220)    # creating an object
grid.add_bus(bus2032)
grid.add_load(bus2032, Load('load@BUS 2032', P=200.0, Q=50.0))
gen2032 = Generator(name='G2032 ', active_power=785.939, Snom=850, voltage_module=1.1, Qmin=-80.0, Qmax=425.0)
grid.add_generator(bus2032, gen2032)


bus4011 = Bus('4_BUS 4011 G', vnom=400, is_slack= True)    # creating an object
grid.add_bus(bus4011)
gen4011 = Generator(name='G4011 ', active_power=654.195, Snom=1000, voltage_module=1.005, Qmin=-100.0, Qmax=500.0)
grid.add_generator(bus4011, gen4011)

bus4012 = Bus('4_BUS 4012 G', vnom=400)    # creating an object
grid.add_bus(bus4012)
gen4012 = Generator(name='G4012 ', active_power=523.959, Snom=800, voltage_module=1.01, Qmin=-160.0, Qmax=400.0)
grid.add_generator(bus4012, gen4012)

bus4021 = Bus('4_BUS 4021 G', vnom=400)    # creating an object
grid.add_bus(bus4021)
gen4021 = Generator(name='G4021 ', active_power=261.38, Snom=300, voltage_module=1.0, Qmin=-30.0, Qmax=150.0)
grid.add_generator(bus4021, gen4021)

bus4022 = Bus('4_BUS 4022', vnom=400)    # creating an object
grid.add_bus(bus4022)


bus4031 = Bus('4_BUS 4031 G', vnom=400)    # creating an object
grid.add_bus(bus4031)
gen4031 = Generator(name='G4031 ', active_power=324.855, Snom=350, voltage_module=1.01, Qmin=-40.0, Qmax=175.0)
grid.add_generator(bus4031, gen4031)

bus4032 = Bus('4_BUS 4032', vnom=400)    # creating an object
grid.add_bus(bus4032)


bus4041 = Bus('4_BUS 4041 G', vnom=400)    # creating an object
grid.add_bus(bus4041)
gen4041 = Generator(name='G4041 ', active_power=0.0, Snom=300, voltage_module=1.0, Qmin=-200.0, Qmax=300.0)
grid.add_generator(bus4041, gen4041)

bus4042 = Bus('4_BUS 4042 G', vnom=400)    # creating an object
grid.add_bus(bus4042)
gen4042 = Generator(name='G4042 ', active_power=660.189, Snom=700, voltage_module=1.0, Qmin=0.0, Qmax=350.0)
grid.add_generator(bus4041, gen4042)


bus4043 = Bus('4_BUS 4043', vnom=400)    # creating an object
grid.add_bus(bus4043)


bus4044 = Bus('4_BUS 4044', vnom=400)    # creating an object
grid.add_bus(bus4044)


bus4045 = Bus('4_BUS 4045 L', vnom=400)    # creating an object
grid.add_bus(bus4045)
grid.add_load(bus4045, Load('load@BUS 4045', P=200.0, Q=0.0))

bus4046 = Bus('4_BUS 4046 L', vnom=400)    # creating an object
grid.add_bus(bus4046)
grid.add_load(bus4046, Load('load@BUS 4046', P=-200.0, Q=0.0))

bus4047 = Bus('4_BUS 4047 G', vnom=400)    # creating an object
grid.add_bus(bus4047)
gen4047_1 = Generator(name='G4047_1', active_power=565.876, Snom=600, voltage_module=1.02, Qmin=0.0, Qmax=300.0)
grid.add_generator(bus4047, gen4047_1)
gen4047_2 = Generator(name='G4047_2', active_power=565.876, Snom=600, voltage_module=1.02, Qmin=0.0, Qmax=300.0)
grid.add_generator(bus4047, gen4047_2)


bus4051 = Bus('4_BUS 4051 G', vnom=400)    # creating an object
grid.add_bus(bus4051)
grid.add_load(bus4046, Load('load@BUS 4051', P=0.0, Q=0.0))
gen4051_1 = Generator(name='G4051_1', active_power=628.751, Snom=700, voltage_module=1.02, Qmin=0.0, Qmax=350.0)
grid.add_generator(bus4051, gen4051_1)
gen4051_2 = Generator(name='G4051_2', active_power=419.168, Snom=700, voltage_module=1.02, Qmin=0.0, Qmax=350.0)
grid.add_generator(bus4051, gen4051_2)


bus4061 = Bus('4_BUS 4061', vnom=400)    # creating an object
grid.add_bus(bus4061)


bus4062 = Bus('4_BUS 4062 G', vnom=400)    # creating an object
grid.add_bus(bus4062)
gen4062_1 = Generator(name='G4062_1', active_power=555.397, Snom=600, voltage_module=1.0, Qmin=0.0, Qmax=300.0)
grid.add_generator(bus4062, gen4062_1)
gen4062_2 = Generator(name='G4062_2', active_power=555.397, Snom=600, voltage_module=1.0, Qmin=0.0, Qmax=300.0)
grid.add_generator(bus4062, gen4062_2)

bus4063 = Bus('4_BUS 4063 G', vnom=400)    # creating an object
grid.add_bus(bus4063)
grid.add_load(bus4063, Load('load@BUS 4063', P=-200.0, Q=0.0))
gen4063 = Generator(name='G4063', active_power=100.0, Snom=150.0, voltage_module=1.0, Qmin=0.0, Qmax=30.0)
grid.add_generator(bus4063, gen4063)

bus5100 = Bus('3_BUS 5100 G', vnom=300)    # creating an object
grid.add_bus(bus5100)
grid.add_load(bus5100, Load('load@BUS 5100', P=1319.0, Q=204.0))
gen5100 = Generator(name='G5100', active_power=502.303, Snom=600.0, voltage_module=1.0)
grid.add_generator(bus5100, gen5100)

bus5101 = Bus('4_BUS 5101_NOR', vnom=400)    # creating an object
grid.add_bus(bus5101)


bus5102 = Bus('4_BUS 5102', vnom=400)    # creating an object
grid.add_bus(bus5102)


bus5103 = Bus('4_BUS 5103', vnom=400)    # creating an object
grid.add_bus(bus5103)


bus5300 = Bus('3_BUS 5300 G', vnom=300)    # creating an object
grid.add_bus(bus5300)
grid.add_load(bus5300, Load('load@BUS 5300', P=67.0, Q=3.0))
gen5300 = Generator(name='G5300', active_power=772.304, Snom=916.0, voltage_module=1.0)
grid.add_generator(bus5300, gen5300)

bus5301 = Bus('4_BUS 5301', vnom=400)    # creating an object
grid.add_bus(bus5301)


bus5400 = Bus('3_BUS 5400 G', vnom=300)    # creating an object
grid.add_bus(bus5400)
grid.add_load(bus5400, Load('load@BUS 5400', P=31.0, Q=0.0))
gen5400 = Generator(name='G5400', active_power=538.983, Snom=633.0, voltage_module=1.0)
grid.add_generator(bus5400, gen5400)

bus5401 = Bus('4_BUS 5401', vnom=400)    # creating an object
grid.add_bus(bus5401)


bus5402 = Bus('4_BUS 5402', vnom=400)    # creating an object
grid.add_bus(bus5402)


bus5500 = Bus('BUS 5500 G', vnom=300)    # creating an object
grid.add_bus(bus5500)
grid.add_load(bus5500, Load('load@BUS 5500', P=409.0, Q=38.0))
gen5500 = Generator(name='G5500', active_power=281.208, Snom=333.0, voltage_module=1.0)
grid.add_generator(bus5500, gen5500)

bus5501= Bus('4_BUS 5501', vnom=400)    # creating an object
grid.add_bus(bus5501)


bus5600= Bus('3_BUS 5600 G', vnom=300)    # creating an object
grid.add_bus(bus5600)
grid.add_load(bus5600, Load('load@BUS 5600', P=1040.0, Q=99.0))
gen5600 = Generator(name='G5600', active_power=806.945, Snom=950.0, voltage_module=1.0)
grid.add_generator(bus5600, gen5600)

bus5601= Bus('4_BUS 5601', vnom=400)    # creating an object
grid.add_bus(bus5601)


bus5602= Bus('4_BUS 5602', vnom=400)    # creating an object
grid.add_bus(bus5602)


bus5603= Bus('3_BUS 5603', vnom=300)    # creating an object
grid.add_bus(bus5603)
grid.add_load(bus5603, Load('load@BUS 5603', P=466.0, Q=171.0))

bus6000= Bus('3_BUS 6000 G', vnom=300)    # creating an object
grid.add_bus(bus6000)
gen6000 = Generator(name='G6000', active_power=383.095, Snom=466.0, voltage_module=1.0)
grid.add_generator(bus6000, gen6000)

bus6001= Bus('4_BUS 6001', vnom=400)    # creating an object
grid.add_bus(bus6001)


bus6100= Bus('3_BUS 6100 G', vnom=300)    # creating an object
grid.add_bus(bus6100)
grid.add_load(bus6100, Load('load@BUS 6100', P=1014.0, Q=326.0))
gen6100 = Generator(name='G6100', active_power=796.757, Snom=966.0, voltage_module=1.0)
grid.add_generator(bus6100, gen6100)

bus7100= Bus('4_BUS 7100 G', vnom=400)    # creating an object
grid.add_bus(bus7100)
grid.add_load(bus7100, Load('load@BUS 7100', P=341.0, Q=50.0))
gen7100 = Generator(name='G7100', active_power=222.114, Snom=333.0, voltage_module=1.01)
grid.add_generator(bus7100, gen7100)

bus7101= Bus('4_BUS 7101 G', vnom=400)    # creating an object
grid.add_bus(bus7101)
grid.add_load(bus7101, Load('load@BUS 7101', P=341.0, Q=50.0))
gen7101 = Generator(name='G7101', active_power=222.114, Snom=333.0, voltage_module=1.01)
grid.add_generator(bus7101, gen7101)

bus7102= Bus('4_BUS 7102', vnom=400)    # creating an object
grid.add_bus(bus7102)


bus7200= Bus('4_BUS 7200', vnom=400)    # creating an object
grid.add_bus(bus7200)


bus7201= Bus('4_BUS 7201 G', vnom=400)    # creating an object
grid.add_bus(bus7201)
grid.add_load(bus7201, Load('load@BUS 7201', P=300.0, Q=70.0))
gen7201 = Generator(name='G7201', active_power=359.661, Snom=433.0, voltage_module=1.01)
grid.add_generator(bus7201, gen7201)

bus7203= Bus('4_BUS 7203 G', vnom=400)    # creating an object
grid.add_bus(bus7203)
grid.add_load(bus7203, Load('load@BUS 7203_1', P=300.0, Q=70.0))
grid.add_load(bus7203, Load('load@BUS 7203_2', P=200.0, Q=0.0))
gen7203 = Generator(name='G7203', active_power=764.153, Snom=866.0, voltage_module=1.01)
grid.add_generator(bus7203, gen7203)

bus7204= Bus('4_BUS 7204 G', vnom=400)    # creating an object
grid.add_bus(bus7204)
grid.add_load(bus7204, Load('load@BUS 7204', P=600.0, Q=140.0))
gen7204 = Generator(name='G7204', active_power=407.548, Snom=475.0, voltage_module=1.01)
grid.add_generator(bus7204, gen7204)


bus7205= Bus('4_BUS 7205 G', vnom=400)    # creating an object
grid.add_bus(bus7205)
grid.add_load(bus7205, Load('load@BUS 7205', P=300.0, Q=70.0))
gen7205 = Generator(name='G7205', active_power=407.548, Snom=475.0, voltage_module=1.01)
grid.add_generator(bus7205, gen7205)

#bus8001= Bus('4_BUS 8001', vnom=400)    # creating an object
#grid.add_bus(bus8001)
#bus8002= Bus('4_BUS 8002 G', vnom=400)    # creating an object
#grid.add_bus(bus8002)
#gen8002 = Generator(name='G8002', active_power=0.0, Snom=500.0, voltage_module=1.0)
#grid.add_generator(bus8002, gen8002)


bus8500= Bus('4_BUS 8500 G', vnom=400)    # creating an object
grid.add_bus(bus8500)
grid.add_load(bus8500, Load('load@BUS 8500', P=333.0, Q=333.0))
gen8500 = Generator(name='G8500', active_power=333.0, Snom=666.0, voltage_module=1.02)
grid.add_generator(bus8500, gen8500)


grid.add_branch(Branch(bus1011, bus1013, '130kV 1011_1013_1', r=0.01, x=0.07, b=0.014))
grid.add_branch(Branch(bus1013, bus1011, '130kV 1011_1013_2', r=0.01, x=0.07, b=0.014))
grid.add_branch(Branch(bus1012, bus1014, '130kV 1012_1014_1', r=0.014, x=0.09, b=0.018))
grid.add_branch(Branch(bus1014, bus1012, '130kV 1012_1014_2', r=0.014, x=0.09, b=0.018))
grid.add_branch(Branch(bus1013, bus1014, '130kV 1013_1014_1', r=0.007, x=0.05, b=0.01))
grid.add_branch(Branch(bus1014, bus1013, '130kV 1013_1014_2', r=0.007, x=0.05, b=0.01))
grid.add_branch(Branch(bus1021, bus1022, '130kV 1021_1022_1', r=0.03, x=0.2, b=0.03))
grid.add_branch(Branch(bus1022, bus1021, '130kV 1021_1022_2', r=0.03, x=0.2, b=0.03))
grid.add_branch(Branch(bus1041, bus1043, '130kV 1041_1043_1', r=0.01, x=0.06, b=0.012))
grid.add_branch(Branch(bus1043, bus1041, '130kV 1041_1043_2', r=0.01, x=0.06, b=0.012))
grid.add_branch(Branch(bus1041, bus1045, '130kV 1041_1045_1', r=0.015, x=0.12, b=0.025))
grid.add_branch(Branch(bus1045, bus1041, '130kV 1041_1045_2', r=0.015, x=0.12, b=0.025))
grid.add_branch(Branch(bus1042, bus1044, '130kV 1042_1044_1', r=0.038, x=0.28, b=0.06))
grid.add_branch(Branch(bus1044, bus1042, '130kV 1042_1044_2', r=0.038, x=0.28, b=0.06))
grid.add_branch(Branch(bus1042, bus1045, '130kV 1042_1045_1', r=0.05, x=0.3, b=0.06))
grid.add_branch(Branch(bus1043, bus1044, '130kV 1043_1044_1', r=0.01, x=0.08, b=0.016))
grid.add_branch(Branch(bus1044, bus1043, '130kV 1043_1044_2', r=0.01, x=0.08, b=0.016))

grid.add_branch(Branch(bus2031, bus2032, '220kV 2031_2032_1', r=0.012, x=0.09, b=0.015))
grid.add_branch(Branch(bus2032, bus2031, '220kV 2031_2032_2', r=0.012, x=0.09, b=0.015))

grid.add_branch(Branch(bus4011, bus4012, '400kV 4011_4012_1', r=0.001, x=0.008, b=0.2))
br2 = Branch(bus4011, bus4021, '400kV 4011_4021_1', r=0.006, x=0.06, b=1.8)
grid.add_branch(br2)
grid.add_branch(Branch(bus4011, bus4022, '400kV 4011_4022_1', r=0.004, x=0.04, b=1.2))
grid.add_branch(Branch(bus4011, bus7100, '400kV 4011_7100_1', r=0.006875, x=0.06875, b=0.15125))
grid.add_branch(Branch(bus4012, bus4022, '400kV 4012_4022_1', r=0.004, x=0.035, b=1.05))
grid.add_branch(Branch(bus4012, bus7101, '400kV 4012_7101_1', r=0.00625, x=0.0625, b=0.13333))
grid.add_branch(Branch(bus4021, bus4032, '400kV 4021_4032_1', r=0.004, x=0.04, b=1.2))
grid.add_branch(Branch(bus4021, bus4042, '400kV 4021_4042_1', r=0.01, x=0.06, b=3.0))
grid.add_branch(Branch(bus4022, bus4031, '400kV 4022_4031_1', r=0.004, x=0.04, b=1.2))
grid.add_branch(Branch(bus4031, bus4022, '400kV 4031_4022_1', r=0.004, x=0.04, b=1.2))

br = Branch(bus4031, bus4032, '400kV 4031_4032_1', r=0.001, x=0.01, b=0.3)     # for N-1, creating it a separate branch for P-V plots
grid.add_branch(br)

grid.add_branch(Branch(bus4031, bus4041, '400kV 4031_4041_1', r=0.006, x=0.04, b=2.4))
grid.add_branch(Branch(bus4041, bus4031, '400kV 4031_4041_2', r=0.006, x=0.04, b=2.4))
grid.add_branch(Branch(bus4032, bus4042, '400kV 4032_4042_1', r=0.01, x=0.04, b=2.0))
grid.add_branch(Branch(bus4032, bus4044, '400kV 4032_4044_1', r=0.006, x=0.05, b=2.4))
grid.add_branch(Branch(bus4041, bus4044, '400kV 4041_4044_1', r=0.003, x=0.03, b=0.9))
grid.add_branch(Branch(bus4041, bus4061, '400kV 4041_4061_1', r=0.006, x=0.045, b=1.3))
grid.add_branch(Branch(bus4041, bus5101, '400kV 4041_5101_1', r=0.00444, x=0.05784, b=0.12))
grid.add_branch(Branch(bus5101, bus4041, '400kV 4041_5101_2', r=0.00444, x=0.05784, b=0.12))
grid.add_branch(Branch(bus4042, bus4043, '400kV 4042_4043_1', r=0.002, x=0.015, b=0.5))
grid.add_branch(Branch(bus4042, bus4044, '400kV 4042_4044_1', r=0.002, x=0.02, b=0.6))
grid.add_branch(Branch(bus4043, bus4044, '400kV 4043_4044_1', r=0.001, x=0.01, b=0.3))
grid.add_branch(Branch(bus4043, bus4046, '400kV 4043_4046_1', r=0.001, x=0.01, b=0.3))
grid.add_branch(Branch(bus4043, bus4047, '400kV 4043_4047_1', r=0.002, x=0.02, b=0.6))
grid.add_branch(Branch(bus4044, bus4045, '400kV 4044_4045_1', r=0.002, x=0.02, b=0.6))
grid.add_branch(Branch(bus4045, bus4044, '400kV 4044_4045_2', r=0.002, x=0.02, b=0.6))
grid.add_branch(Branch(bus4044, bus4045, '400kV 4044_4045_3', r=0.00825, x=0.0825, b=0.15))
grid.add_branch(Branch(bus4045, bus4051, '400kV 4045_4051_1', r=0.004, x=0.04, b=1.2))
grid.add_branch(Branch(bus4051, bus4045, '400kV 4045_4051_2', r=0.004, x=0.04, b=1.2))
grid.add_branch(Branch(bus4045, bus4062, '400kV 4045_4062_1', r=0.011, x=0.08, b=2.4))
grid.add_branch(Branch(bus4046, bus4047, '400kV 4046_4047_1', r=0.001, x=0.015, b=0.5))
grid.add_branch(Branch(bus4061, bus4062, '400kV 4061_4062_1', r=0.002, x=0.02, b=0.6))
grid.add_branch(Branch(bus4062, bus4063, '400kV 4062_4063_1', r=0.003, x=0.03, b=0.9))
grid.add_branch(Branch(bus4063, bus4062, '400kV 4062_4063_2', r=0.003, x=0.03, b=0.9))
grid.add_branch(Branch(bus4063, bus8500, '400kV 4063_8500_1', r=0.024, x=0.093, b=1.0))
grid.add_branch(Branch(bus5100, bus5300, '300kV 5100_5300_1', r=0.012, x=0.12, b=0.166))
grid.add_branch(Branch(bus5100, bus5500, '300kV 5100_5500_1', r=0.0054, x=0.045, b=0.071))
grid.add_branch(Branch(bus5101, bus5501, '400kV 5101_5501_1', r=0.00183, x=0.01929, b=1.086))
grid.add_branch(Branch(bus5102, bus5301, '400kV 5102_5301_1', r=0.00225, x=0.03237, b=0.4296))
grid.add_branch(Branch(bus5102, bus6001, '400kV 5102_6001_1', r=0.006, x=0.105, b=0.333))
grid.add_branch(Branch(bus5103, bus5301, '400kV 5102_6001_1', r=0.0051, x=0.06936, b=0.225))
grid.add_branch(Branch(bus5400, bus5500, '300kV 5400_5500_1', r=0.0024, x=0.0333, b=0.0))
grid.add_branch(Branch(bus5400, bus6000, '300kV 5400_6000_1', r=0.003, x=0.03, b=0.033))
grid.add_branch(Branch(bus5400, bus6100, '300kV 5400_6100_1', r=0.006, x=0.06, b=0.04))
grid.add_branch(Branch(bus5401, bus5501, '400kV 5401_5501_1', r=0.0045, x=0.06, b=0.2))
grid.add_branch(Branch(bus5401, bus5602, '400kV 5401_5602_1', r=0.00462, x=0.07218, b=0.2932))
grid.add_branch(Branch(bus5401, bus6001, '400kV 5401_6001_1', r=0.0009, x=0.015, b=0.05))
grid.add_branch(Branch(bus5402, bus6001, '400kV 5402_6001_1', r=0.00153, x=0.02253, b=0.0784))
grid.add_branch(Branch(bus5500, bus5603, '300kV 5500_5603_1', r=0.012, x=0.135, b=0.0266))
grid.add_branch(Branch(bus5600, bus5603, '300kV 5600_5603_1', r=0.00603, x=0.06633, b=0.0695))
grid.add_branch(Branch(bus5600, bus6000, '300kV 5600_6000_1', r=0.0105, x=0.105, b=0.15))
grid.add_branch(Branch(bus5601, bus6001, '400kV 5601_6001_1', r=0.00411, x=0.06093, b=0.212))
grid.add_branch(Branch(bus6000, bus6100, '300kV 6000_6100_1', r=0.0066, x=0.07182, b=0.0666))
grid.add_branch(Branch(bus7100, bus7101, '400kV 7100_7101_1', r=0.0025, x=0.025, b=0.05567))
grid.add_branch(Branch(bus7100, bus7200, '400kV 7100_7200_1', r=0.02375, x=0.2375, b=0.52883))
grid.add_branch(Branch(bus7200, bus7100, '400kV 7100_7200_2', r=0.02375, x=0.2375, b=0.52883))
grid.add_branch(Branch(bus7101, bus7102, '400kV 7101_7102_1', r=0.01125, x=0.1125, b=0.2505))
grid.add_branch(Branch(bus7102, bus7201, '400kV 7102_7201_1', r=0.01125, x=0.1125, b=0.2505))
grid.add_branch(Branch(bus7200, bus7201, '400kV 7200_7201_1', r=0.005, x=0.05, b=0.11133))
grid.add_branch(Branch(bus7200, bus7205, '400kV 7200_7205_1', r=0.005, x=0.05, b=0.11111))
grid.add_branch(Branch(bus7201, bus7203, '400kV 7201_7203_1', r=0.005, x=0.05, b=0.11133))
grid.add_branch(Branch(bus7203, bus7204, '400kV 7203_7204_1', r=0.005, x=0.05, b=0.11133))
grid.add_branch(Branch(bus7204, bus7205, '400kV 7204_7205_1', r=0.005, x=0.05, b=0.11133))
#grid.add_branch(Branch(bus8001, bus8002, '400kV 8001_8002_1', r=0.00125, x=0.0125, b=0.0))
grid.add_branch(Branch(bus7203, bus4046, 'DC Terminal 1', r=4.0, rate=225))
#grid.add_branch(Branch(bus4045, bus8001, 'DC Terminal 2', r=8.0, rate=260))
grid.add_branch(Branch(bus4045, bus4063, 'DC Terminal 3', r=6.0, rate=450))
grid.add_branch(Branch(bus41, bus4041, 'Transformer line 1041_41_1', r=0.0, x=0.01, b=0.0, tap = 1, rate=1000,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus42, bus4042, 'Transformer line 1042_42_1', r=0.0, x=0.013, b=0.0, tap = 1, rate=770,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus43, bus4043, 'Transformer line 1043_43_1', r=0.0, x=0.007, b=0.0, tap = 1, rate=1430,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus46, bus4046, 'Transformer line 1046_46_1', r=0.0, x=0.01, b=0.0, tap = 1, rate=1000,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus47, bus4047, 'Transformer line 1047_47_1', r=0.0, x=0.04, b=0.0, tap = 1, rate=250,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus51, bus4051, 'Transformer line 1051_51_1', r=0.0, x=0.007, b=0.0, tap = 1, rate=1430,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus61, bus4061, 'Transformer line 1061_61_1', r=0.0, x=0.013, b=0.0, tap = 1, rate=770,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus62, bus4062, 'Transformer line 1062_62_1', r=0.0, x=0.02, b=0.0, tap = 1, rate=500,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus63, bus4063, 'Transformer line 1063_63_1', r=0.0, x=0.01, b=0.0, tap = 1, rate=1000,  branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1011, bus4011, 'Transformer line 1011_4011_1', r=0.0, x=0.008, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1012, bus4012, 'Transformer line 1011_4012_1', r=0.0, x=0.008, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1022, bus4022, 'Transformer line 1022_4022_1', r=0.0, x=0.012, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1044, bus4044, 'Transformer line 1044_4044_1', r=0.0, x=0.01, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1044, bus4044, 'Transformer line 1044_4044_2', r=0.0, x=0.01, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1045, bus4045, 'Transformer line 1045_4045_1', r=0.0, x=0.01, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus1045, bus4045, 'Transformer line 1045_4045_2', r=0.0, x=0.01, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus2031, bus4031, 'Transformer line 2031_4031_2', r=0.0, x=0.012, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5100, bus5101, 'Transformer line 5100_5101', r=0.00024, x=0.00915, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5102, bus5100, 'Transformer line 5102_5100', r=0.00024, x=0.00915, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5103, bus5100, 'Transformer line 5102_5100', r=0.00075, x=0.03, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5300, bus5301, 'Transformer line 5300_5301', r=0.00048, x=0.018, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5400, bus5401, 'Transformer line 5400_5401', r=0.00096, x=0.036, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5400, bus5402, 'Transformer line 5400_5402', r=0.00012, x=0.0045, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5500, bus5501, 'Transformer line 5500_5501', r=0.00012, x=0.0045, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5600, bus5601, 'Transformer line 5600_5601', r=0.0, x=0.00228, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus5603, bus5602, 'Transformer line 5603_5602', r=0.00024, x=0.00915, b=0.0, tap = 1, branch_type=BranchType.Transformer))
grid.add_branch(Branch(bus6000, bus6001, 'Transformer line 6000_6001', r=0.00012, x=0.0045, b=0.0, tap = 1, branch_type=BranchType.Transformer))

grid.add_shunt(bus1022, Shunt( name='shunt 1022', B=50.0))
grid.add_shunt(bus1041, Shunt( name='shunt 1041', B=200.0))
grid.add_shunt(bus1043, Shunt( name='shunt 1043', B=150.0))
grid.add_shunt(bus1044, Shunt( name='shunt 1044', B=200.0))
grid.add_shunt(bus1045, Shunt( name='shunt 1045', B=200.0))
grid.add_shunt(bus4012, Shunt( name='shunt 4012', B=-100.0))
grid.add_shunt(bus4041, Shunt( name='shunt 4041', B=200.0))
grid.add_shunt(bus4043, Shunt( name='shunt 4043', B=200.0))
grid.add_shunt(bus4046, Shunt( name='shunt 4046', B=100.0))
grid.add_shunt(bus4051, Shunt( name='shunt 4051', B=100.0))
grid.add_shunt(bus7100, Shunt( name='shunt 7100', B=-400.0))
#-----------------------------------------End of modeling Nordic-68---------------------------------------------------------------------



#-----------------------------------------Code to run Power Flow ------------------------------------------------------------------------------------------------------------------
'''
options = PowerFlowOptions(SolverType.NR, initialize_with_existing_solution=True, control_p=False, multi_core=False, dispatch_storage=False, control_q=ReactivePowerControlMode.NoControl, control_taps=TapsControlMode.NoControl)
power_flow = PowerFlowDriver(grid, options)
power_flow.run()
vm = np.abs(power_flow.results.voltage)
va = np.angle(power_flow.results.voltage)

for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name

bus_list = list(grid.bus_dictionary.values())
print(bus_list)                                      # list  of buses all
branch_list = list(grid.branch_dictionary.values())  # empty list
print(grid.branch_names)                             # branch names
keys = grid.branch_names
values = abs(power_flow.results.Sbranch)
di = dict(zip(keys, values))     # printing the loading corresponding to respective branch names
#print(di)
sort_di = {k: v for k, v in sorted(di.items(), key=lambda item: item[1], reverse=True)}    # sorting to find the branch with max power for N-1 contingency
print(sort_di)

#print(grid.branches)                                 # branch list of objects
#print(grid.branch_original_idx)                      # empty list
#g1 = grid.build_multi_graph()
#non_gen_non_load = [a for a in g1.nodes() if len(a) > 1]  # collecting all nodes names
#load_nodes = [a for a in g1.nodes() if 'L' in a]  # load buses list
#gen_nodes = [a for a in g1.nodes() if 'G' in a]  # gen buses list
#load_gen = load_nodes + gen_nodes
#remain = [a for a in non_gen_non_load if a not in load_gen]
#print(remain)

result_type = ResultTypes.BusVoltageAngle
mdl = power_flow.results.mdl(result_type, None, np.array(bus_list))
mdl.plot()
result_type = ResultTypes.BusVoltageModule
mdl = power_flow.results.mdl(result_type, None, np.array(bus_list))
mdl.plot()

print('\n\n', grid.name)
print('\t|V|:', abs(power_flow.results.voltage))
print('\t|Theta|:', np.degrees(np.angle(power_flow.results.voltage)))
print('\t|Sbranch|:', abs(power_flow.results.Sbranch))
print('\t|loading|:', abs(power_flow.results.loading) * 100)
print('\terr:', power_flow.results.error)
print('\tConv:', power_flow.results.converged)
'''
#----------------------------------------------Adding Bar plot for Power flow-------------------------------------------------------------------------------
#------------------------------------------reading the nordic--68 PSS/E text file for plotting purpose----------------------------------------------------------
'''
fp = open('nordic 68 psse power flow.txt')
lines = fp.readlines()
lis = []
for i, v in enumerate(lines):
    if "BUS " in v:
        lis.append(v)
print(lis)
mag = []
ang = []
data = lis[0].split()
print(data)
print(data[9])
print(data[10])

for a in lis:
    data = a.split()
    mag.append(data[9])
    ang.append(data[10])

mag = [a.replace('PU', '') for a in mag] # removing the PU tag
print(mag)
mag = [float(a) for a in mag]
print(mag)
ang = [float(a) for a in ang]
print(ang)

B = tuple(bus_list)
y = np.arange(len(B))
y = [3*i for i in y]

magnitude = abs(power_flow.results.voltage)
magnitude = [round(a, 3) for a in magnitude]
print(magnitude)

plt.figure(figsize=(20,25))
plt.barh(y, magnitude, align = 'center', height = 0.5, color="skyblue")
plt.title('Voltage Magnitude plot for all the buses of Nordic-68', fontsize=22)
plt.yticks(y, B)
plt.xlabel('Magnitude of Voltages in Per Unit (P.U)', fontsize=22)
for i, v in enumerate(magnitude):
    plt.text(v + 0.01, 3*i, str(v), color='green', fontweight='bold', fontsize = 15)
plt.xlim(0,1.25)
plt.tick_params(labelsize=20)
plt.tight_layout()
plt.savefig('NORDIC_68_magnitude.png')

angles =  np.degrees(np.angle(power_flow.results.voltage))
angles = [round(a, 3) for a in angles]
plt.figure(figsize=(20,25))
plt.barh(y, angles, align = 'center', height=1.0, color="skyblue")
plt.title('Voltage Angles plot for all the buses of Nordic-68', fontsize=22)
plt.yticks(y, B)
plt.xlabel('Angles of Voltages in Degrees', fontsize=22)
for i, v in enumerate(angles):
    plt.text(v - 0.05, 3*i, str(v), color='green', fontweight='bold', fontsize = 15)
#plt.xlim(0,1.25)
plt.tick_params(labelsize=20)
plt.tight_layout()
plt.savefig('NORDIC_68_angles.png')



# ----------- Modeling the network as a multigraph (add a multigraph module in multicircuit.py file in order for this to work in you're using this code-----------
g1 = grid.build_multi_graph()
print(nx.info(g1))
#-----------------------------------------------------------------------------------------------------------------------------------------------------




#--------Comparison of power flow voltage Magnitudes:-------------------------------------------------------------------------------------------------------------
df = pandas.DataFrame(dict(graph=bus_list, n=magnitude, m=mag))
ind = np.arange(len(df))
width = 0.4
fig, ax = plt.subplots(figsize=(30,30))
ax.barh(ind, df.n, width, color="skyblue", label='GRIDCAL')
ax.barh(ind + width, df.m, width, color='green', label='PSS/E')
ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
ax.legend()
ax.title.set_text('Voltage Magnitudes plot for all the buses of Nordic-68')
ax.set_xlabel('Magnitude of Voltages in Per Unit (P.U)')
#fig.tight_layout()

for i, v in enumerate(magnitude):
    ax.text(v + 0.01, i-0.2, str(v), color='blue', fontweight='bold', fontsize = 10)

for i, v in enumerate(mag):
    ax.text(v + 0.01, i+width-0.2, str(v), color='green', fontweight='bold', fontsize=10)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(25)
ax.tick_params(labelsize=20)
fig.savefig('NORDIC_68_comparison_magnitudes.png')
fig.savefig("NORDIC_68_comparison_magnitudes.pdf", bbox_inches='tight', dpi = 500)

#-----------------Comparison of power flow angles:--------------------------------------------
df = pandas.DataFrame(dict(graph=bus_list, n=angles, m=ang))
ind = np.arange(len(df))
width = 0.4
fig, ax = plt.subplots(figsize=(30,30))
ax.barh(ind, df.n, width, color="skyblue", label='GRIDCAL')
ax.barh(ind + width, df.m, width, color='green', label='PSS/E')
ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
ax.legend()
ax.title.set_text('Voltage Angles plot for all the buses of Nordic-68')
ax.set_xlabel('Angles in Degrees')
#fig.tight_layout()

for i, v in enumerate(angles):
    if v > 0:
        ax.text(v + 0.04, i-0.2, str(v), color='blue', fontweight='bold', fontsize=10)
    else:
        ax.text(v - 2.5, i-0.2, str(v), color='blue', fontweight='bold', fontsize=10)
for i, v in enumerate(ang):
    if v > 0:
        ax.text(v + 0.04, i+width-0.2, str(v), color='green', fontweight='bold', fontsize=10)
    else:
        ax.text(v - 2.5, i+width-0.2, str(v), color='green', fontweight='bold', fontsize=10)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(25)
ax.tick_params(labelsize=20)
fig.savefig('NORDIC_68_comparison_angles.png')
fig.savefig("NORDIC_68_comparison_angles.pdf", bbox_inches='tight', dpi = 500)

plt.show()
'''
#-----------------------------------------End of Power flow code and Power Flow Comparison between GridCal and PSS/E--------------------------------------------------------------------------------------------------------

numeric_circuit = grid.compile_snapshot()
numeric_inputs = numeric_circuit.compute()
ybus_1 = numeric_inputs[0].Ybus             # computing the Y bus of the matrix;
R = ybus_1.A.real                           # Scipy sparse matrix to normal matrix;
I = ybus_1.A.imag

#-----------------------------------------Start of Voltage Collapse Code pre-contingency------------------------------------------------------------------------------------------------------------------
vc_options = VoltageCollapseOptions(step=0.001, adapt_step=True, step_min=0.00001, step_max=0.2, error_tol=1e-4, tol=1e-6, max_it=50, verbose=False)
numeric_circuit = grid.compile()
numeric_inputs = numeric_circuit.compute()
Sbase = np.zeros(len(grid.buses), dtype=complex)
Vbase = np.zeros(len(grid.buses), dtype=complex)
for c in numeric_inputs:
    Sbase[c.original_bus_idx] = c.Sbus
    Vbase[c.original_bus_idx] = c.Vbus
unitary_vector = -1 + 2 * np.random.random(len(grid.buses))
vc_inputs = VoltageCollapseInput(Sbase=Sbase, Vbase=Vbase, Starget=Sbase * (3 + unitary_vector))
vc = VoltageCollapse(circuit=grid, options=vc_options, inputs=vc_inputs)
vc.run()

smoothness_r = []
smoothness_i = []
data = vc.results.voltages
print(data)                 # extracting the graph signals in cartesian coordinates in order to calculate smoothness test statistic

for a in range(data.shape[0]):
    vv = data[a,:]
    vv_r = vv.real
    vv_i = vv.imag
    smoothness_r.append(vv_r.T.dot(R).dot(vv_r))
    smoothness_i.append(vv_i.T.dot(-I).dot(vv_i))

print(smoothness_r)
print(smoothness_i)

data = abs(data)
print(data)

q = [a for a in range(data.shape[0]) if a%25==0]
fig, ax = plt.subplots()
ax.stem(q, np.absolute(smoothness_r[0:data.shape[0]:25]), use_line_collection=True)
ax.set_title('Nordic 68 system', fontsize=20)
ax.set_ylabel('Test Statistic (Real Part)', fontsize=20)
ax.set_xlabel('Number of Iterations of Continuation Power Flow', fontsize=20)

fig, ax = plt.subplots()
ax.stem(q, np.absolute(smoothness_i[0:data.shape[0]:25]), use_line_collection=True)
ax.set_title('Nordic 68 system', fontsize=20)
ax.set_ylabel('Test Statistic (Imaginary Part)', fontsize=20)
ax.set_xlabel('Number of Iterations of Continuation Power Flow', fontsize=20)


for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name
lis = [grid.bus_dictionary[key] for key, value in grid.bus_dictionary.items()]     # full list
print(lis)
load_buses = [load for load in lis if 'L' in load]
print(load_buses)
spec = ['1_BUS 1044 L', '1_BUS 1045 L', '1_BUS 42 L', '1_BUS 43 L']

mdl_1 = vc.results.mdl()
index, columns, data = mdl_1.get_data()
indices = [lis.index(a) for a in load_buses]
indices = [lis.index('1_BUS 1044 L'), lis.index('1_BUS 1045 L'), lis.index('1_BUS 42 L'), lis.index('1_BUS 43 L')]
A = [[sublist[x] for x in indices] for sublist in data]
sub_columns = spec                                            #[columns[x] for x in indices]
df1 = pd.DataFrame(data=A, index=index, columns=sub_columns)
ax = df1.plot()
ax.set_title('Bus Voltage - Nordic 68', fontsize=20)
ax.set_ylabel('Bus Voltage in Per Unit (P.U)', fontsize=20)
ax.set_xlabel('Loading from the base situation ($\lambda$)', fontsize=20)   # able to plot the PV curves for all the load buses specifically
plt.show()
#-----------------------------------------End of Voltage Collapse Code------------------------------------------------------------------------------------------------------------------
'''

'''
#----------------------------------------NetworkX grid plot visualization--------------------------------------------------------------------------------------
g1 = grid.build_multi_graph()
print(nx.info(g1))
save_graph(g1,"NORDIC_68_before_outage.pdf")


#grid.delete_branch(br)
#grid.delete_branch(br2)

g2 = grid.build_multi_graph()
print(nx.info(g2))
save_graph(g2,"NORDIC_68_after_outage.pdf")
'''
'''
#-----------------------------------------Start of Voltage Collapse Code after contingency------------------------------------------------------------------------------------------------------------------
'''
vc_options = VoltageCollapseOptions(step=0.001, adapt_step=True, step_min=0.00001, step_max=0.2, error_tol=1e-4, tol=1e-6, max_it=50, verbose=False)
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
for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name
lis = [grid.bus_dictionary[key] for key, value in grid.bus_dictionary.items()]     # full list
print(lis)
load_buses = [load for load in lis if 'L' in load]
print(load_buses)
mdl = vc.results.mdl()
index, columns, data = mdl.get_data()
indices = [lis.index(a) for a in load_buses]
indices = [lis.index('1_BUS 1044 L'), lis.index('1_BUS 1045 L'), lis.index('1_BUS 42 L'), lis.index('1_BUS 43 L')]
B = [[sublist[x] for x in indices] for sublist in data]
sub_columns = spec   #[columns[x] for x in indices]
df2 = pd.DataFrame(data=B, index=index, columns=sub_columns)
df2.plot(ax=ax, ls="--")
'''


