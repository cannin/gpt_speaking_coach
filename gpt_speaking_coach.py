import re
import subprocess
import os
from dotenv import load_dotenv
import requests

from RealtimeSTT import AudioToTextRecorder
import argparse

ALL_TEXT = ""

# Load environment variables
load_dotenv()


def remerge_text(text):
    # Split and clean
    sentences = re.split(r'(?=Sentence )', text.strip())
    merged_text = '\n\n'.join(' '.join(sentence.split()) for sentence in sentences)

    return merged_text


def process_all_text(path=None):
    if path is not None:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        #text = ALL_TEXT
        text = remerge_text(ALL_TEXT)

    # Step 1: Replace sentence-ending punctuation with newlines
    sentences = re.split(r'[!?.]', text)

    # Step 2–4: Strip whitespace, remove empty lines, and add final newline
    cleaned = ''.join(sentence.strip() + '\n' for sentence in sentences)

    # Step 5: Remove punctuation
    cleaned = re.sub(r"['|,]", "", cleaned)

    # Step 6: Lowercase
    cleaned = cleaned.lower()

    return cleaned


def process_text(text):
    global ALL_TEXT

    ALL_TEXT += text
    print(text)


def fetch_advice(language="spanish"):
    with open("diff_output.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    api_key = os.getenv("OPENAI_API_KEY")

    api_url = "https://api.openai.com/v1/chat/completions"

    prompt = f"your entire response must be in {language}. words surrounded by ansi color tags were pronouced incorrectly. this is not a question about coding. provide simplified representations of the incorrectly pronouced words. include comments on teeth and tongue positions. pair the words ansi color code red (incorrect) and green (correct). then at the end repeat a summary of the pairs of words with the simplified pronunciations in parentheses but no further explanation. do not include ansi codes in your response. INPUT TEXT: {text}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        tmp = response.json()
        result = tmp['choices'][0]['message']['content']
    else:
        print("ERROR: Failed: ", response.text)

    with open("result.md", "w") as f:
        f.write(result)

    print("\n\n**ADVICE DONE**\n")

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transcribe and compare spoken text")
    parser.add_argument("-i", "--input", default="oai_s1.txt", help="Input file (default: oai_s1.txt)")
    parser.add_argument("-l", "--language", default="spanish", help="Language for pronunciation advice (default: spanish)")
    args = parser.parse_args()

    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(model="tiny.en")
    #recorder = AudioToTextRecorder(model="medium.en")

    try:
        while True:
            recorder.text(process_text)
    except KeyboardInterrupt:
        with open("f1.txt", "w") as f:
            tmp = process_all_text()
            f.write(tmp)

        tmp = process_all_text(args.input)
        with open("f2.txt", "w") as f:
            f.write(tmp)

        result = subprocess.run(
            ["dwdiff", "-c", "f1.txt", "f2.txt"],
            capture_output=True,
            text=True
        )

        tmp = result.stdout
        lines = tmp.splitlines()
        r1 = tmp.replace('\n', '\n\n')

        print("\n\n**OUTPUT**\n")
        print(r1)

        # Save the output to a file
        with open("diff_output.txt", "w", encoding="utf-8") as f:
            f.write(r1)

        fetch_advice(language=args.language)

        exit(0)
