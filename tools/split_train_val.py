import argparse
import os
import pandas as pd
import shutil


def parse_args():
    parser = argparse.ArgumentParser('Convert annotation files from MMOCR to PP-OCR')
    parser.add_argument('input_dir_path', type=str, help='Image dir path')
    parser.add_argument('input_file_path', type=str, help='Val file path')
    parser.add_argument('output_train_path', type=str, help='Output train folder path')
    parser.add_argument('output_val_path', type=str, help='Output val folder path')
    args = parser.parse_args()

    return args


def split_train_val():
    args = parse_args()

    if os.path.exists(args.output_train_path):
        print("Train folder already exists!")
        return

    os.makedirs(args.output_train_path)

    if os.path.exists(args.output_val_path):
        print("Val folder already exists!")
        return

    os.makedirs(args.output_val_path)

    file_names = list(pd.read_csv(args.input_file_path, delimiter='\t', header=None, engine='python').iloc[:, [0]][0])

    print('Starting...')
    files = os.listdir(args.input_dir_path)

    total = len(files)
    for i, file_name in enumerate(files):

        if (i + 1) % 1000 == 0:
            print(f'Processed {i + 1}/{total}')

        if file_name.endswith(".txt"):
            continue

        if file_name in file_names:
            shutil.copy(os.path.join(args.input_dir_path, file_name), os.path.join(args.output_val_path, file_name))
        else:
            shutil.copy(os.path.join(args.input_dir_path, file_name), os.path.join(args.output_train_path, file_name))

    print('Done!')


if __name__ == '__main__':
    split_train_val()
