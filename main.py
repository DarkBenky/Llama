from langchain_ollama import OllamaLLM
import subprocess

# Initialize the Ollama model
llm = OllamaLLM(model="llama3.1")

# Define the prompts for generating code and analyzing it
CODE_GENERATION_PROMPT = "crete tick tack toe game using pygame but 5 * 5 and you need to win by getting 4 in a row"
ANALYZE_PROMPT = "Analyze the following error message and suggest a fix."

def generate_code(input_text):
    """Generate Python code using AI based on the input text."""
    response = llm.invoke(input_text)
    return response

def analyze_code(code, error_message=None):
    """Analyze the generated code or errors and give feedback."""
    if error_message:
        prompt = f"{code}\nError: {error_message}\n{ANALYZE_PROMPT}"
    else:
        prompt = f"{code}\n{ANALYZE_PROMPT}"
    
    response = llm.invoke(prompt)
    return response

def save_and_run_code(code, filename="generated_game.py"):
    """Save the generated code to a file and run it."""
    with open(filename, "w") as f:
        # find the code part and write it to the file
        code = code.split("```")
        if len(code) > 1:
            code = code[1]
        else:
            code = code[0]
        code = code.strip('python\n')
        f.write(code)

    try:
        result = subprocess.run(["python", filename], capture_output=True, text=True)
        if result.returncode != 0:
            return result.stderr  # Return error message
        return result.stdout  # Return successful output
    except Exception as e:
        return str(e)


def iterative_code_generation():
    """Main loop to generate code, analyze errors, and retry."""
    steps = generate_code(CODE_GENERATION_PROMPT + " analyze the input and give me steps to follow")
    print("Steps to follow:\n", steps)

    generated_code = generate_code(CODE_GENERATION_PROMPT + " write the code for me based on the steps" + steps + "Provide only the code")
    print("Generated Code:\n", generated_code)

    error_message = save_and_run_code(generated_code)

    retry_attempts = 20
    while error_message and retry_attempts > 0:
        print(f"Error encountered:\n{error_message}")
        analyzed_response = analyze_code(generated_code, error_message)
        print(f"AI Suggestions:\n{analyzed_response}")

        generated_code = generate_code(analyzed_response + " write the updated code based on the suggestions, and provide only the code original code:" + generated_code)
        print("Retrying with updated code...")
        error_message = save_and_run_code(generated_code)
        retry_attempts -= 1

    if not error_message:
        print("Code ran successfully!")
    else:
        print("Failed after multiple attempts.")

# Start the iterative process
iterative_code_generation()
