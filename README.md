# GPT Speaking Coach

This project is a AI-based speaking coach that uses AI (OpenAI GPT models) to:

1. Generate practice sentences for speaking practice on any topic of interest or general hard to pronounce words
2. Listen and evaluate the pronunciation by showing you words that were mispronounced
3. Provide feedback on the pronunciation with
   1. Guidance on tongue and mouth positioning for better pronunciation
   2. Simplified phonetic pronunciation of the word

## Installation

## Dependency Installation
```
brew install dwdiff
brew install portaudio

uv venv --python 3.10
source .venv/bin/activate
uv pip install -r pyproject.toml
```

**NOTE:** A pyaudio dependencies may have issues being installed in the uv virtual environment

## OpenAI API Key

Edit the .env_example file to .env and replace the OPENAI_API_KEY with your OpenAI API key from https://platform.openai.com/settings/organization/api-keys

## Usage
```
python gpt_speaking_coach.py --input oai_s1.txt
```

# Practice Sentence Generation in ChatGPT
## Prompts
```
write 10 sentences each with phonemes or pronunciations specific to english typically missed by non-native speakers. start each sentence with the Sentence followed by a space like "Sentence ". do not use any punctuation other than a period.
```

```
write 10 sentences regarding mathematical modeling of calcium biology in embryoes. each sentence should be on a single line and start with the word sentence. like "Sentence mathematical biology is hard"
```