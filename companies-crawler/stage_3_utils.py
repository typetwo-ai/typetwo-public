import os

import ffmpeg
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

MODEL_ID = "openai/whisper-small"

print(f"Loading model {MODEL_ID} on {DEVICE}...")

processor = AutoProcessor.from_pretrained(MODEL_ID)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    MODEL_ID,
    low_cpu_mem_usage=True,
    use_safetensors=True,
)
model.to(DEVICE)

audio_pipeline = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=1,
    return_timestamps="word",
    device=DEVICE,
)


def transcribe_audio(audio_path):
    print(f"Transcribing {audio_path}...")
    result = audio_pipeline(audio_path)

    full_text = ""
    detailed_output = {"words": []}

    if "text" in result:
        full_text = result["text"]
        detailed_output = result

    elif "chunks" in result:
        for chunk in result["chunks"]:
            full_text += chunk["text"] + " "
            if "timestamp" in chunk:
                detailed_output["chunks"].append({
                    "text": chunk["text"],
                    "start": chunk["timestamp"][0],
                    "end": chunk["timestamp"][1],
                })

    elif isinstance(result, dict) and "words" in result:
        word_list = []
        for word_info in result["words"]:
            if isinstance(word_info, dict) and "word" in word_info:
                word_list.append(word_info["word"])
                detailed_output["words"].append({
                    "word": word_info["word"],
                    "start": word_info.get("start", 0),
                    "end": word_info.get("end", 0),
                })
        full_text = " ".join(word_list)

    elif isinstance(result, dict):
        if "chunks" in result:
            for chunk in result["chunks"]:
                full_text += chunk.get("text", "") + " "

        elif "text" in result:
            full_text = result["text"]

        detailed_output = result

    full_text = full_text.strip()

    return full_text, detailed_output


def extract_audio_from_video(video_path):
    output_audio_path = os.path.join('tmp', f"extracted_audio_{os.path.basename(video_path)}.wav")
    try:
        print(f"Extracting audio from {video_path} to {output_audio_path}...")

        (
            ffmpeg
            .input(video_path)
            .output(output_audio_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(quiet=True, capture_stdout=True, capture_stderr=True)
        )

        return output_audio_path

    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode()}")
        return None