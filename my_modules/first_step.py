import spikeinterface.full as si
from probeinterface import Probe, ProbeGroup
from probeinterface import generate_linear_probe, generate_multi_shank
from probeinterface import combine_probes
from probeinterface.plotting import plot_probe
import numpy as np

"""Load data"""
file_path = '.datahere/continous.dat'
sampling_freq = float(25000)
channels_n = 128
data_type = int
recording = si.BinaryRecordingExtractor(file_paths=file_path,
                                        sampling_frequency=sampling_freq,
                                        num_chan=channels_n,
                                        dtype=data_type,
                                        t_starts=None,
                                        channel_ids=None,
                                        time_axis=0,
                                        tile_offset=0,
                                        gain_to_uV=0.0000001907,
                                        offset_to_uV=None,
                                        is_filtered=None)
print("The recording is: \n {}".format(recording))

"""==== ADD PROBE ===="""

probe = generate_multi_shank(num_shank=32,
                             num_columns=2,
                             num_contact_per_column=2)

# Maybe requires plot.show()?
plot_probe(probe, with_contact_id=True)

""" Attach probe to recording object"""

probe.set_device_channel_indices(np.arange(128))
recording = recording.set_probe(probe)

"""Preprocessing step"""

recording_band_filter = si.bandpass_filter(recording, freq_min=300, freq_max= 6000)
recording_cmr = si.common_reference(recording_band_filter,
                                    reference='global',
                                    operator='median')

#save to folder:
recording_cmr.save(format='binary', folder='./data/', name='recording_cmr')