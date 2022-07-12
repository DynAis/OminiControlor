import scope
import rawdata as l0
import time
from transitions import Machine


class Event(l0.State):
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

    class Button:
        BUTTON_HOLD_THRESHOLD = 0.5
        transitions = [
            # state none
            {"trigger": "rising_edge", "source": "none", "dest": "button_click"},
            {
                "trigger": "falling_edge",
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
            # state button_click
            {
                "trigger": "rising_edge",
                "source": "button_click",
                "dest": "button_double_click",
            },
            {
                "trigger": "falling_edge",
                "source": "button_click",
                "dest": "button_click",
            },
            {
                "trigger": "stil",
                "source": "button_click",
                "dest": "button_hold",
                "conditions": "is_hold",
                "after": "set_event",
            },
            {
                "trigger": "stil",
                "source": "button_click",
                "dest": "none",
                "conditions": "is_released",
                "before": "set_event",
            },
            # state button_hold
            {
                "trigger": "falling_edge",
                "source": "button_hold",
                "dest": "none",
                "after": "set_event",
            },
            {
                "trigger": "stil",
                "source": "button_hold",
                "dest": "button_hold",
                "conditions": "is_hold",
            },
            # state button_double_click
            {
                "trigger": "falling_edge",
                "source": "button_double_click",
                "dest": "none",
                "before": "set_event",
            },
            {
                "trigger": "stil",
                "source": "button_double_click",
                "dest": "none",
                "after": "set_event",
            },
        ]
        event_dict = {
            "none": 0,
            "button_click": 1,
            "button_hold": 2,
            "button_double_click": 3,
        }
        event_list = [
            "none",
            "button_click",
            "button_hold",
            "button_double_click",
        ]

        @property
        def is_hold(self) -> bool:
            return (
                self.button_pressed == 1
                and self.button_hold_time > self.BUTTON_HOLD_THRESHOLD
            )

        @property
        def is_released(self) -> bool:
            return (
                self.button_pressed == 0
                and self.button_hold_time > self.BUTTON_HOLD_THRESHOLD
            )

        def __init__(self) -> None:
            self.button_hold_time = 0
            self.t_diff = 0
            self.button_event = 0
            self.machine = Machine(
                model=self,
                states=self.event_list,
                transitions=self.transitions,
                initial="none",
            )

        def set_event(self) -> None:
            self.button_event = self.event_dict[self.state]

        def update(
            self, button_pressed, t_diff, is_rising_edge, is_falling_edge
        ) -> None:
            self.t_diff = t_diff
            self.button_pressed = button_pressed
            if is_rising_edge or is_falling_edge:
                self.button_hold_time = 0
            else:
                self.button_hold_time += self.t_diff
            # protect none state
            if self.state == "none":
                self.button_event = 0
            # update state event
            if is_rising_edge:
                self.rising_edge()
            elif is_falling_edge:
                self.falling_edge()
            elif self.button_hold_time > self.BUTTON_HOLD_THRESHOLD:
                self.stil()

    def __init__(self):
        super().__init__()
        self.event = 0
        self.t_diff = 0
        self.l_button = Event.Button()
        self.r_button = Event.Button()
        self.pushed = False
        self.pushed_twice = False
        self.pushed_timer = 0

    def __str__(self) -> str:
        return super().__str__() + ", button_hold_time: {}, r_button_hold_time: {}, t_diff: {}, event: {}".format(
            self.l_button.button_hold_time,
            self.r_button.button_hold_time,
            self.t_diff,
            self.event,
        )

    def update(self):
        # update time calculation
        current_time = time.perf_counter()
        self.t_diff = current_time - self.t

        # update button event
        if self.l_button_pressed == 0 and self.raw.buttons[0] == 1:
            self.l_button.update(self.l_button_pressed, self.t_diff, True, False)
        elif self.l_button_pressed == 1 and self.raw.buttons[0] == 0:
            self.l_button.update(self.l_button_pressed, self.t_diff, False, True)
        else:
            self.l_button.update(self.l_button_pressed, self.t_diff, False, False)

        if self.r_button_pressed == 0 and self.raw.buttons[1] == 1:
            self.r_button.update(self.r_button_pressed, self.t_diff, True, False)
        elif self.r_button_pressed == 1 and self.raw.buttons[1] == 0:
            self.r_button.update(self.r_button_pressed, self.t_diff, False, True)
        else:
            self.r_button.update(self.r_button_pressed, self.t_diff, False, False)

        # update push
        if self.pos_diff[2] < -0.95 and not self.pushed:
            self.pushed = True
            self.pushed_timer = 0
        elif self.pos_diff[2] > -0.95 and self.pushed:
            self.pushed_timer += self.t_diff
        elif self.pushed and self.pos_diff[2] < -0.95 and 0<self.pushed_timer<0.3:
            self.pushed_twice = True
        elif self.pos_diff[2] > -0.95 and not self.pushed:
            self.pushed_twice = False
            self.pushed_timer = 0
        elif self.pushed and self.pushed_timer>0.3:
            self.pushed = False
            self.pushed_twice = False
            self.pushed_timer = 0

        # update global event
        # Event 0
        if (
            self.l_button.button_event
            == self.r_button.button_event
            == self.Button.event_dict["none"]
        ):
            self.event = Event.event_dict["none"]
        # Event 1
        if self.l_button.button_event == self.Button.event_dict["button_click"]:
            self.event = Event.event_dict["left_button_click"]
        # Event 2
        if self.r_button.button_event == self.Button.event_dict["button_click"]:
            self.event = Event.event_dict["right_button_click"]
        # Event 3
        if self.l_button.button_event == self.Button.event_dict["button_hold"]:
            self.event = Event.event_dict["left_button_hold"]
        # Event 4
        if self.r_button.button_event == self.Button.event_dict["button_hold"]:
            self.event = Event.event_dict["right_button_hold"]
        # Event 5
        if self.l_button.button_event == self.Button.event_dict["button_double_click"]:
            self.event = Event.event_dict["left_button_double_click"]
        # Event 6
        if self.r_button.button_event == self.Button.event_dict["button_double_click"]:
            self.event = Event.event_dict["right_button_double_click"]
        # Event 7
        if self.l_button.button_event == self.r_button.button_event == self.Button.event_dict["button_click"]:
            self.event = Event.event_dict["all_button_click"]
        # Event 8
        if self.l_button.button_event == self.r_button.button_event == self.Button.event_dict["button_hold"]:
            self.event = Event.event_dict["all_button_hold"]
        # Event 9
        if self.l_button.button_event == self.r_button.button_event == self.Button.event_dict["button_double_click"]:
            self.event = Event.event_dict["all_button_double_click"]
        # Event 10
        if self.pushed_twice:
            self.event = Event.event_dict["push_double"]
            self.pushed_twice = False
            self.pushed = False
            self.pushed_timer = 0
        # Event 11
        # if self.pushed and self.pushed_timer > 0.3:
        #     self.event = Event.event_dict["push_hold"]

        # update properties
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
                event.l_button.button_hold_time,
                event.r_button.button_hold_time,
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
