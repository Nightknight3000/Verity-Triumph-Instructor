import sys
from typing import Literal, Optional

_POSSIBLE_INPUTS = {"init": {"init": "Initial statue inputs: "},
                    "inside": {"left": "Left inside room wall: ",
                               "middle": "Middle inside room wall: ",
                               "right": "Right inside room wall: "},
                    "outside": {"left": "Left outside statue: ",
                                "middle": "Middle outside statue: ",
                                "right": "Right outside statue: "}
                    }
_VALID_SYMBOLS = ["s", "t", "c"]
_SIDES = ["left", "middle", "right"]
_SHAPES_TO_GEOMETRIC_BODIES = {"ss": "cube",
                               "st": "prism",
                               "sc": "cylinder",
                               "ts": "prism",
                               "tt": "pyramid",
                               "tc": "cone",
                               "cs": "cylinder",
                               "ct": "cone",
                               "cc": "sphere",
                               }
_GEOMETRIC_BODIES_TO_SHAPES = {"cube": "ss",
                               "prism": "st",
                               "cylinder": "sc",
                               "pyramid": "tt",
                               "cone": "tc",
                               "sphere": "cc",
                               }


def main():
    skip_str = "===================================================================="
    print(f"{skip_str}\n                      Verity Triumph Instructor                     \n{skip_str}")

    last_side = None
    for i in range(3):
        print(f"\nRound {i + 1}")
        print(skip_str)
        # Collect and check init inputs
        init_inputs = collect_inputs("init")
        print(skip_str)

        # Collect and check inside inputs
        inside_room_inputs = collect_inputs("inside", init_inputs)
        print(skip_str)

        # Collect and check inside inputs
        outside_room_inputs = collect_inputs("outside", init_inputs)
        print(skip_str)

        # Double-check if constitution of inputs is valid
        if room_inputs_valid(inside_room_inputs, init_inputs) and room_inputs_valid(outside_room_inputs, init_inputs):

            # Process inside
            print("\tStarting inside...")
            last_side = swap_strategy("inside", inside_room_inputs, init_inputs, last_side)
            print()

            # Process outside
            print("\tStarting outside...")
            last_side = swap_strategy("outside", outside_room_inputs, init_inputs, last_side)
            print(skip_str)
        else:
            print("Failed. Rerun script to try again.")


def collect_inputs(room: Literal["init", "inside", "outside"],
                   init_inputs: Optional[dict[str, str]] = None) -> dict[str, str]:
    room_inputs = {}
    if room != "init":
        while not (room_inputs and room_inputs_valid(room_inputs, init_inputs)):
            room_inputs = {r: await_correct_input(r, _POSSIBLE_INPUTS[room][r], init_inputs["init"][i])
                           for i, r in enumerate(list(_POSSIBLE_INPUTS[room].keys())[:-1])}
            room_inputs[list(_POSSIBLE_INPUTS[room].keys())[-1]] = get_missing_shapes(room_inputs)
            print('\t' + list(_POSSIBLE_INPUTS[room].values())[-1] +
                  f"{room_inputs[list(_POSSIBLE_INPUTS[room].keys())[-1]]}")
    else:
        room_inputs = {r: await_correct_input(r, _POSSIBLE_INPUTS[room][r]) for r in _POSSIBLE_INPUTS[room].keys()}
    return room_inputs


def room_inputs_valid(inputs: dict[str, str], init_inputs: dict[str, str]) -> bool:
    total_str = ""
    for v in inputs.values():
        total_str += v

    symbol_count_valid = [total_str.count(s) == 2 for s in _VALID_SYMBOLS]
    sides_having_init_symbol = [init_inputs["init"][i] in inputs[side] for i, side in enumerate(inputs.keys())]
    for s in _VALID_SYMBOLS:
        if total_str.count(s) != 2:
            print(f"\t{s} appeared {total_str.count(s)}-times in {list(inputs.keys())}"
                  f" instead of the expected 2-times.")
        elif not all(sides_having_init_symbol):
            print(f"\tInside/Outside rooms always contains their symbol at least once (here: not the case in "
                  f"{[side for i, side in enumerate(inputs.keys()) if not sides_having_init_symbol[i]][0]} room"
                  f").")
            break
    return all(symbol_count_valid) and all(sides_having_init_symbol)


def await_correct_input(mode: str, msg: str, init_input: Optional[str] = None) -> str:
    symbols = None
    is_valid = False
    while not is_valid:
        symbols = input('\t' + msg).lower()
        if mode == "init":
            if (len(symbols) == 3) and all([s in symbols for s in _VALID_SYMBOLS]):
                is_valid = True
            else:
                print(f"\tReceived invalid input for initialization. Retry..")
        else:
            if init_input is not None:
                if symbols in _GEOMETRIC_BODIES_TO_SHAPES.keys():
                    symbols = _GEOMETRIC_BODIES_TO_SHAPES[symbols]
                if (len(symbols) == 2) and all([s in _VALID_SYMBOLS for s in symbols]) and (init_input in symbols):
                    is_valid = True
                else:
                    if len(symbols) != 2:
                        error_msg = "Received more/less than 2 symbols or no known 3D shape."
                    elif not all([s in _VALID_SYMBOLS for s in symbols]):
                        error_msg = "Received at least one invalid symbol."
                    else:
                        error_msg = "Inside/Outside rooms always contains their symbol at least once"
                    print(f"\tReceived invalid input for {mode} ({error_msg}). Retry..")
            else:
                raise ValueError("Missing correct initial inputs.")

    if symbols is None:
        raise ValueError("Inputs are incorrect.")
    else:
        return symbols


def get_missing_shapes(inputs: dict[str, str]) -> str:
    found_shapes = ""
    for v in inputs.values():
        found_shapes += v

    missing_shapes = ""
    for s in _VALID_SYMBOLS:
        while found_shapes.count(s) < 2:
            found_shapes += s
            missing_shapes += s
    return missing_shapes


def swap_strategy(room: Literal["inside", "outside"],
                  inputs: dict[str, str],
                  init_inputs: dict[str, str],
                  last_side: Optional[str]) -> str:
    step_count = 1
    if room == "inside":
        none_pure = not any([is_pure(i) for i in inputs.values()])
        side_done = {side: False for side in inputs.keys()}
        # print(f"\t\tInits: ", init_inputs)
        # print("\t\tbefore: ", inputs)
        while not all([v for v in side_done.values()]):
            not_done_sides = [k for k in side_done.keys() if not side_done[k]]
            side = last_side if (last_side is not None) and (not side_done[last_side]) else \
                ("left" if last_side is None else not_done_sides[0])
            if not side_done[side]:
                shapes = inputs[side][:2]
                for shape in shapes:
                    shape_init_side = _SIDES[init_inputs["init"].index(shape)]
                    possible_sides = [s for s in inputs.keys() if s != side]
                    remaining_shape = shapes.replace(shape, '', 1)
                    remaining_shape_init_side = _SIDES[init_inputs["init"].index(remaining_shape)]
                    for n_side in possible_sides:
                        remaining_side = [s for s in possible_sides if s != n_side][0]
                        if (n_side != last_side) and \
                                (shape_init_side != n_side) and \
                                (remaining_shape_init_side != remaining_side):
                            inputs, last_side, step_count, _ = interact_with_statue(room, shape, n_side, inputs,
                                                                                    step_count, loc_inside=side)
                            side_done[side] = True
                            break

        if none_pure:
            for _ in range(3):
                for n_side in [s for s in _SIDES if s != last_side]:
                    n_init_side_shape = init_inputs["init"][_SIDES.index(n_side)]
                    shape = inputs[last_side][0]
                    if n_init_side_shape != shape:
                        inputs, last_side, step_count, _ = interact_with_statue(room, shape, n_side, inputs,
                                                                                step_count, loc_inside=last_side)
                        break
        # print("\t\tafter: ", inputs)
    else:
        num_pure = sum([is_pure(i) for i in inputs.values()])
        # print(f"\t\tInits: ", init_inputs)
        # print("\t\tbefore: ", inputs)
        start_side, other_side1, other_side2 = (None for _ in range(3))
        for s in inputs.keys():
            if (s != last_side) and (start_side is None) and (not is_pure(inputs[s]) if num_pure == 1 else True):
                start_side = s
            elif is_pure(inputs[s]) if num_pure == 1 else (other_side1 is None):
                other_side1 = s
            else:
                other_side2 = s
        try:
            start_shape, other_shape1, other_shape2 = (None for _ in range(3))
            for s in inputs[start_side]:
                if init_inputs["init"][_SIDES.index(start_side)] == s:
                    start_shape = s
            for s in inputs[other_side1]:
                if init_inputs["init"][_SIDES.index(other_side1)] == s:
                    other_shape1 = s
            for s in inputs[other_side2]:
                if init_inputs["init"][_SIDES.index(other_side2)] == s:
                    other_shape2 = s
        except:
            raise ValueError("Could not determine sides outside.")
        # First swap
        inputs, last_side, step_count, first_interact = interact_with_statue(room, start_shape, start_side, inputs,
                                                                             step_count)
        inputs, last_side, step_count, _ = interact_with_statue(room, other_shape1, other_side1, inputs,
                                                                step_count, outside_first_interact=first_interact)

        # Second swap
        inputs, last_side, step_count, first_interact = interact_with_statue(room, other_shape2, other_side2, inputs,
                                                                             step_count)
        if num_pure == 0:
            final_side, final_shape = (start_side, inputs[start_side][0]) \
                if is_pure(inputs[start_side]) else (other_side1, inputs[other_side1][0])
        else:
            final_side, final_shape = (other_side1, inputs[other_side1][1])
        inputs, last_side, step_count, _ = interact_with_statue(room, final_shape, final_side, inputs,
                                                                step_count, outside_first_interact=first_interact)

        # Third swap
        if num_pure == 3:
            final_side1, final_side2, final_shape1, final_shape2 = (None for _ in range(4))
            for s in inputs.keys():
                s_shape = init_inputs["init"][_SIDES.index(s)]
                if (s != last_side) and (s_shape in inputs[s]) and (final_side1 is None):
                    final_side1, final_shape1 = (s, s_shape)
            for s in inputs.keys():
                s_shape = init_inputs["init"][_SIDES.index(s)]
                if (s_shape in inputs[s]) and (final_side2 is None) and (final_side1 != s):
                    final_side2, final_shape2 = (s, s_shape)
            inputs, last_side, step_count, first_interact = interact_with_statue(room, final_shape1, final_side1,
                                                                                 inputs, step_count)
            inputs, _, _, _ = interact_with_statue(room, final_shape2, final_side2, inputs,
                                                   step_count, outside_first_interact=first_interact)
        # print("\t\tafter: ", {k: _SHAPES_TO_GEOMETRIC_BODIES[v] for k, v in inputs.items()})
    return last_side


def find_pure_one(inputs: dict[str, str]) -> str:
    for k, v in inputs.items():
        if is_pure(v):
            return k


def is_pure(double_shape: str) -> bool:
    return double_shape[0] == double_shape[1]


def interact_with_statue(room: Literal["inside", "outside"],
                         shape: str,
                         interact_side: str,
                         inputs: dict[str, str],
                         step_count: int,
                         loc_inside: Optional[str] = None,
                         outside_first_interact: Optional[tuple[str, str]] = None) -> tuple[dict[str, str],
                                                                                            str,
                                                                                            int,
                                                                                            Optional[tuple[str, str]]]:
    if room == "inside":
        print(f"\t\t{step_count}.Inside {loc_inside}: swap {shape} to {interact_side} side.")
        inputs[loc_inside] = inputs[loc_inside].replace(shape, '', 1)
        inputs[interact_side] += shape
        return inputs, interact_side, step_count + 1, None
    else:
        if outside_first_interact is not None:
            print(f"\t\t{step_count}.Outside: use {shape} on {interact_side} side.")
            first_interact_shape, first_interact_side = outside_first_interact
            inputs[interact_side] = inputs[interact_side].replace(shape, first_interact_shape, 1)
            inputs[first_interact_side] = inputs[first_interact_side].replace(first_interact_shape, shape, 1)
            return inputs, interact_side, step_count + 1, None
        else:
            print(f"\t\t{step_count}.Outside: use {shape} on {interact_side} side.")
            return inputs, interact_side, step_count + 1, (shape, interact_side)


if __name__ == "__main__":
    main()
