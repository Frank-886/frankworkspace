from flask import Flask, render_template_string, request
import random
import time
import webbrowser
from threading import Timer

app = Flask(__name__)

# 全局变量
score = 0
question_count = 0
start_time = 0
questions = []
current_question = None

def generate_questions():
    """生成20道数学题"""
    global questions
    questions = []
    for _ in range(20):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        op = random.choice(['+', '-'])
        
        # 确保减法结果为正数
        if op == '-' and a < b:
            a, b = b, a
            
        questions.append((a, op, b))

def get_progress():
    """获取进度信息"""
    elapsed = round(time.time() - start_time, 1)
    return f"进度: {question_count+1}/20 | 得分: {score} | 用时: {elapsed}秒"

def get_final_results():
    """获取最终结果"""
    total_time = round(time.time() - start_time, 1)
    avg_time = round(total_time / 20, 1)
    
    result = {
        'score': score,
        'total_time': total_time,
        'avg_time': avg_time
    }
    
    # 根据得分添加评语
    if score == 20:
        result['comment'] = "🌟 太棒了！满分！"
    elif score >= 15:
        result['comment'] = "👍 很好！继续努力！"
    elif score >= 10:
        result['comment'] = "💪 还不错，再加把劲！"
    else:
        result['comment'] = "✏️ 需要多多练习哦！"
    
    return result

@app.route('/', methods=['GET', 'POST'])
def math_quiz():
    global score, question_count, start_time, current_question
    
    if request.method == 'POST':
        # 处理答案提交
        if 'answer' in request.form:
            try:
                user_answer = int(request.form['answer'])
                a, op, b = current_question
                
                # 计算正确答案
                if op == '+':
                    correct = a + b
                else:
                    correct = a - b
                
                # 检查答案
                if user_answer == correct:
                    score += 1
                    feedback = "✓ 回答正确！"
                else:
                    feedback = f"✗ 回答错误！正确答案是: {correct}"
                
                question_count += 1
                
            except ValueError:
                feedback = "请输入有效的数字！"
                return render_template_string(TEMPLATE, 
                    question=current_question,
                    progress=get_progress(),
                    feedback=feedback)
        
        # 处理重新开始
        elif 'restart' in request.form:
            score = 0
            question_count = 0
            start_time = time.time()
            generate_questions()
    
    # 显示下一题或结果
    if question_count < len(questions):
        current_question = questions[question_count]
        a, op, b = current_question
        question_str = f"{a} {op} {b} = ?"
        return render_template_string(TEMPLATE, 
            question=question_str,
            progress=get_progress(),
            feedback=None)
    else:
        results = get_final_results()
        return render_template_string(RESULT_TEMPLATE, results=results)

def open_browser():
    """在默认浏览器中打开应用"""
    webbrowser.open_new('http://127.0.0.1:5000/')

# HTML模板
TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>一年级数学练习</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .question {
            font-size: 24px;
            margin: 20px 0;
        }
        input {
            font-size: 20px;
            padding: 8px;
            width: 100px;
            text-align: center;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px;
        }
        .progress {
            margin: 20px 0;
            font-size: 16px;
        }
        .feedback {
            margin: 10px 0;
            font-size: 18px;
            min-height: 30px;
        }
        .correct {
            color: green;
        }
        .incorrect {
            color: red;
        }
    </style>
</head>
<body>
    <h1>一年级数学练习</h1>
    <div class="progress">{{ progress }}</div>
    <div class="question">{{ question }}</div>
    <form method="POST">
        <input type="text" name="answer" autocomplete="off" autofocus>
        <button type="submit">提交</button>
    </form>
    <div class="feedback">
        {% if feedback %}
            {% if '✓' in feedback %}
                <span class="correct">{{ feedback }}</span>
            {% else %}
                <span class="incorrect">{{ feedback }}</span>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
'''

RESULT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>练习结果</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .results {
            font-size: 18px;
            margin: 20px 0;
            line-height: 1.6;
        }
        .comment {
            font-size: 24px;
            margin-top: 20px;
            font-weight: bold;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>练习结果</h1>
    <div class="results">
        得分: {{ results.score }}/20<br>
        总用时: {{ results.total_time }}秒<br>
        平均每题用时: {{ results.avg_time }}秒
    </div>
    <div class="comment">{{ results.comment }}</div>
    <form method="POST">
        <button type="submit" name="restart">重新开始</button>
    </form>
</body>
</html>
'''

if __name__ == '__main__':
    # 初始化题目
    generate_questions()
    start_time = time.time()
    
    # 启动浏览器
    Timer(1, open_browser).start()
    
    # 启动Flask应用
    app.run(debug=True)