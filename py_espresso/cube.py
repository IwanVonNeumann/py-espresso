from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Cube:
    """
    Boolean cube represented by two bit masks.

    value:
        Bits assigned to fixed variables.

    care:
        Bit mask saying which variables are fixed.
        care bit = 1 means the variable is fixed.
        care bit = 0 means don't-care inside the cube, shown as '-'.

    Example for n = 5:

        pattern "00101"

        value = 0b00101
        care  = 0b11111

        pattern "--101"

        value = 0b00101
        care  = 0b00111

    Variable indexing:
        index 0 is the leftmost variable in the string representation.

        For n = 5:
            index:   0 1 2 3 4
            pattern: x x x x x

        Internally, index 0 corresponds to bit n - 1.
    """

    value: int
    care: int
    n: int

    def __post_init__(self) -> None:
        if self.n <= 0:
            raise ValueError("n must be positive")

        full_mask = (1 << self.n) - 1

        if self.value < 0:
            raise ValueError("value must be non-negative")

        if self.care < 0:
            raise ValueError("care must be non-negative")

        if self.value & ~full_mask:
            raise ValueError("value contains bits outside n variables")

        if self.care & ~full_mask:
            raise ValueError("care contains bits outside n variables")

        # Bits outside care are irrelevant. We normalize them to zero.
        normalized_value = self.value & self.care

        if normalized_value != self.value:
            object.__setattr__(self, "value", normalized_value)

    @classmethod
    def from_minterm(cls, point: int, n: int) -> Cube:
        """Create a fully specified cube from a minterm number."""
        if point < 0:
            raise ValueError("point must be non-negative")

        if point >= (1 << n):
            raise ValueError("point does not fit into n variables")

        return cls(
            value=point,
            care=(1 << n) - 1,
            n=n,
        )

    @classmethod
    def from_pattern(cls, pattern: str) -> Cube:
        """
        Create a cube from a string like '00101', '--101', or '10-0-'.

        Allowed symbols:
            '0' fixed zero
            '1' fixed one
            '-' don't-care inside cube
        """
        if not pattern:
            raise ValueError("pattern must not be empty")

        n = len(pattern)
        value = 0
        care = 0

        for i, ch in enumerate(pattern):
            bit = n - 1 - i

            if ch == "0":
                care |= 1 << bit
            elif ch == "1":
                value |= 1 << bit
                care |= 1 << bit
            elif ch == "-":
                pass
            else:
                raise ValueError(
                    "pattern may contain only '0', '1', and '-'"
                )

        return cls(value=value, care=care, n=n)

    def to_pattern(self) -> str:
        """Return string representation like '00101' or '--101'."""
        chars: list[str] = []

        for i in range(self.n):
            bit = self.n - 1 - i
            mask = 1 << bit

            if not (self.care & mask):
                chars.append("-")
            elif self.value & mask:
                chars.append("1")
            else:
                chars.append("0")

        return "".join(chars)

    def __str__(self) -> str:
        return self.to_pattern()

    def __repr__(self) -> str:
        return (
            f"Cube.from_pattern({self.to_pattern()!r})"
        )

    def expand_var(self, index: int) -> Cube:
        """
        Return a new cube where variable `index` is made don't-care.

        Example:
            Cube.from_pattern("00101").expand_var(0) -> "-0101"
            Cube.from_pattern("00101").expand_var(1) -> "0-101"
        """
        self._check_index(index)

        bit = self.n - 1 - index
        mask = 1 << bit

        return Cube(
            value=self.value & ~mask,
            care=self.care & ~mask,
            n=self.n,
        )

    def fix_var(self, index: int, bit_value: int) -> Cube:
        """
        Return a new cube where variable `index` is fixed to 0 or 1.
        """
        self._check_index(index)

        if bit_value not in (0, 1):
            raise ValueError("bit_value must be 0 or 1")

        bit = self.n - 1 - index
        mask = 1 << bit

        new_care = self.care | mask

        if bit_value == 1:
            new_value = self.value | mask
        else:
            new_value = self.value & ~mask

        return Cube(value=new_value, care=new_care, n=self.n)

    def covers_point(self, point: int) -> bool:
        """
        Check whether this cube covers a concrete minterm.

        A point is covered iff all fixed variables of the cube match.
        """
        if point < 0:
            raise ValueError("point must be non-negative")

        if point >= (1 << self.n):
            raise ValueError("point does not fit into n variables")

        return (point & self.care) == self.value

    def intersects(self, other: Cube) -> bool:
        """
        Check whether two cubes share at least one concrete point.

        Two cubes conflict only if some variable is fixed in both cubes
        and has different values.
        """
        self._check_compatible(other)

        conflict = (self.value ^ other.value) & self.care & other.care
        return conflict == 0

    def contains(self, other: Cube) -> bool:
        """
        Check whether this cube fully contains another cube.

        That is:
            every point covered by `other` is also covered by `self`.

        Example:
            '--101' contains '00101'
            '00101' does not contain '--101'
        """
        self._check_compatible(other)

        # If self fixes a variable, other must also fix it to the same value.
        required_fixed_by_self = self.care

        other_has_all_required_fixes = (
                                               other.care & required_fixed_by_self
                                       ) == required_fixed_by_self

        values_match = (
                               (other.value ^ self.value) & required_fixed_by_self
                       ) == 0

        return other_has_all_required_fixes and values_match

    def literal_count(self) -> int:
        """Number of fixed variables in the cube."""
        return self.care.bit_count()

    def dimension(self) -> int:
        """Number of free variables in the cube."""
        return self.n - self.literal_count()

    def size(self) -> int:
        """Number of concrete minterms covered by the cube."""
        return 1 << self.dimension()

    def variables(self) -> range:
        """Return range of variable indices: 0, 1, ..., n-1."""
        return range(self.n)

    def fixed_variables(self) -> list[int]:
        """Return indices of fixed variables."""
        result: list[int] = []

        for i in range(self.n):
            bit = self.n - 1 - i
            if self.care & (1 << bit):
                result.append(i)

        return result

    def free_variables(self) -> list[int]:
        """Return indices of don't-care variables inside the cube."""
        result: list[int] = []

        for i in range(self.n):
            bit = self.n - 1 - i
            if not (self.care & (1 << bit)):
                result.append(i)

        return result

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self.n:
            raise IndexError(
                f"variable index {index} out of range for n={self.n}"
            )

    def _check_compatible(self, other: Cube) -> None:
        if self.n != other.n:
            raise ValueError(
                f"cubes have different dimensions: {self.n} and {other.n}"
            )
