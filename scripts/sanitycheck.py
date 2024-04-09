import subprocess
import sys
import re
import glob
from benedict import benedict

# Constants
PATH_TO_TESTS = 'tests/tests.yml'
SYS_TRACEBACK_LIMIT = 0
COLORIZED = True

# Color codes
if COLORIZED:
    ENDCODE = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
else:
    ENDCODE = ''
    BOLD = ''
    GREEN = ''
    RED = ''
    BLUE= ''

def run_subprocess(cmd):
    """Run a subprocess and capture its output and return code."""
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        output = p.stdout.read()
        error_output = p.stderr.read()
        returncode = p.poll()
        p.kill()
    return output, error_output, returncode

def perform_output_test(test_case):
    """Perform an output-based test and display results."""
    correct_output = test_case["solution"]
    cmd = test_case["command"]
    output_stream = test_case.get("stream", "stdout")  # Default to "stdout"
    # print(output_stream)
    print(f"  {BOLD}{test_case['name']}{ENDCODE}")
    print(f"  ", cmd[1:])
    std_output, error_output, returncode = run_subprocess(cmd)

    if output_stream == "stderr":
        output = error_output
    else:
        output = std_output

    try:
        assert output == correct_output
        print(GREEN, "   PASS", '✓', ENDCODE)
        print(f'    YOURS: {output.decode("utf-8", errors="ignore")}\n')
        return 1
    except Exception as err:
        print(RED, "   FAIL", '✗', ENDCODE)
        print('~'*30)
        print(f'YOURS {output_stream}: \n{RED}{output.decode("utf-8", errors="ignore")}{ENDCODE}\n{BLUE}{output}{ENDCODE}\n')
        print('~'*10)
        print(f'OURS : \n{GREEN}{correct_output.decode("utf-8", errors="ignore")}{ENDCODE}\n{BLUE}{correct_output.decode("utf-8").encode("utf-8")}{ENDCODE} \n')
        print('~'*30)
        return 0
    
def perform_memcheck_test(test_case):
    """Perform an output-based test and display results."""
    correct_output = test_case["solution"]
    cmd = test_case["command"]
    output_stream = test_case.get("stream", "stderr")  # Default to "stderr"
    # print(output_stream)
    print(f"  {BOLD}{test_case['name']}{ENDCODE}")
    print(f"  ", cmd[1:])
    std_output, error_output, returncode = run_subprocess(cmd)

   
    b_output = error_output
    output = b_output.decode("utf-8", errors="ignore")
    # print("TESTING", output.strip().split('\n')[-10:-8])
    output = '\n'.join(output.strip().split('\n')[-10:-8])
    b_output = output.encode("utf-8")
    
    if "HEAP SUMMARY" in output:
        output = "No memory leaks"
        b_output = output.encode("utf-8")

    try:
        assert b_output == correct_output
        print(GREEN, "   PASS", '✓', ENDCODE)
        print(f'    YOURS: {output}\n')
        return 1
    except Exception as err:
        print(RED, "   FAIL", '✗', ENDCODE)
        print('~'*30)
        print(f'YOURS {output_stream}: \n{RED}{output}{ENDCODE}\n{BLUE}{b_output}{ENDCODE}\n')
        print('~'*10)
        print(f'OURS : \n{GREEN}{correct_output.decode("utf-8", errors="ignore")}{ENDCODE}\n{BLUE}{correct_output.decode("utf-8").encode("utf-8")}{ENDCODE} \n')
        print('~'*30)
        return 0
    
def perform_returncode_test(test_case):
    """Perform a return code-based test and display results."""
    correct_returncode = test_case["solution"]
    cmd = test_case["command"]

    print(f"  {BOLD}{test_case['name']}{ENDCODE}")
    print(f"  ", cmd[1:])
    output, error_output, returncode = run_subprocess(cmd)

    try:
        assert returncode == int(correct_returncode)
        print(GREEN, "   PASS", '✓', ENDCODE)
        print(f'    YOURS: {returncode}\n')
        return 1
    except Exception as err:
        print(RED, "   FAIL", '✗', ENDCODE)
        print(f'    YOURS: {returncode}\n    OURS : {GREEN}{correct_returncode}{ENDCODE}')
        return 0

def perform_regex_test(test_case):
    """Perform a regex-based test and calculate points."""
    regex_pattern = test_case["regex"]
    score_type = test_case.get("score", "perfect")
    files = test_case["files"]
    solution = test_case.get("solution", 1)  # Default to 1 if no solution is specified
    cmd = test_case["command"]

    print(f"  {BOLD}{test_case['name']}{ENDCODE}")
    print(f"  ", cmd[1:])
    matched_count = 0

    for file_pattern in files.split(", "):
        for filename in glob.glob(file_pattern):
            print("  ", filename)
            with open(filename, "r") as file:
                contents = file.read()
                matched_count += len(re.findall(regex_pattern, contents))

    try:
        if score_type == "count":
            score = matched_count
            points_awarded = score / float(solution)
        elif score_type == "perfect":
            score = matched_count
            points_awarded = 1 if score == solution else 0
        else:
            # Handle other score types if needed
            pass
        if score >= float(solution):
            score = float(solution)
            print(GREEN, f"  PASS ✓ {score_type}: {score} / {solution}, {points_awarded}", '✓', ENDCODE)
        else:
            print(RED, f"  PARTIAL - {score_type}: {score} / {solution}, {points_awarded}", '✓', ENDCODE)

            
        return points_awarded
    except Exception as err:
        print(RED, "   FAIL", '✗', ENDCODE)
        print("   Error:", err)
        return 0


def load_tests_from_yaml(path):
    """Load test data from a YAML file."""
    return benedict.from_yaml(path)

def main():
    """Main program entry point."""
    sys.tracebacklimit = SYS_TRACEBACK_LIMIT

    test_data = load_tests_from_yaml(PATH_TO_TESTS)
    PROBLEM_NAME = test_data['problem']

    results = []
    total_possible_points = []

    suites_to_run = list(range(len(test_data["suites"])))

    # Check for command line arguments to select which suites to run
    if len(sys.argv) > 1:
        try:
            selected_suite = int(sys.argv[1]) - 1  # Convert to 0-based index
            if selected_suite < len(test_data["suites"]) and selected_suite >= 0:
                suites_to_run = [selected_suite]
            else:
                print(f"Invalid suite number {selected_suite + 1}. Only {len(test_data['suites'])} suites available.")
                sys.exit(1)
        except ValueError:
            print(f"Invalid argument {sys.argv[1]}. Please provide a valid suite number.")
            sys.exit(1)

    for i in suites_to_run:
        test_suite = test_data["suites"][i]
        suite_name = test_suite["name"]
        suite_pts = test_suite["pts"]
        suite_tests = test_suite["tests"]
        total_possible_points.append(suite_pts)
        print(f"\n{BOLD}{suite_name}{ENDCODE} - Points: {suite_pts}")
        print('-'*60)

        total_points_for_suite = 0
        total_tests_in_suite = len(suite_tests)

        if total_tests_in_suite > 0:
            points_per_test = suite_pts / total_tests_in_suite
        else:
            points_per_test = 0

        for test_case in suite_tests:
            test_name = test_case["name"]
            test_type = test_case.get("type", "output")
            points_awarded = 0

            if test_type == "output":
                points_awarded = perform_output_test(test_case)
            elif test_type == "memcheck":
                points_awarded = perform_memcheck_test(test_case)
            elif test_type == "returncode":
                points_awarded = perform_returncode_test(test_case)
            elif test_type == "regex":
                points_awarded = perform_regex_test(test_case)

            total_points_for_suite += points_awarded * points_per_test

        total_points_for_suite = min(total_points_for_suite, suite_pts)  # Ensure not more than max points
        results.append(total_points_for_suite)

        print(f" Points per Test: {points_per_test} pts")
        print(f" Total Points for Suite: {total_points_for_suite} / {suite_pts} pts")
        print("\n", '*'*20)

    print(f"   {BOLD}{PROBLEM_NAME}{ENDCODE}")
    print("", '*'*20)
    print('\n', BOLD, "SUMMARY", ENDCODE)
    print(" ", '-'*20)
    total_points = sum(results)
    total_possible_points = sum(total_possible_points)
    # print(f" Total Points: {total_points} / {total_possible_points} pts")
    print(f"{BOLD} PROBLEM GRADE: {total_points} / {total_possible_points} pts{ENDCODE}")
    print(f" Note: These are sample test cases. We will run your program with different parameters");
    print("", '*'*20)
    print(total_points)


if __name__ == '__main__':
    main()
