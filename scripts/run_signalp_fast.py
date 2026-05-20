import os
import subprocess
import time
from tqdm import tqdm

proteome_dir = "../data/proteomes"
output_root = "../results/signalp_fast"

signalp_mode = "fast"
organism = "euk"

os.makedirs(output_root, exist_ok=True)

proteome_files = sorted([
    f for f in os.listdir(proteome_dir)
    if f.endswith(".fasta")
])

print(f"Found {len(proteome_files)} proteomes")

failed = []

for proteome_file in tqdm(proteome_files):

    species_name = proteome_file.replace(".fasta", "")

    input_path = os.path.join(proteome_dir, proteome_file)

    output_dir = os.path.join(output_root, species_name)

    prediction_file = os.path.join(
        output_dir,
        "prediction_results.txt"
    )

    # -------------------------
    # Skip completed
    # -------------------------

    if os.path.exists(prediction_file):

        if os.path.getsize(prediction_file) > 0:

            print(f"\nSkipping completed: {species_name}")

            continue

    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "signalp6",
        "--fastafile", input_path,
        "--organism", organism,
        "--mode", signalp_mode,
        "--format", "none",
        "--output_dir", output_dir
    ]

    print("\n" + "="*80)
    print(f"RUNNING: {species_name}")
    print("="*80)

    print("\nCOMMAND:")
    print(" ".join(cmd))

    start = time.time()

    try:

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # live output
        for line in process.stdout:

            print(line.strip(), flush=True)

        process.wait()

        elapsed = (time.time() - start) / 60

        if process.returncode != 0:

            print(f"\nFAILED: {species_name}")

            failed.append({
                "species": species_name,
                "error": "Non-zero return code"
            })

        else:

            print(f"\nCOMPLETED: {species_name}")
            print(f"TIME: {elapsed:.1f} min")

    except Exception as e:

        print(f"\nEXCEPTION: {species_name}")
        print(str(e))

        failed.append({
            "species": species_name,
            "error": str(e)
        })

# -------------------------
# Failure log
# -------------------------

if failed:

    log_path = "../results/signalp_fast_failures.txt"

    with open(log_path, "w") as f:

        for item in failed:

            f.write(f"{item['species']}\n")
            f.write(f"{item['error']}\n")
            f.write("\n" + "="*80 + "\n\n")

    print(f"\nFailures logged to: {log_path}")

else:

    print("\nAll SignalP runs completed successfully.")

print("\nDone.")