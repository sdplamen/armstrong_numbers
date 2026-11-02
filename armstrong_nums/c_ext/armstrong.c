/*
 * C engine for the Armstrong numbers calculator, loaded from Python via ctypes
 * (see armstrong_nums/c_engine.py). Uses the same algorithm as the Python engine.
 *
 * Build manually: cc -O2 -shared -fPIC -o armstrong.so armstrong.c
 */
#include <stdint.h>
#include <stddef.h>

typedef unsigned __int128 u128;

typedef struct {
    int digits;
    uint64_t low, high;
    u128 powers[10];
    int counts[10];
    uint64_t *out;
    size_t cap, found;
} search_t;

static void add_result(search_t *s, uint64_t number)
{
    if (s->found < s->cap)
        s->out[s->found] = number;
    s->found++;
}

static int digit_count(uint64_t n)
{
    int digits = 1;
    while (n >= 10) {
        n /= 10;
        digits++;
    }
    return digits;
}

/* Number of digit multisets of the given length: C(digits + 9, 9). */
static uint64_t multiset_count(int digits)
{
    uint64_t result = 1;
    for (int i = 1; i <= 9; i++)
        result = result * (digits + i) / i;
    return result;
}

static u128 digit_power_sum(uint64_t n, const u128 *powers)
{
    u128 total = 0;
    do {
        total += powers[n % 10];
        n /= 10;
    } while (n > 0);
    return total;
}

/* Is `total` in range and made of exactly the digits in s->counts? */
static void check_candidate(search_t *s, u128 total)
{
    if (total < s->low || total > s->high)
        return;

    int seen[10] = {0};
    int length = 0;
    u128 t = total;
    do {
        seen[(int) (t % 10)]++;
        length++;
        t /= 10;
    } while (t > 0);

    if (length != s->digits)
        return;
    for (int d = 0; d < 10; d++)
        if (seen[d] != s->counts[d])
            return;
    add_result(s, (uint64_t) total);
}

/* Try every way to choose how many times each digit appears. */
static void enumerate(search_t *s, int digit, int remaining, u128 total)
{
    if (digit == 9) {
        s->counts[9] = remaining;
        check_candidate(s, total + remaining * s->powers[9]);
        return;
    }
    for (int k = 0; k <= remaining; k++) {
        u128 next = total + k * s->powers[digit];
        if (next > s->high)
            break; /* later digits only make the sum bigger */
        s->counts[digit] = k;
        enumerate(s, digit + 1, remaining - k, next);
    }
}

static void sort_results(uint64_t *a, size_t n)
{
    for (size_t i = 1; i < n; i++) {
        uint64_t v = a[i];
        size_t j = i;
        while (j > 0 && a[j - 1] > v) {
            a[j] = a[j - 1];
            j--;
        }
        a[j] = v;
    }
}

static void search_digits(search_t *s)
{
    for (int d = 0; d < 10; d++) {
        u128 p = 1;
        for (int i = 0; i < s->digits; i++)
            p *= d;
        s->powers[d] = p;
    }

    /* Few candidates: checking each number directly is cheaper. */
    if (s->high - s->low < multiset_count(s->digits)) {
        for (uint64_t n = s->low;; n++) {
            if (digit_power_sum(n, s->powers) == n)
                add_result(s, n);
            if (n == s->high)
                break;
        }
        return;
    }

    size_t first = s->found;
    enumerate(s, 0, s->digits, 0);
    if (s->found <= s->cap)
        sort_results(s->out + first, s->found - first);
}

/*
 * Writes Armstrong numbers in [start, end] to `out` (at most `cap` of them)
 * and returns how many exist. Call again with a bigger buffer if the result > cap.
 */
size_t armstrong_numbers_in_range(uint64_t start, uint64_t end, uint64_t *out, size_t cap)
{
    search_t s = {0};
    s.out = out;
    s.cap = cap;

    if (start > end)
        return 0;

    uint64_t power_of_ten = 1; /* 10^(digits - 1) */
    for (int digits = 1; digits <= digit_count(end); digits++) {
        uint64_t low_bound = digits == 1 ? 0 : power_of_ten;
        uint64_t high_bound = digits == 20 ? UINT64_MAX : power_of_ten * 10 - 1;

        if (digits >= digit_count(start)) {
            s.digits = digits;
            s.low = start > low_bound ? start : low_bound;
            s.high = end < high_bound ? end : high_bound;
            search_digits(&s);
        }
        if (digits < 20)
            power_of_ten *= 10;
    }
    return s.found;
}
