"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
import math


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

def calc(control_dist_km,max_dist,open):
    time = 0
    min_v = 15
    max_v = 34

    control_dist_km = round(control_dist_km)
    if open == 0:
        if control_dist_km >= 200:
            time+=200/34
            if (control_dist_km >= max_dist and max_dist == 200):
                return time
        else:
            time += (control_dist_km/max_v)

    #close
    if open == 1:
        if control_dist_km >= 200:

            time+=200/15
            if (control_dist_km >= max_dist and max_dist == 200):
                return time+(1/6)
        else:
            if(control_dist_km<=60):
                min_v = 20
                time += (control_dist_km/min_v)+1
            else:
                time += (control_dist_km/min_v)


    if control_dist_km >= 200:
        min_v = 15
        max_v = 32
        if open == 0:
            time += max(0,min(control_dist_km-200,200))/max_v
            if (control_dist_km >= max_dist) and max_dist == 300:
                time = 300/max_v
                return time
        else:
            time += max(0,min(control_dist_km-200,200))/min_v
            if (control_dist_km >= max_dist) and max_dist == 300:
                time = 300/min_v
                return time

    if control_dist_km >= 400:
        min_v = 15
        max_v = 30
        if open == 0:
            time += max(0,min(control_dist_km-400,200))/max_v
            if (control_dist_km >= max_dist) and max_dist == 400:
                time -= max(0,min(control_dist_km-400,200))/max_v
                return time
        else:
            time += max(0,min(control_dist_km-400,200))/min_v
            if (control_dist_km >= max_dist) and max_dist == 400:
                time -= max(0,min(control_dist_km-400,200))/min_v
                return time + 2/6

    if control_dist_km >= 600:
        min_v = 11.428
        max_v = 28
        if open == 0:
            time += max(0,min(control_dist_km-600,400))/max_v
            if (control_dist_km >= max_dist) and max_dist == 600:
                time -= max(0,min(control_dist_km-600,400))/max_v
                return time
        else:
            time += max(0,min(control_dist_km-600,400))/min_v
            if (control_dist_km >= max_dist) and max_dist == 600:
                time -= max(0,min(control_dist_km-600,400))/min_v
                return time
    if control_dist_km >= 1000:
        min_v = 13.33
        max_v = 26
        if open == 0:
            time += max(0,min(control_dist_km-1000,0))/max_v
        else:
            time += max(0,min(control_dist_km-1000,0))/min_v
    return time

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if(control_dist_km > 1.2*brevet_dist_km):
        raise Exception('control greater than max dist by more than 20%')
        return
    else:
        a = calc(control_dist_km,brevet_dist_km,0)
        m = (a%1)*60
        h = math.floor(a)
        m = round(m)
        open = brevet_start_time.shift(hours=+h,minutes=+m)
    return open


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if(control_dist_km > 1.2*brevet_dist_km):
        raise Exception('control greater than max dist by more than 20%')
        return
    else:
        a = calc(control_dist_km,brevet_dist_km,1)
        m = (a%1)*60

        h = math.floor(a)
        m = round(m)
        open = brevet_start_time.shift(hours=+h,minutes=+m)
    return open
    

