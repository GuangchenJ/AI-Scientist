import openai
import anthropic
import os.path as osp
import shutil
import json
import argparse
import os
import sys
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
from datetime import datetime
from ai_scientist.perform_writeup import perform_writeup, generate_latex
from ai_scientist.perform_review import perform_review, load_paper, perform_improvement
from utils import insert_references

def print_time():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run AI scientist experiments")
    parser.add_argument(
        "--model",
        type=str,
        default="openai/gpt-4o-2024-08-06",
        choices=[
            "claude-3-5-sonnet-20240620",
            "openai/gpt-4-turbo-2024-04-09",
            "openai/gpt-4o-2024-08-06",
            "openai/gpt-4o-mini-2024-07-18",
            "openai/gpt-3.5-turbo-0613",
            "deepseek-coder-v2-0724",
            "llama3.1-405b",
            # Anthropic Claude models via Amazon Bedrock
            "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
            "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            "bedrock/anthropic.claude-3-haiku-20240307-v1:0",
            "bedrock/anthropic.claude-3-opus-20240229-v1:0"
            # Anthropic Claude models Vertex AI
            "vertex_ai/claude-3-opus@20240229",
            "vertex_ai/claude-3-5-sonnet@20240620",
            "vertex_ai/claude-3-sonnet@20240229",
            "vertex_ai/claude-3-haiku@20240307",
        ],
        help="Model to use for AI Scientist.",
    )
    parser.add_argument(
        "--writeup",
        type=str,
        default="latex",
        choices=["latex"],
        help="What format to use for writeup",
    )
    parser.add_argument(
        "--project-name",
        type=str,
        default="PGG-VE-Chaos",
        help="The project name for polish",
    )
    parser.add_argument(
        "--improvement",
        action="store_true",
        help="Improve based on reviews.",
    )
    # 捕获额外的未知参数
    parser.add_argument('--f', type=str, help=argparse.SUPPRESS)
    args, _ = parser.parse_known_args()
    return args


def choose_model(_model: str):
    # Create client
    if _model == "claude-3-5-sonnet-20240620":
        print(f"Using Anthropic API with model {_model}.")
        client_model = "claude-3-5-sonnet-20240620"
        client = anthropic.Anthropic()
    elif _model.startswith("bedrock") and "claude" in _model:
        # Expects: bedrock/<MODEL_ID>
        client_model = _model.split("/")[-1]

        print(f"Using Amazon Bedrock with model {client_model}.")
        client = anthropic.AnthropicBedrock(
            aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.getenv("AWS_REGION_NAME"),
        )
    elif _model.startswith("vertex_ai") and "claude" in _model:
        # Expects: vertex_ai/<MODEL_ID>
        client_model = _model.split("/")[-1]

        print(f"Using Vertex AI with model {client_model}.")
        client = anthropic.AnthropicVertex()
    elif _model.startswith("openai") and "gpt" in _model:
        # Expects: openai/<MODEL_ID>
        client_model = _model.split("/")[-1]

        print(f"Using OpenAI API with model {client_model}.")
        client = openai.OpenAI()
    elif _model == "deepseek-coder-v2-0724":
        print(f"Using OpenAI API with {_model}.")
        client_model = "deepseek-coder-v2-0724"
        client = openai.OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com"
        )
    elif _model == "llama3.1-405b":
        print(f"Using OpenAI API with {_model}.")
        client_model = "meta-llama/llama-3.1-405b-instruct"
        client = openai.OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        raise ValueError(f"Model {_model} not supported.")
    return client, client_model


def do_refine(
    project_name,
    base_dir,
    results_dir,
    model,
    writeup,
    improvement=True,
    log_file=False,
):
    # CREATE PROJECT FOLDER
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    item_name = f"{timestamp}_{project_name}"
    folder_name = osp.join(results_dir, item_name)
    print(f"folder_name: {folder_name}")
    assert not osp.exists(folder_name), f"Folder {
        folder_name} already exists."
    destination_dir = folder_name
    shutil.copytree(base_dir, destination_dir, dirs_exist_ok=True)

    if log_file:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        log_path = osp.join(folder_name, "log.txt")
        log = open(log_path, "a")
        sys.stdout = log
        sys.stderr = log

    source_latex = osp.join(folder_name, "sources", "source_latex.tex")
    source_reference = osp.join(
        folder_name, "sources", "source_reference.bib")

    print(f"source_latex: {source_latex}")
    print(f"source_reference: {source_reference}")

    try:
        print_time()
        print(f"*Starting project: {item_name}*")
        # PERFORM EXPERIMENTS
        io = InputOutput(
            yes=True, chat_history_file=f"{folder_name}/{item_name}_aider.txt"
        )
        print_time()
        print(f"*Starting Writeup*")
        if writeup == "latex":
            writeup_file = osp.join(folder_name, "latex", "template.tex")
            # a list of files to add to the chat
            fnames = [writeup_file, source_latex, source_reference]
            if model == "deepseek-coder-v2-0724":
                main_model = Model("deepseek/deepseek-coder")
            elif model == "llama3.1-405b":
                main_model = Model(
                    "openrouter/meta-llama/llama-3.1-405b-instruct")
            else:
                main_model = Model(model)

            insert_references(writeup_file, source_reference, writeup_file)
            coder = Coder.create(
                main_model=main_model,
                fnames=fnames,
                io=io,
                stream=False,
                use_git=False,
                edit_format="diff",
            )
            try:
                perform_writeup(project_name, folder_name, coder)
            except Exception as e:
                print(f"Failed to perform writeup: {e}")
                return False
            print("Done writeup")
        else:
            raise ValueError(f"Writeup format {writeup} not supported.")

        print_time()
        print(f"*Starting Review*")
        # REVIEW PAPER
        if args.writeup == "latex":
            try:
                paper_text = load_paper(
                    f"{folder_name}/{project_name}.pdf")
                print("---------")
                review = perform_review(
                    paper_text,
                    model=model,
                    client=openai.OpenAI(),
                    num_reflections=5,
                    num_fs_examples=1,
                    num_reviews_ensemble=5,
                    temperature=0.1,
                )
                # Store the review in separate review.txt file
                with open(osp.join(folder_name, "review.txt"), "w") as f:
                    f.write(json.dumps(review, indent=4))
            except Exception as e:
                print(f"Failed to perform review: {e}")
                return False
            # IMPROVE WRITEUP
            if writeup == "latex" and improvement:
                print_time()
                print(f"*Starting Improvement*")
                try:
                    perform_improvement(review, coder)
                    generate_latex(
                        coder, folder_name, f"{
                            folder_name}/{project_name}_improved.pdf"
                    )
                    paper_text = load_paper(
                        f"{folder_name}/{project_name}_improved.pdf")
                    review = perform_review(
                        paper_text,
                        model=model,
                        client=openai.OpenAI(),
                        num_reflections=5,
                        num_fs_examples=1,
                        num_reviews_ensemble=5,
                        temperature=0.1,
                    )
                    # Store the review in separate review.txt file
                    with open(osp.join(folder_name, "review_improved.txt"), "w") as f:
                        f.write(json.dumps(review))
                except Exception as e:
                    print(f"Failed to perform improvement: {e}")
    except Exception as e:
        print(f"Failed to evaluate project {project_name}: {str(e)}")
        return False
    finally:
        print("FINISHED PROJECT")
        if log_file:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            log.close()


if __name__ == "__main__":
    args = parse_arguments()
    client, client_model = choose_model(args.model)

    base_dir = osp.join("templates", args.project_name)
    results_dir = osp.join("results", args.project_name)

    print(f"base_dir: {base_dir}")
    print(f"results_dir: {results_dir}")

    print(f"Processing project: {args.project_name}")
    try:
        success = do_refine(
            args.project_name,
            base_dir,
            results_dir,
            client_model,
            args.writeup,
        )
        print(f"Completed project: {args.project_name}, Success: {success}")
    except Exception as e:
        print(f"Failed to evaluate idea {args.project_name}: {str(e)}")
