import os

from flask import Flask, request, jsonify, render_template, send_from_directory

# from src.label_images import LabelImages


def init_video_controller(app: Flask):
    folder_path = "videos"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    @app.route('/videos', methods=['GET'])
    def show_videos():
        video_files = os.listdir('videos')
        return render_template('videos.html', video_files=video_files, mimetype='video/mp4')

    @app.route('/result/<filename>', methods=['GET'])
    def show_results(filename):
        image_files = os.listdir('templates/assets/result/' + filename)
        return render_template('results.html', image_files=image_files, filename=filename)

    @app.route('/videos/<filename>')
    def get_video(filename):
        return send_from_directory('videos', filename)

    @app.route('/get_image_dir/<filename>')
    def get_image_dir(filename):
        return send_from_directory('templates/assets/result/' + filename, 'videos_results')

    @app.route('/api/upload_video', methods=['POST'])
    def upload_video():
        if 'video' not in request.files:
            return "No video part", 400
        file = request.files['video']
        if file.filename == '':
            return "No selected video", 400
        if file:
            filename = file.filename
            file.save(os.path.join('videos', filename))
            # LabelImages(filename)
            return "Video uploaded successfully", 200

