import spikeinterface.full as si
import spikeinterface.sorters as ss
from spikeinterface.exporters import export_to_phy

""" Spike sorting"""

recording_cmr = si.load_extractor("./data/")

other_params_SC = ss.get_default_params('spykingcircus')
other_params_SC['detect_sign'] = -1
other_params_SC['adjacency_radius'] = 100
other_params_SC['detect_threshold'] = 6
other_params_SC['template_width_ms'] = 3
other_params_SC['filter'] = False
other_params_SC['merge_spikes'] = True
other_params_SC['auto_merge'] = 0.75
other_params_SC['num_workers'] = None
other_params_SC['whitening_max_elts'] = 1000
other_params_SC['clustering_max_elts'] = 10000

sorting_SC = ss.run_spykingcircus(recording=recording_cmr, 
                                  output_folder="spykingcircus_output", 
                                  **other_params_SC)
print(sorting_SC)

we_SC = si.WaveformExtractor.create(recording_cmr, 
                                    sorting_SC, 'waveforms_sc', 
                                    remove_if_exists=True)

we_SC.set_params(ms_before=3., 
                 ms_after=4., 
                 max_spikes_per_unit=500)

we_SC.run_extract_waveforms(n_jobs=1, chunk_size=30000)
print(we_SC)

unit_id0_SC = sorting_SC.unit_ids[0]

wavefroms_SC = we_SC.get_waveforms(unit_id0_SC)
print(wavefroms_SC.shape)

template_SC = we_SC.get_template(unit_id0_SC)
print(template_SC.shape)

# Exports to Phy
export_to_phy(we_SC, './phy_folder_for_SC', remove_if_exists=True,
              compute_pc_features=False, compute_amplitudes=True)