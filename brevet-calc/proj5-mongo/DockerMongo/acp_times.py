"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,

           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    
    brevet_start_time = arrow.get(brevet_start_time)

    # locals
    speeds = [34, 32, 30, 28, 26]  # speeds for each range
    controls = [200, 400, 600, 1000, 1300]  # control ranges
    ranges = [200, 200, 200, 400, 300]  # length of each range
    total = 0  # init total hours
    copy = 0  # var to add each range to
    
    # all controls > brevet_dist_km = brevet_dist_km
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km
    
    for i in range(5):  # for each control range
        # keep adding ranges 
        if control_dist_km > controls[i]:
            total += ranges[i] / speeds[i]
            copy += ranges[i]
        # base case, return after
        else:
            # find overlap and divide by speed
            total += ((control_dist_km - copy) / speeds[i])
            # isolate time values
            hours = int(total)
            minutes = round((total * 60) % 60)
            seconds = round((total * 3600) % 60)
            # the following only works sometimes
            # if seconds > 50:
            #    minutes += 1
            # create ISO 8610 formal
            final = brevet_start_time.shift(hours=+hours)  # new return val (in ISO 8610 format)
            final = final.shift(minutes=+minutes)
            final = final.replace(second=0, microsecond=0)  # get rid of seconds, microseconds 
            return final.isoformat()

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    # this algo similar to my open_time() algo
  
    brevet_start_time = arrow.get(brevet_start_time)

    # brevet_start_time = brevet_start_time.isoformat()
    # loops
    limits = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}
    speeds = [15, 15, 15, 11.428, 13.333]  # min speeds for each control range
    controls = [200, 400, 600, 1000, 1300]  # control ranges
    ranges = [200, 200, 200, 400, 300]  # length of each range
    total = 0  # init total hours
    copy = 0  # var to add each range to
    
    # control must be <= 20% of total brevet
    if control_dist_km > brevet_dist_km * .2 + brevet_dist_km:
        # print("ERROR: Control more than 20% of brevet distance.")
        return -1  # might have to handle in HTML file
    
    # time limit edge cases
    if control_dist_km in limits:
        hours = limits[control_dist_km]
        final = brevet_start_time.shift(hours=+hours)
        return final.isoformat()

    # edge case for French rules
    if control_dist_km < 60:
        new = control_dist_km
        ret = (new / 20) + 1
        final = brevet_start_time
        final = final.shift(hours=+ret)
        final = final.replace(second=0, microsecond=0)
        return final.isoformat()
    
    # all controls past brevet length are equal to brevet
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km

    # main loop
    for i in range(5):  # for each control range
        # keep adding ranges 
        if control_dist_km > controls[i]:
            total += ranges[i] / speeds[i]
            copy += ranges[i]
        # base case, return after
        else:
            # find overlap and divide by speed
            total += ((control_dist_km - copy) / speeds[i])
            # isolate time values
            hours = int(total)
            minutes = round((total * 60) % 60)
            seconds = round((total * 3600) % 60)
            # the following only works sometimes
            # if seconds > 50:
            #    minutes += 1
            # create ISO 8610 formal
            final = brevet_start_time.shift(hours=+hours)  # new return val (in ISO 8610 format)
            final = final.shift(minutes=+minutes)
            final = final.replace(second=0, microsecond=0)  # get rid of seconds, microseconds 
            return final.isoformat()

