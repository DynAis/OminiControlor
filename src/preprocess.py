import scope
import event as l1
import filters as f
import time


class PrePreocess(l1.Event):
    def __init__(self):
        super().__init__()
        # filter list that storage filter function handle
        self.pos_filter_list = []
        self.rot_filter_list = []
        for i in range(len(self.event_dict)):
            self.pos_filter_list.append([])
            self.rot_filter_list.append([])

    def __str__(self) -> str:
        return super().__str__()

    def add_pos_filter(self, event_number: int = 0, func_list: list = []):
        if len(func_list) > 0:
            for func in func_list:
                self.pos_filter_list[event_number].append(func)
        else:
            print("add_pos_filter: func_list is empty")

    def add_rot_filter(self, event_number: int = 0, func_list: list = []):
        if len(func_list) > 0:
            for func in func_list:
                self.rot_filter_list[event_number].append(func)
        else:
            print("add_rot_filter: func_list is empty")

    def update(self):
        super().update()
        # filter list not empty
        if len(self.pos_filter_list[self.event]) > 0:
            try:
                for func in self.pos_filter_list[self.event]:
                    self.pos_diff = func(self.pos_diff)
            except Exception as e:
                print("update: pos_filter_list error: {}".format(e))
        if len(self.rot_filter_list[self.event]) > 0:
            try:
                for func in self.rot_filter_list[self.event]:
                    self.rot_diff = func(self.rot_diff)
            except Exception as e:
                print("update: rot_filter_list error: {}".format(e))


# output data to vofa as debuger
@scope.send_to_vofa
def debug_l1(filter: PrePreocess):
    # convert to csv string
    MESSAGE = ",".join(
        map(
            str,
            (
                filter.t,
                filter.pos_diff[0],
                filter.pos_diff[1],
                filter.pos_diff[2],
                filter.rot_diff[0],
                filter.rot_diff[1],
                filter.rot_diff[2],
                filter.l_button_pressed,
                filter.r_button_pressed,
                filter.event,
                filter.t_diff,
                filter.l_button.button_hold_time,
                filter.r_button.button_hold_time,
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE


if __name__ == "__main__":
    filter = PrePreocess()
    # append filter function to filter list according to event
    filter.add_pos_filter(filter.event_dict["left_button_hold"], [f.half])
    filter.add_rot_filter(filter.event_dict["left_button_hold"], [f.half])
    while True:
        filter.update_raw_data()
        filter.update()
        print(filter)
        debug_l1(filter)
        time.sleep(0.01)
