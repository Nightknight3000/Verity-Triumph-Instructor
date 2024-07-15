import io
import sys
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional

from verity_triumph import main as verity_triumph
from verity_triumph import _GEOMETRIC_BODIES_TO_SHAPES, _SIDES

_SYMBOL_MAP = {'Circle': 'c',
               'Square': 's',
               'Triangle': 't'}
_SHAPE_MAP = {v: k for k, v in _SYMBOL_MAP.items()}


def main():
    component_groups = {"init_button": {"init": {"Circle": [None, None],
                                                 "Square": [None, None],
                                                 "Triangle": [None, None]}},
                        "inside_button": {"left": {"Circle": [None, None],
                                                   "Square": [None, None],
                                                   "Triangle": [None, None]},
                                          "middle": {"Circle": [None, None],
                                                     "Square": [None, None],
                                                     "Triangle": [None, None]},
                                          "right": {"Circle": [None, None],
                                                    "Square": [None, None],
                                                    "Triangle": [None, None]}},
                        "outside_button": {"left": {"Circle": [None, None],
                                                    "Square": [None, None],
                                                    "Triangle": [None, None]},
                                           "middle": {"Circle": [None, None],
                                                      "Square": [None, None],
                                                      "Triangle": [None, None]},
                                           "right": {"Circle": [None, None],
                                                     "Square": [None, None],
                                                     "Triangle": [None, None]}},
                        "text_field": {"init": "tsc",
                                       "inside": "ts,sc,ct",
                                       "outside": "ts,sc,ct"},
                        "error_field": {"init": None,
                                        "inside": None,
                                        "outside": None},
                        "output_field": None
                        }

    root = tk.Tk()
    root.title("Verity Triumph Instructor")
    root.geometry("270x1000")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    group_starts = [0, 3, 8]
    for i, category in enumerate(component_groups["text_field"].keys()):
        tk.Label(mainframe, text=f"{category}s:").grid(column=0, row=group_starts[i], sticky=tk.W)
        error_field = tk.StringVar(value=f"error{i+1}")  # TODO: Remove inherent error msg
        tk.Label(mainframe, textvariable=error_field).grid(column=1, row=group_starts[i] + 1, sticky=tk.W)
        component_groups["error_field"][category] = error_field
        text_field = tk.StringVar(value=component_groups["text_field"][category])
        component_groups["text_field"][category] = text_field
        text_entry = ttk.Entry(mainframe, width=7, textvariable=text_field)
        text_entry.grid(column=0, row=group_starts[i] + 1, sticky=(tk.W, tk.E))
        count = 1
        for j, side in enumerate((_SIDES if category != "init" else ["init"])):
            for k, symbol in enumerate(_SYMBOL_MAP.keys()):
                count += 1
                button = tk.Button(mainframe, text=symbol)
                button.grid(column=(j if category != "init" else k),
                            row=group_starts[i]+2+(k if category != "init" else 0),
                            sticky=tk.W)
                component_groups[f"{category}_button"][side][symbol] = [button, "unselected"]
                button.config(bg="white", command=lambda b=button: select_and_execute_button(b, component_groups))

    tk.Label(mainframe).grid(columnspan=100, row=13, sticky=tk.W)
    tk.Label(mainframe).grid(columnspan=100, row=14, sticky=tk.W)
    output_field = tk.StringVar(value=f"result")  # TODO: Remove inherent output msg
    tk.Label(mainframe, textvariable=output_field, anchor='w').grid(columnspan=100, row=16, sticky=tk.W)
    component_groups["output_field"] = output_field

    run_button = tk.Button(mainframe, text="Run")
    run_button.grid(column=0, row=15, sticky=tk.W)
    run_button.config(bg="white", command=lambda b=run_button: check_and_run_calc(component_groups["text_field"],
                                                                                  component_groups["output_field"]))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
    sys.exit()


def select_and_execute_button(button: tk.Button,
                              component_groups: dict[str: Any]) -> None:
    component_key, button_group_key, button_group, button_key, text_field, error_field, output_field = (None for _ in range(7))

    class EscapeError(Exception):
        def __init__(self, elements: list[Any]):
            if all([e is not None for e in elements]):
                pass
            else:
                raise ValueError("Could not find specified component.")
    try:
        for k in component_groups.keys():
            if k.endswith("button"):
                for group_key in component_groups[k].keys():
                    for i, (group_button, _) in enumerate(component_groups[k][group_key].values()):
                        if button == group_button:
                            component_key = k
                            button_group_key = group_key
                            button_group = component_groups[k][group_key]
                            button_key = list(component_groups[k][group_key].keys())[i]
                            layer = component_key.replace('_button', '')
                            text_field = component_groups["text_field"][layer]
                            error_field = component_groups["error_field"][layer]
                            output_field = component_groups["output_field"]
                            raise EscapeError([component_key,
                                               button_group_key,
                                               button_group,
                                               button_key,
                                               text_field,
                                               error_field,
                                               output_field])
    except EscapeError:
        pass

    state = component_groups[k][group_key][button_key][1]
    b_text = button.config().get("text")[4]
    symbol = _SYMBOL_MAP[b_text] if b_text in _SYMBOL_MAP.keys() else _GEOMETRIC_BODIES_TO_SHAPES[b_text]
    if (button_group_key != "init") and (',' not in text_field.get()):
        text_field.set(text_field.get() + ',,')
    multi_input_i = list(component_groups[k].keys()).index(group_key)
    if state == "unselected":
        if text_field.get() and not any(s == "selected" for _, s in button_group.values()):
            if button_group_key == "init":
                text_field.set('')
            elif text_field.get().split(',')[multi_input_i]:
                text_field.set(','.join(['' if i == multi_input_i else string
                                         for i, string in enumerate(text_field.get().split(','))]))
        if multi_input_i is None:
            text_field.set(text_field.get() + symbol)
        else:
            text_field.set(','.join([string + symbol if i == multi_input_i else string
                                     for i, string in enumerate(text_field.get().split(','))]))
        component_groups[k][group_key][button_key][1] = "selected"
        button.config(bg="light blue")
    else:
        if multi_input_i is None:
            text_field.set(text_field.get().replace(symbol, '', 1))
        else:
            text_field.set(','.join([string.replace(symbol, '', 1) if i == multi_input_i else string
                                     for i, string in enumerate(text_field.get().split(','))]))
        component_groups[k][group_key][button_key][1] = "unselected"
        button.config(bg="white")

    num_selected = sum([s == "selected" for _, s in button_group.values()])
    if num_selected >= 2:
        for b, s in button_group.values():
            if s == "unselected":
                b.config(state="disabled")
                if button_group_key == "init":
                    text_field.set(text_field.get() + _SYMBOL_MAP[b.config().get("text")[4]])
    elif num_selected <= 1:
        for b, s in button_group.values():
            if s == "unselected":
                b.config(state="normal")


def check_and_run_calc(input_fields: dict[str, tk.StringVar], output_field: tk.StringVar):
    if len(input_fields) == 3:
        inits, inside, outside = (v.get() for v in input_fields.values())
        print(inits, inside, outside)
        if input_valid(inits, inside, outside):
            _stdout = sys.stdout
            output = io.StringIO()
            sys.stdout = output
            verity_triumph(inits=inits, inside=inside, outside=outside)
            sys.stdout = _stdout
            output_field.set(output.getvalue())
        else:
            output_field.set('')


def input_valid(inits: str, inside: str, outside: str) -> bool:
    try:
        inside_left, inside_middle, inside_right = inside.split(',')
        outside_left, outside_middle, outside_right = outside.split(',')

        # First check: inits valid?
        inits_valid = (len(inits) == 3) and (all(v in inits for v in _SYMBOL_MAP.values()))

        # Second check: total numbers in side match up each?
        total_inside = ''.join([inside_left, inside_middle, inside_right])
        numbers_match_inside = all(total_inside.count(v) == 2 for v in _SYMBOL_MAP.values()) and (len(total_inside) == 6)
        total_outside = ''.join([outside_left, outside_middle, outside_right])
        numbers_match_outside = all(total_outside.count(v) == 2 for v in _SYMBOL_MAP.values()) and (len(total_outside) == 6)
        numbers_match = numbers_match_inside and numbers_match_outside

        # Third check: inits in sides?
        inits_in_all_inside = all(inits[i] in inside.split(',')[i] for i in range(3))
        inits_in_all_outside = all(inits[i] in outside.split(',')[i] for i in range(3))
        inits_in_all = inits_in_all_inside and inits_in_all_outside

        return inits_valid and numbers_match and inits_in_all
    except:
        return False


if __name__ == "__main__":
    main()
