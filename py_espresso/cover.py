from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from py_espresso.cube import Cube
from py_espresso.problem import BooleanProblem


@dataclass(frozen=True, slots=True)
class Cover:
    cubes: tuple[Cube, ...]

    def __init__(self, cubes: Iterable[Cube] = ()) -> None:
        object.__setattr__(self, "cubes", tuple(cubes))

    @classmethod
    def from_minterms(cls, points: Iterable[int], n: int) -> Cover:
        return cls(Cube.from_minterm(point, n=n) for point in points)

    def __len__(self) -> int:
        return len(self.cubes)

    def __iter__(self):
        return iter(self.cubes)

    def __getitem__(self, index: int) -> Cube:
        return self.cubes[index]

    def __str__(self) -> str:
        return "\n".join(cube.to_pattern() for cube in self.cubes)

    def patterns(self) -> list[str]:
        return [cube.to_pattern() for cube in self.cubes]

    def literal_count(self) -> int:
        return sum(cube.literal_count() for cube in self.cubes)

    def cube_count(self) -> int:
        return len(self.cubes)

    def cost(self) -> tuple[int, int]:
        """
        Default cost:
            1) fewer cubes
            2) fewer literals

        Smaller tuple is better.
        """
        return self.cube_count(), self.literal_count()

    def covered_on(self, problem: BooleanProblem) -> frozenset[int]:
        self._check_problem(problem)

        covered: set[int] = set()
        for cube in self.cubes:
            covered.update(problem.on_covered_by(cube))

        return frozenset(covered)

    def covered_dc(self, problem: BooleanProblem) -> frozenset[int]:
        self._check_problem(problem)

        covered: set[int] = set()
        for cube in self.cubes:
            covered.update(problem.dc_covered_by(cube))

        return frozenset(covered)

    def covered_off(self, problem: BooleanProblem) -> frozenset[int]:
        self._check_problem(problem)

        covered: set[int] = set()
        for cube in self.cubes:
            covered.update(problem.off_covered_by(cube))

        return frozenset(covered)

    def is_valid(self, problem: BooleanProblem) -> bool:
        return len(self.covered_off(problem)) == 0

    def is_complete(self, problem: BooleanProblem) -> bool:
        return self.covered_on(problem) == problem.on

    def is_solution(self, problem: BooleanProblem) -> bool:
        return self.is_valid(problem) and self.is_complete(problem)

    def add(self, cube: Cube) -> Cover:
        self._check_cube(cube)
        return Cover((*self.cubes, cube))

    def remove_at(self, index: int) -> Cover:
        cubes = list(self.cubes)
        del cubes[index]
        return Cover(cubes)

    def replace_at(self, index: int, cube: Cube) -> Cover:
        self._check_cube(cube)

        cubes = list(self.cubes)
        cubes[index] = cube
        return Cover(cubes)

    def without_duplicates(self) -> Cover:
        seen: set[Cube] = set()
        result: list[Cube] = []

        for cube in self.cubes:
            if cube not in seen:
                seen.add(cube)
                result.append(cube)

        return Cover(result)

    def _check_problem(self, problem: BooleanProblem) -> None:
        for cube in self.cubes:
            if cube.n != problem.n:
                raise ValueError(
                    f"cube has n={cube.n}, but problem has n={problem.n}"
                )

    def _check_cube(self, cube: Cube) -> None:
        if self.cubes and cube.n != self.cubes[0].n:
            raise ValueError(
                f"cube has n={cube.n}, but cover has n={self.cubes[0].n}"
            )
