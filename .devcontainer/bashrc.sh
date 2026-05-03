# Dev container shell configuration — sourced from ~/.bashrc

# ── Custom PS1 ────────────────────────────────────────────────────────────────
# Format: repo | branch | /path/to/cwd $
# Colors: cyan=repo, green=branch, yellow=path
# Uses \001 / \002 (readline RL_PROMPT_START/END_IGNORE) so readline correctly
# accounts for invisible characters when wrapping long lines.
__dc_ps1() {
    local repo branch cwd

    if git rev-parse --is-inside-work-tree &>/dev/null; then
        repo=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null)
        branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    fi

    cwd=$(pwd | sed "s|^${HOME}|~|")

    local CYAN=$'\001\033[0;96m\002'
    local GREEN=$'\001\033[0;92m\002'
    local YELLOW=$'\001\033[0;93m\002'
    local RESET=$'\001\033[0m\002'

    if [[ -n "$repo" ]]; then
        printf '%s' \
            "${CYAN}${repo}${RESET} | ${GREEN}${branch}${RESET} | ${YELLOW}${cwd}${RESET}"
    else
        printf '%s' "${YELLOW}${cwd}${RESET}"
    fi
}

export PS1='$(__dc_ps1) \$ '

# ── Flask dev settings ────────────────────────────────────────────────────────
export FLASK_APP=sample_1.app
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5000

# ── Docker settings ───────────────────────────────────────────────────────────
export DOCKER_HOST="unix:///var/run/docker.sock"
export DOCKER_BUILDKIT=1

# ── PATH extras ───────────────────────────────────────────────────────────────
# pip --user installs land here
export PATH="$HOME/.local/bin:$PATH"

# ── Convenience aliases ───────────────────────────────────────────────────────
alias ll='ls -lah --color=auto'
alias l='ls -lh --color=auto'
alias grep='grep --color=auto'

# docker compose shorthand
alias dc='docker compose'
alias dcu='docker compose up'
alias dcd='docker compose down'
alias dcb='docker compose build'

# project shortcuts — avoid shadowing the bash 'test' built-in
alias lint='ruff check .'
alias typecheck='mypy sample_1'
alias run-tests='pytest -v'
alias check='ruff check . && mypy sample_1 && pytest -v'
alias serve='flask run'
