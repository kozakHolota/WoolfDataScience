from pathlib import Path
from timeit import timeit

from home_works.algorithms_data_structures.homework_4.util import kmp_search, boyer_moore_search, rabin_karp_search, \
    ResultSet

publication1 = Path("publication1.txt").read_text()
publication2 = Path("publication2.txt").read_text()

if __name__ == "__main__":
    word_at_begin_kmp_publication1 = timeit(lambda: kmp_search(publication1, "вален"))
    word_at_begin_boyer_moore_publication1 = timeit(lambda: boyer_moore_search(publication1, "вален"))
    word_at_begin_rabin_karp_publication1 = timeit(lambda: rabin_karp_search(publication1, "вален"))

    word_at_begin_kmp_publication2 = timeit(lambda: kmp_search(publication2, "для"))
    word_at_begin_boyer_moore_publication2 = timeit(lambda: boyer_moore_search(publication2, "для"))
    word_at_begin_rabin_karp_publication2 = timeit(lambda: rabin_karp_search(publication2, "для"))

    word_at_middle_kmp_publication1 = timeit(lambda: kmp_search(publication1, "binarySearch"))
    word_at_middle_boyer_moore_publication1 = timeit(lambda: boyer_moore_search(publication1, "binarySearch"))
    word_at_middle_rabin_karp_publication1 = timeit(lambda: rabin_karp_search(publication1, "binarySearch"))

    word_at_middle_kmp_publication2 = timeit(lambda: kmp_search(publication2, "розгалудже"))
    word_at_middle_boyer_moore_publication2 = timeit(lambda: boyer_moore_search(publication2, "розгалудже"))
    word_at_middle_rabin_karp_publication2 = timeit(lambda: rabin_karp_search(publication2, "розгалудже"))

    word_at_end_kmp_publication1 = timeit(lambda: kmp_search(publication1, "Distance learning"))
    word_at_end_boyer_moore_publication1 = timeit(lambda: boyer_moore_search(publication1, "Distance learning"))
    word_at_end_rabin_karp_publication1 = timeit(lambda: rabin_karp_search(publication1, "Distance learning"))

    word_at_end_kmp_publication2 = timeit(lambda: kmp_search(publication2, "Minato"))
    word_at_end_boyer_moore_publication2 = timeit(lambda: boyer_moore_search(publication2, "Minato"))
    word_at_end_rabin_karp_publication2 = timeit(lambda: rabin_karp_search(publication2, "Minato"))

    result_set = ResultSet(
        word_at_begin_kmp_publication1,
        word_at_begin_kmp_publication2,
        word_at_begin_boyer_moore_publication1,
        word_at_begin_boyer_moore_publication2,
        word_at_begin_rabin_karp_publication1,
        word_at_begin_rabin_karp_publication2,
        word_at_middle_kmp_publication1,
        word_at_middle_kmp_publication2,
        word_at_middle_boyer_moore_publication1,
        word_at_middle_boyer_moore_publication2,
        word_at_middle_rabin_karp_publication1,
        word_at_middle_rabin_karp_publication2,
        word_at_end_kmp_publication1,
        word_at_end_kmp_publication2,
        word_at_end_boyer_moore_publication1,
        word_at_end_boyer_moore_publication2,
        word_at_end_rabin_karp_publication1,
        word_at_end_rabin_karp_publication2,
    )


    result_set.print_results()
    result_set.draw_search_results_graph()
    result_set.draw_search_results_grow_speed()
    result_set.to_csv_file()