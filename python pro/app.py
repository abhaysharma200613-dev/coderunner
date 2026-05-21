from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

HTML_TEMPLATE = '''

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Advanced AI Code Analyzer</title>

    <style>

        body{
            background:#0f172a;
            font-family:Arial,sans-serif;
            color:white;
            margin:0;
            padding:0;
        }

        .container{
            width:90%;
            max-width:1200px;
            margin:30px auto;
            background:#1e293b;
            padding:25px;
            border-radius:15px;
            box-shadow:0px 0px 15px rgba(0,0,0,0.4);
        }

        h1{
            text-align:center;
            color:#38bdf8;
        }

        textarea{
            width:100%;
            height:320px;
            background:#020617;
            color:#22c55e;
            border:1px solid #334155;
            border-radius:10px;
            padding:15px;
            font-size:15px;
            resize:vertical;
        }

        button{
            width:100%;
            margin-top:20px;
            padding:15px;
            border:none;
            border-radius:10px;
            background:#38bdf8;
            color:black;
            font-size:18px;
            font-weight:bold;
            cursor:pointer;
        }

        button:hover{
            background:#0ea5e9;
        }

        .card{
            background:#0f172a;
            padding:20px;
            margin-top:20px;
            border-radius:12px;
        }

        .score{
            font-size:45px;
            color:#22c55e;
            font-weight:bold;
        }

        ul{
            padding-left:20px;
        }

        li{
            margin-bottom:20px;
        }

        pre{
            background:#020617;
            color:#22c55e;
            padding:15px;
            border-radius:10px;
            overflow-x:auto;
        }

        .error-title{
            color:#ef4444;
            font-size:20px;
            font-weight:bold;
        }

        .solution{
            color:#38bdf8;
            margin-top:10px;
        }

        .footer{
            text-align:center;
            margin-top:20px;
            color:gray;
        }

    </style>

</head>

<body>

    <div class="container">

        <h1>⚡ Advanced AI Code Analyzer</h1>

        <form method="POST">

            <textarea name="code" placeholder="Paste Python code here...">{{ code }}</textarea>

            <button type="submit">Analyze Code</button>

        </form>

        {% if analyzed %}

        <div class="card">

            <h2>📊 Code Score</h2>

            <div class="score">{{ score }}/100</div>

        </div>

        <div class="card">

            <h2>❌ Errors & Solutions</h2>

            {% if errors %}

                <ul>

                    {% for error in errors %}

                    <li>

                        <div class="error-title">
                            {{ error.title }}
                        </div>

                        <br>

                        <strong>Error:</strong>

                        {{ error.message }}

                        {% if error.line_number %}

                        <br><br>

                        <strong>Line Number:</strong>

                        {{ error.line_number }}

                        {% endif %}

                        {% if error.error_line %}

                        <br><br>

                        <strong>Error Line:</strong>

                        <pre>{{ error.error_line }}</pre>

                        {% endif %}

                        <br>

                        <strong>How To Fix:</strong>

                        <div class="solution">
                            {{ error.solution }}
                        </div>

                    </li>

                    {% endfor %}

                </ul>

            {% else %}

                <p>No errors found ✅</p>

            {% endif %}

        </div>

        <div class="card">

            <h2>⚡ Optimization Suggestions</h2>

            {% if suggestions %}

                <ul>

                    {% for suggestion in suggestions %}
                        <li>{{ suggestion }}</li>
                    {% endfor %}

                </ul>

            {% else %}

                <p>Code looks optimized 🚀</p>

            {% endif %}

        </div>

        <div class="card">

            <h2>🚀 Optimized Code</h2>

            <pre>{{ optimized_code }}</pre>

        </div>

        <div class="card">

            <h2>📈 Code Statistics</h2>

            <p><strong>Total Lines:</strong> {{ stats.lines }}</p>

            <p><strong>Functions:</strong> {{ stats.functions }}</p>

            <p><strong>Loops:</strong> {{ stats.loops }}</p>

            <p><strong>Comments:</strong> {{ stats.comments }}</p>

        </div>

        {% endif %}

        <div class="footer">
            Made with Python + Flask 🚀
        </div>

    </div>

</body>

</html>

'''

def analyze_code(code):

    errors = []
    suggestions = []
    optimized_code = code
    score = 100

    lines = code.split('\n')

    # --------------------------------
    # Syntax Error Detection
    # --------------------------------

    try:
        compile(code, '<string>', 'exec')

    except SyntaxError as e:

        error_line = ""

        if e.lineno and e.lineno <= len(lines):
            error_line = lines[e.lineno - 1]

        errors.append({

            "title": "Syntax Error",

            "message": e.msg,

            "line_number": e.lineno,

            "error_line": error_line,

            "solution":
            "Check brackets, indentation, colons or operators."

        })

        score -= 25

    # --------------------------------
    # Global Variable Detection
    # --------------------------------

    if 'global ' in code:

        errors.append({

            "title": "Global Variable Usage",

            "message":
            "Using global variables makes code difficult to maintain.",

            "line_number": "",

            "error_line": "",

            "solution":
            "Use function parameters and return values instead."

        })

        optimized_code = optimized_code.replace(
            'global ',
            '# Removed global variable: '
        )

        score -= 10

    # --------------------------------
    # Infinite Loop Detection
    # --------------------------------

    if 'while True' in code:

        errors.append({

            "title": "Infinite Loop",

            "message":
            "while True may create unnecessary infinite execution.",

            "line_number": "",

            "error_line": "while True",

            "solution":
            "Use a condition-based loop."

        })

        optimized_code = optimized_code.replace(
            'while True',
            'while condition'
        )

        score -= 10

    # --------------------------------
    # range(len()) Optimization
    # --------------------------------

    if 'range(len(' in code:

        errors.append({

            "title": "Inefficient Loop",

            "message":
            "Using range(len()) increases time complexity.",

            "line_number": "",

            "error_line": "for i in range(len(...))",

            "solution":
            "Use enumerate() instead."

        })

        optimized_code = optimized_code.replace(
            'for i in range(len(numbers)):',
            'for i, value in enumerate(numbers):'
        )

        score -= 5

    # --------------------------------
    # Missing Comments
    # --------------------------------

    if '#' not in code:

        suggestions.append(
            "Add comments for better readability."
        )

        score -= 5

    # --------------------------------
    # Large Code Detection
    # --------------------------------

    if len(lines) > 50:

        suggestions.append(
            "Split large code into smaller reusable functions."
        )

        score -= 10

    # --------------------------------
    # Unused Variable Detection
    # --------------------------------

    variables = re.findall(r'(\w+)\s*=', code)

    unused_vars = []

    for var in variables:

        occurrences = len(
            re.findall(rf'\b{var}\b', code)
        )

        if occurrences == 1:
            unused_vars.append(var)

    if unused_vars:

        errors.append({

            "title": "Unused Variables",

            "message":
            f"Unused variables found: {', '.join(unused_vars)}",

            "line_number": "",

            "error_line": "",

            "solution":
            "Remove unused variables to reduce memory usage."

        })

        score -= 10

    # --------------------------------
    # Complexity Analysis
    # --------------------------------

    loop_count = len(
        re.findall(r'for\s|while\s', code)
    )

    if loop_count > 3:

        suggestions.append(
            "High loop usage detected. Reduce nested loops."
        )

        score -= 10

    # --------------------------------
    # Statistics
    # --------------------------------

    stats = {

        "lines": len(lines),

        "functions": len(
            re.findall(r'def\s+\w+\(', code)
        ),

        "loops": loop_count,

        "comments": len(
            re.findall(r'#', code)
        )

    }

    # --------------------------------
    # Score Protection
    # --------------------------------

    if score < 0:
        score = 0

    return (
        errors,
        suggestions,
        optimized_code,
        score,
        stats
    )

@app.route('/', methods=['GET', 'POST'])

def home():

    analyzed = False

    errors = []
    suggestions = []
    optimized_code = ''

    score = 0

    stats = {}

    code = ''

    if request.method == 'POST':

        code = request.form['code']

        analyzed = True

        (
            errors,
            suggestions,
            optimized_code,
            score,
            stats

        ) = analyze_code(code)

    return render_template_string(

        HTML_TEMPLATE,

        analyzed=analyzed,

        errors=errors,

        suggestions=suggestions,

        optimized_code=optimized_code,

        score=score,

        stats=stats,

        code=code

    )

if __name__ == '__main__':

    print("Starting Advanced AI Code Analyzer...")

    app.run(host='127.0.0.1', port=5000, debug=True)