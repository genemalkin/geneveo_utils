#!/usr/bin/env python3
import argparse


# Thin lens equation: find position of an image while knowing
# the focal length (focal_length) and the input position (in_position)
def out_focus(in_position, focal_length):
    return (focal_length * in_position) / (in_position - focal_length)


# Focus in mm
focus = 4.4
# Lens diameter using F/#=1.2
diameter = 3.666

# Half of sensor's pixel size
limit = 0.00875  # mm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--focus",
        help="define focusing distance",
        required=True,
    )

    args = parser.parse_args()
    fdistance = float(args.focus)

    # Focusing done here:
    best_focus = out_focus(fdistance, focus)

    start = 200
    end = 40000
    step = 1
    # Loop from start [mm] to 40 m
    inputs = range(start, end+step, step)
    del1 = 1.0  # initialized just to avoid warnings
    for inp in inputs:
        # Position of image
        out_image = out_focus(inp, focus)

        # Z-shift between the optimal focus (as focused above) and the position of the image
        delta_f = abs(best_focus - out_image)

        # Confusion spot
        defocus = delta_f * diameter / out_image
        # print(f"Distance: {inp} mm => Defocusing: {defocus * 1000.0} micron")

        if inp == start:
            del1 = defocus - limit

        # We find 'inp' position where the size of confusion spot exceeds the limit
        # Specifically the difference "defocus-limit" changes its sign
        if inp != start:
            sign = (defocus - limit) * del1
            del1 = defocus - limit

            # Change of sign means that we have switched from below limit to above or vice versa
            if sign < 0:
                print(f"Distance: {inp} mm => Defocusing: {(defocus * 1000.0):0.2f} micron")
