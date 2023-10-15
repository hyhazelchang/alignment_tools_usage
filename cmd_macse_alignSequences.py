#!/usr/bin/python3

# cmd_macse_alignSequences.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/05/19

# Usage: python3 /home/xinchang/pyscript_xin/cmd_macse_alignSequences.py --macse_exe=/home/xinchang/macse_v2.07.jar --seq_dir=/scratch/xinchang/cyano11/cyano11.17/ortho_fasta/all+1 --out_NT_dir=/scratch/xinchang/cyano11/cyano11.17/macse/all+1/nt --out_AA_dir=/scratch/xinchang/cyano11/cyano11.17/macse/all+1/aa --sh_dir=/scratch/xinchang/cyano11/cyano11.17/sh/macse/align --n_job=30


import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Make the shscript for macse execution."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--macse_exe",
                        default=None,
                        type=str,
                        help="MACSE file directory. Please provide absolute path.")
    parser.add_argument("--seq_dir",
                        default=None,
                        type=str,
                        help="Directory containing sequence files (the file should have fasta extension). Please provide absolute path.")
    parser.add_argument("--out_NT_dir",
                        default=None,
                        type=str,
                        help="Output directory for nucleotide alignments. Please provide absolute path.")
    parser.add_argument("--out_AA_dir",
                        default=None,
                        type=str,
                        help="Output directory for amino acid alignments. Please provide absolute path.")
    parser.add_argument("--sh_dir",
                        default=None,
                        type=str,
                        help="Directory for shell scripts. Please provide absolute path.")
    parser.add_argument("--n_job",
                        default=1,
                        type=int)

    args = parser.parse_args()
    macse_exe = args.macse_exe
    seq_dir = args.seq_dir
    out_NT_dir = args.out_NT_dir
    out_AA_dir = args.out_AA_dir
    sh_dir = args.sh_dir
    n_job = args.n_job

    # Find alignment files
    seqfiles = glob.glob(seq_dir + "*.fasta")

    # Make output directory
    if not os.path.exists(out_NT_dir):
        os.system("mkdir -p " + out_NT_dir)
    if not os.path.exists(out_AA_dir):
        os.system("mkdir -p " + out_AA_dir)

    # Get file names
    count = 0
    macse_cmd = []
    for seq in seqfiles:
        count += 1
        seq_name = os.path.basename(seq).split(".")[0]
        macse_cmd.append("java -jar " + macse_exe + " -prog alignSequences -seq " + seq + " -out_NT " + out_NT_dir + seq_name + ".al.nt.fasta -out_AA " + out_AA_dir + seq_name + ".al.aa.fasta;")

    # print out job scripts
    os.system("mkdir -p " + sh_dir)
    quo = int(count / n_job)
    mod = int(count % n_job)
    cmd_num = 0
    for n in range(n_job):
        job = open(sh_dir + "job" + str(n+1) + ".sh" , "w")
        if n + 1 <= mod:
            for num in range(quo + 1):
                job.write(macse_cmd[cmd_num] + "\n")
                cmd_num += 1
            job.close()
        else:
            for num in range(quo):
                job.write(macse_cmd[cmd_num] + "\n")
                cmd_num += 1
            job.close()

if __name__ == "__main__":
    main()
