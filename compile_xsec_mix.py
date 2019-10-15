import numpy as np
import h5py
import sklearn

if __name__ == '__main__':
    data_files = ['/eos/home-o/oknapp/record_7719/data.hdf5',
                  '/eos/home-o/oknapp/record_7721/data.hdf5',
                  '/eos/home-o/oknapp/record_7722/data.hdf5',
                  '/eos/home-o/oknapp/record_7723/data.hdf5',
                  '/eos/home-o/oknapp/record_9863/data.hdf5',
                  '/eos/home-o/oknapp/record_9864/data.hdf5',
                  '/eos/home-o/oknapp/record_9865/data.hdf5']

    xsec = np.array([561, 181, 51.1, 15, 4480, 1435, 304.2])
    output_file = '/eos/home-o/oknapp/wjets_dyjets_mix.hdf5'

    # data_files = ['/home/oliverkn/pro/6021/data_hlf.hdf5', '/home/oliverkn/pro/9865/data_hlf.hdf5']
    # xsec = np.array([0.001, 0.002])
    # output_file = '/home/oliverkn/pro/testseetst.hdf5'

    max_length = -1

    fraction = xsec / np.sum(xsec)

    # load data
    data_list = []
    for data_file in data_files:
        print('loading ' + data_file)
        if data_file.endswith('.npy'):
            x = np.load(data_file)
        elif data_file.endswith('.hdf5'):
            hdf5_file = h5py.File(data_file, "r")
            x = hdf5_file['data']
        data_list.append(x)

    # computing N s.t. fraction is possible
    N = np.amin([data.shape[0] / f for data, f in zip(data_list, fraction)])
    N = int(N)
    if max_length > 0 and N > max_length:
        N = max_length
    print('N = ' + str(N))

    for i in range(len(data_list)):
        N_i = int(fraction[i] * N)
        print('loading %s of %s' % (N_i, data_files[i]))
        data_list[i] = data_list[i][0:N_i]

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
