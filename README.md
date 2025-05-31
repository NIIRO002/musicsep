# MusicControl - Source Separation with Demucs

This project uses [Demucs](https://github.com/facebookresearch/demucs) to perform music source separation on an input audio file.

## Requirements

To get started, install the required packages:

```bash
pip install git+https://github.com/facebookresearch/demucs.git
pip install torch torchaudio
pip install numpy==1.24.3
```

Terminal Command :
```bash
python musiccontrol.py --input "example.wav" --output_folder "/path/to/output"
```


output
|
|-drum_example.wav\
|-bass_example.wav\
|-vocals_example.wav\
|-other_example.wav\
|-rhythm_example.wav (drum + bass)\
|-melody_example.wav (vocals + other)\
 \
