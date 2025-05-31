#!/usr/bin/env python3
import argparse
import os
import subprocess
from demucs.api import Separator, save_audio

def main():
    parser = argparse.ArgumentParser(
        description="Demucs로 음원을 분리한 후, stem들을 저장합니다. "
                    "drums+bass를 합쳐 rhythm, vocals+other를 합쳐 melody로 저장하고, "
                    "또한 개별 drum 파일을 DrumSep으로 추가 분리합니다."
    )
    parser.add_argument('--input', type=str, required=True,
                        help='입력 음악 파일 경로 (예: file.mp3 또는 file.wav)')
    parser.add_argument('--output_folder', type=str, required=True,
                        help='분리된 결과를 저장할 출력 폴더 경로')
    parser.add_argument('--model', type=str, default="htdemucs",
                        help='사용할 Demucs 모델 (기본값: htdemucs)')
    args = parser.parse_args()

    # 출력 폴더가 없으면 생성
    os.makedirs(args.output_folder, exist_ok=True)

    # Demucs Separator 객체 생성
    separator = Separator(model=args.model)
    
    # 파일 분리: origin은 원본 오디오, separated는 {stem: waveform} 딕셔너리
    origin, separated = separator.separate_audio_file(args.input)
    print("Separation complete!")

    file_name = os.path.basename(args.input)

    # 개별 스템 저장 (drums, bass, vocals, other 등)
    for stem, waveform in separated.items():
        out_path = os.path.join(args.output_folder, f"{stem}_{file_name}")
        save_audio(waveform, out_path, samplerate=separator.samplerate)
        print(f"Saved {stem} to {out_path}")

    # drums와 bass를 합쳐 rhythm 생성 및 저장
    try:
        rhythm_waveform = separated["drums"] + separated["bass"]
        rhythm_out_path = os.path.join(args.output_folder, f"rhythm_{file_name}")
        save_audio(rhythm_waveform, rhythm_out_path, samplerate=separator.samplerate)
        print(f"Saved rhythm (drums+bass) to {rhythm_out_path}")
    except KeyError:
        print("drums 또는 bass 스템이 없어 rhythm을 생성하지 못했습니다.")
    
    # vocals와 other를 합쳐 melody 생성 및 저장
    try:
        melody_waveform = separated["vocals"] + separated["other"]
        melody_out_path = os.path.join(args.output_folder, f"melody_{file_name}")
        save_audio(melody_waveform, melody_out_path, samplerate=separator.samplerate)
        print(f"Saved melody (vocals+other) to {melody_out_path}")
    except KeyError:
        print("vocals 또는 other 스템이 없어 melody를 생성하지 못했습니다.")

    # 추가: 개별 drum 파일을 DrumSep을 통해 추가 분리
    # 이미 저장된 drum 파일의 경로 (예: drums_bts_dynamite_3_verse.mp3)
    drum_file = os.path.join(args.output_folder, f"drums_{file_name}")
    # DrumSep 결과를 저장할 폴더 생성 (output_folder 내 "drumsep_output")
    drumsep_output = os.path.join(args.output_folder, "drumsep_output")
    os.makedirs(drumsep_output, exist_ok=True)
    
    print(f"Running drumsep on {drum_file}...")
    try:
        # drumsep의 CLI 명령어 실행 (drumsep이 설치되어 있어야 함)
        subprocess.run(["drumsep", drum_file,  drumsep_output], check=True)
        print(f"Drumsep processing complete. Results are in {drumsep_output}")
    except Exception as e:
        print("Drumsep processing failed:", e, drumsep_output)

if __name__ == '__main__':
    main()
