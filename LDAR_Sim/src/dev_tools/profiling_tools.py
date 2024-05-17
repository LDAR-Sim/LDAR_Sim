from contextlib import contextmanager
import cProfile
import pstats


@contextmanager
def profile_function(filename: str = "Benchmarking/test_results"):
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    with open("Benchmarking/" + filename + ".txt", "w") as f:
        ps = pstats.Stats(pr, stream=f)
        ps.strip_dirs().sort_stats("cumulative").print_stats()
