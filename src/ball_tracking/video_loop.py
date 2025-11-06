import time
from pathlib import Path
from types import TracebackType

import cv2
import numpy as np


class VideoLoop:
    cap: cv2.VideoCapture
    fps: int
    frame_count: int
    width: int
    height: int
    frame_time: float
    video_resolution: tuple[int, int]
    last_frame_time: float
    is_webcam: bool

    def __init__(
        self,
        video_source: str | Path | int,
        loop: bool = False,
        skip_seconds: float = 0.0,
    ) -> None:
        self.video_source = video_source
        self.is_webcam = isinstance(video_source, int)
        self.loop = loop and not self.is_webcam  # Webcam can't loop
        self.skip_seconds = skip_seconds if not self.is_webcam else 0.0  # Webcam can't skip

    def __iter__(self) -> "VideoLoop":
        return self

    def __next__(self) -> tuple[int, np.ndarray]:
        """
        Read the next frame from the video and calculate the time to wait

        Returns
            tuple[int, np.ndarray]:
                - time to wait in milliseconds
                - frame read from the video
        """
        ret, frame = self.cap.read()
        if not ret:
            if self.loop and not self.is_webcam:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                return self.__next__()
            else:
                self.cap.release()
                raise StopIteration

        # For webcam, we don't need to control timing as strictly
        if self.is_webcam:
            return 1, frame  # Minimal wait time for webcam

        # calculate the time elapsed since the last frame
        current_frame_time = time.time()
        dt = (current_frame_time - self.last_frame_time) * 1000
        self.last_frame_time = current_frame_time

        sleep_time = max(1, int(self.frame_time - dt))

        return sleep_time, frame

    def __del__(self) -> None:
        self.cap.release()

    def __enter__(self) -> "VideoLoop":
        if self.is_webcam:
            self.cap = cv2.VideoCapture(self.video_source)
        else:
            self.cap = cv2.VideoCapture(str(self.video_source))

        if not self.cap.isOpened():
            if self.is_webcam:
                raise RuntimeError(f"Error: cannot open webcam {self.video_source}")
            else:
                raise FileNotFoundError(f"Error: cannot read video file {self.video_source}")

        # get video properties
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if self.is_webcam:
            # For webcam, we might not get a valid FPS, so set a default
            if self.fps <= 0:
                self.fps = 30  # Default to 30 FPS for webcam
            self.frame_count = -1  # Webcam has infinite frames
        else:
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # calculate utility variables
        self.frame_time = 1000 / self.fps
        self.last_frame_time = time.time()
        self.video_resolution = (self.width, self.height)

        if not self.is_webcam and self.skip_seconds > self.frame_count / self.fps:
            raise ValueError(
                f"Error: skip_seconds ({self.skip_seconds:.2f}s) is greater than the video duration ({self.frame_count / self.fps:.2f}s)"
            )

        self.reset()

        return self

    def __exit__(
        self,
        _: type[BaseException] | None,
        __: BaseException | None,
        ___: TracebackType | None,
    ) -> None:
        self.cap.release()

    def reset(self) -> None:
        if not self.is_webcam:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(self.fps * self.skip_seconds))
        self.last_frame_time = time.time()
