# Runs step 1 to step 4 one after another
import subprocess, sys

for script in ["step1_acquire_data.py", "step2_clean_data.py",
               "step3_eda_visualization.py", "step4_model.py"]:
    print("\n========== Running", script, "==========")
    subprocess.run([sys.executable, script], check=True)

print("\nAll steps done. Now run:  python app.py")
