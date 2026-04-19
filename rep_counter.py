class RepCounter:
    def __init__(self, up_thresh=160, down_thresh=70):
        self.up_thresh = up_thresh
        self.down_thresh = down_thresh
        self.state = None
        self.count = 0
        self.feedback = "Get into position"

    def update(self, angle):
        if angle > self.up_thresh:
            if self.state != "up":
                self.state = "up"
                self.feedback = "Go down"

        elif angle < self.down_thresh:
            if self.state == "up":
                self.state = "down"
                self.count += 1
                self.feedback = "Go up!"

        return self.count, self.feedback

    def reset(self):
        self.state = None
        self.count = 0
        self.feedback = "Get into position"
