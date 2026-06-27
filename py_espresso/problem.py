from __future__ import annotations

from dataclasses import dataclass, field

from py_espresso.cube import Cube


@dataclass(frozen=True, slots=True)
class BooleanProblem:
    n: int
    on: frozenset[int] = field(default_factory=frozenset)
    dc: frozenset[int] = field(default_factory=frozenset)

    def __init__(
        self,
        n: int,
        on: set[int] | frozenset[int],
        dc: set[int] | frozenset[int] | None = None,
    ) -> None:
        if n <= 0:
            raise ValueError("n must be positive")

        dc_set = frozenset() if dc is None else frozenset(dc)
        on_set = frozenset(on)

        full_size = 1 << n

        for name, points in {"on": on_set, "dc": dc_set}.items():
            for point in points:
                if point < 0 or point >= full_size:
                    raise ValueError(
                        f"{name} contains point {point}, "
                        f"which does not fit into n={n}"
                    )

        overlap = on_set & dc_set
        if overlap:
            raise ValueError(f"on and dc overlap: {sorted(overlap)}")

        object.__setattr__(self, "n", n)
        object.__setattr__(self, "on", on_set)
        object.__setattr__(self, "dc", dc_set)

    @property
    def all_points(self) -> range:
        return range(1 << self.n)

    @property
    def off(self) -> frozenset[int]:
        return frozenset(
            p for p in self.all_points
            if p not in self.on and p not in self.dc
        )

    def status(self, point: int) -> str:
        self._check_point(point)

        if point in self.on:
            return "ON"

        if point in self.dc:
            return "DC"

        return "OFF"

    def cube_points(self, cube: Cube) -> frozenset[int]:
        self._check_cube(cube)

        return frozenset(
            p for p in self.all_points
            if cube.covers_point(p)
        )

    def on_covered_by(self, cube: Cube) -> frozenset[int]:
        self._check_cube(cube)

        return frozenset(
            p for p in self.on
            if cube.covers_point(p)
        )

    def dc_covered_by(self, cube: Cube) -> frozenset[int]:
        self._check_cube(cube)

        return frozenset(
            p for p in self.dc
            if cube.covers_point(p)
        )

    def off_covered_by(self, cube: Cube) -> frozenset[int]:
        self._check_cube(cube)

        return frozenset(
            p for p in self.off
            if cube.covers_point(p)
        )

    def cube_is_valid(self, cube: Cube) -> bool:
        self._check_cube(cube)

        return len(self.off_covered_by(cube)) == 0

    def _check_point(self, point: int) -> None:
        if point < 0 or point >= (1 << self.n):
            raise ValueError(
                f"point {point} does not fit into n={self.n}"
            )

    def _check_cube(self, cube: Cube) -> None:
        if cube.n != self.n:
            raise ValueError(
                f"cube has n={cube.n}, but problem has n={self.n}"
            )
