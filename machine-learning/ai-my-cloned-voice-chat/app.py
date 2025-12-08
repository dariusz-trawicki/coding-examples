from audio_io import record_wav, play_wav
from asr_local import speech_to_text
from llm_local import chat_reply
from tts_local import tts_to_file


def main():
    print("Local voice assistant. Say something (or 'exit' to end).")

    while True:
        # 1. Record audio
        record_wav("input.wav", duration=5)

        # 2. ASR (Automatic Speech Recognition)
        print("I recognize text from input.wav...")
        user_text = speech_to_text("input.wav")
        print("Ty:", user_text)

        if user_text.strip().lower() in ["exit", "quit"]:
            print("I'm finishing.")
            break

        # 3. LLM (Large Language Model)
        print("Generating a model response...")
        answer = chat_reply(user_text)
        print("Asystent:", answer)

        # 4. TTS (Text-To-Speech)
        print("I synthesize the answer with the voice...")
        out_file = tts_to_file(answer, "reply.wav", language="en")

        # 5. Playback
        print("I'm playing reply.wav...")
        play_wav(out_file)
        print("-" * 40)


if __name__ == "__main__":
    main()
