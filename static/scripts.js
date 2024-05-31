document.addEventListener("DOMContentLoaded", function () {
    // DOM 요소에 대한 참조를 가져옵니다.
    const generateButton = document.getElementById("generate-answer-inputs");
    const answerInputsContainer = document.getElementById("answer-inputs-container");
    const gradeButton = document.getElementById("grade-btn");
    const gradingResult = document.getElementById("grading-result");

    generateButton.addEventListener("click", function () {
        const numAnswers = parseInt(document.getElementById("num_of_answers").value, 10);
        if (!isNaN(numAnswers) && numAnswers > 0) {
            generateAnswerInputs(numAnswers);
        } else {
            alert("올바른 문제 수를 입력하세요.");
        }
    });

    gradeButton.addEventListener("click", function () {
        const answers = getAnswers();
        const studentFilesInput = document.getElementById("student_files");
        const studentFiles = studentFilesInput.files;

        if (studentFiles.length === 0) {
            alert('학생 답안 파일을 업로드하세요.');
            return;
        }

        const formData = new FormData();
        formData.append('answers', JSON.stringify(answers));
        for (let i = 0; i < studentFiles.length; i++) {
            formData.append('student_files', studentFiles[i]);
        }

        fetch('/grade', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'result.csv';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            })
            .catch(error => {
                console.error('채점 요청 중 오류 발생:', error);
                alert('채점 중에 오류가 발생했습니다. 나중에 다시 시도하세요.');
            });
    });

    function generateAnswerInputs(numAnswers) {
        answerInputsContainer.innerHTML = "";
        for (let i = 1; i <= numAnswers; i++) {
            const answerInput = document.createElement("input");
            answerInput.type = "text";
            answerInput.placeholder = `정답 ${i}`;
            answerInput.className = "file-input";
            answerInput.name = `answer_${i}`;
            answerInputsContainer.appendChild(answerInput);
        }
    }

    function getAnswers() {
        const answerInputs = document.querySelectorAll("#answer-inputs-container input");
        const answers = [];
        for (const input of answerInputs) {
            answers.push(input.value);
        }
        return answers;
    }
});
