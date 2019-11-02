import numpy as np
import h5py
import sklearn

if __name__ == '__main__':
    base_dir = '/eos/home-o/oknapp/opendata_v2/'
    output_file = '/eos/home-o/oknapp/opendata_v2/wjets_dyjets_mix.hdf5'

    data_files = [base_dir + '7719/data.hdf5',  # DY1
                  base_dir + '7721/data.hdf5',  # DY2
                  base_dir + '7722/data.hdf5',  # DY3
                  base_dir + '7723/data.hdf5',  # DY4
                  base_dir + '9863/data.hdf5',  # W1
                  base_dir + '9864/data.hdf5',  # W2
                  base_dir + '9865/data.hdf5']  # W3

    xsec = np.array([561, 181, 51.1, 15, 4480, 1435, 304.2])
    fraction = xsec / np.sum(xsec)

    print(fraction)

    max_length = -1

    # load data
    data_list = []
    for data_file in data_files:
        if data_file.endswith('.npy'):
            x = np.load(data_file)
        elif data_file.endswith('.hdf5'):
            hdf5_file = h5py.File(data_file, "r")
            x = hdf5_file['data']
        data_list.append(x)

    # computing N s.t. fraction is possible
    N = [data.shape[0] / f for data, f in zip(data_list, fraction)]
    i_min = np.argmin(N)
    print('limiting (%d): %s' % (N[i_min], data_files[i_min]))
    N = N[i_min]
    N = int(N)
    if max_length > 0 and N > max_length:
        N = max_length
    print('N = ' + str(N))

    # taking random subsets and meeting fractions
    for i in range(len(data_list)):
        N_i = int(fraction[i] * N)

        print('loading %s of %s' % (N_i, data_files[i]))
        idx = np.arange(0, data_list[i].shape[0])
        idx = np.random.choice(idx, N_i, replace=False)
        data_list[i] = data_list[i][()][idx]

    for i in range(len(data_list)):
        print('%s: %s (%s)' % (data_files[i], data_list[i].shape, data_list[i].shape[0] / float(N)))

    print('concatenating...')
    data_fused = np.concatenate(data_list, axis=0)
    print('concatenation finished. shape: ' + str(data_fused.shape))

    print('shuffling...')
    data_fused = sklearn.utils.shuffle(data_fused)

    print('saving to: ' + output_file)
    hdf5_file = h5py.File(output_file, "w")
    hdf5_file.create_dataset('data', data=data_fused, compression='gzip')
    hdf5_file.close()

    print('finished')
