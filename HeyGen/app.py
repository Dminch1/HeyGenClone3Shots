import gradio as gr, os
from pipeline import AvatarPipeline

pipe = AvatarPipeline()

def run(mode, img, vid, wav, text):
    if mode=="still" and not img:  return None, "🥸 Upload a face image!"
    if mode=="video" and not vid: return None, "🎬 Upload a reference video!"
    if not (text or wav):         return None, "🔊 Provide text or an audio sample!"
    target = img if mode=="still" else vid
    out = pipe.generate(mode, target, text, wav)
    return out, f"✅ Done → {os.path.basename(out)}"

with gr.Blocks(title="HeyGen-clone", theme=gr.themes.Soft(), show_api=False) as demo:
    gr.Markdown("## HeyGen-clone – dual-mode (Still | Video)")
    mode = gr.Radio(["still","video"], value="still", label="Mode")
    img  = gr.Image(type="filepath", label="Face image (still mode)")
    vid  = gr.Video(type="filepath", label="Reference video (video mode)")
    text = gr.Textbox(label="Text to speak (optional)")
    wav  = gr.Audio(type="filepath", label="Speaker WAV (optional)")
    outV = gr.Video()
    outM = gr.Textbox()
    gr.Button("Generate").click(run, [mode,img,vid,wav,text], [outV,outM])

if __name__=="__main__":
    demo.launch(server_name="0.0.0.0", share=True, show_error=True)
