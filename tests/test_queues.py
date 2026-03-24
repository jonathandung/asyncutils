from asyncutils.queues import *
def test_pwdq():
    Q = password_queue('password')
    Q.put_nowait(0, 'password')
    assert Q.get_nowait() == 0