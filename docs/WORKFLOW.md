# Development Workflow

## Overview

This document outlines the development workflow for UnifiedAI Hub, from initial setup to release deployment.

## Git Workflow

### Branch Strategy
```
main (production)
├── develop (integration)
├── feature/feature-name
├── bugfix/issue-number
└── hotfix/critical-fix
```

### Branch Types

#### Main Branch
- **Purpose**: Production-ready code
- **Protection**: Direct commits not allowed
- **Updates**: Only via pull requests

#### Develop Branch
- **Purpose**: Integration branch for features
- **Base**: For feature branches
- **Sync**: Regularly with main

#### Feature Branches
- **Naming**: `feature/description-of-feature`
- **Creation**: From develop branch
- **Lifespan**: Until feature complete

#### Bugfix Branches
- **Naming**: `bugfix/issue-number-description`
- **Creation**: From develop or main (critical)
- **Target**: Issue being fixed

#### Hotfix Branches
- **Naming**: `hotfix/description-of-fix`
- **Creation**: From main branch
- **Purpose**: Critical production fixes

## Development Process

### 1. Setup Development Environment
```bash
# Fork repository (GitHub UI)
# Clone your fork
git clone https://github.com/YOUR_USERNAME/unified-ai-wrapper.git
cd unified-ai-wrapper

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/unified-ai-wrapper.git

# Install dependencies
npm install

# Create develop branch if not exists
git checkout -b develop upstream/develop
```

### 2. Start New Feature
```bash
# Sync with latest
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/your-feature-name

# Start development
npm start
```

### 3. Development Workflow
```bash
# Regular commits
git add .
git commit -m "feat: implement feature description"

# Push to your fork
git push origin feature/your-feature-name

# Keep branch updated
git checkout develop
git pull upstream develop
git checkout feature/your-feature-name
git rebase develop
```

### 4. Code Review Process
```bash
# Create pull request
# Via GitHub UI or CLI
gh pr create --title "Feature: Your Feature Name" --body "Description..."

# Request reviews from maintainers
# Address feedback
# Update PR as needed
```

### 5. Merge Process
```bash
# After approval and CI passes
# Squash merge for clean history
git checkout develop
git merge --squash feature/your-feature-name
git push upstream develop

# Delete feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## Commit Message Convention

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples
```
feat(layout): add four-column layout for wide displays

Implement new layout system to support four AI services
side-by-side, optimized for ultrawide monitors.

Closes #123
```

```
fix(session): resolve login persistence issue

AI services were losing sessions on restart due to
incorrect partition naming. Fixed by updating partition
format to match service names.

Fixes #145
```

## Release Process

### 1. Preparation
```bash
# Ensure develop is up to date
git checkout develop
git pull upstream develop

# Run full test suite
npm test

# Update version in package.json
npm version patch|minor|major

# Update CHANGELOG.md
# Add release notes
```

### 2. Release Branch
```bash
# Create release branch
git checkout -b release/v1.1.0

# Final checks
npm run build
npm run test:release
```

### 3. Merge to Main
```bash
# Merge to main
git checkout main
git merge --no-ff release/v1.1.0
git tag -a v1.1.0 -m "Release version 1.1.0"

# Push to upstream
git push upstream main
git push upstream --tags
```

### 4. Merge Back to Develop
```bash
# Merge changes back
git checkout develop
git merge --no-ff release/v1.1.0
git push upstream develop

# Delete release branch
git branch -d release/v1.1.0
```

## Code Review Guidelines

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console errors
- [ ] Performance considered
- [ ] Security implications checked
- [ ] Cross-platform compatibility

### Review Process
1. **Self-Review**
   - Review your own code first
   - Check against checklist
   - Fix obvious issues

2. **Peer Review**
   - Request at least one reviewer
   - Provide constructive feedback
   - Ask clarifying questions

3. **Maintainer Review**
   - Final approval from maintainer
   - Checks project alignment
   - Merges if approved

## Quality Assurance

### Testing Strategy
1. **Unit Tests** (Future)
   - Test individual functions
   - Mock external dependencies
   - Fast feedback loop

2. **Integration Tests**
   - Test component interactions
   - Real environment setup
   - End-to-end scenarios

3. **Manual Testing**
   - Use checklist in AGENTS.md
   - Test on all platforms
   - Verify user workflows

### Test Environments
```bash
# Local development
npm start

# Production build test
npm run pack
./dist/Unified\ AI\ Hub.app

# Cross-platform testing
# Use GitHub Actions or manual
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Build
        run: npm run dist:current
```

### Automated Checks
- Linting: ESLint configuration
- Type checking: TypeScript (future)
- Security: npm audit
- Dependencies: Check for updates

## Deployment Workflow

### Build Process
```bash
# Clean build
rm -rf dist/
npm run dist

# Verify artifacts
ls -la dist/
# Check sizes, signatures
```

### Distribution Channels
1. **GitHub Releases**
   - Automated on tag push
   - All platforms included
   - Checksums provided

2. **App Stores** (Future)
   - Apple App Store
   - Microsoft Store
   - Snap Store

3. **Package Managers**
   - Homebrew (macOS)
   - Chocolatey (Windows)
   - AUR (Arch Linux)

### Release Communication
1. **GitHub Release**
   - Detailed changelog
   - Download links
   - Upgrade instructions

2. **Community Announcements**
   - Reddit: r/ElectronApps
   - Twitter: @unifiedai_hub
   - Discord/Slack communities

3. **In-App Notification**
   - Update banner
   - Link to changelog
   - One-click update

## Tools and Configuration

### Essential Tools
```bash
# Git configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# GitHub CLI (optional)
brew install gh  # macOS
choco install gh  # Windows

# Node tools
npm install -g nodemon
npm install -g electron
```

### VS Code Setup
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "files.exclude": {
    "**/node_modules": true,
    "**/dist": true
  }
}
```

### Git Hooks (Optional)
```bash
# Install husky for pre-commit hooks
npm install --save-dev husky

# Package.json hooks
"husky": {
  "hooks": {
    "pre-commit": "npm run lint && npm run test"
  }
}
```

## Best Practices

### Daily Workflow
1. **Morning**
   - Pull latest changes
   - Review notifications
   - Plan day's tasks

2. **Development**
   - Work on feature branch
   - Commit frequently
   - Push progress

3. **End of Day**
   - Push work
   - Create PR if ready
   - Update task tracker

### Collaboration
1. **Communication**
   - Use GitHub for technical discussions
   - Slack/Discord for quick questions
   - Email for private matters

2. **Code Reviews**
   - Turn around within 24 hours
   - Provide specific feedback
   - Help improve, not just criticize

3. **Issue Triage**
   - Label new issues promptly
   - Assign to milestones
   - Set priority levels

---

**Last Updated**: October 2024  
**Maintained by**: UnifiedAI Hub Team  
**Questions**: Create an issue or discussion