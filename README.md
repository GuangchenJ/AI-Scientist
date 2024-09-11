# PaperSmith

## English Usage Instructions

This project is designed to assist users in optimizing and adjusting the structure of their academic papers. We extend our heartfelt gratitude to [AI-Scientist](https://github.com/SakanaAI/AI-Scientist), as this project is developed based on [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) to facilitate document structure optimization.

If you use The [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) in your research, please cite it as follows:

```bibtex
@article{lu2024aiscientist,
  title={The {AI} {S}cientist: Towards Fully Automated Open-Ended Scientific Discovery},
  author={Lu, Chris and Lu, Cong and Lange, Robert Tjarko and Foerster, Jakob and Clune, Jeff and Ha, David},
  journal={arXiv preprint arXiv:2408.06292},
  year={2024}
}
```
### Instructions for Use

#### Setting Environment Variables

First, using **OpenAI API** as an example, we need to set up the relevant environment variables:

```bash
export OPENAI_API_KEY="sk-*****"
export OPENAI_BASE_URL="https://api.***.com/v1"
export OPENAI_API_BASE="https://api.***.com/v1"
```

#### Adding Modifications

Place the LaTeX file content of the article you wish to improve in `./templates/<YOUR_PROJECT_NAME>/sources/source_latex.tex`, and the corresponding BibTeX file content in `./templates/<YOUR_PROJECT_NAME>/sources/source_reference.bib`.

> For instance, if your project name is `<YOUR_PROJECT_NAME> = manuscript`, the respective file paths would be [`./templates/manuscript/sources/source_latex.tex`](./templates/manuscript/sources/source_latex.tex) and [`./templates/manuscript/sources/source_reference.bib`](./templates/manuscript/sources/source_reference.bib).

#### Configuring Program Parameters

In the [`docker-compose.yml`](./docker-compose.yml) file, you can set the required parameters:

```yml
command: ["--model", "openai/gpt-4o-mini-2024-07-18", "--project-name", "manuscript"]
```

Here we specify using the model `openai/gpt-4o-mini-2024-07-18` for refining the project `manuscript` (./templates/manuscript).

Available models include:

- claude-3-5-sonnet-20240620
- openai/gpt-4-turbo-2024-04-09
- openai/gpt-4o-2024-08-06
- openai/gpt-4o-mini-2024-07-18
- openai/gpt-3.5-turbo-0613
- deepseek-coder-v2-0724
- llama3.1-405b
- bedrock/anthropic.claude-3-sonnet-20240229-v1:0
- bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
- bedrock/anthropic.claude-3-haiku-20240307-v1:0
- bedrock/anthropic.claude-3-opus-20240229-v1:0
- vertex_ai/claude-3-opus@20240229
- vertex_ai/claude-3-5-sonnet@20240620
- vertex_ai/claude-3-sonnet@20240229
- vertex_ai/claude-3-haiku@20240307

> **Note**: When using models other than OpenAI, ensure that the respective API and URL settings are correct, as some models may not guarantee compatibility.

#### Running the Program Through Docker

Then, run the project through `docker compose`:

```bash
docker compose up
```

> If Docker is not installed, please refer to the official website tutorial: [Get Started with Docker](https://www.docker.com/get-started/)

The generated files will be saved in the `./results` folder.

#### Special Reminder

**Note**: The revised paper may still contain errors. Please review carefully and make any necessary corrections.

#### Acknowledgements

Special thanks to Researcher [@Shuyue Hu](https://shuyuehu.github.io/index.html) for the significant support and assistance with this project. 

## 中文使用说明

本项目旨在协助用户优化和调整论文结构。
我们衷心感谢 [AI-Scientist](https://github.com/SakanaAI/AI-Scientist)，因为本项目正是基于 [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) 开发，以辅助文档结构优化。

如果您在研究中采用了 [AI-Scientist](https://github.com/SakanaAI/AI-Scientist)，请使用以下方式引用其成果：

```bibtex
@article{lu2024aiscientist,
  title={The {AI} {S}cientist: Towards Fully Automated Open-Ended Scientific Discovery},
  author={Lu, Chris and Lu, Cong and Lange, Robert Tjarko and Foerster, Jakob and Clune, Jeff and Ha, David},
  journal={arXiv preprint arXiv:2408.06292},
  year={2024}
}
```

### 使用说明

#### 设定环境变量

首先以 **OpenAI API** 为例，我们需要配置相关的环境变量：

```bash
export OPENAI_API_KEY="sk-*****"
export OPENAI_BASE_URL="https://api.***.com/v1"
export OPENAI_API_BASE="https://api.***.com/v1"
```

#### 添加更改内容

将需要改进的文章的 LaTeX 文件内容置于  `./templates/<YOUR_PROJECT_NAME>/sources/source_latex.tex` 中，相应的 BibTeX 文件内容置于 `./templates/<YOUR_PROJECT_NAME>/sources/source_reference.bib`

> 例如，若您的项目名称为 `<YOUR_PROJECT_NAME> = manuscript`，相关文件路径分别为 [`./templates/manuscript/source_latex.tex`](./templates/manuscript/sources/source_latex.tex) 和 [`./templates/manuscript/source_reference.bib`](./templates/manuscript/sources/source_reference.bib)

#### 配置程序参数

在 [`docker-compose.yml`](./docker-compose.yml)  文件中，您可以设置所需的参数，例如修改模型参数等：

```yml
command: ["--model", "openai/gpt-4o-mini-2024-07-18", "--project-name", "manuscript"]
```

这里设定使用模型 `openai/gpt-4o-mini-2024-07-18` 对于项目 `manuscript`(./templates/manuscript) 进行润色改进。

可用的模型如下：

- claude-3-5-sonnet-20240620
- openai/gpt-4-turbo-2024-04-09
- openai/gpt-4o-2024-08-06
- openai/gpt-4o-mini-2024-07-18
- openai/gpt-3.5-turbo-0613
- deepseek-coder-v2-0724
- llama3.1-405b
- bedrock/anthropic.claude-3-sonnet-20240229-v1:0
- bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
- bedrock/anthropic.claude-3-haiku-20240307-v1:0
- bedrock/anthropic.claude-3-opus-20240229-v1:0
- vertex_ai/claude-3-opus@20240229
- vertex_ai/claude-3-5-sonnet@20240620
- vertex_ai/claude-3-sonnet@20240229
- vertex_ai/claude-3-haiku@20240307

> **注意**: 使用除 OpenAI 之外的其他模型时，需要确保相应的 API 和 URL 配置正确，部分模型可能无法保证兼容性。

如果在中国大陆境内，可以考虑向 [`pyproject.toml`](./pyproject.toml) 文件中添加

```toml
[[tool.rye.sources]]
name = "mirrors.tuna"
url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/"
```

来加快 docker 镜像的构建速度。

#### 通过 Docker 运行程序

然后通过 `docker compose` 来运行该项目： 

```bash
docker compose up
```

> 如未安装 docker，请参见官方网站教程：[Get Started with Docker](https://www.docker.com/get-started/)

生成的文件将保存在 `./results` 文件夹中。

#### 特别提醒

**注意**：修订后的论文可能仍包含错误，请仔细检查并进行必要的修改！！！

#### 致谢

特别感谢 [@Shuyue Hu](https://shuyuehu.github.io/index.html) 对本项目的大力支持和帮助。
