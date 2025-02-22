import operator
from typing import Any, Dict, List

from janis_core import File, Array, Logger
from janis_core.tool.test_classes import TTestExpectedOutput, TTestPreprocessor


class Fastq(File):
    def __init__(self, optional=False):
        super().__init__(
            optional=optional, extension=".fastq", alternate_extensions={".fq"}
        )

    @staticmethod
    def name():
        return "Fastq"

    def doc(self):
        return (
            "FASTQ files are text files containing sequence data with quality score, there are different types"
            "with no standard: https://www.drive5.com/usearch/manual/fastq_files.html"
        )


class FastqGz(File):
    def __init__(self, optional=False):
        super().__init__(
            optional=optional, extension=".fastq.gz", alternate_extensions={".fq.gz"}
        )

    @staticmethod
    def name():
        return "FastqGz"

    def doc(self):
        return (
            "FastqGz files are compressed sequence data with quality score, there are different types"
            "with no standard: https://en.wikipedia.org/wiki/FASTQ_format"
        )

    @classmethod
    def basic_test(cls, tag: str, min_size: int) -> List[TTestExpectedOutput]:
        return [
            TTestExpectedOutput(
                tag=tag,
                preprocessor=TTestPreprocessor.FileSize,
                operator=operator.ge,
                expected_value=min_size,
            ),
        ]


class FastqGzPairedEnd(Array):
    def __init__(self, optional=False):
        super().__init__(FastqGz, optional=optional)

    @staticmethod
    def name():
        return "FastqGzPair"

    def id(self):
        if self.optional:
            return f"Optional<{self.name()}>"
        return self.name()

    def doc(self):
        return "Paired end FastqGz files"

    def validate_value(self, meta: Any, allow_null_if_not_optional: bool):
        super_is_valid = super().validate_value(meta, allow_null_if_not_optional)
        if not super_is_valid or meta is None:
            return super_is_valid

        return len(meta) == 2

    def invalid_value_hint(self, meta):
        prev = super().invalid_value_hint(meta)
        hints = []
        if prev:
            hints.append(prev)

        if meta is not None and len(meta) != 2:
            hints.append(f"There must be exactly 2 (found {len(meta)}) fastq files")
        return ", ".join(hints)

    @classmethod
    def basic_test(
        cls, tag: str, min_first_size: int, min_second_size: int
    ) -> List[TTestExpectedOutput]:
        return [
            TTestExpectedOutput(
                tag=tag,
                preprocessor=TTestPreprocessor.ListSize,
                operator=operator.eq,
                expected_value=2,
            ),
            TTestExpectedOutput(
                tag=tag,
                array_index=0,
                preprocessor=TTestPreprocessor.FileSize,
                operator=operator.ge,
                expected_value=min_first_size,
            ),
            TTestExpectedOutput(
                tag=tag,
                array_index=1,
                preprocessor=TTestPreprocessor.FileSize,
                operator=operator.ge,
                expected_value=min_second_size,
            ),
        ]


class FastqPairedEnd(Array):
    def __init__(self, optional=False):
        super().__init__(Fastq(optional=False), optional=optional)

    def id(self):
        if self.optional:
            return f"Optional<{self.name()}>"
        return self.name()

    @staticmethod
    def name():
        return "FastqPair"

    def doc(self):
        return "Paired end Fastq files "

    def validate_value(self, meta: Any, allow_null_if_not_optional: bool):
        if not super().validate_value(meta, allow_null_if_not_optional):
            return False
        return len(meta) == 2

    def invalid_value_hint(self, meta):
        prev = super().invalid_value_hint(meta)
        hints = []
        if prev:
            hints.append(prev)
        if len(meta) != 2:
            hints.append(f"There must be exactly 2 (found {len(meta)}) fastq files")
        return ", ".join(hints)


FastqGzPair = FastqGzPairedEnd
FastqPair = FastqPairedEnd
