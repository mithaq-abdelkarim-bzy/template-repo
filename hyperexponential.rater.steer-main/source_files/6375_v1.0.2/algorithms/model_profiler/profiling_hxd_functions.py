import hx
from libraries.model_profiler.algorithms.profiling import Timer

from functools import wraps

def get_complete_times(timer):
    ''' 
    Method to extract timing amounts
    Note Rating Algorithm is implied from the earliest start and end times
    This is because the overall rating algorithms cannot be captured by the decorator in the same way as the other sub functions
    '''
    times =  [ {'name':timer_name, 'time_taken': leg_times.get('end_leg',0) - leg_times['start_leg'], 'start_time': leg_times['start_leg'], 'end_time': leg_times.get('end_leg',0)} 
                for timer_name, timer in timer._timers.items()
                for leg_times in timer['leg_times']]
                # if timer_name != 'rating_algorithm']


    start_time = min(x['start_time'] for x in times)
    end_time = max(x['end_time'] for x in times)

    times_rebased =  [ {'name':t['name'],
                        'time_taken': t['time_taken'],
                        'start_time': t['start_time'] - start_time,
                        'end_time': t.get('end_time',0) - start_time, 
                        'max_time': end_time-start_time} 

                        for t in times]

    implied_rating_time = end_time - start_time

    times_rebased.append({'name':'rating_algorithm',
                            'time_taken':implied_rating_time,
                            'start_time': 0,
                            'end_time': implied_rating_time,
                            'max_time': end_time-start_time})

    ordered_tasks = sorted(times_rebased, key=lambda x: (x['start_time'], -x['end_time']))

    return ordered_tasks

def apply_filtering_by_parent_function(times, selected_segment):
    """
    Sets show field of the timed_segments list to False if it as sub-function of the selected function
    Where sub function is any function with a start and end time which is contained in the parents start and end time
    """
    # If no segment is selected
    if not selected_segment:
        for segment in times:
            segment['show'] = True and  segment['show']
        return times

    # Pruning by parent function
    selected_segment_timing = [segment for segment in times if  segment['name'] == selected_segment][0]
    start_time = selected_segment_timing['start_time']
    end_time = selected_segment_timing['end_time']

    for segment in times:
        segment['show'] = (segment['start_time'] >= start_time) and (segment['end_time'] <= end_time) and segment['show']
    
    return times

def apply_filtering_by_threshold(times, timer_threshold):
    """
    Sets show field of the timed_segments list to False if the time to execute the function exceeds some user defined amount
    if the amount is None, we treat this as a marker not to apply the threshold
    """

    # If not selected leave the filtering as is
    if not timer_threshold:
        for segment in times:
            segment['show'] = True

        return times
    
    for segment in times:
        segment['show'] = segment['time_taken'] > timer_threshold
    
    return times



def show_timer(profiling_hxd):
    """
    Show Timer Page
    """
    show_timer = (hx.meta.policy_option_id == 0)
    profiling_hxd.show = show_timer
    return show_timer



def mark_in_development_boolean(profiling_hxd):
    """
    Marks node as True when in developer mode
    """
    profiling_hxd.policy_in_dev = (hx.meta.policy_option_id == 0)



def is_contained(task, stack_top):
    return (stack_top["start_time"] <= task["start_time"] 
            and task["end_time"] <= stack_top["end_time"])

def write_function_tree_to_string_node(hxd, times):
    ordered_functions = [{"name": x['name'],
                          "start_time": x['start_time'],
                          "end_time": x['end_time'],
                          "time_taken": x['time_taken']}
                          
                         for x in times if x['show']]
    
    # Initialize the stack with a dummy range
    stack = [{"start_time": float('-inf'), "end_time": float('inf')}]

    # Initialize the string representation
    result_string = ""

    # Iterate through the ordered functions and update the stack
    for fn in ordered_functions:
        while not is_contained(fn, stack[-1]):
            stack.pop()
        
        indent_level = len(stack) - 1
        indentation = f"{chr(8206)}{'    ' * indent_level}"  # Repeat chr(8206) for each level
        result_string += f"{indentation}|-- {fn['name']} - ({fn['time_taken']:.1f}s)\n"
        stack.append(fn)
    
    hxd.function_tree = result_string



def timer_representation(hxd):
    """ 
    Timer code to extract time taken for each function and create a function call tree.
    This code is abstracted to the decorator function so the only rating code changes required for the 
    developer are the decorators.
    """

    if not show_timer(hxd.model_profiling):
        return

    times = get_complete_times(timer)
    times = apply_filtering_by_threshold(times, hxd.model_profiling.timer_threshold)
    times = apply_filtering_by_parent_function(times, hxd.model_profiling.selected_segment)
    hxd.model_profiling.timed_segments = times
    write_function_tree_to_string_node(hxd.model_profiling, times)
    mark_in_development_boolean(hxd.model_profiling)

timer = Timer()

def time_me(func):
    '''
    Decorator impplementation of timer library
    where function name is implied from the decorated function 
    
    ''' 

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Early return check
        if not (hx.meta.policy_option_id == 0):
            return func(*args, **kwargs)
        
        # Timing the decorated function
        timer_name = func.__name__  
        timer.start(timer_name)
        result = func(*args, **kwargs)
        timer.end(timer_name)

        # Post overall Rating timer printing
        if timer_name == 'rating_algorithm':
            timer_representation(*args, **kwargs)
            timer.print_all()
            timer.reset_all_timers()

        return result
    return wrapper
