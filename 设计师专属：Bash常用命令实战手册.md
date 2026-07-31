# 设计师专属：Bash 常用命令实战手册

## 目标：掌握 Linux/Bash 命令行，高效管理文件与代码

Cam，既然你决定将终端环境切换到 Bash，这是一个非常明智的选择！Bash 是 Linux 和 macOS 系统默认的命令行解释器，也是服务器管理、自动化脚本编写的基石。掌握 Bash 命令，能让你更高效地管理本地文件、与 Git 仓库交互，并为未来的自动化工作流打下坚实基础。

本手册将为你梳理设计师日常工作中常用的 Bash 命令，并结合你的实际场景进行解释。

---

## 一、文件与目录操作：你的数字工作台

| 命令 | 作用 | 示例 | 设计师场景 |
|---|---|---|---|
| `pwd` | **P**rint **W**orking **D**irectory，显示当前所在目录的绝对路径。 | `pwd` | 确认你当前在哪个项目文件夹下。 |
| `ls` | **L**i**s**t，列出当前目录下的文件和子目录。 | `ls -l` (显示详细信息) <br> `ls -a` (显示所有文件，包括隐藏文件) | 查看当前文件夹有哪些设计稿、素材或代码文件。 |
| `cd` | **C**hange **D**irectory，切换目录。 | `cd my_project` (进入 `my_project` 目录) <br> `cd ..` (返回上一级目录) <br> `cd ~` (回到用户主目录) <br> `cd /` (回到根目录) | 快速切换到你的设计项目文件夹、素材库或代码仓库。 |
| `mkdir` | **M**a**k**e **Dir**ectory，创建新目录。 | `mkdir new_folder` | 创建新的设计项目文件夹，如 `mkdir 05_brand_research`。 |
| `touch` | 创建空文件或更新文件时间戳。 | `touch my_notes.md` | 快速创建 Markdown 笔记文件，如 `touch day33_learning_log.md`。 |
| `cp` | **C**o**p**y，复制文件或目录。 | `cp file.txt new_folder/` (复制文件) <br> `cp -r old_folder/ new_folder/` (复制目录) | 备份设计稿，如 `cp -r arper_project_v1/ arper_project_v2_backup/`。 |
| `mv` | **M**o**v**e，移动文件或目录；也可用于重命名。 | `mv file.txt new_folder/` (移动文件) <br> `mv old_name.txt new_name.txt` (重命名文件) | 整理你的素材文件，如 `mv *.jpg images/` (将所有 JPG 图片移动到 `images` 文件夹)。 |
| `rm` | **R**e**m**ove，删除文件或目录。 | `rm file.txt` (删除文件) <br> `rm -r folder/` (删除目录) <br> `rm -rf folder/` (强制删除目录，**慎用！**)| 清理无用的临时文件或旧版本设计稿。 |
| `cat` | **Cat**enate，显示文件内容。 | `cat my_notes.md` | 快速查看 Markdown 笔记或代码文件的内容。 |
| `less` | 分页显示文件内容，适合大文件。 | `less large_log.txt` | 查看大型日志文件或长篇文档，按 `q` 退出。 |
| `head` / `tail` | 显示文件开头/结尾的几行。 | `head -n 5 file.txt` (显示前5行) <br> `tail -n 10 file.txt` (显示后10行) | 快速预览日志文件或代码文件的开头/结尾。 |

---

## 二、文本处理：快速查找与筛选

| 命令 | 作用 | 示例 | 设计师场景 |
|---|---|---|---|
| `grep` | 全局正则表达式打印，在文件中搜索匹配指定模式的文本。 | `grep "Arper" my_notes.md` (搜索包含 "Arper" 的行) <br> `grep -r "product_name" scripts/` (在 `scripts` 目录下递归搜索) | 在你的代码或笔记中查找特定关键词，如 `grep "Catifa" *.md`。 |
| `find` | 在目录树中搜索文件。 | `find . -name "*.jpg"` (查找当前目录下所有 JPG 文件) <br> `find /home/ubuntu/projects -type d -name "arper*"` (查找项目目录下以 arper 开头的目录) | 查找特定类型的设计素材或项目文件夹。 |

---

## 三、Git 版本控制：你的设计历史记录仪

| 命令 | 作用 | 示例 | 设计师场景 |
|---|---|---|---|
| `git status` | 查看工作区和暂存区的状态。 | `git status` | 确认哪些文件被修改了，哪些可以提交。 |
| `git add` | 将文件添加到暂存区。 | `git add .` (添加所有修改) <br> `git add my_script.py` (添加指定文件) | 准备提交你的代码或文档修改。 |
| `git commit` | 将暂存区的文件提交到本地仓库。 | `git commit -m "feat: 完成 Stage 4 Day 5 抓取脚本"` | 记录你的每次学习进度或设计迭代。 |
| `git push` | 将本地仓库的提交推送到远程仓库。 | `git push` | 将你的学习成果同步到 GitHub，方便备份和分享。 |
| `git pull` | 从远程仓库拉取最新代码到本地。 | `git pull` | 更新你的学习仓库，获取最新的课程内容。 |
| `git clone` | 克隆远程仓库到本地。 | `git clone https://github.com/your_user/your_repo.git` | 第一次设置你的学习仓库。 |

---

## 四、Python 与包管理：你的工具箱

| 命令 | 作用 | 示例 | 设计师场景 |
|---|---|---|---|
| `python3` | 运行 Python 脚本。 | `python3 my_script.py` | 运行你的爬虫脚本或数据处理脚本。 |
| `pip3 install` | 安装 Python 包。 | `pip3 install requests beautifulsoup4 playwright` | 安装爬虫所需的库。 |

---

## 五、其他实用命令

| 命令 | 作用 | 示例 | 设计师场景 |
|---|---|---|---|
| `clear` | 清除终端屏幕内容。 | `clear` | 让你的终端界面保持整洁。 |
| `history` | 显示你最近执行过的命令历史。 | `history` | 查找之前用过的复杂命令。 |
| `man` | 显示命令的帮助手册。 | `man ls` | 忘记某个命令的用法时，快速查询。 |

---

## 六、重要提示：

*   **路径分隔符**：在 Bash 中，路径使用 `/` 而不是 `\`。
*   **Tab 键补全**：在输入命令、文件名或目录名时，多按 `Tab` 键，Bash 会自动帮你补全，这能大大提高效率并减少输入错误。
*   **历史命令**：使用键盘的 `↑` 和 `↓` 箭头键可以快速翻阅你之前输入过的命令。
*   **善用 `.` 和 `..`**：`.` 代表当前目录，`..` 代表上一级目录。

从现在开始，你所有的课程中的终端操作指令都将以 Bash 命令的形式给出。如果你在学习过程中遇到任何 Bash 命令的疑问，随时向我提问！
