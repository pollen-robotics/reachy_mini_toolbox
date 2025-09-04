import threading
import time
from collections import namedtuple

from reachy_mini import ReachyMini
from reachy_mini.motion.dance import DanceMove
from reachy_mini.motion.dance.collection.dance import AVAILABLE_MOVES

from reachy_mini_toolbox.moves.recorder import record

possible_moves: list[str] = list(AVAILABLE_MOVES.keys())

Args = namedtuple(
    "Args",
    [
        "library",
        "name",
        "description",
        "freq",
        "audio_device",
        "list_audio_devices",
        "no_sound",
    ],
)

with ReachyMini() as reachy:
    for move_name in possible_moves:
        move: DanceMove = DanceMove(move_name)
        args = Args(
            library="dances",
            name=move_name,
            description=move.move_metadata["description"],
            freq=100,
            audio_device=None,
            list_audio_devices=False,
            no_sound=True,
        )
        print(f"Playing move: {move_name}: {move.move_metadata['description']}\n")
        stop = threading.Event()
        t = threading.Thread(target=record, args=(args, stop))
        t.start()
        time.sleep(1.5)
        move.play_on(reachy, repeat=1)
        stop.set()
        t.join()
