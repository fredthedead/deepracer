import math
import random
import numpy
import scipy
import shapely

def reward_function(params):
    

    def all_wheels_on_track(reward,params):

        # Read input variables
        all_wheels_on_track = params['all_wheels_on_track']
        speed = params['speed']

        # Set the speed threshold based your action space
        SPEED_THRESHOLD = 1.0

        if not all_wheels_on_track:
            # Penalize if the car goes off track
            reward = 1e-3
        elif speed < SPEED_THRESHOLD:
            # Penalize if the car goes too slow
            reward = 0.5
        else:
            # High reward if the car stays on track and goes fast
            reward = 1.0

        return float(reward)


    def waypoints(reward,params):

        # Read input variables
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        heading = params['heading']

        # Calculate the direction of the center line based on the closest waypoints
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        # Convert to degree
        track_direction = math.degrees(track_direction)

        # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - heading)
        if direction_diff > 180:
            direction_diff = 360 - direction_diff

        # Penalize the reward if the difference is too large
        DIRECTION_THRESHOLD = 10.0
        if direction_diff > DIRECTION_THRESHOLD:
            reward *= 0.5

        return float(reward)

    def stay_at_center(reward,params):

        # Read input variable
        track_width = params['track_width']
        distance_from_center = params['distance_from_center']

        # Penalize if the car is too far away from the center
        marker_1 = 0.1 * track_width
        marker_2 = 0.25 * track_width
        marker_3 = 0.5 * track_width

        # Give higher reward if the car is closer to center line and vice versa
        if distance_from_center <= marker_1:
            reward *= 1.2
        elif distance_from_center <= marker_2:
            reward *= 0.8
        elif distance_from_center <= marker_3:
            reward += 0.5
        else:
            reward = 1e-3  # likely crashed/ close to off track
        return reward

            
    def steering_angle(reward,params):

        # Read input variable
        steering = abs(params['steering_angle']) # We don't care whether it is left or right steering

        # Penalize if car steer too much to prevent zigzag
        ABS_STEERING_THRESHOLD = 20.0
        if steering > ABS_STEERING_THRESHOLD:
            reward *= 0.8

        return float(reward)

    def progress(reward,params):

        # Read input variable
        steps = params['steps']
        progress = params['progress']

        # Total num of steps we want the car to finish the lap, it will vary depends on the track length
        TOTAL_NUM_STEPS = 300

        # Give additional reward if the car pass every 100 steps faster than expected
        if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
            reward += 10.0

        return float(reward)
        
    def fast_speed(reward, params):
        
	    speed=params['speed']
	    if speed < 3.5:
	        reward *= 0.90
	    elif speed >= 3.5:
	        reward *= 1.25
	    return reward

    def throttle(reward, params):
        
        speed=params['speed']
        steering=params['steering_angle']
        # Decrease throttle while steering
        if speed > 3.0 - (0.4 * abs(steering)):
            reward *= 0.8
        return reward
        
    def keep_left(reward, params):
        keep_left=params['is_left_of_center']
        if keep_left:
            reward *= 1.2
        else:
            reward *= 0.9
        return reward

    def keep_one_side(reward,params):
        is_reversed=params['is_reversed']
        keep_left=params['is_left_of_center']
        if is_reversed==True:
            if keep_left:
                reward *= 0.9
            else:
                reward *= 1.2
        else:
            if keep_left:
                reward *= 1.2
            else:
                reward *= 0.9
        return reward
            
               
    reward=0
    reward=all_wheels_on_track(reward,params)
    reward=waypoints(reward,params)
    reward=stay_at_center(reward,params)
    reward=steering_angle(reward,params)
    reward=progress(reward,params)
    reward=fast_speed(reward,params)
    reward=throttle(reward,params)
    #reward=keep_left(reward,params)
    reward=keep_one_side(reward,params)

    
    return float(reward)
