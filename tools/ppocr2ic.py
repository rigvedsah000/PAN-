import json
import argparse
import os
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser('Convert annotation files from MMOCR to PP-OCR')
    parser.add_argument('input', type=str, help='PPOCR annotation file path')
    parser.add_argument('output', type=str, help='Output folder path')
    args = parser.parse_args()

    return args


def ppocr2ic():
    args = parse_args()

    df = pd.read_csv(args.input, delimiter='\t', header=None, engine='python')

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    total = len(df)

    print('Starting...')

    for i, row in enumerate(df.iterrows()):
        row = row[1]
        f_name = '.'.join(row[0].split('.')[:-1]) + '.txt'
        out_file = open(os.path.join(args.output, f_name), 'w', encoding='utf8')

        for ann in json.loads(row[1]):
            transcription = ann['transcription'].strip()
            points = ann['points']

            out_file.write(
                str(points[0][0]) + ',' + str(points[0][1]) + ',' +
                str(points[1][0]) + ',' + str(points[1][1]) + ',' +
                str(points[2][0]) + ',' + str(points[2][1]) + ',' +
                str(points[3][0]) + ',' + str(points[3][1]) + ',' +
                transcription + '\n')

        out_file.close()

        if i%2 == 0:
            print(f'Processed {i}/{total}')

    print('Done!')


if __name__ == '__main__':
    ppocr2ic()