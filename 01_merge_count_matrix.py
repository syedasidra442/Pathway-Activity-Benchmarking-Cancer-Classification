"""
00 - Merge GDC STAR gene-count files into a single count matrix.

Input : a folder of GDC downloads (gdc-client output). Each sample sits in its
        own UUID-named sub-folder containing one STAR gene-counts .tsv file.
Output: genes x samples count matrix (protein-coding genes only). Columns are
        the GDC file UUIDs, which are the "File ID" values used by the GDC
        sample sheet, so later metadata steps can match on them.

Note: the output is TAB-separated even though it ends in .csv. Every later
step reads it with sep="\\t".

Usage:
    python 01_merge_count_matrix.py
    python 01_merge_count_matrix.py --input-dir data/raw/TCGA_Download \
        --output data/processed/merged_count_matrix_UUID.csv
"""
import argparse
import os

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input-dir", default="data/raw/TCGA_Download",
                        help="Folder holding the GDC download (one UUID sub-folder per sample).")
    parser.add_argument("--output", default="data/processed/merged_count_matrix_UUID.csv",
                        help="Path of the merged count matrix to write.")
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isdir(args.input_dir):
        raise FileNotFoundError(f"Input folder not found: {args.input_dir}")

    # Recursively find all gene count files
    tsv_files = []
    for root, dirs, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith(".tsv"):
                tsv_files.append(os.path.join(root, file))

    print("Total files found:", len(tsv_files))

    all_samples = []

    for file_path in tsv_files:
        # UUID folder name is used as the sample ID
        sample_id = os.path.basename(os.path.dirname(file_path))
        print(f"Processing file {sample_id}")

        # Read file (skip the first metadata line)
        df = pd.read_csv(file_path, sep="\t", skiprows=1)

        # Keep protein-coding genes only
        df_pc = df[df["gene_type"] == "protein_coding"].copy()

        # Keep required columns
        df_pc = df_pc[["gene_name", "unstranded"]]

        # Sum counts of duplicate gene names
        df_pc = df_pc.groupby("gene_name", as_index=False).sum()

        # Name the counts column after the sample UUID
        df_pc.rename(columns={"unstranded": sample_id}, inplace=True)

        all_samples.append(df_pc)

    print(f"Processed {len(all_samples)} samples")

    # Dictionary of series, then a single concat (efficient)
    gene_counts_dict = {}
    for df in all_samples:
        sample_id = df.columns[1]
        gene_counts_dict[sample_id] = df.set_index("gene_name")[sample_id]

    counts_matrix = pd.concat(gene_counts_dict, axis=1).reset_index()

    print("Count matrix shape:", counts_matrix.shape)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    counts_matrix.to_csv(args.output, sep="\t", index=False)

    print(f"Done. File saved as {args.output}")


if __name__ == "__main__":
    main()
