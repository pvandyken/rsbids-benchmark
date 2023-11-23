from typing import Callable, ParamSpec, Protocol, TypeVar

import bids
import pytest

from rsbids import BidsLayout
import ancpbids
from bids2table import bids2table

_T = TypeVar("_T")
_P = ParamSpec("_P")


example_subs = [
    "NDAREW937RMY",
    "NDARRU979UBW",
    "NDARXV209WYA",
    "NDARZC344VH2",
    "NDARZE389XF0",
    "NDARBH512BHA",
    "NDARGT682ZWN",
    "NDARYE221LZB",
    "NDARFJ000DCY",
    "NDARMJ849UKD",
    "NDARTA819MF0",
    "NDARJJ356DAL",
    "NDARMJ219AKU",
    "NDARBL444FBA",
    "NDARKT952ML4",
]


class Benchmark(Protocol):
    def __call__(
        self, func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> _T:
        ...


# def test_benchmark_validate(benchmark: Benchmark):
#     benchmark(BidsLayout, "data", validate=True)


@pytest.mark.indexing
def test_benchmark_rsbids_indexing(benchmark: Benchmark):
    benchmark(BidsLayout, f"data/indexing")


@pytest.mark.metadata
def test_benchmark_rsbids_indexing_metadata(benchmark: Benchmark):
    benchmark(lambda d: BidsLayout(d).index_metadata(), f"data/metadata")


@pytest.mark.indexing
def test_benchmark_ancp_indexing(benchmark: Benchmark):
    benchmark(ancpbids.load_dataset, "data/indexing")


@pytest.mark.indexing
def test_benchmark_pybids_indexing(benchmark: Benchmark):
    benchmark(
        bids.BIDSLayout,
        "data/indexing",
        indexer=bids.BIDSLayoutIndexer(index_metadata=False),
    )


@pytest.mark.metadata
def test_benchmark_pybids_indexing_metadata(benchmark: Benchmark):
    benchmark(bids.BIDSLayout, "data/metadata", validate=False)


@pytest.mark.metadata
def test_benchmark_bids2table_indexing_metadata(benchmark: Benchmark):
    benchmark(bids2table, "data/metadata")


@pytest.mark.query
def test_benchmark_rsbids_query(benchmark: Benchmark):
    layout = BidsLayout("data/query")
    benchmark(layout.get, subject="001")


@pytest.mark.query
def test_benchmark_ancp_query(benchmark: Benchmark):
    layout = ancpbids.load_dataset("data/query")
    benchmark(layout.query, subject="001")


@pytest.mark.query
def test_benchmark_pybids_query(benchmark: Benchmark):
    layout = bids.BIDSLayout(
        "data/query",
        validate=False,
        indexer=bids.BIDSLayoutIndexer(index_metadata=False),
    )
    benchmark(layout.get, subject="001")


@pytest.mark.query
def test_benchmark_bids2table_query(benchmark: Benchmark):
    layout = bids2table("data/query")
    benchmark(layout.filter, "subject", "001")


@pytest.mark.large_query
def test_benchmark_rsbids_large_query(benchmark: Benchmark):
    layout = BidsLayout("data/large_query")
    benchmark(
        layout.get,
        subject=example_subs,
        suffix="coordsystem",
        run=3,
    )


@pytest.mark.large_query
def test_benchmark_ancp_large_query(benchmark: Benchmark):
    layout = ancpbids.load_dataset("data/large_query")
    benchmark(
        layout.query,
        subject=example_subs,
        suffix="coordsystem",
        run=3,
    )


@pytest.mark.large_query
def test_benchmark_pybids_large_query(benchmark: Benchmark):
    layout = bids.BIDSLayout(
        "data/large_query",
        validate=False,
        indexer=bids.BIDSLayoutIndexer(index_metadata=False),
    )
    benchmark(
        layout.get,
        subject=example_subs,
        suffix="coordsystem",
        run=3,
    )


@pytest.mark.large_query
def test_benchmark_bids2table_large_query(benchmark: Benchmark):
    layout = bids2table("data/large_query")
    benchmark(
        layout.filter_multi,
        subject={"items": example_subs},
        suffix="coordsystem",
        run=3,
    )
