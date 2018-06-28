## task_server.py

import random, time, queue
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

## Windows
def return_task_queue():
    global task_queue
    return task_queue
 
def return_result_queue():
    global result_queue
    return result_queue
## Windows

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

if __name__=='__main__':
    QueueManager.register('get_task_queue', callable=return_task_queue)
    QueueManager.register('get_result_queue', callable=return_result_queue)
    manager = QueueManager(address=('127.0.0.1', 10086), authkey=b'ChineseMobile')
    manager.start()
    
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=30)
        print('Result: %s' % r)
    
    # 关闭:
    manager.shutdown()
    print('master exit.')