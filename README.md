# gpt_pronounciation_coach

## Installation
```
brew install dwdiff
brew install portaudio

uv venv --python 3.10
source .venv/bin/activate
uv pip install -r pyproject.toml
```

**NOTE:** A pyaudio dependencies may have issues being insteall in the uv virtual environment

## Usage
```
python gpt_speaking_coach.py --input oai_s1.txt
```

# Practice Sentence Generation in ChatGPT
```
write 10 sentences each with phonemes or pronunciations specific to english typically missed by non-native speakers. start each sentence with the Sentence followed by a space like "Sentence ". do not use any punctuation other than a period.
```

```
write 10 sentences regarding mathematical modeling of calcium biology in embryoes. each sentence should be on a single line and start with the word sentence. like "Sentence mathematical biology is hard"
```