def insertion_sort(arr):
    
    n = len(arr) # getting a length of a list

    for i in range(n):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr
    #demo test

if __name__ == "__main__":
     data = [23, 77, 10, 12, 50, 60, 9]
     print("Unsorted Data:", data)
     sorted_data = insertion_sort(data)
     print("Sorted Data:", sorted_data)