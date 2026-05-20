import os
import subprocess
import time
import pandas as pd
from Bio import SeqIO
from tqdm import tqdm

# =========================
# CONFIG
# =========================

proteome_dir = "../data/proteomes"

fast_results_dir = "../results/signalp_fast"

slow_results_root = "../results/signalp_fast_slow"

signalp_mode = "slow-sequential"

organism = "euk"

model_dir = "../tools/signalp6_slow_sequential/models"

os.makedirs(slow_results_root, exist_ok=True)

# =========================
# FIND SPECIES
# =========================

species_dirs = sorted([
    d for d in os.listdir(fast_results_dir)
    if os.path.isdir(os.path.join(fast_results_dir, d))
])

print(f"Found {len(species_dirs)} species")

failed = []

# =========================
# MAIN LOOP
# =========================

for species_name in tqdm(species_dirs):

    print("\n" + "="*80)
    print(f"PROCESSING: {species_name}")
    print("="*80)

    # -------------------------
    # Paths
    # -------------------------

    proteome_fasta = os.path.join(
        proteome_dir,
        species_name + ".fasta"
    )

    fast_prediction = os.path.join(
        fast_results_dir,
        species_name,
        "prediction_results.txt"
    )

    slow_output_dir = os.path.join(
        slow_results_root,
        species_name
    )

    os.makedirs(slow_output_dir, exist_ok=True)

    slow_prediction = os.path.join(
        slow_output_dir,
        "prediction_results.txt"
    )

    secretome_fasta = os.path.join(
        slow_output_dir,
        "fast_secretome_full_length.fasta"
    )

    # -------------------------
    # Skip completed
    # -------------------------

    if os.path.exists(slow_prediction):

        if os.path.getsize(slow_prediction) > 0:

            print("Skipping completed")

            continue

    # -------------------------
    # Load FAST predictions
    # -------------------------

    try:

        fast_df = pd.read_csv(
            fast_prediction,
            sep="\t",
            skiprows=1
        )

        fast_df.columns = [
            "protein_id",
            "Prediction",
            "OTHER",
            "SP",
            "CS_Position"
        ]

    except Exception as e:

        print("Failed reading FAST prediction file")

        failed.append({
            "species": species_name,
            "error": str(e)
        })

        continue

    # -------------------------
    # Extract SP-positive IDs
    # -------------------------

    sp_df = fast_df[
        fast_df["Prediction"] == "SP"
    ]

    sp_ids = set()

    for pid in sp_df["protein_id"]:

        try:
            uid = pid.split("|")[1]
            sp_ids.add(uid)

        except:
            continue

    print(f"FAST secretome proteins: {len(sp_ids)}")

    # -------------------------
    # Extract ORIGINAL sequences
    # -------------------------

    records = []

    for record in SeqIO.parse(proteome_fasta, "fasta"):

        try:
            uid = record.id.split("|")[1]

        except:
            continue

        if uid in sp_ids:

            records.append(record)

    print(f"Recovered full-length proteins: {len(records)}")

    # -------------------------
    # Write secretome FASTA
    # -------------------------

    SeqIO.write(
        records,
        secretome_fasta,
        "fasta"
    )

    # -------------------------
    # Build SignalP command
    # -------------------------

    cmd = [
        "signalp6",
        "--fastafile", secretome_fasta,
        "--organism", organism,
        "--mode", signalp_mode,
        "--model_dir", model_dir,
        "--format", "none",
        "--output_dir", slow_output_dir
    ]

    print("\nCOMMAND:")
    print(" ".join(cmd))

    start = time.time()

    # -------------------------
    # Run SignalP
    # -------------------------

    try:

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

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

# =========================
# FAILURE LOG
# =========================

if failed:

    log_path = "../results/signalp_fast_slow_failures.txt"

    with open(log_path, "w") as f:

        for item in failed:

            f.write(f"{item['species']}\n")
            f.write(f"{item['error']}\n")
            f.write("\n" + "="*80 + "\n\n")

    print(f"\nFailures logged to: {log_path}")

else:

    print("\nAll slow validations completed successfully.")

print("\nDone.")