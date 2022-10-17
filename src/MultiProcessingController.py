from multiprocessing import Process


def spawn_new_process(func_name, args):
    process = Process(target=func_name, args=args)
    # run the process
    process.start()
    # wait for the process to finish
    print('Waiting for the process...')
    process.join()

