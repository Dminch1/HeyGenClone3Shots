# HeyGen Clone

This project implements a dual-mode HeyGen clone that can generate talking head videos from either a still image or a reference video, using real-time voice cloning.

## Project Structure

```
HeyGen/
├─ requirements.txt
├─ constraints.txt
├─ pipeline.py
├─ app.py
├─ README.md
└─ models/           # (will be populated by scripts)
```

## Setup and Installation

Follow these steps to set up the environment and run the application.

### 1. Create and Activate Virtual Environment

Open your terminal or PowerShell and run the following commands:

```powershell
python -m venv venv_heygen
.\venv_heygen\Scripts\activate
```

### 2. Install Dependencies

Upgrade pip and install the required packages using the provided `requirements.txt` and `constraints.txt` files. The constraints file ensures that compatible versions of libraries are installed, avoiding potential conflicts.

```powershell
pip install --upgrade pip
pip install -r requirements.txt -c constraints.txt
```

### 3. Clone Model Repositories and Download Checkpoints

Clone the necessary repositories for voice cloning (Real-Time-Voice-Cloning), still image animation (SadTalker), and video lip-syncing (Wav2Lip). Then, run their respective setup/download scripts.

*   **Navigate to the `HeyGen` directory before running these commands if you are not already there.**

```powershell
git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning rtvc
git clone https://github.com/OpenTalker/SadTalker sadtalker
git clone https://github.com/Rudrabha/Wav2Lip wav2lip

cd sadtalker
bash scripts/download_models.sh
cd ..

cd wav2lip
python -m pip install -r requirements.txt --no-deps
cd ..
```
**Note:** The `download_models.sh` script for SadTalker might require `gdown` or other utilities. If you encounter issues, you might need to install them or download the models manually as per SadTalker's documentation. Wav2Lip's requirements are installed with `--no-deps` to avoid conflicts with the main project's locked dependencies.

The `models/` directory inside each cloned repository (e.g., `sadtalker/checkpoints`, `wav2lip/checkpoints`) will be populated with pre-trained model files. The `rtvc` models are typically downloaded on first use by the library itself or may require manual download as per its documentation.

## Running the Application

Once the setup is complete, you can run the Gradio application:

```powershell
python app.py
```

This will start a local server. Open your web browser and go to the URL displayed in the terminal (usually `http://127.0.0.1:7860`).

### Using the Interface

1.  **Choose Mode**: Select either "still" (for image-to-video) or "video" (for video-to-video).
2.  **Upload Input**:
    *   If "still" mode: Upload a clear face image using the "Face image" component.
    *   If "video" mode: Upload a reference video using the "Reference video" component.
3.  **Provide Audio Source** (at least one is required):
    *   **Text to speak**: Type the desired text into the "Text to speak" textbox. This will use the voice from the "Speaker WAV" if provided, or from the input image/video if a speaker WAV is not provided (RTVC attempts to clone from the video's audio track if it's a video).
    *   **Speaker WAV**: Upload an audio file (e.g., a 5-30 second WAV) using the "Speaker WAV" component. If text is also provided, this WAV will be used as the reference voice. If no text is provided, this audio will be directly used for lip-syncing.
4.  **Generate**: Click the "Generate" button.
5.  **Output**: The generated video will appear in the "Video" output component, and a status message will be displayed. Videos are saved in the `HeyGen/outputs` directory.

Enjoy your HeyGen-clone!
