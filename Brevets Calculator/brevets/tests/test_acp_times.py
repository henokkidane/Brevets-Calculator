"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""
import nose    # Testing framework
from nose.tools import assert_raises
import flask

from acp_times import close_time,open_time
from flask_brevets import insert,display
import logging
import arrow


logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_valid_max_dist():
    assert_raises(Exception,lambda:acp_times.open_time,241,200,arrow.now().format('YYYY-MM-DDTHH:mm'))
    assert_raises(Exception,lambda:acp_times.close_time,361,300,arrow.now().format('YYYY-MM-DDTHH:mm'))
    assert_raises(Exception,lambda:acp_times.open_time,481,400,arrow.now().format('YYYY-MM-DDTHH:mm'))
    assert_raises(Exception,lambda:acp_times.close_time,721,600,arrow.now().format('YYYY-MM-DDTHH:mm'))
    assert_raises(Exception,lambda:acp_times.open_time,1201,1000,arrow.now().format('YYYY-MM-DDTHH:mm'))
def test_valid_open_times():
    arr = arrow.Arrow(2022,2,7,0,0)
    assert open_time(200,1000,arr).datetime == arrow.Arrow(2022,2,7,5,53).datetime
    assert open_time(400,1000,arr).datetime == arrow.Arrow(2022,2,7,12,8).datetime
    assert open_time(800,1000,arr).datetime == arrow.Arrow(2022,2,8,1,57).datetime
def test_valid_close_times():
    arr = arrow.Arrow(2022,2,7,0,0)
    assert close_time(200,1000,arr).datetime == arrow.Arrow(2022,2,7,13,20).datetime
    assert close_time(400,1000,arr).datetime == arrow.Arrow(2022,2,8,2,40).datetime
    assert close_time(800,1000,arr).datetime == arrow.Arrow(2022,2,9,9,30).datetime
def test_validfrench_begin_close():
    arr = arrow.Arrow(2022,2,7,0,0)
    assert open_time(60,1000,arr).datetime == arrow.Arrow(2022,2,7,1,46).datetime
    assert open_time(40,1000,arr).datetime == arrow.Arrow(2022,2,7,1,11).datetime
    assert open_time(20,1000,arr).datetime == arrow.Arrow(2022,2,7,0,35).datetime
    assert close_time(60,1000,arr).datetime == arrow.Arrow(2022,2,7,4,0).datetime
    assert close_time(40,1000,arr).datetime == arrow.Arrow(2022,2,7,3,0).datetime
    assert close_time(20,1000,arr).datetime == arrow.Arrow(2022,2,7,2,0).datetime
def test_valid():
    test_valid_max_dist()
    test_valid_open_times()
    test_valid_close_times()
    test_validfrench_begin_close()
    # 400 and 200 dist exceptions
    arr = arrow.Arrow(2022,2,7,0,0)
    assert open_time(200,200,arr).datetime == arrow.Arrow(2022,2,7,5,53).datetime
    assert close_time(200,200,arr).datetime == arrow.Arrow(2022,2,7,13,30).datetime
    assert open_time(400,400,arr).datetime == arrow.Arrow(2022,2,7,12,8).datetime
    assert close_time(400,400,arr).datetime == arrow.Arrow(2022,2,8,3,0).datetime
def test_norequest():
    temp = insert(None)
    assert(temp == 403)
    
def test_sub_dis():
    temp = {"Start":"02:00","MaxDist":"200km","Checkpoints":"12"}
    insert(temp)
    d = display()
    assert(d == {"Start":'02:00',
                 "MaxDist":"200km",
                 "CheckPoints":"12"})

nose.run()