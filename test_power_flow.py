from pathlib import Path
import networkx as nx
import matplotlib as plt
from GridCal.Engine import *
from GridCal.Engine.IO.file_handler import FileOpen
from GridCal.Engine.Simulations.PowerFlow.power_flow_worker import \
    PowerFlowOptions, ReactivePowerControlMode, SolverType
from GridCal.Engine.Simulations.PowerFlow.power_flow_driver import PowerFlowDriver
from GridCal.Engine.Simulations.ContinuationPowerFlow.voltage_collapse_driver import VoltageCollapseOptions, \
    VoltageCollapseInput, VoltageCollapse

def test_power_flow():
    fname = Path(__file__).parent.parent.parent / \
            'Grids_and_profiles' / 'grids' / 'IEEE 5 Bus.xlsx'

    print('Reading...')

    main_circuit = FileOpen(fname).open()

    options = PowerFlowOptions(SolverType.NR, verbose=False,
                               initialize_with_existing_solution=False,
                               multi_core=False, dispatch_storage=True,
                               control_q=ReactivePowerControlMode.Direct,
                               control_p=True)

    # grid.export_profiles('ppppppprrrrroooofiles.xlsx')
    # exit()
    ####################################################################################################################
    # PowerFlowDriver
    ####################################################################################################################
    print('\n\n')
    power_flow = PowerFlowDriver(main_circuit, options)
    power_flow.run()

    main_circuit.build_graph()

    print('\n\n', main_circuit.name)
    print('\t|V|:', abs(power_flow.results.voltage))
    print('\t|Sbranch|:', abs(power_flow.results.Sbranch))
    print('\t|loading|:', abs(power_flow.results.loading) * 100)
    print('\tReport')
    print(power_flow.results.get_report_dataframe())


    vc_options = VoltageCollapseOptions()
    numeric_circuit = main_circuit.compile()
    numeric_inputs = numeric_circuit.compute()
    Sbase = np.zeros(len(main_circuit.buses), dtype=complex)
    Vbase = np.zeros(len(main_circuit.buses), dtype=complex)
    for c in numeric_inputs:
        Sbase[c.original_bus_idx] = c.Sbus
        Vbase[c.original_bus_idx] = c.Vbus
    unitary_vector = -1 + 2 * np.random.random(len(main_circuit.buses))
    vc_inputs = VoltageCollapseInput(Sbase=Sbase,
                                     Vbase=Vbase,
                                     Starget=Sbase * (1 + unitary_vector))
    vc = VoltageCollapse(circuit=main_circuit, options=vc_options,
                         inputs=vc_inputs)
    vc.run()
    mdl = vc.results.mdl()
    mdl.plot()
    plt.show()

if __name__ == '__main__':
    test_power_flow()
