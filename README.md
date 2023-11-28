# Hooks

Repository for git hooks and related GitHub actions.

## Git Hooks

Reference: [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

## GitHub Actions

Reference: [GitHub Actions](https://docs.github.com/en/actions)

### Actions

Currently, the following actions are available to be used in workflows (alphabetical order):

- [commit-validation.yaml](/.github/workflows/commit-validation.yaml)
- [linters](/.github/workflows/linter.yaml)

### Commit Validation

This action validates the commit message format and the commit message body
using [Commitizen](https://commitizen-tools.github.io/commitizen/).

You can check the [Commitizen configuration](/.cz.toml) to see the expected commit message format.
Simply put, the commit message should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
specification:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Where `type` is one of the following:

- feat: A new feature.
- fix: A bug fix.
- docs: Documentation only changes.
- style: Code style changes (formatting, missing semi-colons, etc.)
- refactor: A code change that neither fixes a bug nor adds a feature.
- perf: A code change that improves performance.
- test: Adding missing tests or correcting existing tests.
- build: Changes that affect the build system or external dependencies.
- ci: Changes to our CI configuration files and scripts.
- chore: Other changes that don’t modify src or test files.
- revert: Reverts a previous commit.

The other fields are optional and their usage should be agreed upon by the team.
