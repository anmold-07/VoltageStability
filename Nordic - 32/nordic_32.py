from GridCal.Engine import *
import networkx as nx
import pandas
from matplotlib import pylab
from GridCal.Engine.Simulations.ContinuationPowerFlow.voltage_collapse_driver import VoltageCollapseOptions, VoltageCollapseInput, VoltageCollapse


np.set_printoptions(precision=4)
grid = MultiCircuit()

#-----------------------------------------Graph Visualization for Nordic 32------------------------------------------------------------------------------------------------------------------
def save_graph(graph, file_name):

     plt.figure(num=None, figsize=(100, 100), dpi=300)
     plt.axis('off')
     fig = plt.figure(1)
     pos = nx.kamada_kawai_layout(graph)

     non_gen_non_load = [a for a in graph.nodes() if len(a) == 4]          # all nodes
     one_hun_kv_nodes = [a for a in non_gen_non_load if a[0] == '1']       # 130kV nodes
     two_hun_kv_nodes = [a for a in non_gen_non_load if a[0] == '2']       # 220 kv nodes or buses
     four_hun_kv_nodes = [a for a in non_gen_non_load if a[0] == '4']      # 400kV nodes
     load_nodes = [a for a in graph.nodes() if 'L' in a]
     gen_nodes = [a for a in graph.nodes() if 'G' in a]
     nx.draw_networkx_nodes(graph, pos, nodelist = four_hun_kv_nodes, node_color='blue', node_size=10000, alpha = 0.7, with_labels = True)
     nx.draw_networkx_nodes(graph, pos, nodelist = two_hun_kv_nodes, node_color='blue', node_size=10000, alpha=0.4, with_labels=True)
     nx.draw_networkx_nodes(graph, pos, nodelist = one_hun_kv_nodes, node_color='blue', node_size=10000, alpha=0.1, with_labels=True)
     nx.draw_networkx_nodes(graph, pos, nodelist = load_nodes, node_color='pink', node_size=30000, node_shape='d',  alpha=0.8, with_labels = True)
     nx.draw_networkx_nodes(graph, pos, nodelist = gen_nodes, node_color='red', node_size=20000, alpha=0.6, with_labels = True)

     for key, value in grid.bus_dictionary.items():
         grid.bus_dictionary[key] = key.name          # bus_dictionary modified with key as objects and values as bus names: altering the names of the nodes

     labels = {key.name:val for key, val in grid.bus_dictionary.items()}
     node_names = [val for key, val in grid.bus_dictionary.items()]
     nx.draw_networkx_labels(graph, pos, labels = labels, font_family='serif', font_size = 25)
     edge_labels = {}
     fro = []
     to =  []
     for i, branch in enumerate(grid.branches):
        f = grid.bus_dictionary[branch.bus_from]
        t = grid.bus_dictionary[branch.bus_to]
        fro.append(f)
        to.append(t)
        edge_labels[(f,t)] = branch.name

     #print(edge_labels)
     four_hun_edges_dict = {key:val for key, val in edge_labels.items() if '400' in val}
     four_hun_edges_list = [key for key, val in four_hun_edges_dict.items()]

     two_hun_edges_dict = {key: val for key, val in edge_labels.items() if '220' in val}
     two_hun_edges_list = [key for key, val in two_hun_edges_dict.items()]

     one_hun_edges_dict = {key: val for key, val in edge_labels.items() if '130' in val}
     one_hun_edges_list = [key for key, val in one_hun_edges_dict.items()]

     transfomer_edges_dict = {key: val for key, val in edge_labels.items() if 'Transformer' in val}
     transfomer_edges_list = [key for key, val in transfomer_edges_dict.items()]

     nx.draw_networkx_edges(graph, pos, width = 2.0, alpha = 0.5)
     nx.draw_networkx_edges(graph, pos, edgelist = four_hun_edges_list, edge_color = 'b', width = 30.0, alpha = 0.7, font_weight='bold')
     nx.draw_networkx_edges(graph, pos, edgelist = two_hun_edges_list, edge_color='b', width=50.0, alpha=0.4,  font_weight='bold')
     nx.draw_networkx_edges(graph, pos, edgelist = one_hun_edges_list, edge_color='b', width=50.0, alpha=0.1,  font_weight='bold')
     nx.draw_networkx_edges(graph, pos, edgelist = transfomer_edges_list, edge_color='g', width=30.0, alpha=0.4,  font_weight='bold')
     nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels, font_color='red',  font_weight='bold')

     plt.savefig(file_name, bbox_inches="tight")
     pylab.close()
     del fig
#-----------------------------------------End of Visualizing code------------------------------------------------------------------------------------------------------------------

#-----------------------------------------Start of modeling Nordi-32------------------------------------------------------------------------------------------------------------------

bus1 = Bus('1_LOAD 1041', vnom=20)    # creating an object
grid.add_bus(bus1)                    # appending an object to the list
grid.add_load(bus1, Load('load@BUS1041', P=600, Q=148.2))

bus2 = Bus('2_LOAD 1042', vnom=20)    # creating an object
grid.add_bus(bus2)                    # appending an object to the list
grid.add_load(bus2, Load('load@BUS1042', P=330.0, Q=71.0))

bus3 = Bus('3_LOAD 1043', vnom=20)    # creating an object
grid.add_bus(bus3)                    # appending an object to the lis
grid.add_load(bus3, Load('load@BUS1043', P=260.0, Q=83.8))

bus4 = Bus('4_LOAD 1044', vnom=20)    # creating an object
grid.add_bus(bus4)                    # appending an object to the list
grid.add_load(bus4, Load('load@BUS1044', P=840.0, Q=252.0))

bus5 = Bus('5_LOAD 1045', vnom=20)    # creating an object
grid.add_bus(bus5)                    # appending an object to the list
grid.add_load(bus5, Load('load@BUS1045', P=720.0, Q=190.4))

bus11 = Bus('11_LOAD 1011', vnom=20)    # creating an object
grid.add_bus(bus11)                    # appending an object to the list
grid.add_load(bus11, Load('load@BUS1011', P=200.0, Q=68.8))

bus12 = Bus('12_LOAD 1012', vnom=20)    # creating an object
grid.add_bus(bus12)                    # appending an object to the list
grid.add_load(bus12, Load('load@BUS1012', P=300.0, Q=83.8))

bus13 = Bus('13_LOAD 1013', vnom=20)    # creating an object
grid.add_bus(bus13)
grid.add_load(bus13, Load('load@BUS1013', P=100.0, Q=34.4))

bus22 = Bus('22_LOAD 1022', vnom=20)    # creating an object
grid.add_bus(bus22)
grid.add_load(bus22, Load('load@BUS1022', P=280.0, Q=79.9))

bus31 = Bus('31_LOAD 2031', vnom=20)    # creating an object
grid.add_bus(bus31)
grid.add_load(bus31, Load('load@BUS2031', P=100.0, Q=24.7))

bus32 = Bus('32_LOAD 2032', vnom=20)    # creating an object
grid.add_bus(bus32)
grid.add_load(bus32, Load('load@BUS2032', P=200.0, Q=39.6))

bus41 = Bus('41_LOAD 4041', vnom=20)    # creating an object
grid.add_bus(bus41)
grid.add_load(bus41, Load('load@BUS4041', P=540.0, Q=131.4))

bus42 = Bus('42_LOAD 4042', vnom=20)    # creating an object
grid.add_bus(bus42)
grid.add_load(bus42, Load('load@BUS4042', P=400.0, Q=127.4))

bus43 = Bus('43_LOAD 4043', vnom=20)    # creating an object
grid.add_bus(bus43)
grid.add_load(bus43, Load('load@BUS4043', P=900.0, Q=254.6))

bus46 = Bus('46_LOAD 4046', vnom=20)    # creating an object
grid.add_bus(bus46)
grid.add_load(bus46, Load('load@BUS4046', P=700.0, Q=211.8))

bus47 = Bus('47_LOAD 4047', vnom=20)    # creating an object
grid.add_bus(bus47)
grid.add_load(bus47, Load('load@BUS4047', P=100.0, Q=44.0))

bus51 = Bus('51_LOAD 4051', vnom=20)    # creating an object
grid.add_bus(bus51)
grid.add_load(bus51, Load('load@BUS4051', P=800.0, Q=258.2))

bus61 = Bus('61_LOAD 4061', vnom=20)    # creating an object
grid.add_bus(bus61)
grid.add_load(bus61, Load('load@BUS4061', P=500.0, Q=122.5))

bus62 = Bus('62_LOAD 4062', vnom=20)    # creating an object
grid.add_bus(bus62)
grid.add_load(bus62, Load('load@BUS4062', P=300.0, Q=83.8))

bus63 = Bus('63_LOAD 4063', vnom=20)    # creating an object
grid.add_bus(bus63)
grid.add_load(bus63, Load('load@BUS4063', P=590.0, Q=264.6))

bus71 = Bus('71_LOAD 4071', vnom=20)    # creating an object
grid.add_bus(bus71)
grid.add_load(bus71, Load('load@BUS4071', P=300.0, Q=83.8))

bus72 = Bus('72_LOAD 4072', vnom=20)    # creating an object
grid.add_bus(bus72)
grid.add_load(bus72, Load('load@BUS4072', P=2000.0, Q=396.1))

bus1011 = Bus('1011', vnom=130)    # creating an object
grid.add_bus(bus1011)
bus1012 = Bus('1012', vnom=130)    # creating an object
grid.add_bus(bus1012)
bus1013 = Bus('1013', vnom=130)    # creating an object
grid.add_bus(bus1013)
bus1014 = Bus('1014', vnom=130)    # creating an object
grid.add_bus(bus1014)
bus1021 = Bus('1021', vnom=130)    # creating an object
grid.add_bus(bus1021)
bus1022 = Bus('1022', vnom=130)    # creating an object
grid.add_bus(bus1022)
bus1041 = Bus('1041', vnom=130)    # creating an object
grid.add_bus(bus1041)
bus1042 = Bus('1042', vnom=130)    # creating an object
grid.add_bus(bus1042)
bus1043 = Bus('1043', vnom=130)    # creating an object
grid.add_bus(bus1043)
bus1044 = Bus('1044', vnom=130)    # creating an object
grid.add_bus(bus1044)
bus1045 = Bus('1045', vnom=130)    # creating an object
grid.add_bus(bus1045)

bus2031 = Bus('2031', vnom=220)    # creating an object
grid.add_bus(bus2031)
bus2032 = Bus('2032', vnom=220)    # creating an object
grid.add_bus(bus2032)

bus4011 = Bus('4011', vnom=400)    # creating an object
grid.add_bus(bus4011)
bus4012 = Bus('4012', vnom=400)    # creating an object
grid.add_bus(bus4012)
bus4021 = Bus('4021', vnom=400)    # creating an object
grid.add_bus(bus4021)
bus4022 = Bus('4022', vnom=400)    # creating an object
grid.add_bus(bus4022)
bus4031 = Bus('4031', vnom=400)    # creating an object
grid.add_bus(bus4031)
bus4032 = Bus('4032', vnom=400)    # creating an object
grid.add_bus(bus4032)
bus4041 = Bus('4041', vnom=400)    # creating an object
grid.add_bus(bus4041)
bus4042 = Bus('4042', vnom=400)    # creating an object
grid.add_bus(bus4042)
bus4043 = Bus('4043', vnom=400)    # creating an object
grid.add_bus(bus4043)
bus4044 = Bus('4044', vnom=400)    # creating an object
grid.add_bus(bus4044)
bus4045 = Bus('4045', vnom=400)    # creating an object
grid.add_bus(bus4045)
bus4046 = Bus('4046', vnom=400)    # creating an object
grid.add_bus(bus4046)
bus4047 = Bus('4047', vnom=400)    # creating an object
grid.add_bus(bus4047)
bus4051 = Bus('4051', vnom=400)    # creating an object
grid.add_bus(bus4051)
bus4061 = Bus('4061', vnom=400)    # creating an object
grid.add_bus(bus4061)
bus4062 = Bus('4062', vnom=400)    # creating an object
grid.add_bus(bus4062)
bus4063 = Bus('4063', vnom=400)    # creating an object
grid.add_bus(bus4063)
bus4071 = Bus('4071', vnom=400)    # creating an object
grid.add_bus(bus4071)
bus4072 = Bus('4072', vnom=400)    # creating an object
grid.add_bus(bus4072)

bus50001 = Bus('50001_G1', vnom=15)    # creating an object
grid.add_bus(bus50001)
gen1 = Generator(name='G1', active_power=600.0, Snom=800, voltage_module=1.0684, Qmin=-249.8, Qmax=249.8, p_max=760.0)
grid.add_generator(bus50001, gen1)

bus50002 = Bus('50002_G2', vnom=15)    # creating an object
grid.add_bus(bus50002)
gen2 = Generator(name='G2', active_power=300.0, Snom=600, voltage_module=1.0565, Qmin=-187.35, Qmax=187.35, p_max=570.0)
grid.add_generator(bus50002, gen2)

bus50003 = Bus('50003_G3', vnom=15)    # creating an object
grid.add_bus(bus50003)
gen3 = Generator(name='G3', active_power=550.0, Snom=700, voltage_module=1.0595, Qmin=-218.575, Qmax=218.575, p_max=665.0)
grid.add_generator(bus50003, gen3)

bus50004 = Bus('50004_G4', vnom=15)    # creating an object
grid.add_bus(bus50004)
gen4 = Generator(name='G4', active_power=400.0, Snom=600, voltage_module=1.0339, Qmin=-187.35, Qmax=187.35, p_max=570.0)
grid.add_generator(bus50004, gen4)

bus50005 = Bus('50005_G5', vnom=15)    # creating an object
grid.add_bus(bus50005)
gen5 = Generator(name='G5', active_power=200.0, Snom=250, voltage_module=1.0294, Qmin=-78.062, Qmax=78.062, p_max=237.5)
grid.add_generator(bus50005, gen5)

bus50006 = Bus('50006_G6', vnom=15)    # creating an object
grid.add_bus(bus50006)
gen6 = Generator(name='G6', active_power=360.0, Snom=400, voltage_module=1.0084, Qmin=-124.9, Qmax=174.356, p_max=360.0)
grid.add_generator(bus50006, gen6)

bus50007 = Bus('50007_G7', vnom=15)    # creating an object
grid.add_bus(bus50007)
gen7 = Generator(name='G7', active_power=182.0, Snom=200, voltage_module=1.0141, Qmin=-62.45, Qmax=87.178, p_max=180.0)
grid.add_generator(bus50007, gen7)

bus50008 = Bus('50008_G8', vnom=15)    # creating an object
grid.add_bus(bus50008)
gen8 = Generator(name='G8', active_power=750.0, Snom=850, voltage_module=1.0498, Qmin=-265.412, Qmax=265.412, p_max=807.5)
grid.add_generator(bus50008, gen8)

bus50009 = Bus('50009_G9', vnom=15)    # creating an object
grid.add_bus(bus50009)
gen9 = Generator(name='G9', active_power=668.5, Snom=1000, voltage_module=0.9988, Qmin=-312.25, Qmax=312.25, p_max=950.0)
grid.add_generator(bus50009, gen9)

bus50010 = Bus('50010_G10', vnom=15)    # creating an object
grid.add_bus(bus50010)
gen10 = Generator(name='G10', active_power=600, Snom=800, voltage_module=1.0157, Qmin=-249.8, Qmax=249.8, p_max=760.0)
grid.add_generator(bus50010, gen10)

bus50011 = Bus('50011_G11', vnom=15)    # creating an object
grid.add_bus(bus50011)
gen11 = Generator(name='G11', active_power=250, Snom=300, voltage_module=1.0211, Qmin=-93.675, Qmax=93.675, p_max=285.0)
grid.add_generator(bus50011, gen11)

bus50012 = Bus('50012_G12', vnom=15)    # creating an object
grid.add_bus(bus50012)
gen12 = Generator(name='G12', active_power=310, Snom=350, voltage_module=1.02, Qmin=-109.287, Qmax=109.287, p_max=332.5)
grid.add_generator(bus50012, gen12)

bus50013 = Bus('50013_G13', vnom=15)    # creating an object
grid.add_bus(bus50013)
gen13 = Generator(name='G13', active_power=0.0, Snom=300, voltage_module=1.017, Qmin=-200, Qmax=300, p_max=0.0)
grid.add_generator(bus50013, gen13)

bus50014 = Bus('50014_G14', vnom=15)    # creating an object
grid.add_bus(bus50014)
gen14 = Generator(name='G14', active_power=630.0, Snom=700.0, voltage_module=1.0454, Qmin=-218.575, Qmax=305.123, p_max=630.0)
grid.add_generator(bus50014, gen14)

bus50015 = Bus('50015_G15', vnom=15)    # creating an object
grid.add_bus(bus50015)
gen15 = Generator(name='G15', active_power=1080.0, Snom=1200.0, voltage_module=1.0455, Qmin=-374.7, Qmax=523.068, p_max=1080.0)
grid.add_generator(bus50015, gen15)

bus50016 = Bus('50016_G16', vnom=15)    # creating an object
grid.add_bus(bus50016)
gen16 = Generator(name='G16', active_power=600.0, Snom=700.0, voltage_module=1.0531, Qmin=-218.575, Qmax=305.123, p_max=630.0)
grid.add_generator(bus50016, gen16)

bus50017 = Bus('50017_G17', vnom=15)    # creating an object
grid.add_bus(bus50017)
gen17 = Generator(name='G17', active_power=530.0, Snom=600.0, voltage_module=1.0092, Qmin=-187.35, Qmax=261.534, p_max=540.0)
grid.add_generator(bus50017, gen17)

bus50018 = Bus('50018_G18', vnom=15)    # creating an object
grid.add_bus(bus50018)
gen18 = Generator(name='G18', active_power=1060.0, Snom=1200.0, voltage_module=1.0307, Qmin=-374.7, Qmax=523.068, p_max=1080.0)
grid.add_generator(bus50018, gen18)

bus50019 = Bus('50019_G19', vnom=15)    # creating an object
grid.add_bus(bus50019)
gen19 = Generator(name='G19', active_power=300.0, Snom=500.0, voltage_module=1.03, Qmin=-156.125, Qmax=156.125, p_max=475.0)
grid.add_generator(bus50019, gen19)

bus50020 = Bus('50020_G20', vnom=15, is_slack= True)    # creating an object
grid.add_bus(bus50020)
gen20 = Generator(name='G20', active_power=2137.588, Snom=4500.0, voltage_module=1.0185, Qmin=-1405.125, Qmax=1405.125, p_max=4275.0)
grid.add_generator(bus50020, gen20)


grid.add_branch(Branch(bus1011, bus1013, '130kV 1011_1013_1', r=0.01, x=0.07, b=0.0138, rate=350))
grid.add_branch(Branch(bus1013, bus1011, '130kV 1011_1013_2', r=0.01, x=0.07, b=0.0138, rate=350))
grid.add_branch(Branch(bus1012, bus1014, '130kV line 1012_1014_1', r=0.0140237, x=0.09, b=0.01805, rate=350))
grid.add_branch(Branch(bus1014, bus1012, '130kV line 1012_1014_2', r=0.0140237, x=0.09, b=0.01805, rate=350))
grid.add_branch(Branch(bus1013, bus1014, '130kV line 1013_1014_1', r=0.00698225, x=0.05, b=0.01009, rate=350))
grid.add_branch(Branch(bus1014, bus1013, '130kV line 1013_1014_2', r=0.00698225, x=0.05, b=0.01009, rate=350))
grid.add_branch(Branch(bus1021, bus1022, '130kV line 1021_1022_1', r=0.03, x=0.2, b=0.03026, rate=350))
grid.add_branch(Branch(bus1022, bus1021, '130kV line 1021_1022_2', r=0.03, x=0.2, b=0.03026, rate=350))
grid.add_branch(Branch(bus1041, bus1043, '130kV line 1041_1043_1', r=0.01, x=0.06, b=0.01221, rate=350))
grid.add_branch(Branch(bus1043, bus1041, '130kV line 1041_1043_2', r=0.01, x=0.06, b=0.01221, rate=350))
grid.add_branch(Branch(bus1041, bus1045, '130kV line 1041_1045_1', r=0.01497040, x=0.12, b=0.02495, rate=350))
grid.add_branch(Branch(bus1045, bus1041, '130kV line 1041_1045_2', r=0.01497040, x=0.12, b=0.02495, rate=350))
grid.add_branch(Branch(bus1042, bus1044, '130kV line 1042_1044_1', r=0.03798820, x=0.28, b=0.05999, rate=350))
grid.add_branch(Branch(bus1044, bus1042, '130kV line 1042_1044_2', r=0.03798820, x=0.28, b=0.05999, rate=350))
grid.add_branch(Branch(bus1042, bus1045, '130kV line 1042_1045_1', r=0.05, x=0.3, b=0.05999, rate=350))
grid.add_branch(Branch(bus1043, bus1044, '130kV line 1043_1044_1', r=0.01, x=0.08, b=0.01593, rate=350))
grid.add_branch(Branch(bus1044, bus1043, '130kV line 1043_1044_2', r=0.01, x=0.08, b=0.01593, rate=350))
grid.add_branch(Branch(bus2031, bus2032, '220kV line 2031_2032_1', r=0.012, x=0.09, b=0.01521, rate=500))
grid.add_branch(Branch(bus2032, bus2031, '220kV line 2031_2032_2', r=0.012, x=0.09, b=0.01521, rate=500))

br4011_4012 = Branch(bus4011, bus4012, '400kV line 4011_4012_1', r=0.001, x=0.008, b=0.20106, rate=1400)
grid.add_branch(br4011_4012)

grid.add_branch(Branch(bus4011, bus4021, '400kV line 4011_4021_1', r=0.006, x=0.06, b=1.79949, rate=1400))
grid.add_branch(Branch(bus4021, bus4011, '400kV line 4011_4022_1', r=0.004, x=0.04, b=1.20134, rate=1400))
grid.add_branch(Branch(bus4011, bus4071, '400kV line 4011_4071_1', r=0.005, x=0.045, b=1.4024, rate=1400))

br1 = Branch(bus4012, bus4022, '400kV line 4012_4022_1', r=0.004, x=0.035, b=1.05056, rate=1400)
grid.add_branch(br1)

grid.add_branch(Branch(bus4012, bus4071, '400kV line 4012_4071_1', r=0.005, x=0.05, b=1.49792, rate=1400))
grid.add_branch(Branch(bus4021, bus4032, '400kV line 4021_4032_1', r=0.004, x=0.04, b=1.20134, rate=1400))

br2 = Branch(bus4021, bus4042, '400kV line 4021_4042_1', r=0.01, x=0.06, b=3.00086, rate=1400)
grid.add_branch(br2)

grid.add_branch(Branch(bus4022, bus4031, '400kV line 4022_4031_1', r=0.004, x=0.04, b=1.20134, rate=1400))
grid.add_branch(Branch(bus4031, bus4022, '400kV line 4022_4031_2', r=0.004, x=0.04, b=1.20134, rate=1400))

br4031_4032 = Branch(bus4031, bus4032, '400kV line 4031_4032_1', r=0.001, x=0.01, b=0.30159, rate=1400)
grid.add_branch(br4031_4032)

grid.add_branch(Branch(bus4031, bus4041, '400kV line 4031_4041_1', r=0.006, x=0.04, b=2.39766, rate=1400))
grid.add_branch(Branch(bus4041, bus4031, '400kV line 4031_4041_2', r=0.006, x=0.04, b=2.39766, rate=1400))
grid.add_branch(Branch(bus4032, bus4042, '400kV line 4032_4042_1', r=0.01, x=0.04, b=2.00058, rate=1400))
grid.add_branch(Branch(bus4032, bus4044, '400kV line 4032_4044_1', r=0.006, x=0.05, b=2.39766, rate=1400))
grid.add_branch(Branch(bus4041, bus4044, '400kV line 4041_4044_1', r=0.003, x=0.03, b=0.89974, rate=1400))
grid.add_branch(Branch(bus4041, bus4061, '400kV line 4041_4061_1', r=0.006, x=0.045, b=1.30189, rate=1400))
grid.add_branch(Branch(bus4042, bus4043, '400kV line 4042_4043_1', r=0.002, x=0.015, b=0.49763, rate=1400))
grid.add_branch(Branch(bus4042, bus4044, '400kV line 4042_4044_1', r=0.002, x=0.02, b=0.59818, rate=1400))
grid.add_branch(Branch(bus4043, bus4044, '400kV line 4043_4044_1', r=0.001, x=0.01, b=0.30159, rate=1400))
grid.add_branch(Branch(bus4043, bus4046, '400kV line 4043_4046_1', r=0.001, x=0.01, b=0.30159, rate=1400))
grid.add_branch(Branch(bus4043, bus4047, '400kV line 4043_4047_1', r=0.002, x=0.02, b=0.59818, rate=1400))
grid.add_branch(Branch(bus4044, bus4045, '400kV line 4043_4045_1', r=0.002, x=0.02, b=0.59818, rate=1400))
grid.add_branch(Branch(bus4045, bus4044, '400kV line 4044_4045_2', r=0.002, x=0.02, b=0.59818, rate=1400))
grid.add_branch(Branch(bus4045, bus4051, '400kV line 4045_4051_1', r=0.004, x=0.04, b=1.20134, rate=1400))
grid.add_branch(Branch(bus4051, bus4045, '400kV line 4045_4051_2', r=0.004, x=0.04, b=1.20134, rate=1400))
grid.add_branch(Branch(bus4045, bus4062, '400kV line 4045_4062_1', r=0.011, x=0.08, b=2.39766, rate=1400))
grid.add_branch(Branch(bus4046, bus4047, '400kV line 4046_4047_1', r=0.001, x=0.015, b=0.49763, rate=1400))
grid.add_branch(Branch(bus4061, bus4062, '400kV line 4061_4062_1', r=0.002, x=0.02, b=0.59818, rate=1400))
grid.add_branch(Branch(bus4062, bus4063, '400kV line 4062_4063_1', r=0.003, x=0.03, b=0.89974, rate=1400))
grid.add_branch(Branch(bus4063, bus4062, '400kV line 4062_4063_2', r=0.003, x=0.03, b=0.89974, rate=1400))
grid.add_branch(Branch(bus4071, bus4072, '400kV line 4071_4072_1', r=0.003, x=0.03, b=3.00086, rate=1400))
grid.add_branch(Branch(bus4072, bus4071, '400kV line 4071_4072_2', r=0.003, x=0.03, b=3.00086, rate=1400))

#---------------these transofmers are redundant as the Transformer is added as part of grid.add_branch ( branch_type...  )------#---------------
SS1 = TransformerType(name="SS1",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1200, # MV1
                    ) # %
grid.add_transformer_type(SS1)
#---------------#---------------#---------------#---------------#---------------#---------------#---------------#---------------#---------------
grid.add_branch(Branch(bus1041, bus1, 'Transformer line 1041_1_1', r=0.0, x=0.00833300, b=0.0, tap = 1, rate=1200, bus_to_regulated=True,  branch_type=BranchType.Transformer))

SS2 = TransformerType(name="SS2",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=600, # MV1
                    ) # %
grid.add_transformer_type(SS2)
grid.add_branch(Branch(bus1042, bus2, 'Transformer line 1042_2_1', r=0.0, x=0.01666000, b=0.0, tap = 1, rate=600, bus_to_regulated=True, branch_type=BranchType.Transformer))


SS3 = TransformerType(name="SS3",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=460, # MV1
                    ) # %
grid.add_transformer_type(SS3)
grid.add_branch(Branch(bus1043, bus3, 'Transformer line 1043_3_1', r=0.0, x=0.02170000, b=0.0, tap = 1.01, rate=460, bus_to_regulated=True,  branch_type=BranchType.Transformer))

SS4 = TransformerType(name="SS4",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1600, # MV1
                    ) # %
grid.add_transformer_type(SS4)
grid.add_branch(Branch(bus1044, bus4, 'Transformer line 1044_4_1', r=0.0, x=0.00625000, b=0.0, tap = 0.99, rate=1600, bus_to_regulated=True,  branch_type=BranchType.Transformer))

SS5 = TransformerType(name="SS5",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1400, # MV1
                    ) # %
grid.add_transformer_type(SS5)
grid.add_branch(Branch(bus1045, bus5, 'Transformer line 1045_5_1', r=0.0, x=0.00714280, b=0.0, tap = 1, rate=1400, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS6 = TransformerType(name="SS6",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=400, # MV1
                    ) # %
grid.add_transformer_type(SS6)
grid.add_branch(Branch(bus1011, bus11, 'Transformer line 1011_11_1', r=0.0, x=0.02500000, b=0.0, tap = 1.04, rate=400, bus_to_regulated=True,   branch_type=BranchType.Transformer))


SS7 = TransformerType(name="SS7",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=600, # MV1
                    ) # %
grid.add_transformer_type(SS7)
grid.add_branch(Branch(bus1012, bus12, 'Transformer line 1012_12_1', r=0.0, x=0.01666000, b=0.0, tap = 1.05, rate=600, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS8 = TransformerType(name="SS8",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=200, # MV1
                    ) # %
grid.add_transformer_type(SS8)
grid.add_branch(Branch(bus1013, bus13, 'Transformer line 1013_13_1', r=0.0, x=0.05000000, b=0.0, tap = 1.04, rate=200, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS9 = TransformerType(name="SS9",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=560, # MV1
                    ) # %
grid.add_transformer_type(SS9)
grid.add_branch(Branch(bus1022, bus22, 'Transformer line 1022_22_1', r=0.0, x=0.01785714, b=0.0, tap = 1.04, rate=560, bus_to_regulated=True, branch_type=BranchType.Transformer))



SS10 = TransformerType(name="SS10",
                     hv_nominal_voltage=220, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=200, # MV1
                    ) # %
grid.add_transformer_type(SS10)
grid.add_branch(Branch(bus2031, bus31, 'Transformer line 2031_31_1', r=0.0, x=0.05000000, b=0.0, tap = 1.01, rate=200, bus_to_regulated=True, branch_type=BranchType.Transformer))



SS11 = TransformerType(name="SS11",
                     hv_nominal_voltage=220, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=200, # MV1
                    ) # %
grid.add_transformer_type(SS11)
grid.add_branch(Branch(bus2032, bus32, 'Transformer line 2032_32_1', r=0.0, x=0.02500000, b=0.0, tap = 1.06, rate=200, bus_to_regulated=True,  branch_type=BranchType.Transformer))




SS12 = TransformerType(name="SS12",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1080, # MV1
                    ) # %
grid.add_transformer_type(SS12)
grid.add_branch(Branch(bus4041, bus41, 'Transformer line 4041_41_1', r=0.0, x=0.00925925, b=0.0, tap = 1.04, rate=1080, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS13 = TransformerType(name="SS13",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=800, # MV1
                    ) # %
grid.add_transformer_type(SS13)
grid.add_branch(Branch(bus4042, bus42, 'Transformer line 4042_42_1', r=0.0, x=0.01250000, b=0.0, tap = 1.03, rate=800, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS14 = TransformerType(name="SS14",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1800, # MV1
                    ) # %
grid.add_transformer_type(SS14)
grid.add_branch(Branch(bus4043, bus43, 'Transformer line 4043_43_1', r=0.0, x=0.00555000, b=0.0, tap = 1.03, rate=1800, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS15 = TransformerType(name="SS15",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1400, # MV1
                    ) # %
grid.add_transformer_type(SS15)
grid.add_branch(Branch(bus4046, bus46, 'Transformer line 4046_46_1', r=0.0, x=0.00714200, b=0.0, tap = 1.02, rate=1400, bus_to_regulated=True, branch_type=BranchType.Transformer))



SS16 = TransformerType(name="SS16",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=200, # MV1
                    ) # %
grid.add_transformer_type(SS16)
grid.add_branch(Branch(bus4047, bus47, 'Transformer line 4047_47_1', r=0.0, x=0.05000000, b=0.0, tap = 1.04, rate=200, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS17 = TransformerType(name="SS17",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1600, # MV1
                    ) # %
grid.add_transformer_type(SS17)
grid.add_branch(Branch(bus4051, bus51, 'Transformer line 4051_51_1', r=0.0, x=0.00625000, b=0.0, tap = 1.05, rate=1600, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS18 = TransformerType(name="SS18",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1000, # MV1
                    ) # %
grid.add_transformer_type(SS18)
grid.add_branch(Branch(bus4061, bus61, 'Transformer line 4061_61_1', r=0.0, x=0.01000000, b=0.0, tap = 1.03, rate=1000, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS19 = TransformerType(name="SS19",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=600, # MV1
                    ) # %
grid.add_transformer_type(SS19)
grid.add_branch(Branch(bus4062, bus62, 'Transformer line 4062_62_1', r=0.0, x=0.01660000, b=0.0, tap = 1.04, rate=600, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS20 = TransformerType(name="SS20",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=1180, # MV1
                    ) # %
grid.add_transformer_type(SS20)
grid.add_branch(Branch(bus4063, bus63, 'Transformer line 4063_63_1', r=0.0, x=0.00847500, b=0.0, tap = 1.03, rate=1180, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS21 = TransformerType(name="SS21",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=600, # MV1
                    ) # %
grid.add_transformer_type(SS21)
grid.add_branch(Branch(bus4071, bus71, 'Transformer line 4071_71_1', r=0.0, x=0.01660000, b=0.0, tap = 1.03, rate=600, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS22 = TransformerType(name="SS22",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=20, # kV
                     nominal_power=4000, # MV1
                    ) # %
grid.add_transformer_type(SS22)
grid.add_branch(Branch(bus4072, bus72, 'Transformer line 4072_72_1', r=0.0, x=0.00250000, b=0.0, tap = 1.05, rate=4000, bus_to_regulated=True, branch_type=BranchType.Transformer))



SS23 = TransformerType(name="SS23",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=1250, # MV1
                    ) # %
grid.add_transformer_type(SS23)
grid.add_branch(Branch(bus4011, bus1011, 'Transformer line 4011_1011', r=0.0, x=0.00800000, b=0.0, tap = 0.95, rate=1250, bus_to_regulated=True, branch_type=BranchType.Transformer))


SS24 = TransformerType(name="SS24",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=1250, # MV1
                    ) # %
grid.add_transformer_type(SS24)
grid.add_branch(Branch(bus4012, bus1012, 'Transformer line 4012_1012', r=0.0, x=0.00800000, b=0.0, tap = 0.95, rate=1250, bus_to_regulated=True, branch_type=BranchType.Transformer))


SS25 = TransformerType(name="SS25",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=800, # MV1
                    ) # %
grid.add_transformer_type(SS25)
grid.add_branch(Branch(bus1012, bus50001, 'Transformer line 1012_50001', r=0.0, x=0.01875000, b=0.0, tap = 1.0, rate=800, bus_to_regulated=True,  branch_type=BranchType.Transformer))




SS26 = TransformerType(name="SS26",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=600, # MV1
                    ) # %
grid.add_transformer_type(SS26)
grid.add_branch(Branch(bus1013, bus50002, 'Transformer line 1013_50002', r=0.0, x=0.02500000, b=0.0, tap = 1.0, rate=600, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS27 = TransformerType(name="SS27",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=700, # MV1
                    ) # %
grid.add_transformer_type(SS27)
grid.add_branch(Branch(bus1014, bus50003, 'Transformer line 1014_50003', r=0.0, x=0.02142000, b=0.0, tap = 1.0, rate=700, bus_to_regulated=True,  branch_type=BranchType.Transformer))

SS28 = TransformerType(name="SS28",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=600, # MV1
                    ) # %
grid.add_transformer_type(SS28)
grid.add_branch(Branch(bus1021, bus50004, 'Transformer line 1021_50004', r=0.0, x=0.02500000, b=0.0, tap = 1.0, rate=600, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS29 = TransformerType(name="SS29",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=833.3, # MV1
                    ) # %
grid.add_transformer_type(SS29)
grid.add_branch(Branch(bus4022, bus1022, 'Transformer line 4022_1022', r=0.0, x=0.01800000, b=0.0, tap = 0.93, rate=833.3, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS30 = TransformerType(name="SS30",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=250, # MV1
                    ) # %
grid.add_transformer_type(SS30)
grid.add_branch(Branch(bus1022, bus50005, 'Transformer line 1022_50005', r=0.0, x=0.04000000, b=0.0, tap = 1.05, rate=250, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS31 = TransformerType(name="SS31",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=400, # MV1
                    ) # %
grid.add_transformer_type(SS31)
grid.add_branch(Branch(bus1042, bus50006, 'Transformer line 1042_50006', r=0.0, x=0.03750000, b=0.0, tap = 1.05, rate=400, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS32 = TransformerType(name="SS32",
                     hv_nominal_voltage=130, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=200, # MV1
                    ) # %
grid.add_transformer_type(SS32)
grid.add_branch(Branch(bus1043, bus50007, 'Transformer line 1043_50007', r=0.0, x=0.07500000, b=0.0, tap = 1.05, rate=200, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS33 = TransformerType(name="SS33",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=1000, # MV1
                    ) # %
grid.add_transformer_type(SS33)
grid.add_branch(Branch(bus1044, bus4044, 'Transformer line 1044_4044 A', r=0.0, x=0.01000000, b=0.0, tap = 1.03, rate=1000, bus_to_regulated=True, branch_type=BranchType.Transformer))


SS34 = TransformerType(name="SS34",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=1000, # MV1
                    ) # %
grid.add_transformer_type(SS34)
grid.add_branch(Branch(bus1044, bus4044, 'Transformer line 1044_4044 B', r=0.0, x=0.01000000, b=0.0, tap = 1.03, rate=1000, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS35 = TransformerType(name="SS35",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=1000, # MV1
                    ) # %
grid.add_transformer_type(SS35)
grid.add_branch(Branch(bus1045, bus4045, 'Transformer line 1045_4045 A', r=0.0, x=0.01000000, b=0.0, tap = 1.04, rate=1000, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS36 = TransformerType(name="SS36",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=130, # kV
                     nominal_power=1000, # MV1
                    ) # %
grid.add_transformer_type(SS36)
grid.add_branch(Branch(bus1045, bus4045, 'Transformer line 1045_4045 B', r=0.0, x=0.01000000, b=0.0, tap = 1.04, rate=1000, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS37 = TransformerType(name="SS37",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=220, # kV
                     nominal_power=833.3, # MV1
                    ) # %
grid.add_transformer_type(SS37)
grid.add_branch(Branch(bus2031, bus4031, 'Transformer line 4031_2031', r=0.0, x=0.01200000, b=0.0, tap = 1.0, rate=833.3, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS38 = TransformerType(name="SS38",
                     hv_nominal_voltage=220, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=850, # MV1
                    ) # %
grid.add_transformer_type(SS38)
grid.add_branch(Branch(bus2032, bus50008, 'Transformer line 2032_50008', r=0.0, x=0.01760000, b=0.0, tap = 1.05, rate=850.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))




SS39 = TransformerType(name="SS39",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=1000, # MV1
                    ) # %
grid.add_transformer_type(SS39)
grid.add_branch(Branch(bus4011, bus50009, 'Transformer line 4011_50009', r=0.0, x=0.015, b=0.0, tap = 1.05, rate=1000.0, bus_to_regulated=True, branch_type=BranchType.Transformer))


SS40 = TransformerType(name="SS40",
                     hv_nominal_voltage=400, # kV
                     lv_nominal_voltage=15, # kV
                     nominal_power=800, # MV1
                    ) # %
grid.add_transformer_type(SS40)
grid.add_branch(Branch(bus4012, bus50010, 'Transformer line 4011_50010', r=0.0, x=0.01875000, b=0.0, tap = 1.05, rate=800.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS41 = TransformerType(name="SS41",
                       hv_nominal_voltage=400, # kV
                       lv_nominal_voltage=15, # kV
                       nominal_power=300, # MV1
                       ) # %
grid.add_transformer_type(SS41)
grid.add_branch(Branch(bus4021, bus50011, 'Transformer line 4021_50011', r=0.0, x=0.05000000, b=0.0, tap = 1.05, rate=300.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS42 = TransformerType(name="SS42",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=350, # MV1
                      ) # %
grid.add_transformer_type(SS42)
grid.add_branch(Branch(bus4031, bus50012, 'Transformer line 4031_50012', r=0.0, x=0.04285000, b=0.0, tap = 1.05, rate=350.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))



SS43 = TransformerType(name="SS43",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=300, # MV1
                      ) # %
grid.add_transformer_type(SS43)
grid.add_branch(Branch(bus4041, bus50013, 'Transformer line 4041_50013', r=0.0, x=0.03330000, b=0.0, tap = 1.05, rate=300.0, bus_to_regulated=True, branch_type=BranchType.Transformer))



SS44 = TransformerType(name="SS44",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=700, # MV1
                      ) # %
grid.add_transformer_type(SS44)
grid.add_branch(Branch(bus4042, bus50014, 'Transformer line 4042_50014', r=0.0, x=0.02140000, b=0.0, tap = 1.05, rate=700.0,bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS45 = TransformerType(name="SS45",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=700, # MV1
                      ) # %
grid.add_transformer_type(SS45)
grid.add_branch(Branch(bus4047, bus50015, 'Transformer line 4047_50015', r=0.0, x=0.01250000, b=0.0, tap = 1.05, rate=1200.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))

SS46 = TransformerType(name="SS46",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=700, # MV1
                      ) # %
grid.add_transformer_type(SS46)
grid.add_branch(Branch(bus4051, bus50016, 'Transformer line 4051_50016', r=0.0, x=0.02142000, b=0.0, tap = 1.05, rate=700.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS47 = TransformerType(name="SS47",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=600, # MV1
                      ) # %
grid.add_transformer_type(SS47)
grid.add_branch(Branch(bus4062, bus50017, 'Transformer line 4062_50017', r=0.0, x=0.02500000, b=0.0, tap = 1.05, rate=600.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))


SS48 = TransformerType(name="SS48",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=1200, # MV1
                      ) # %
grid.add_transformer_type(SS48)
grid.add_branch(Branch(bus4063, bus50018, 'Transformer line 4063_50018', r=0.0, x=0.01250000, b=0.0, tap = 1.05, rate=1200.0, bus_to_regulated=True,  branch_type=BranchType.Transformer, template = SS48))


SS49 = TransformerType(name="SS49",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=500, # MV1
                      ) # %
grid.add_transformer_type(SS49)
grid.add_branch(Branch(bus4071, bus50019, 'Transformer line 4071_50019', r=0.0, x=0.03000000, b=0.0, tap = 1.05, rate=500.0, bus_to_regulated=True, branch_type=BranchType.Transformer))

SS50 = TransformerType(name="SS50",
                      hv_nominal_voltage=400, # kV
                      lv_nominal_voltage=15, # kV
                      nominal_power=4500, # MV1
                      ) # %
grid.add_transformer_type(SS50)
grid.add_branch(Branch(bus4072, bus50020, 'Transformer line 4072_50020', r=0.0, x=0.00333000, b=0.0, tap = 1.05, rate=4500.0, bus_to_regulated=True,  branch_type=BranchType.Transformer))


grid.add_shunt(bus1022, Shunt( name='shunt 1022', B=50.0))
grid.add_shunt(bus1041, Shunt( name='shunt 1041', B=250.0))
grid.add_shunt(bus1043, Shunt( name='shunt 1043', B=200.0))
grid.add_shunt(bus1044, Shunt( name='shunt 1044', B=200.0))
grid.add_shunt(bus1045, Shunt( name='shunt 1045', B=200.0))
grid.add_shunt(bus4012, Shunt( name='shunt 4012', B=-100.0))
grid.add_shunt(bus4041, Shunt( name='shunt 4041', B=200.0))
grid.add_shunt(bus4043, Shunt( name='shunt 4043', B=200.0))
grid.add_shunt(bus4046, Shunt( name='shunt 4046', B=100.0))
grid.add_shunt(bus4051, Shunt( name='shunt 4051', B=100.0))
grid.add_shunt(bus4071, Shunt( name='shunt 4071', B=-400.0))
#-----------------------------------------End of modeling Nordi-32-----------------------------------------


#-----------------------------------------Code to run Power Flow ------------------------------------------------------------------------------------------------------------------

options = PowerFlowOptions(SolverType.NR, initialize_with_existing_solution=True, control_p=False, multi_core=False, dispatch_storage=False, control_q=ReactivePowerControlMode.NoControl, control_taps=TapsControlMode.NoControl)
power_flow = PowerFlowDriver(grid, options)
power_flow.run()
vm = np.abs(power_flow.results.voltage)
va = np.angle(power_flow.results.voltage)

for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name

bus_list = list(grid.bus_dictionary.values())
print(bus_list)                                      # list of all buses can be used for comparing power flows:
branch_list = list(grid.branch_dictionary.values())  # empty list
print(grid.branch_names)                             # branch names
keys = grid.branch_names
values = abs(power_flow.results.Sbranch)
di = dict(zip(keys, values))                         # printing the loading corresponding to respective branch names
#print(di)
sort_di = {k: v for k, v in sorted(di.items(), key=lambda item: item[1], reverse=True)}    # sorting to find the branch with max power for N-1 contingency
print(sort_di)

bus_list = list(grid.bus_dictionary.values())

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
#-----------Adding Bar plot for Power flow-------------------------------------------------------------------------------

#------------------------------------------reading the nordic--32 PSS/E text file for plotting purpose------------------------------
fp = open('nordic 32 psse power flow.txt')
lines = fp.readlines()
lis = []
for i, v in enumerate(lines):
    if "BUS" in v:
        lis.append(v)
print(lis)
mag = []
ang = []
data = lis[0].split()
print(data)
print(data[10])
print(data[11])

for a in lis:
    data = a.split()
    mag.append(data[10])
    ang.append(data[11])

mag = [a.replace('PU', '') for a in mag] # removing the PU tag
print(mag)
mag = [float(a) for a in mag]
print(mag)
ang = [float(a) for a in ang]
print(ang)
#--------------------------------------------------------------------------------------------------------------------------

B = tuple(bus_list)
y = np.arange(len(B))
y = [3*i for i in y]

magnitude = abs(power_flow.results.voltage)
magnitude = [round(a, 3) for a in magnitude]
print(magnitude)

plt.figure(figsize=(20,25))
plt.barh(y, magnitude, align = 'center', height = 0.5, color="skyblue")
plt.title('Voltage Magnitude plot for all the buses of Nordic-32', fontsize=22)
plt.yticks(y, B)
plt.xlabel('Magnitude of Voltages in Per Unit (P.U)', fontsize=22)
for i, v in enumerate(magnitude):
    plt.text(v + 0.01, 3*i, str(v), color='green', fontweight='bold', fontsize = 15)
plt.xlim(0,1.25)
plt.tick_params(labelsize=20)
plt.tight_layout()
plt.savefig('NORDIC_32_magnitude.png')

angles =  np.degrees(np.angle(power_flow.results.voltage))
angles = [round(a, 3) for a in angles]
plt.figure(figsize=(20,25))
plt.barh(y, angles, align = 'center', height=1.0, color="skyblue")
plt.title('Voltage Angles plot for all the buses of Nordic-32', fontsize=22)
plt.yticks(y, B)
plt.xlabel('Angles of Voltages in Degrees', fontsize=22)
for i, v in enumerate(angles):
    plt.text(v - 0.05, 3*i, str(v), color='green', fontweight='bold', fontsize = 15)
#plt.xlim(0,1.25)
plt.tick_params(labelsize=20)
plt.tight_layout()
plt.savefig('NORDIC_32_angles.png')


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
ax.title.set_text('Voltage Magnitudes plot for all the buses of Nordic-32')
ax.set_xlabel('Magnitude of Voltages in Per Unit (P.U)')
#fig.tight_layout()

for i, v in enumerate(magnitude):
    ax.text(v + 0.01, i, str(v), color='blue', fontweight='bold', fontsize = 10)

for i, v in enumerate(mag):
    ax.text(v + 0.01, i+width, str(v), color='green', fontweight='bold', fontsize=10)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(30)
ax.tick_params(labelsize=25)
fig.savefig('NORDIC_32_comparison_magnitudes.png')
fig.savefig("NORDIC_32_comparison_magnitudes.pdf", bbox_inches='tight', dpi = 500)

#-----------------Comparison of power flow angles:--------------------------------------
df = pandas.DataFrame(dict(graph=bus_list, n=angles, m=ang))
ind = np.arange(len(df))
width = 0.4
fig, ax = plt.subplots(figsize=(30,30))
ax.barh(ind, df.n, width, color="skyblue", label='GRIDCAL')
ax.barh(ind + width, df.m, width, color='green', label='PSS/E')
ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
ax.legend()
ax.title.set_text('Voltage Angles plot for all the buses of Nordic-32')
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
    item.set_fontsize(30)
ax.tick_params(labelsize=25)
fig.savefig('NORDIC_32_comparison_angles.png')
fig.savefig("NORDIC_32_comparison_angles.pdf", bbox_inches='tight', dpi = 500)


plt.show()

#-----------------------------------------End of Power FLow code--------------------------------------------------------------------------------------------------------

#-----------------------------------------Start of Voltage Collapse Code------------------------------------------------------------------------------------------------------------------
'''
vc_options = VoltageCollapseOptions(step=0.001, adapt_step=True, step_min=0.00001, step_max=0.2, error_tol=1e-3, tol=1e-6, max_it=20, verbose=False)
numeric_circuit = grid.compile()
numeric_inputs = numeric_circuit.compute()
Sbase = np.zeros(len(grid.buses), dtype=complex)
Vbase = np.zeros(len(grid.buses), dtype=complex)
for c in numeric_inputs:
    Sbase[c.original_bus_idx] = c.Sbus
    Vbase[c.original_bus_idx] = c.Vbus
unitary_vector = -1 + 2 * np.random.random(len(grid.buses))
vc_inputs = VoltageCollapseInput(Sbase=Sbase, Vbase=Vbase, Starget=Sbase * (5 + unitary_vector))
vc = VoltageCollapse(circuit=grid, options=vc_options, inputs=vc_inputs)
vc.run()
spec = ['1_LOAD 1041', '4_LOAD 1044', '4044']

for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name
lis = [grid.bus_dictionary[key] for key, value in grid.bus_dictionary.items()]
print(lis)

mdl = vc.results.mdl()
index, columns, data = mdl.get_data()

indices = [lis.index('1_LOAD 1041'), lis.index('4_LOAD 1044'), lis.index('4044')]      # selecting the required buses you want to plot
A = [[sublist[x] for x in indices] for sublist in data]
#print(data)
#print(A)
print(columns)
sub_columns = spec
df1 = pd.DataFrame(data=A, index=index, columns=sub_columns)
ax = df1.plot()
ax.set_title('Bus Voltage - Nordic 32', fontsize=20)
ax.set_ylabel('Bus Voltage in Per Unit (P.U)', fontsize=20)
ax.set_xlabel('Loading from the base situation ($\lambda$)', fontsize=20)
'''
#-----------------------------------------End of Voltage Collapse Code------------------------------------------------------------------------------------------------------------------

#----------------------------------------NetworkX grid plot visulaization--------------------------------------------
'''
g2 = grid.build_multi_graph()
print(nx.info(g2))
save_graph(g2,"nordic_32_before_outage.pdf")
'''





#mdl.plot()
#grid.delete_branch(br1)            # removing the most heavily loaded branch
#grid.delete_branch(br2)            # removing the loaded branch < br1
'''
grid.delete_branch(br4031_4032)
#grid.delete_branch(br4011_4012)


#-----------------------------------------Start of Voltage Collapse Code after contingency------------------------------------------------------------------------------------------------------------------
vc_options = VoltageCollapseOptions(step=0.001, adapt_step=True, step_min=0.00001, step_max=0.2, error_tol=1e-3, tol=1e-6, max_it=20, verbose=False)
numeric_circuit = grid.compile()
numeric_inputs = numeric_circuit.compute()
Sbase = np.zeros(len(grid.buses), dtype=complex)
Vbase = np.zeros(len(grid.buses), dtype=complex)
for c in numeric_inputs:
    Sbase[c.original_bus_idx] = c.Sbus
    Vbase[c.original_bus_idx] = c.Vbus
unitary_vector = -1 + 2 * np.random.random(len(grid.buses))
vc_inputs = VoltageCollapseInput(Sbase=Sbase, Vbase=Vbase, Starget=Sbase * (5 + unitary_vector))
vc = VoltageCollapse(circuit=grid, options=vc_options, inputs=vc_inputs)
vc.run()

for key, value in grid.bus_dictionary.items():
    grid.bus_dictionary[key] = key.name
lis = [grid.bus_dictionary[key] for key, value in grid.bus_dictionary.items()]
print(lis)

mdl = vc.results.mdl()
index, columns, data = mdl.get_data()
indices = [lis.index('1_LOAD 1041'), lis.index('4_LOAD 1044'), lis.index('4044')]      # selecting the required buses you want to plot
sub_columns = spec
B = [[sublist[x] for x in indices] for sublist in data]
df2 = pd.DataFrame(data=B, index=index, columns=sub_columns)
df2.plot(ax=ax, ls="--")
plt.show()
'''
#-----------------------------------------NetworkX grid visualization after --------------------------------------------
'''
g1 = grid.build_multi_graph()
print(nx.info(g1))
save_graph(g1,"nordic_32_after_outage.pdf")
'''

