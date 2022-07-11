import scope
import rawdata as l0
import time
from transitions import Machine


class Event(l0.State):
    BUTTON_HOLD_THRESHOLD = 0.3
    transitions = [
        # state none
        {"trigger": "l_rising_edge", "source": "none", "dest": "left_button_click"},
        {
            "trigger": "l_falling_edge",
            "source": "none",
            "dest": "none",
            "before": "set_event",
        },
        {
            "trigger": "stil",
            "source": "none",
            "dest": "none",
            "before": "set_event",
        },
        # state left_button_click
        {
            "trigger": "l_rising_edge",
            "source": "left_button_click",
            "dest": "left_button_double_click",
        },
        {
            "trigger": "l_falling_edge",
            "source": "left_button_click",
            "dest": "left_button_click",
        },
        {
            "trigger": "stil",
            "source": "left_button_click",
            "dest": "left_button_hold",
            "conditions": "is_hold",
            "after": "set_event",
        },
        {
            "trigger": "stil",
            "source": "left_button_click",
            "dest": "none",
            "conditions": "is_released",
            "before": "set_event",
        },
        # state left_button_hold
        {
            "trigger": "l_falling_edge",
            "source": "left_button_hold",
            "dest": "none",
            "after": "set_event",
        },
        {
            "trigger": "stil",
            "source": "left_button_hold",
            "dest": "left_button_hold",
            "conditions": "is_hold",
        },
        # state left_button_double_click
        {
            "trigger": "l_falling_edge",
            "source": "left_button_double_click",
            "dest": "none",
            "before": "set_event",
        },
        {
            "trigger": "stil",
            "source": "left_button_double_click",
            "dest": "none",
            "after": "set_event",
        },
    ]

    event_dict = {
        "none": 0,
        "left_button_click": 1,
        "right_button_click": 2,
        "left_button_hold": 3,
        "right_button_hold": 4,
        "left_button_double_click": 5,
        "right_button_double_click": 6,
        "all_button_click": 7,
        "all_button_hold": 8,
        "all_button_double_click": 9,
        "push_double": 10,
        "push_hold": 11,
    }

    event_list = [
        "none",
        "left_button_click",
        "right_button_click",
        "left_button_hold",
        "right_button_hold",
        "left_button_double_click",
        "right_button_double_click",
        "all_button_click",
        "all_button_hold",
        "all_button_double_click",
        "push_double",
        "push_hold",
    ]

    def __init__(self):
        super().__init__()
        self.l_button_hold_time = 0
        self.r_button_hold_time = 0
        self.t_diff = 0
        self.event = 0
        self.machine = Machine(
            model=self,
            states=Event.event_list,
            transitions=Event.transitions,
            initial="none",
        )

    def __str__(self) -> str:
        return super().__str__() + ", l_button_hold_time: {}, r_button_hold_time: {}, t_diff: {}, event: {}".format(
            self.l_button_hold_time,
            self.r_button_hold_time,
            self.t_diff,
            self.event,
        )

    def __update_state_machine(self) -> int:
        pass

    @property
    def is_hold(self) -> bool:
        return (
            self.l_button_pressed == 1
            and self.l_button_hold_time > Event.BUTTON_HOLD_THRESHOLD
        )

    @property
    def is_released(self) -> bool:
        return (
            self.l_button_pressed == 0
            and self.l_button_hold_time > Event.BUTTON_HOLD_THRESHOLD
        )

    def set_event(self) -> None:
        self.event = self.event_dict[self.state]

    def update(self):
        # update time calculation
        current_time = time.perf_counter()
        self.t_diff = current_time - self.t
        if self.l_button_pressed != self.raw.buttons[0]:
            self.l_button_hold_time = 0
        else:
            self.l_button_hold_time += self.t_diff
        if self.r_button_pressed != self.raw.buttons[1]:
            self.r_button_hold_time = 0
        else:
            self.r_button_hold_time += self.t_diff

        # protect none state
        if self.state == "none":
            self.event = 0
        # update state event
        if self.l_button_pressed == 0 and self.raw.buttons[0] == 1:
            self.l_rising_edge()
        elif self.l_button_pressed == 1 and self.raw.buttons[0] == 0:
            self.l_falling_edge()
        elif self.l_button_hold_time > Event.BUTTON_HOLD_THRESHOLD:
            self.stil()
        
        super().update()


# output data to vofa as debuger
@scope.send_to_vofa
def debug_l1(event: Event):
    # convert to csv string
    MESSAGE = ",".join(
        map(
            str,
            (
                event.t,
                event.pos_diff[0],
                event.pos_diff[1],
                event.pos_diff[2],
                event.rot_diff[0],
                event.rot_diff[1],
                event.rot_diff[2],
                event.l_button_pressed,
                event.r_button_pressed,
                event.event,
                event.t_diff,
                event.l_button_hold_time,
                event.r_button_hold_time,
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE


if __name__ == "__main__":
    event = Event()
    while True:
        event.update_raw_data()
        event.update()
        print(event)
        debug_l1(event)
        time.sleep(0.01)
