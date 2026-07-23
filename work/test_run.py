import sys
import io
import os

# Redirect stdout to a file to avoid the terminal NUL restriction
log_path = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'test_loop.log')
with open(log_path, 'w', encoding='utf-8') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    try:
        from nexus_autonomous_loop import run_nexus_autonomous_loop
        run_nexus_autonomous_loop(duration_sim_seconds=0)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sys.stdout = old_stdout

print(f"DONE. Saved to {log_path}")
