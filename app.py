import random
import time

import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Interactive Algorithm Visualizer",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Interactive Algorithm Visualizer")
st.caption("DAA Mini-Project | Explore sorting and searching algorithms")

SORT_INFO = {
    "Bubble Sort": {
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "description": "Repeatedly compares adjacent elements and swaps them when they are in the wrong order."
    },
    "Selection Sort": {
        "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "description": "Finds the smallest remaining element and places it at the beginning of the unsorted section."
    },
    "Insertion Sort": {
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "description": "Builds a sorted section by inserting each new element into its correct position."
    },
    "Merge Sort": {
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)",
        "description": "Divides the array into smaller parts, sorts them, and merges the sorted parts."
    },
    "Quick Sort": {
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)", "space": "O(log n) average",
        "description": "Partitions elements around a pivot and recursively sorts the resulting sections."
    },
    "Heap Sort": {
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(1)",
        "description": "Builds a max heap and repeatedly moves the largest element to the end of the array."
    },
}


def sorting_steps(original, algorithm):
    """Return animation snapshots and operation counts for a sorting algorithm."""
    a = original.copy()
    steps = []
    comparisons = swaps = writes = 0

    def record(active=(), action="Processing"):
        steps.append({
            "array": a.copy(),
            "active": list(active),
            "comparisons": comparisons,
            "swaps": swaps,
            "writes": writes,
            "action": action,
        })

    record(action="Initial array")

    if algorithm == "Bubble Sort":
        n = len(a)
        for i in range(n):
            changed = False
            for j in range(n - i - 1):
                comparisons += 1
                record((j, j + 1), "Comparing adjacent elements")
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swaps += 1
                    writes += 2
                    changed = True
                    record((j, j + 1), "Swapping elements")
            if not changed:
                break

    elif algorithm == "Selection Sort":
        for i in range(len(a)):
            minimum = i
            for j in range(i + 1, len(a)):
                comparisons += 1
                record((minimum, j), "Finding the minimum")
                if a[j] < a[minimum]:
                    minimum = j
            if minimum != i:
                a[i], a[minimum] = a[minimum], a[i]
                swaps += 1
                writes += 2
                record((i, minimum), "Placing minimum element")

    elif algorithm == "Insertion Sort":
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                record((j, j + 1), "Comparing with the key")
                if a[j] > key:
                    a[j + 1] = a[j]
                    writes += 1
                    record((j, j + 1), "Shifting an element")
                    j -= 1
                else:
                    break
            a[j + 1] = key
            writes += 1
            record((j + 1,), "Inserting the key")

    elif algorithm == "Merge Sort":
        def merge_sort(left, right):
            nonlocal comparisons, writes
            if right - left <= 1:
                return
            mid = (left + right) // 2
            merge_sort(left, mid)
            merge_sort(mid, right)
            left_part = a[left:mid]
            right_part = a[mid:right]
            i = j = 0
            k = left
            while i < len(left_part) and j < len(right_part):
                comparisons += 1
                record((k,), "Comparing elements for merging")
                if left_part[i] <= right_part[j]:
                    a[k] = left_part[i]
                    i += 1
                else:
                    a[k] = right_part[j]
                    j += 1
                writes += 1
                record((k,), "Merging elements")
                k += 1
            while i < len(left_part):
                a[k] = left_part[i]
                i += 1
                k += 1
                writes += 1
                record((k - 1,), "Copying remaining element")
            while j < len(right_part):
                a[k] = right_part[j]
                j += 1
                k += 1
                writes += 1
                record((k - 1,), "Copying remaining element")
        merge_sort(0, len(a))

    elif algorithm == "Quick Sort":
        def quick_sort(low, high):
            nonlocal comparisons, swaps, writes
            if low >= high:
                return
            pivot = a[high]
            i = low
            for j in range(low, high):
                comparisons += 1
                record((j, high), "Comparing with pivot")
                if a[j] <= pivot:
                    if i != j:
                        a[i], a[j] = a[j], a[i]
                        swaps += 1
                        writes += 2
                        record((i, j), "Moving element before pivot")
                    i += 1
            if i != high:
                a[i], a[high] = a[high], a[i]
                swaps += 1
                writes += 2
                record((i, high), "Placing pivot")
            quick_sort(low, i - 1)
            quick_sort(i + 1, high)
        quick_sort(0, len(a) - 1)

    elif algorithm == "Heap Sort":
        n = len(a)

        def heapify(size, root):
            nonlocal comparisons, swaps, writes
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2
            if left < size:
                comparisons += 1
                record((largest, left), "Comparing heap elements")
                if a[left] > a[largest]:
                    largest = left
            if right < size:
                comparisons += 1
                record((largest, right), "Comparing heap elements")
                if a[right] > a[largest]:
                    largest = right
            if largest != root:
                a[root], a[largest] = a[largest], a[root]
                swaps += 1
                writes += 2
                record((root, largest), "Restoring max heap")
                heapify(size, largest)

        for i in range(n // 2 - 1, -1, -1):
            heapify(n, i)
        for end in range(n - 1, 0, -1):
            a[0], a[end] = a[end], a[0]
            swaps += 1
            writes += 2
            record((0, end), "Moving maximum to the end")
            heapify(end, 0)

    record(action="Sorting completed")
    return steps


def searching_steps(original, algorithm, target):
    a = original.copy()
    if algorithm == "Binary Search":
        a.sort()

    steps = []
    comparisons = 0
    found_index = -1

    def record(active=(), action="Searching"):
        steps.append({
            "array": a.copy(),
            "active": list(active),
            "comparisons": comparisons,
            "swaps": 0,
            "writes": 0,
            "action": action,
        })

    record(action="Initial array")

    if algorithm == "Linear Search":
        for i, value in enumerate(a):
            comparisons += 1
            record((i,), f"Checking index {i}")
            if value == target:
                found_index = i
                record((i,), "Target found")
                break
    else:
        low, high = 0, len(a) - 1
        while low <= high:
            mid = (low + high) // 2
            comparisons += 1
            record((mid,), f"Checking middle index {mid}")
            if a[mid] == target:
                found_index = mid
                record((mid,), "Target found")
                break
            if a[mid] < target:
                low = mid + 1
                record((mid,), "Searching the right half")
            else:
                high = mid - 1
                record((mid,), "Searching the left half")

    if found_index == -1:
        record(action="Target not found")

    return steps, found_index, a


def draw_array(step, chart_placeholder):
    values = step["array"]
    active = step["active"]
    colors = [
        "#F59E0B" if i in active else "#3B82F6"
        for i in range(len(values))
    ]

    fig = go.Figure(go.Bar(
        x=list(range(len(values))),
        y=values,
        marker_color=colors,
        text=values if len(values) <= 30 else None,
        textposition="outside",
        hovertemplate="Index: %{x}<br>Value: %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=step["action"],
        xaxis_title="Array Index",
        yaxis_title="Value",
        showlegend=False,
        height=430,
        margin=dict(l=20, r=20, t=55, b=35),
        xaxis=dict(dtick=1) if len(values) <= 30 else {},
    )
    fig.update_yaxes(rangemode="tozero")
    chart_placeholder.plotly_chart(fig, use_container_width=True)


def show_metrics(step, metric_placeholder, elapsed=None):
    with metric_placeholder.container():
        cols = st.columns(4)
        cols[0].metric("Comparisons", step["comparisons"])
        cols[1].metric("Swaps", step["swaps"])
        cols[2].metric("Writes", step["writes"])
        cols[3].metric(
            "Algorithm time",
            "—" if elapsed is None else f"{elapsed * 1000:.3f} ms",
        )


# Sidebar settings
st.sidebar.header("Visualizer Settings")
mode = st.sidebar.radio("Choose operation", ["Sorting", "Searching"])
array_size = st.sidebar.slider("Array size", 5, 30, 12)

if "array" not in st.session_state:
    st.session_state.array = random.sample(range(5, 201), array_size)

if st.sidebar.button("🎲 Generate New Array"):
    st.session_state.array = random.sample(range(5, 201), array_size)

custom_array = st.sidebar.text_input(
    "Or enter your own numbers (comma-separated)",
    placeholder="45, 12, 78, 23, 56",
)
if st.sidebar.button("Use Custom Array"):
    try:
        numbers = [int(x.strip()) for x in custom_array.split(",") if x.strip()]
        if not numbers:
            st.sidebar.error("Enter at least one number.")
        elif len(numbers) > 30:
            st.sidebar.error("Maximum array size is 30.")
        else:
            st.session_state.array = numbers
            st.rerun()
    except ValueError:
        st.sidebar.error("Enter valid integers separated by commas.")

speed = st.sidebar.slider(
    "Animation delay (seconds)", 0.0, 0.5, 0.08, 0.02
)

current_array = st.session_state.array.copy()
st.subheader("Input Array")
st.write(current_array)

if mode == "Sorting":
    algorithm = st.selectbox("Select sorting algorithm", list(SORT_INFO))
    info = SORT_INFO[algorithm]
    st.info(info["description"])

    cols = st.columns(4)
    cols[0].metric("Best Case", info["best"])
    cols[1].metric("Average Case", info["average"])
    cols[2].metric("Worst Case", info["worst"])
    cols[3].metric("Space Complexity", info["space"])

    if st.button("▶ Start Sorting", type="primary"):
        start = time.perf_counter()
        steps = sorting_steps(current_array, algorithm)
        elapsed = time.perf_counter() - start

        chart = st.empty()
        metrics = st.empty()
        progress = st.progress(0)
        status = st.empty()
        playback_start = time.perf_counter()

        for i, step in enumerate(steps):
            draw_array(step, chart)
            show_metrics(step, metrics)
            progress.progress((i + 1) / len(steps))
            status.caption(f"Step {i + 1}/{len(steps)}: {step['action']}")
            if speed > 0:
                time.sleep(speed)

        show_metrics(steps[-1], metrics, elapsed)
        st.success(f"Sorting completed! Result: {steps[-1]['array']}")
        st.caption(
            f"Algorithm computation time: {elapsed * 1000:.3f} ms. "
            f"Visualization playback time: "
            f"{time.perf_counter() - playback_start:.2f} seconds."
        )
        if steps[-1]["array"] == sorted(current_array):
            st.success("Verification passed: the array is sorted.")
        else:
            st.error("Verification failed: check the algorithm.")

else:
    algorithm = st.selectbox(
        "Select searching algorithm", ["Linear Search", "Binary Search"]
    )
    target = st.number_input("Enter target value", value=int(current_array[0]), step=1)

    if algorithm == "Linear Search":
        st.info("Linear Search checks elements one by one and works on unsorted input.")
        best, average, worst = "O(1)", "O(n)", "O(n)"
    else:
        st.info("Binary Search halves the search space. Input is sorted automatically.")
        best, average, worst = "O(1)", "O(log n)", "O(log n)"

    cols = st.columns(3)
    cols[0].metric("Best Case", best)
    cols[1].metric("Average Case", average)
    cols[2].metric("Worst Case", worst)

    if st.button("🔎 Start Searching", type="primary"):
        start = time.perf_counter()
        steps, found_index, searched_array = searching_steps(
            current_array, algorithm, int(target)
        )
        elapsed = time.perf_counter() - start

        chart = st.empty()
        metrics = st.empty()
        progress = st.progress(0)
        status = st.empty()
        playback_start = time.perf_counter()

        for i, step in enumerate(steps):
            draw_array(step, chart)
            show_metrics(step, metrics)
            progress.progress((i + 1) / len(steps))
            status.caption(f"Step {i + 1}/{len(steps)}: {step['action']}")
            if speed > 0:
                time.sleep(speed)

        show_metrics(steps[-1], metrics, elapsed)
        if found_index != -1:
            st.success(
                f"Target {target} found at index {found_index} "
                "in the displayed search array."
            )
        else:
            st.warning(f"Target {target} was not found.")
        st.caption(
            f"Algorithm computation time: {elapsed * 1000:.3f} ms. "
            f"Visualization playback time: "
            f"{time.perf_counter() - playback_start:.2f} seconds."
        )

st.divider()
with st.expander("📚 About this project and DAA concepts"):
    st.markdown("""
    **Project:** Interactive Algorithm Visualizer  
    **Subject:** Design and Analysis of Algorithms (DAA)

    **Concepts demonstrated**
    - Sorting and searching
    - Divide and conquer
    - Recursion
    - Time and space complexity
    - Operation counting and empirical analysis

    **Color legend**
    - Blue: Normal array elements
    - Orange: Elements currently being examined

    Execution time depends on hardware and runtime conditions.
    Theoretical complexity describes how an algorithm scales as input grows.
    """)
