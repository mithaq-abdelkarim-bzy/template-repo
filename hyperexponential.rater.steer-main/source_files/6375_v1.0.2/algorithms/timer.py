from time import perf_counter

class Timer():
    def __init__(self):
        self._timers = {}

    def reset(self):
        self._timers = {}

    def print_all(self):
        for timer_name, timer in self._timers.items():
            timer_text = f"{timer_name}:   {timer['total_time']:.4f}"
            if timer["active"]:
                timer_text += " - STILL RUNNING"
            print(timer_text)

    def get_timer(self, timer_name):
        return self._timers[timer_name]["total_time"]

    def reset_timer(self, timer_name):
        self._timers[timer_name] = {"total_time": 0, "active": False}

    def start(self, timer_name):
        if timer_name not in self._timers:
            self.reset_timer(timer_name)
        if self._timers[timer_name]["active"]:
            print(f"Can't start timer '{timer_name}' as it is already running")
            return
            # raise ValueError(f"Can't start timer '{timer_name}' as it is already running")
        self._timers[timer_name]["start_time"] = perf_counter()
        self._timers[timer_name]["active"] = True

    def end(self, timer_name):
        if self._timers[timer_name]["active"]:
            timer = self._timers[timer_name]
            end_time = perf_counter()
            start_time = timer["start_time"]
            marginal_time = end_time - start_time
            timer["total_time"] += marginal_time
            timer["active"] = False
        else:
            print(f"Can't end timer '{timer_name}' as it is not running")
            return
            # raise ValueError(f"Can't end timer '{timer_name}' as it is not running")

timer = Timer()