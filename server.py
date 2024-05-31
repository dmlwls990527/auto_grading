from flask import Flask, request, send_from_directory, jsonify, render_template, current_app
import os
import subprocess
import tempfile
import json
import csv
import shutil

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/grade', methods=['POST'])
def grade():
    student_files = request.files.getlist('student_files')
    answers = json.loads(request.form.get('answers'))

    # 임시 파일을 생성하고, 삭제되지 않도록 설정
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as answers_file:
        json.dump(answers, answers_file)
        answers_path = answers_file.name  # 임시 파일 경로 저장

    # 임시 디렉터리를 생성하지만, 자동 삭제는 하지 않음
    tmpdirname = tempfile.mkdtemp()

    result_file = os.path.join(tmpdirname, 'result.csv')
    with open(result_file, 'w', newline='', encoding='cp949') as csvfile:
        fieldnames = ['student_id', 'student_name', 'test_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, file in enumerate(student_files):
            student_file_path = os.path.join(tmpdirname, f"student_file_{i}.pdf")
            file.save(student_file_path)

            cmd = ["python", "C:/Users/dmlwl/source/repos/capstone/src/score.py", answers_path, student_file_path]
            result = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE)
            student_info = json.loads(result.stdout)
            writer.writerow(student_info)

    # 파일 전송
    response = send_from_directory(tmpdirname, 'result.csv', as_attachment=True)

    # 파일 전송 후 처리
    def remove_files():
        try:
            shutil.rmtree(tmpdirname)  # 임시 디렉터리 삭제
            os.remove(answers_path)    # 임시 파일 삭제
        except Exception as e:
            current_app.logger.error(f"Error removing files: {e}")

    # 파일이 성공적으로 닫힌 후에 cleanup 함수 호출
    response.call_on_close(remove_files)

    return response

if __name__ == '__main__':
    app.run(debug=True)
