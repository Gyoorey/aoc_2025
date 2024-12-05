import subprocess
import time


def measure_time(command):
    start_time = time.time()
    subprocess.run(command, shell=True)
    end_time = time.time()
    return end_time - start_time


# Measure time for sol.py
python_time = measure_time("python3 sol.py")

# Measure time for sol (compiled C++ program)
cpp_time = measure_time("./sol")

print(f"sol.py execution time: {python_time:.6f} seconds")
print(f"sol (C++ program) execution time: {cpp_time:.6f} seconds")

if python_time < cpp_time:
    print("sol.py is faster")
    times_faster = cpp_time / python_time
    print(f"sol.py is {times_faster:.2f} times faster than sol (C++ program)")
else:
    print("sol (C++ program) is faster")
    times_faster = python_time / cpp_time
    print(f"sol (C++ program) is {times_faster:.2f} times faster than sol.py")
