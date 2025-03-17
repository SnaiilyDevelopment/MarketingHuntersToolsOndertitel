from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
from logic.spreek_logic import srt_to_cleaned_word
from logic.subtitle_modifier_logic import modify_subtitles
from logic.syncsrt_logic import sync_srt

app = Flask(__name__)

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spreek')
def spreek():
    return render_template('spreek.html')

@app.route('/run_spreek', methods=['POST'])
def run_spreek():
    srt_files = request.files.getlist('srt_files')
    output_file_name = request.form['output_file_name']
    output_file_path = os.path.join(TOOLS_DIR, 'uploads', output_file_name + '.docx')

    srt_file_paths = []
    for srt_file in srt_files:
        srt_file_path = os.path.join(TOOLS_DIR, 'uploads', srt_file.filename)
        try:
            srt_file.save(srt_file_path)
            srt_file_paths.append(srt_file_path)
        except Exception as e:
            return render_template('spreek.html', result=f"Error saving file: {e}")

    try:
        srt_to_cleaned_word(srt_file_paths, output_file_path)
        return send_file(output_file_path, as_attachment=True, download_name=output_file_name + '.docx')
    except Exception as e:
        return render_template('spreek.html', result=f"Error: {e}")
    finally:
        # Clean up uploaded files
        for srt_file_path in srt_file_paths:
            os.remove(srt_file_path)
        try:
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
        except PermissionError as e:
            print(f"Could not delete file {output_file_path}: {e}")
    return render_template('spreek.html', result=result)

@app.route('/subtitle_modifier')
def subtitle_modifier():
    return render_template('subtitle_modifier.html')

@app.route('/run_subtitle_modifier', methods=['POST'])
def run_subtitle_modifier():
    srt_file = request.files['srt_file']
    srt_file_path = os.path.join(TOOLS_DIR, 'uploads', srt_file.filename)
    try:
        srt_file.save(srt_file_path)
    except Exception as e:
        return render_template('subtitle_modifier.html', result=f"Error saving file: {e}")

    base_name = os.path.basename(srt_file_path)
    name_without_extension = os.path.splitext(base_name)[0]
    output_file_path = os.path.join(TOOLS_DIR, 'uploads', f"{name_without_extension}_modified.srt")

    try:
        modify_subtitles(srt_file_path, output_file_path)
        return send_file(output_file_path, as_attachment=True, download_name=f"{name_without_extension}_modified.srt")
    except Exception as e:
        return render_template('subtitle_modifier.html', result=f"Error: {e}")
    finally:
        os.remove(srt_file_path)
        try:
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
        except PermissionError as e:
            print(f"Could not delete file {output_file_path}: {e}")

@app.route('/syncsrt')
def syncsrt():
    return render_template('syncsrt.html')

@app.route('/run_syncsrt', methods=['POST'])
def run_syncsrt():
    video_file = request.files['video_file']
    srt_file = request.files['srt_file']

    video_file_path = os.path.join(TOOLS_DIR, 'uploads', video_file.filename)
    try:
        video_file.save(video_file_path)
    except Exception as e:
        return render_template('syncsrt.html', result=f"Error saving video file: {e}")

    srt_file_path = os.path.join(TOOLS_DIR, 'uploads', srt_file.filename)
    try:
        srt_file.save(srt_file_path)
    except Exception as e:
        return render_template('syncsrt.html', result=f"Error saving srt file: {e}")

    output_file_name = os.path.splitext(os.path.basename(srt_file_path))[0] + "_synced.srt"
    output_file_path = os.path.join(TOOLS_DIR, 'uploads', output_file_name)

    try:
        sync_srt(video_file_path, srt_file_path, output_file_path)
        return send_file(output_file_path, as_attachment=True, download_name=output_file_name)
    except Exception as e:
        return render_template('syncsrt.html', result=f"Error: {e}")
    finally:
        os.remove(video_file_path)
        os.remove(srt_file_path)
        try:
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
        except PermissionError as e:
            print(f"Could not delete file {output_file_path}: {e}")

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"Application failed to start: {e}")
