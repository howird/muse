import os
from pathlib import Path
import shutil
import argparse
import demucs.api

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def process_project(project_name, input_base, output_base):
    """
    Exports a project with its directory structure, separating audio files into folders containing their stems.
    
    Args:
        project_name (str): The name of the project to export.
        input_base (str): The base input folder containing projects.
        output_base (str): The base output folder where the project will be exported.
    """
    # Initialize Demucs separator
    separator = demucs.api.Separator(model="mdx_extra", segment=12)
    
    # Define project paths
    input_base_path = Path(input_base)
    output_base_path = Path(output_base)
    project_path = input_base_path / project_name
    output_project_path = output_base_path / project_name
    
    # Ensure the output base path exists
    output_project_path.mkdir(parents=True, exist_ok=True)
    
    # Walk through the project directory
    for root, dirs, files in os.walk(project_path):
        root_path = Path(root)
        # Handle relative path even if files are directly in the root folder
        if root_path == project_path:
            relative_path = Path(".")  # Base level
        else:
            relative_path = root_path.relative_to(project_path)
        output_dir = output_project_path / relative_path
        
        # Create corresponding directory in the output
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            file_path = root_path / file
            if file_path.suffix in ('.mp3', '.wav'):  # Process only audio files
                print(f"Processing {file_path}...")
                
                origin, separated = separator.separate_audio_file(str(file_path))
                
                # Create a folder for the current song
                song_folder_name = file_path.stem
                song_output_dir = output_dir / song_folder_name
                song_output_dir.mkdir(parents=True, exist_ok=True)
                
                # Save separated stems in the song folder
                for stem, source in separated.items():
                    output_file = song_output_dir / f"{stem}.wav"
                    demucs.api.save_audio(source, str(output_file), samplerate=separator.samplerate)

                print(f"Finished processing {file_path} and saved to {song_output_dir}")
            else:
                # Copy non-audio files directly to the same folder
                shutil.copy2(file_path, output_dir / file)

    print(f"Exported project '{project_name}' to '{output_project_path}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project and export its files with separated stems.")
    parser.add_argument(
        "project_name", 
        type=str, 
        help="The name of the project to process."
    )
    parser.add_argument(
        "--input-base", 
        type=str, 
        default="projects", 
        help="Base directory containing the projects (default: 'projects')."
    )
    parser.add_argument(
        "--output-base", 
        type=str, 
        default="output", 
        help="Base directory where the output will be saved (default: 'output')."
    )
    args = parser.parse_args()

    process_project(args.project_name, args.input_base, args.output_base)
