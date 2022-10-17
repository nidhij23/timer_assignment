from multiprocessing import Process


def spawn_new_process(func_name, args):
    process = Process(target=func_name, args=args)
    process.start()
    print('Started a new process...')
    process.join()

