from apscheduler.schedulers.blocking import BlockingScheduler


# test
def observer():
    test =3
    if test < 3:
        test_()
        test += 1
    elif test == 3:
        print('changed_schedule')
        scheduler.reschedule_job('test_', trigger='interval', seconds=10)
        print('1')

def test_():
    print('run_exp')

scheduler = BlockingScheduler()
scheduler.add_job(test_, 'interval', weeks=10, id = 'test_')
scheduler.add_job(observer, 'interval', seconds=2, id = 'observer')
scheduler.start()
