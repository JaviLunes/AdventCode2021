# coding=utf-8
"""Tools used for solving the Day 17: Trick Shot puzzle."""

# Third party imports:
import matplotlib.pyplot as plt


class Probe:
    """Highly scientific ballistic device for oceanic investigations."""
    def __init__(self, launch_speed_x: int, launch_speed_y: int):
        self.launch = launch_speed_x, launch_speed_y
        self.x, self.y, self.t = 0, 0, 0
        self.speed_x, self.speed_y = launch_speed_x, launch_speed_y
        self.trajectory = [(self.x, self.y)]
        self.succeeds = False

    def __repr__(self) -> str:
        return f"Probe({self.launch[0]}, {self.launch[1]})"

    def move_step(self):
        """Update the position and speed of the Probe after one time step."""
        self.x += self.speed_x
        self.y += self.speed_y
        if self.speed_x > 0:
            self.speed_x -= 1
        elif self.speed_x < 0:
            self.speed_x += 1
        self.speed_y -= 1
        self._register_movement()

    def _register_movement(self):
        """Add the current point to the trajectory history."""
        self.trajectory.append((self.x, self.y))
        self.t += 1

    @property
    def max_height(self) -> int:
        """Provide the maximum altitude reached by this Probe so far."""
        return max(point[1] for point in self.trajectory)

    @property
    def max_reach(self) -> int:
        """Provide the maximum horizontal distance reached by this Probe so far."""
        return max(point[0] for point in self.trajectory)


class TargetArea:
    """2D space region that a successfully launched Probe must reach at least once."""
    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int):
        self.x_range = range(min_x, max_x + 1)
        self.y_range = range(min_y, max_y + 1)

    @classmethod
    def from_description(cls, string: str) -> "TargetArea":
        """Build a TargetArea object from a properly formatted string description."""
        string = string.removeprefix("target area: x=")
        string = string.replace(", y=", "|").replace("..", "|")
        x1, x2, y1, y2 = [int(v) for v in string.split("|")]
        min_x, max_x, min_y, max_y = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        return TargetArea(min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y)

    def is_inside(self, probe: Probe) -> bool:
        """Check if a Probe object is currently within this TargetArea."""
        return probe.x in self.x_range and probe.y in self.y_range

    @property
    def plot_details(self) -> tuple[tuple[int, int], int, int]:
        """Provide the anchor point, width and height of this TargetArea."""
        xs, ys = self.x_range, self.y_range
        return (min(xs), min(ys)), max(xs) - min(xs), max(ys) - min(ys)


class ProbeLauncher:
    """Super cool artillery tool able to launch Probe objects towards a TargetArea."""
    def __init__(self, target_area: TargetArea):
        self.target = target_area
        self.min_speed_x = self._calibrate_min_range()
        self.max_speed_x = self._calibrate_max_range()
        self.min_speed_y = self._calibrate_min_height()
        self.max_speed_y = self._calibrate_max_height()

    def _calibrate_max_height(self):
        """Find the maximum vertical launch speed for reaching the TargetArea."""
        return -min(self.target.y_range) - 1  # From y=0 to target's bottom on last step.

    def _calibrate_min_height(self) -> int:
        """Find the minimum vertical launch speed for reaching the TargetArea."""
        return min(self.target.y_range)  # TargetArea's bottom reached in one step.

    def _calibrate_max_range(self) -> int:
        """Find the maximum horizontal launch speed for reaching the TargetArea."""
        return max(self.target.x_range)  # TargetArea's far border reached in one step.

    def _calibrate_min_range(self) -> int:
        """Find the minimum horizontal launch speed for reaching the TargetArea."""
        launch_x = 0
        while True:
            probe = self.launch(launch_x=launch_x, launch_y=0)
            if probe.x >= min(self.target.x_range):
                return launch_x  # TargetArea's near border reached on last step.
            launch_x += 1

    @classmethod
    def from_description(cls, target_string: str) -> "ProbeLauncher":
        """Build a ProbeLauncher object from the description string of its TargetArea."""
        target = TargetArea.from_description(string=target_string)
        return ProbeLauncher(target_area=target)

    def plot_launches(self, probes: list[Probe]):
        """Plot the TargetArea and the trajectories of the provided Probe objects."""
        # Create plot:
        fig, ax = plt.subplots()
        # Plot TargetArea:
        area = plt.Rectangle(*self.target.plot_details, facecolor="orange",
                             edgecolor="red", linestyle="-", linewidth=5)
        ax.add_patch(area)
        # Plot each Probe's trajectory:
        for probe in probes:
            x_probe, y_probe = zip(*probe.trajectory)
            probe_colour = "green" if probe.succeeds else "blue"
            ax.plot(x_probe, y_probe, color=probe_colour, marker="o", label=str(probe))
        # Set plot limits:
        min_x = min(0, min(self.target.x_range)) - 1
        min_y = min(self.target.y_range) - 1
        max_x = max(max(p.max_reach for p in probes), max(self.target.x_range)) + 1
        max_y = max(max(p.max_height for p in probes), max(self.target.y_range)) + 1
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        # Add legend:
        ax.legend()
        plt.show()

    def launch(self, launch_x: int, launch_y: int, plot: bool = False) -> "Probe":
        """Launch a new Probe and return it when it is within the stored TargetArea."""
        # We suppose that the Probe never starts within the TargetArea.
        # We also suppose that the Probe never floats back upwards after sinking.
        probe = Probe(launch_speed_x=launch_x, launch_speed_y=launch_y)
        while probe.y >= min(self.target.y_range):
            probe.move_step()
            if self.target.is_inside(probe=probe):
                probe.succeeds = True
                break
        if plot:
            self.plot_launches(probes=[probe])
        return probe

    def launch_trick_shot(self, plot: bool = False) -> "Probe":
        """Launch a new Probe following a maximum height trajectory."""
        speed_x, speed_y = self.min_speed_x, self.max_speed_y
        return self.launch(launch_x=speed_x, launch_y=speed_y, plot=plot)

    def find_valid_shots(self, plot: bool = False) -> list[Probe]:
        """Get all possible different Probes able to reach the TargetArea."""
        x_range = range(self.min_speed_x, self.max_speed_x + 1)
        y_range = range(self.min_speed_y, self.max_speed_y + 1)
        probes = [self.launch(launch_x=x, launch_y=y) for x in x_range for y in y_range]
        valid_probes = list(filter(lambda p: p.succeeds, probes))
        if plot:
            self.plot_launches(probes=valid_probes)
        return valid_probes
