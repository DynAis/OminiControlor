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
    }

    # set 1 and 0 just in order to debug in vofa
    event_state_dict = {
        "left_button_click": 0,
        "right_button_click": 0,
        "left_button_hold": 0,
        "right_button_hold": 0,
        "left_button_double_click": 0,
        "right_button_double_click": 0,
        "all_button_click": 0,
        "all_button_hold": 0,
        "all_button_double_click": 0,
        "push_double": 0,
    }

    is_toggle_dict = {
        "left_button_click": False,
        "right_button_click": False,
        # "left_button_hold": False,
        # "right_button_hold": False,
        "left_button_double_click": False,
        "right_button_double_click": False,
        "all_button_click": False,
        # "all_button_hold": False,
        "all_button_double_click": False,
        "push_double": False,
    }

    class Button:
        BUTTON_HOLD_THRESHOLD = 0.3
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

        def is_clicked(self) -> bool:
            return self.button_event == self.event_dict["button_click"]

        def is_double_click(self) -> bool:
            return self.button_event == self.event_dict["button_double_click"]

        def is_on_hold(self) -> bool:
            return self.button_event == self.event_dict["button_hold"]

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

        self.is_pushed = False
        self.is_pushed_double = False
        self.pushed_timer = 0

    def __str__(self) -> str:
        return super().__str__() + ", button_hold_time: {}, r_button_hold_time: {}, t_diff: {}, event: {}".format(
            self.l_button.button_hold_time,
            self.r_button.button_hold_time,
            self.t_diff,
            self.event,
        )

    def __is_idle(self) -> bool:
        return (
            self.l_button.button_event
            == self.r_button.button_event
            == self.Button.event_dict["none"]
        )

    def __is_lb_rising_edge(self) -> bool:
        return self.l_button_pressed == 0 and self.raw.buttons[0] == 1

    def __is_lb_falling_edge(self) -> bool:
        return self.l_button_pressed == 1 and self.raw.buttons[0] == 0

    def __is_rb_rising_edge(self) -> bool:
        return self.r_button_pressed == 0 and self.raw.buttons[1] == 1

    def __is_rb_falling_edge(self) -> bool:
        return self.r_button_pressed == 1 and self.raw.buttons[1] == 0

    def __set_event(self, event_name) -> None:
        self.event = Event.event_dict[event_name]

    def register_toggle(self, event_name: str):
        self.is_toggle_dict[event_name] = True

    def __is_toggle(self, event_name: str) -> bool:
        return self.is_toggle_dict[event_name]

    def get_event_state(self, event_name: str):
        return self.event_state_dict[event_name]

    def get_active_event_state_list(self) -> list:
        state_list = [self.event_dict["none"]]
        for event_name, is_active in self.event_state_dict.items():
            if is_active == 1:
                state_list.append(self.event_dict[event_name])
        return state_list

    def __reverse_state(self, event_name: str):
        self.event_state_dict[event_name] = 1 ^ self.event_state_dict[event_name]

    def __on_state(self, event_name: str):
        self.event_state_dict[event_name] = 1

    def __off_state(self, event_name: str):
        self.event_state_dict[event_name] = 0

    def __init_push_timer(self):
        self.event = Event.event_dict["push_double"]
        self.is_pushed_double = False
        self.is_pushed = False
        self.pushed_timer = 0

    def update(self):
        # update time calculation
        current_time = time.perf_counter()
        self.t_diff = current_time - self.t

        # update button event
        if self.__is_lb_rising_edge():
            self.l_button.update(self.l_button_pressed, self.t_diff, True, False)
        elif self.__is_lb_falling_edge():
            self.l_button.update(self.l_button_pressed, self.t_diff, False, True)
        else:
            self.l_button.update(self.l_button_pressed, self.t_diff, False, False)

        if self.__is_rb_rising_edge():
            self.r_button.update(self.r_button_pressed, self.t_diff, True, False)
        elif self.__is_rb_falling_edge():
            self.r_button.update(self.r_button_pressed, self.t_diff, False, True)
        else:
            self.r_button.update(self.r_button_pressed, self.t_diff, False, False)

        # update push
        if self.raw.z < -0.95 and not self.is_pushed:
            self.is_pushed = True
            self.pushed_timer = 0
        elif self.raw.z > -0.95 and self.is_pushed:
            self.pushed_timer += self.t_diff
        elif (
            self.is_pushed and self.raw.z < -0.95 and 0 < self.pushed_timer < 0.3
        ):
            self.is_pushed_double = True
        elif self.raw.z > -0.95 and not self.is_pushed:
            self.is_pushed_double = False
            self.pushed_timer = 0
        elif self.is_pushed and self.pushed_timer > 0.3:
            self.is_pushed = False
            self.is_pushed_double = False
            self.pushed_timer = 0

        # update global event
        # Event 0
        if self.__is_idle():
            self.__set_event("none")

        # Event 1
        if self.__is_toggle("left_button_click"):
            if self.l_button.is_clicked():
                self.__reverse_state("left_button_click")
                self.__set_event("left_button_click")
        else:
            if self.l_button.is_clicked():
                self.__on_state("left_button_click")
                self.__set_event("left_button_click")
            else:
                self.__off_state("left_button_click")

        # Event 2
        if self.__is_toggle("right_button_click"):
            if self.r_button.is_clicked():
                self.__reverse_state("right_button_click")
                self.__set_event("right_button_click")
        else:
            if self.r_button.is_clicked():
                self.__on_state("right_button_click")
                self.__set_event("right_button_click")
            else:
                self.__off_state("right_button_click")

        # Event 3
        if self.l_button.is_on_hold():
            self.__on_state("left_button_hold")
            self.__set_event("left_button_hold")
        else:
            self.__off_state("left_button_hold")

        # Event 4
        if self.r_button.is_on_hold():
            self.__on_state("right_button_hold")
            self.__set_event("right_button_hold")
        else:
            self.__off_state("right_button_hold")

        # Event 5
        if self.__is_toggle("left_button_double_click"):
            if self.l_button.is_double_click():
                self.__reverse_state("left_button_double_click")
                self.__set_event("left_button_double_click")
        else:
            if self.l_button.is_double_click():
                self.__on_state("left_button_double_click")
                self.__set_event("left_button_double_click")
            else:
                self.__off_state("left_button_double_click")

        # Event 6
        if self.__is_toggle("right_button_double_click"):
            if self.r_button.is_double_click():
                self.__reverse_state("right_button_double_click")
                self.__set_event("right_button_double_click")
        else:
            if self.r_button.is_double_click():
                self.__on_state("right_button_double_click")
                self.__set_event("right_button_double_click")
            else:
                self.__off_state("right_button_double_click")

        # Event 7
        if self.__is_toggle("all_button_click"):
            if self.l_button.is_clicked() and self.r_button.is_clicked():
                self.__reverse_state("all_button_click")
                self.__reverse_state("left_button_click")
                self.__reverse_state("right_button_click")
                self.__set_event("all_button_click")
        else:
            if self.l_button.is_clicked() and self.r_button.is_clicked():
                self.__on_state("all_button_click")
                self.__reverse_state("left_button_click")
                self.__reverse_state("right_button_click")
                self.__set_event("all_button_click")
            else:
                self.__off_state("all_button_click")

        # Event 8
        if self.l_button.is_on_hold() and self.r_button.is_on_hold():
            self.__on_state("all_button_hold")
            self.__off_state("left_button_hold")
            self.__off_state("right_button_hold")
            self.__set_event("all_button_hold")
        else:
            self.__off_state("all_button_hold")

        # Event 9
        if self.__is_toggle("all_button_double_click"):
            if self.l_button.is_double_click() and self.r_button.is_double_click():
                self.__reverse_state("all_button_double_click")
                self.__reverse_state("left_button_double_click")
                self.__reverse_state("right_button_double_click")
                self.__set_event("all_button_double_click")
        else:
            if self.l_button.is_double_click() and self.r_button.is_double_click():
                self.__on_state("all_button_double_click")
                self.__reverse_state("left_button_double_click")
                self.__reverse_state("right_button_double_click")
                self.__set_event("all_button_double_click")
            else:
                self.__off_state("all_button_double_click")

        # Event 10
        if self.__is_toggle("push_double"):
            if self.is_pushed_double:
                self.__reverse_state("push_double")
                self.__init_push_timer()
        else:
            if self.is_pushed_double:
                self.__on_state("push_double")
                self.__init_push_timer()
            else:
                self.__off_state("push_double")

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
                event.get_event_state("left_button_click"),
                event.get_event_state("right_button_click"),
                event.get_event_state("left_button_hold"),
                event.get_event_state("right_button_hold"),
                event.get_event_state("left_button_double_click"),
                event.get_event_state("right_button_double_click"),
                event.get_event_state("all_button_click"),
                event.get_event_state("all_button_hold"),
                event.get_event_state("all_button_double_click"),
                event.get_event_state("push_double"),
            ),
        )
    )
    MESSAGE = MESSAGE + "\n"
    return MESSAGE


if __name__ == "__main__":
    event = Event()
    event.register_toggle("left_button_click")
    event.register_toggle("right_button_click")
    event.register_toggle("left_button_double_click")
    event.register_toggle("right_button_double_click")
    event.register_toggle("all_button_click")
    event.register_toggle("all_button_double_click")
    event.register_toggle("push_double")
    while True:
        event.update_raw_data()
        event.update()
        info_str = ""
        for key, value in event.event_state_dict.items():
            info_str += key + ":" + str(value) + "   "
        print(info_str)
        debug_l1(event)
        time.sleep(0.01)
