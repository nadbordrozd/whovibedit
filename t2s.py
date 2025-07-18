import pandas as pd
import traceback
import sys
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

# Your system prompt goes here
SYSTEM_PROMPT = """
[YOUR SYSTEM PROMPT WITH TABLE DESCRIPTIONS AND INSTRUCTIONS]

When you receive execution results, analyze them and:
1. If there are errors, debug and provide corrected code
2. If results look unexpected (empty, wrong format, missing data), investigate and adapt
3. If results are good, proceed with analysis/visualization as requested
4. Always explain what you discovered from the execution results
"""

conversation_history = []

def execute_generated_code(code_string, globals_dict=None):
    """Execute Python code and capture results, errors, and outputs"""
    if globals_dict is None:
        globals_dict = {'query': query, 'pd': pd, 'plt': plt, 'sns': sns}
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    result = {
        'success': False,
        'output': None,
        'stdout': '',
        'error': None,
        'variables': {}
    }
    
    try:
        # Execute the code
        exec(code_string, globals_dict)
        
        # Capture any printed output
        result['stdout'] = captured_output.getvalue()
        
        # Look for common variable names that might contain results
        for var_name in ['df', 'result', 'data', 'results']:
            if var_name in globals_dict and isinstance(globals_dict[var_name], pd.DataFrame):
                result['variables'][var_name] = globals_dict[var_name]
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
        result['traceback'] = traceback.format_exc()
    
    finally:
        sys.stdout = old_stdout
    
    return result

def format_execution_results(execution_result):
    """Format execution results for LLM consumption"""
    feedback = []
    
    if execution_result['success']:
        feedback.append("✅ Code executed successfully")
        
        # Add stdout output
        if execution_result['stdout'].strip():
            feedback.append(f"Printed output:\n{execution_result['stdout']}")
        
        # Analyze DataFrames
        for var_name, df in execution_result['variables'].items():
            feedback.append(f"\n📊 Variable '{var_name}' contains:")
            feedback.append(f"  - Shape: {df.shape}")
            feedback.append(f"  - Columns: {list(df.columns)}")
            
            # Show data preview
            if len(df) > 0:
                feedback.append(f"  - First 3 rows:\n{df.head(3).to_string()}")
                
                # Basic statistics
                feedback.append(f"  - Null counts: {df.isnull().sum().to_dict()}")
                
                # Data types
                feedback.append(f"  - Data types: {df.dtypes.to_dict()}")
                
                # Flag potential issues
                if df.empty:
                    feedback.append("  ⚠️  WARNING: DataFrame is empty")
                elif df.isnull().all().any():
                    null_cols = df.columns[df.isnull().all()].tolist()
                    feedback.append(f"  ⚠️  WARNING: Columns with all nulls: {null_cols}")
            else:
                feedback.append("  ⚠️  WARNING: DataFrame is empty")
    
    else:
        feedback.append("❌ Code execution failed")
        feedback.append(f"Error: {execution_result['error']}")
        feedback.append(f"Traceback:\n{execution_result['traceback']}")
    
    return "\n".join(feedback)

def get_llm_response(messages):
    """
    Replace this with your actual LLM API call
    This is a placeholder that should call your preferred LLM
    """
    # Example for OpenAI:
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=messages
    # )
    # return response.choices[0].message.content
    
    # For now, return a placeholder
    return "LLM response would go here"

def analyze_with_feedback(user_query, max_iterations=3):
    """Main function that handles the feedback loop"""
    
    # Initialize conversation with system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add user query
    messages.append({"role": "user", "content": user_query})
    
    print(f"🔄 Analyzing: {user_query}")
    print("=" * 50)
    
    for iteration in range(max_iterations):
        print(f"\n🤖 Iteration {iteration + 1}")
        
        # Get LLM response
        llm_response = get_llm_response(messages)
        print(f"LLM Response: {llm_response}")
        
        # Extract code blocks (assume they're in ```python blocks)
        code_blocks = []
        lines = llm_response.split('\n')
        in_code_block = False
        current_code = []
        
        for line in lines:
            if line.strip().startswith('```python'):
                in_code_block = True
                current_code = []
            elif line.strip() == '```' and in_code_block:
                in_code_block = False
                if current_code:
                    code_blocks.append('\n'.join(current_code))
            elif in_code_block:
                current_code.append(line)
        
        # Execute each code block
        execution_results = []
        for i, code in enumerate(code_blocks):
            print(f"\n💻 Executing code block {i+1}:")
            print(code)
            print("\n" + "—" * 30)
            
            result = execute_generated_code(code)
            execution_results.append(result)
            
            # Format and display results
            formatted_result = format_execution_results(result)
            print(formatted_result)
        
        # If no code blocks found, this might be a clarification or final response
        if not code_blocks:
            print("No code blocks found - LLM may be asking for clarification or providing final answer")
            break
        
        # Check if all executions were successful
        all_successful = all(result['success'] for result in execution_results)
        
        if all_successful:
            # Check if results look reasonable (not empty, no major warnings)
            needs_iteration = False
            for result in execution_results:
                for var_name, df in result['variables'].items():
                    if df.empty or df.isnull().all().any():
                        needs_iteration = True
                        break
            
            if not needs_iteration:
                print(f"\n✅ Analysis completed successfully in {iteration + 1} iterations")
                break
        
        # Prepare feedback for next iteration
        if iteration < max_iterations - 1:  # Don't add feedback on last iteration
            feedback_message = "EXECUTION RESULTS:\n"
            for i, result in enumerate(execution_results):
                feedback_message += f"\nCode block {i+1} results:\n"
                feedback_message += format_execution_results(result)
            
            feedback_message += "\n\nPlease analyze these results and provide improved code if needed."
            
            # Add to conversation history
            messages.append({"role": "assistant", "content": llm_response})
            messages.append({"role": "user", "content": feedback_message})
    
    return messages

# Example usage:
def run_analysis():
    """Interactive loop for running analyses"""
    print("Text2SQL Tool with Feedback Loop")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\n🔍 What analysis would you like to perform? ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            analyze_with_feedback(user_input)
        except Exception as e:
            print(f"Error in analysis: {e}")
            traceback.print_exc()

# Run the tool
# run_analysis()
