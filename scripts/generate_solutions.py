import subprocess
import sys
import yaml



def run_subprocess(cmd):
    """Run a subprocess and capture its output and return code."""
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        output = p.stdout.read()
        error_output = p.stderr.read()
        returncode = p.poll()
        p.kill()
    return output, error_output, returncode

print("GENERATING SOLUTIONS")
# Load the YAML data from the file
with open('tests/tests.yml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

# Iterate through the test cases
for test_suite in yaml_data.get("suites", []):
    for test_case in test_suite.get("tests", []):
        
        cmd = test_case.get("command", [])
        stream = test_case.get("stream", "stdout")
        test_type = test_case.get("type", "output")
        if test_type == "regex":
            test_case["solution"] = test_case.get("solution", "")
            continue
        # Run the command and capture the program output
        std_output, error_output, returncode = run_subprocess(cmd)
        
        print("Command: ", cmd)
        if stream == "stderr" or test_type == "memcheck":
            output = error_output
        else:
            output = std_output

        if test_type == "returncode":
            if(returncode == None):
                output = "Program did not return a value"
            else:
                output = int(returncode)
  
        
        # Update the YAML with the program output as the solution
        if(test_type == "memcheck"):
            output = output.decode("utf-8", errors="ignore")
            output = '\n'.join(output.strip().split('\n')[-10:-8])
            if "HEAP SUMMARY" in output:
                output = "No memory leaks"
                b_output = output.encode("utf-8")
            test_case["solution"] = b_output
        else:
            test_case["solution"] = output

# Save the updated YAML back to the file
with open('tests/tests.yml', 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=False)