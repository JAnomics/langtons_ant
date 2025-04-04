from dataclasses import dataclass
import mediapy as media
import numpy as np


@dataclass
class Ant:
    pos: np.ndarray
    dir: np.ndarray
    rules: str

    def move(self, world_size: int):
        self.pos += self.dir
        self.pos %= world_size

    def rotate(self, clockwise: bool):
        if clockwise:
            self.dir = np.array([-self.dir[1], self.dir[0]])
        else:
            self.dir = np.array([self.dir[1], -self.dir[0]])

    def update(self, ground):
        match self.rules[int(ground)]:
            case "R":
                self.rotate(clockwise=True)
            case "L":
                self.rotate(clockwise=False)


GRID_SIZE = 400
SHOW_SIZE = 800
STEPS = 5_000_000
RULE_SET = "LLRR" * 20

num_states = len(RULE_SET)
scale = SHOW_SIZE // GRID_SIZE
assert int(scale) == scale, "SHOW_SIZE must be a whole number multiple of GRID_SIZE"

ants = [
    Ant(pos=np.array([GRID_SIZE // 2, GRID_SIZE // 2]), dir=np.array([0, -1]), rules=RULE_SET),
]
frame = np.ones(shape=(GRID_SIZE, GRID_SIZE))

with media.VideoWriter("../../out/multi_state.mp4", shape=(SHOW_SIZE, SHOW_SIZE), fps=30) as vid:
    for step in range(1, STEPS):
        this_frame = frame.copy()
        for ant in ants:
            # rotate (black clockwise, white anticlockwise)
            ant.update(frame[*ant.pos])
            # update state
            this_frame[*ant.pos] += 1
            this_frame[*ant.pos] %= num_states
            # move
            ant.move(GRID_SIZE)
        frame = this_frame
        if step % 5000 == 0:
            show_frame = np.kron(frame, np.ones((scale, scale)))
            show_frame = ((show_frame / num_states) * 255).astype(np.uint8)
            vid.add_image(show_frame)
