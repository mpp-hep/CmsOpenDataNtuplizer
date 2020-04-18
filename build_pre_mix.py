import numpy as np
import h5py
import sklearn

base_dir = '/eos/home-o/oknapp/opendata_v2/'
output_file = '/eos/home-o/oknapp/opendata_v2/b_mix.hdf5'

# base_dir = '/home/oliverkn/pro/opendata_v2/'
# output_file = '/home/oliverkn/pro/opendata_v2/b_mix.hdf5'

data_files = [base_dir + '7719/data_pre.hdf5',  # DY1
              base_dir + '7721/data_pre.hdf5',  # DY2
              base_dir + '7722/data_pre.hdf5',  # DY3
              base_dir + '7723/data_pre.hdf5',  # DY4
              base_dir + '9863/data_pre.hdf5',  # W1
              base_dir + '9864/data_pre.hdf5',  # W2
              base_dir + '9865/data_pre.hdf5']  # W3

xsec = np.array([561, 181, 51.1, 15, 4480, 1435, 304.2])
K = np.array([1.23, 1.23, 1.23, 1.23, 1.23, 1.23, 1.23])

# load data and compute target fractions
x_list = []
fractions = []
for i, data_file in enumerate(data_files):
    hdf5_file = h5py.File(data_file, "r")
    x = hdf5_file['data']
    x_list.append(x)

    N_tot = hdf5_file['n_tot'][()]
    N_tot_target = K[i] * xsec[i]
    weight = N_tot_target / N_tot

    N_pre = x.shape[0]
    N_pre_target = weight * N_pre

    fractions.append(N_pre_target)

fractions = np.array(fractions)
fractions = fractions / np.sum(fractions)

print(fractions)

##
max_length = -1

# computing N s.t. fraction is possible
N = [data.shape[0] / f for data, f in zip(x_list, fractions)]
i_min = np.argmin(N)
print('limiting (%d): %s' % (N[i_min], data_files[i_min]))
N = N[i_min]
N = int(N)
if max_length > 0 and N > max_length:
    N = max_length
print('N = ' + str(N))

# taking random subsets and meeting fractions
for i in range(len(x_list)):
    N_i = int(fractions[i] * N)

    print('loading %s of %s' % (N_i, data_files[i]))
    idx = np.arange(0, x_list[i].shape[0])
    idx = np.random.choice(idx, N_i, replace=False)
    x_list[i] = x_list[i][()][idx]

for i in range(len(x_list)):
    print('%s: %s (%s)' % (data_files[i], x_list[i].shape, x_list[i].shape[0] / float(N)))

print('concatenating...')
data_fused = np.concatenate(x_list, axis=0)
print('concatenation finished. shape: ' + str(data_fused.shape))

print('shuffling...')
data_fused = sklearn.utils.shuffle(data_fused)

print('saving to: ' + output_file)
hdf5_file = h5py.File(output_file, "w")
hdf5_file.create_dataset('data', data=data_fused, compression='gzip')
hdf5_file.close()

print('finished')
