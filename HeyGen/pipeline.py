from pathlib import Path
import subprocess, uuid, shutil

class AvatarPipeline:
    def __init__(self):
        self.rtvc = Path("rtvc")
        self.sadtalker = Path("sadtalker")
        self.wav2lip = Path("wav2lip")

    # ---------- TTS ----------
    def voice_clone(self, text:str, ref_wav:str, out_wav:str):
        from rtvc.demo_cli import synthesize
        synthesize(text=text, reference_wav=ref_wav, output_path=Path(out_wav))

    # ---------- still image ----------
    def still2vid(self, img:str, wav:str, out_mp4:str, res:int=256):
        cmd = [
            "python", self.sadtalker/"inference_sadtalker.py",
            "--source_image", img, "--driven_audio", wav,
            "--result_dir", Path(out_mp4).parent, "--size", str(res),
            "--fp16", "--still"
        ]
        subprocess.run(cmd, check=True)
        newest = max(Path(out_mp4).parent.glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        newest.rename(out_mp4)

    # ---------- reference video ----------
    def video2vid(self, video:str, wav:str, out_mp4:str):
        cmd = [
            "python", self.wav2lip/"inference.py",
            "--checkpoint_path", self.wav2lip/"checkpoints/wav2lip_gan.pth",
            "--face", video, "--audio", wav,
            "--outfile", out_mp4
        ]
        subprocess.run(cmd, check=True)

    # ---------- orchestration ----------
    def generate(self, mode:str, image_or_video:str, text:str|None, speaker_wav:str|None):
        tmp = Path("tmp"); tmp.mkdir(exist_ok=True)
        uid = uuid.uuid4().hex[:8]
        wav = tmp/f"{uid}.wav"
        # 1) make audio
        if text:
            self.voice_clone(text, speaker_wav or image_or_video, wav)
        else:
            shutil.copy(speaker_wav, wav)
        # 2) make video
        out = Path("outputs"); out.mkdir(exist_ok=True)
        mp4 = out/f"{uid}.mp4"
        if mode=="still":
            self.still2vid(image_or_video, wav, mp4)
        else:
            self.video2vid(image_or_video, wav, mp4)
        return str(mp4)
