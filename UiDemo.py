import gradio as gr


def play_audio(audio):
    if audio is None:
        return None
    return audio


with gr.Blocks() as demo:
    gr.Markdown("## SHATO")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Audio")

    with gr.Row():
        play_button = gr.Button("▶Play Recording")

    audio_output = gr.Audio(label="Playback", type="filepath")

    play_button.click(fn=play_audio, inputs=audio_input, outputs=audio_output)

demo.launch()
