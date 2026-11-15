# Learning Log

Rough notes after each build step. These become post drafts for the site.

## Stage 0, Step 1: project folder and Git repo (2026-11-15)

- I made the project folder and ran `git init -b main`, which turns a normal folder into a Git repository by adding a hidden `.git` folder where the history lives.
- The folder is named `dejaneiro555.github.io` because GitHub Pages only serves a site at that address from a repo with exactly that name.
- What broke later: I had renamed my GitHub username (fixing the spelling to match Rio de Janeiro), so the first folder name was out of date. We fixed the name in the files, the Git author email, and the folder, then saved that as its own commit.
- What broke: nothing crashed, but Git had no name or email set, and it needs both before it can record a commit.
- How we fixed it: `git config user.name` and `git config user.email` for this repo only, using GitHub's no-reply address so my personal email stays out of the public history.
- A commit is a saved snapshot. `git add` picks which files go in, and `git commit -m "..."` saves them with a message.

## Stage 0, Step 2: .gitignore (2026-11-15)

- macOS created a `.DS_Store` file in my project folder on its own. It stores Finder view settings and has nothing to do with my site.
- What broke: `git status` listed `.DS_Store` as untracked, so one careless `git add .` would have put it in my public repo.
- How we fixed it: a `.gitignore` file with one line, `.DS_Store`. Git skips any file whose name matches a line in that file.
- `.gitignore` only hides files Git is not already tracking. If a file was committed earlier, ignoring it later does not remove it.
- Files starting with a dot are hidden in Finder. `ls -a` shows them in the terminal, and Cmd+Shift+. toggles them in Finder.
