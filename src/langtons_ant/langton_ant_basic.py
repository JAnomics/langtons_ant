from dataclasses import dataclass
import mediapy as media
import numpy as np


@dataclass
class Ant:
    pos: np.ndarray
    dir: np.ndarray

    def move(self, world_size: int):
        self.pos += self.dir
        self.pos %= world_size

    def rotate(self, clockwise: bool):
        if clockwise:
            self.dir = np.array([-self.dir[1], self.dir[0]])
        else:
            self.dir = np.array([self.dir[1], -self.dir[0]])


GRID_SIZE = 200
SHOW_SIZE = 200
STEPS = 40_000


ants = [
    Ant(pos=np.array([GRID_SIZE // 3, GRID_SIZE // 3]), dir=np.array([0, -1])),
    Ant(pos=np.array([int(GRID_SIZE * (2 / 3)), int(GRID_SIZE * (2 / 3))]), dir=np.array([0, 1])),
]
scale = SHOW_SIZE // GRID_SIZE
frame = np.ones(shape=(GRID_SIZE, GRID_SIZE))

with media.VideoWriter("../../out/video_test.mp4", shape=(SHOW_SIZE, SHOW_SIZE), fps=30) as vid:
    for step in range(1, STEPS):
        this_frame = frame.copy()
        for ant in ants:
            # rotate (black clockwise, white anticlockwise)
            ant.rotate(this_frame[*ant.pos] == 0)
            # flip
            this_frame[*ant.pos] = 1 - this_frame[*ant.pos]
            # move
            ant.move(GRID_SIZE)
        # update
        frame = this_frame
        if step % 100 == 0:
            show_frame = np.kron(frame, np.ones((scale, scale)))
            vid.add_image(show_frame)
