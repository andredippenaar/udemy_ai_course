"""
Notebook Helper - Use the Learning Companion Agent directly within Jupyter notebooks
This module provides simple functions to get help while you're learning.

====================
HOW TO USE THIS FILE
====================

1. In any Jupyter notebook, add this import at the top:

    from notebook_helper import explain, experiments, teach

2. Write your code in a cell and run it (Shift+Enter)

3. In the NEXT cell, run one of these commands:

    explain()       # Get a clear explanation of what the previous cell does
    experiments()   # Get hands-on experiments to try
    teach()         # Get BOTH explanation + experiments (recommended!)

4. Learn by doing! Try the suggested experiments in new cells.

====================
EXAMPLE USAGE
====================

Cell 1:
    from notebook_helper import explain, teach
    from openai import OpenAI

Cell 2:
    openai = OpenAI()

Cell 3:
    teach()  # This will explain Cell 2 and suggest experiments!

====================
"""

from learning_agent import LearningAgent
from IPython.display import Markdown, display, HTML
import inspect

# Global agent instance
_agent = None

def get_agent():
    """Get or create the global agent instance."""
    global _agent
    if _agent is None:
        _agent = LearningAgent()
    return _agent


def explain_this_cell():
    """
    Explains the code in the cell that just ran before this one.

    Usage: Run this in the cell immediately after your code:
        explain()
    """
    agent = get_agent()

    # Get the notebook context using IPython
    from IPython import get_ipython
    ipython = get_ipython()

    # Get the execution count of the current cell
    current_execution_count = ipython.execution_count

    if current_execution_count is None or current_execution_count <= 1:
        display(Markdown("⚠️ Need at least one previous cell to explain."))
        return

    # Get the previous cell's input (execution_count - 1)
    prev_execution = current_execution_count - 1

    # input_hist_raw is a list indexed from 1, so we need to access it correctly
    try:
        if hasattr(ipython.history_manager, 'input_hist_parsed'):
            # Try parsed history first (list indexed from 1)
            prev_cell = ipython.history_manager.input_hist_parsed[prev_execution] if prev_execution < len(ipython.history_manager.input_hist_parsed) else ""
        else:
            # Fall back to In dict
            prev_cell = ipython.user_ns.get('In', {})[prev_execution] if 'In' in ipython.user_ns else ""
    except (IndexError, KeyError):
        prev_cell = ""

    if not prev_cell or not prev_cell.strip():
        display(Markdown("⚠️ Previous cell appears to be empty."))
        return

    # Clean the code
    clean_code = prev_cell.strip()

    # Generate explanation
    display(HTML("<hr style='border: 2px solid #4CAF50; margin: 20px 0;'>"))
    display(Markdown("# 🎓 Understanding This Code"))
    display(Markdown("```python\n" + clean_code + "\n```"))

    explanation = agent.explain_concept(clean_code, prev_execution, None)
    display(Markdown(explanation))


def experiments_for_this_cell():
    """
    Suggests experiments for the code in the cell that just ran before this one.

    Usage: Run this in the cell immediately after your code:
        experiments()
    """
    agent = get_agent()

    from IPython import get_ipython
    ipython = get_ipython()

    current_execution_count = ipython.execution_count

    if current_execution_count is None or current_execution_count <= 1:
        display(Markdown("⚠️ Need at least one previous cell to generate experiments for."))
        return

    prev_execution = current_execution_count - 1

    # Get the previous cell's input
    try:
        if hasattr(ipython.history_manager, 'input_hist_parsed'):
            prev_cell = ipython.history_manager.input_hist_parsed[prev_execution] if prev_execution < len(ipython.history_manager.input_hist_parsed) else ""
        else:
            prev_cell = ipython.user_ns.get('In', {})[prev_execution] if 'In' in ipython.user_ns else ""
    except (IndexError, KeyError):
        prev_cell = ""

    if not prev_cell or not prev_cell.strip():
        display(Markdown("⚠️ Previous cell appears to be empty."))
        return

    clean_code = prev_cell.strip()

    display(HTML("<hr style='border: 2px solid #FF9800; margin: 20px 0;'>"))
    display(Markdown("# 🔬 Experiments to Try"))

    experiments = agent.suggest_experiments(clean_code, prev_execution)
    display(Markdown(experiments))


def teach_me_this_cell():
    """
    Complete teaching session: both explanation and experiments.

    Usage: Run this in the cell immediately after your code:
        teach()
    """
    agent = get_agent()

    from IPython import get_ipython
    ipython = get_ipython()

    current_execution_count = ipython.execution_count

    if current_execution_count is None or current_execution_count <= 1:
        display(Markdown("⚠️ Need at least one previous cell to teach."))
        return

    prev_execution = current_execution_count - 1

    # Get the previous cell's input
    try:
        if hasattr(ipython.history_manager, 'input_hist_parsed'):
            prev_cell = ipython.history_manager.input_hist_parsed[prev_execution] if prev_execution < len(ipython.history_manager.input_hist_parsed) else ""
        else:
            prev_cell = ipython.user_ns.get('In', {})[prev_execution] if 'In' in ipython.user_ns else ""
    except (IndexError, KeyError):
        prev_cell = ""

    if not prev_cell or not prev_cell.strip():
        display(Markdown("⚠️ Previous cell appears to be empty."))
        return

    clean_code = prev_cell.strip()

    # Show the complete learning experience
    display(HTML("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h1 style='color: white; margin: 0;'>📚 Learning Companion Session</h1>
        </div>
    """))

    display(Markdown("## 📝 Your Code"))
    display(Markdown("```python\n" + clean_code + "\n```"))

    display(HTML("<hr style='border: 2px solid #4CAF50; margin: 20px 0;'>"))
    display(Markdown("## 🎓 Concept Explanation"))

    explanation = agent.explain_concept(clean_code, prev_execution, None)
    display(Markdown(explanation))

    display(HTML("<hr style='border: 2px solid #FF9800; margin: 20px 0;'>"))
    display(Markdown("## 🔬 Hands-On Experiments"))

    experiments = agent.suggest_experiments(clean_code, prev_execution)
    display(Markdown(experiments))

    display(HTML("""
        <div style='background: #e8f5e9; padding: 15px; border-radius: 5px;
                    border-left: 4px solid #4CAF50; margin: 20px 0;'>
            <strong>💡 Tip:</strong> Try the experiments in new cells below.
            Learning by doing is the most effective way to master these concepts!
        </div>
    """))


def explain_code(code_string):
    """
    Explain any code snippet directly.

    Usage:
        explain_code('''
        openai = OpenAI()
        response = openai.chat.completions.create(...)
        ''')
    """
    agent = get_agent()

    display(HTML("<hr style='border: 2px solid #4CAF50; margin: 20px 0;'>"))
    display(Markdown("# 🎓 Code Explanation"))
    display(Markdown("```python\n" + code_string + "\n```"))

    explanation = agent.explain_concept(code_string, 0, None)
    display(Markdown(explanation))


def suggest_experiments(code_string):
    """
    Get experiment suggestions for any code snippet.

    Usage:
        suggest_experiments('''
        messages = [{"role": "user", "content": "Hello"}]
        ''')
    """
    agent = get_agent()

    display(HTML("<hr style='border: 2px solid #FF9800; margin: 20px 0;'>"))
    display(Markdown("# 🔬 Experiments to Try"))

    experiments = agent.suggest_experiments(code_string, 0)
    display(Markdown(experiments))


# Convenience shortcuts
explain = explain_this_cell
experiments = experiments_for_this_cell
teach = teach_me_this_cell


def help_learning_companion():
    """Display help information about using the learning companion."""
    display(HTML("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 10px;'>
            <h1 style='color: white; margin-top: 0;'>📚 Learning Companion Help</h1>
        </div>
        <div style='background: #f5f5f5; padding: 20px; border-radius: 5px; margin-top: 10px;'>
            <h2>Quick Start</h2>
            <p>Add these imports to your notebook:</p>
            <pre style='background: white; padding: 10px; border-radius: 3px;'>from notebook_helper import explain, experiments, teach</pre>

            <h2>Functions Available</h2>

            <h3>1. 🎓 explain_this_cell() or explain()</h3>
            <p>Get a clear explanation of what your code does and why it matters.</p>
            <pre style='background: white; padding: 10px; border-radius: 3px;'>openai = OpenAI()
explain()  # Run this in the next cell</pre>

            <h3>2. 🔬 experiments_for_this_cell() or experiments()</h3>
            <p>Get hands-on experiments to try with your code.</p>
            <pre style='background: white; padding: 10px; border-radius: 3px;'>response = openai.chat.completions.create(...)
experiments()  # Run this in the next cell</pre>

            <h3>3. 📚 teach_me_this_cell() or teach()</h3>
            <p>Get both explanation AND experiments in one beautiful output.</p>
            <pre style='background: white; padding: 10px; border-radius: 3px;'>messages = [{"role": "user", "content": "Hello"}]
teach()  # Run this in the next cell</pre>

            <h3>4. explain_code(code_string)</h3>
            <p>Explain any code snippet directly.</p>
            <pre style='background: white; padding: 10px; border-radius: 3px;'>explain_code('''
    for item in list:
        print(item)
''')</pre>

            <h3>5. suggest_experiments(code_string)</h3>
            <p>Get experiments for any code snippet.</p>
            <pre style='background: white; padding: 10px; border-radius: 3px;'>suggest_experiments('x = [1, 2, 3]')</pre>

            <h2>💡 Pro Tips</h2>
            <ul>
                <li>Use these functions as you work through the labs</li>
                <li>Try the suggested experiments - they're designed to deepen your understanding</li>
                <li>Use <code>teach()</code> when you want the complete learning experience</li>
                <li>These functions analyze the <em>previous</em> cell, so run them in a new cell right after your code</li>
            </ul>
        </div>
    """))


# Show help on import
print("✅ Learning Companion loaded!")
print("📚 Type: help_learning_companion() for usage guide")
print("🚀 Quick start: explain(), experiments(), or teach()")
