"""
Sorting algorithm visualization generators
Contains step-by-step sorting implementations
"""

class SortingVisualizers:
    @staticmethod
    def bubble_sort_visual(sorting_array, app_instance):
        """Generator for bubble sort visualization"""
        n = len(sorting_array)
        app_instance.add_console_message("sortingapp$ visualizing...")

        for i in range(n):
            swapped = False

            for j in range(0, n-i-1):
                if not app_instance.sorting or app_instance.paused:
                    yield False

                app_instance.current_indices = [j, j+1]
                app_instance.add_console_message(f"sortingapp$ [type] took #{j} seconds")

                if sorting_array[j] > sorting_array[j+1]:
                    sorting_array[j], sorting_array[j+1] = sorting_array[j+1], sorting_array[j]
                    swapped = True

                yield True

            if not swapped:
                break

        app_instance.add_console_message("sortingapp$ cleaning up...")
        app_instance.sorted = True
        app_instance.sorting = False
        app_instance.current_indices = []
        yield False

    # Future sorting algorithms will be added here
    @staticmethod
    def quick_sort_visual(sorting_array, app_instance):
        """Placeholder for quick sort visualization"""
        pass

    @staticmethod
    def merge_sort_visual(sorting_array, app_instance):
        """Placeholder for merge sort visualization"""
        pass

    @staticmethod
    def insertion_sort_visual(sorting_array, app_instance):
        """Placeholder for insertion sort visualization"""
        pass
