from typing import List, Dict
import time
import random

def _counting_sort_by_digit(a: List[int], exp: int, base: int = 10) -> None:
    n = len(a)
    output = [0] * n
    count = [0] * base

    for i in range(n):
        digit = (a[i]// exp) % base
        count[digit] += 1
    for d in range(1, base):
        count[d] += count[d - 1]

    for i in range(n - 1, -1, -1):
        digit = (a[i] // exp) % base
        pos = count[digit] -1
        output[pos] = a[i]
        count[digit] -= 1

    for i in range(n):
        a[i] = output[i]

def radix_sort_lsd_nonneg(a: List[int], base: int = 10) -> List[int]:
    if not a:
        return a
    
    start = time.perf_counter()

    max_val = max(a)
    exp = 1 

    while max_val // exp > 0:
        _counting_sort_by_digit(a, exp, base)
        exp *= base
    end = time.perf_counter()
    print (f"[Radix] nonneg sort in {end - start:.6f} sec (base={base})")
    return a

def radix_sort_lsd(a: List[int], base: int = 10) -> List[int]:
    if not a:
        return a
    neg = [-x for x in a if x <0]
    pos = [x for x in a if x >= 0]

    if neg:
        radix_sort_lsd_nonneg(neg, base)

    if pos: 
        radix_sort_lsd_nonneg(pos, base)

    neg_sorted = [-x for x in reversed(neg)]

    out = neg_sorted + pos
    return out

def sort_orders_by_id(orders: List[Dict], key: str = "order_id", base: int = 10) -> List[Dict]:
    if not orders:
        return orders
    keys = [o[key] for o in orders]
    indx = list(range(len(orders)))
    def stable_pass_with_companion(keys: List[int], comp: List[int], exp: int, base: int) -> None:
        n = len(keys)
        out_keys = [0] * n
        out_comp = [0] * n
        count = [0] * base

        for i in range(n):
            d = (keys[i] // exp) % base
            count[d] += 1

        for i in range(1, base):        # FIXED: use i, not d
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):  # stable
            d = (keys[i] // exp) % base
            pos = count[d] - 1
            out_keys[pos] = keys[i]
            out_comp[pos] = comp[i]
            count[d] -= 1

        for i in range(n):
            keys[i] = out_keys[i]
            comp[i] = out_comp[i]

    max_key = max(keys) if keys else 0
    exp = 1
    start = time.perf_counter()
    while max_key // exp > 0:
        stable_pass_with_companion(keys, indx, exp, base)
        exp *= base
    end = time.perf_counter()
    print(f"[Radix] order sort in {end - start:.6f} sec for {len(orders)} records")

    sorted_orders = [orders[i] for i in indx]
    return sorted_orders




#Demo
if __name__ == "__main__":
    data = [170, -7, 35, 802, 24, -100, 2, 66, 0, -1]
    print ("Original Data: ", data)
    sorted_data  = radix_sort_lsd(data, base=10)
    print("Sorted Data:", sorted_data)
    assert sorted_data == sorted(data)

    rng = random.Random(42)
    orders = []
    for i in range(15):
        orders.append({
            "order_id": rng.randint(10000, 10500),
            "line_item": i,
            "desc": f"Item-(i)"
        })

    for extra in [101010, 101010, 101010]:
        orders.append({
            "order_id": extra,
            "line_item": len(orders),
            "desc": "TIE"       
        })
    print("\nFirst 6 unsorted orders (id, line_item):",
          [(o["order_id"], o["line_item"]) for o in orders[:6]])
    
    sorted_orders = sort_orders_by_id(orders, key ="order_id", base =10)
    print("\nFirst 10 unsorted orders (id, line_item):", 
            [(o["order_id"], o["line_item"]) for o in orders[:10]])
    
    expected =  sorted(orders, key = lambda r: r["order_id"])
    assert [(o["order_id"], o["line_item"]) for o in sorted_orders] == \
        [(o["order_id"], o["line_item"]) for o in expected], "Stability/correctness mismatch"
    
    print("\n[CHECK] Radix record-sort matches Python's stable sort.")