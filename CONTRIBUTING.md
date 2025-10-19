# Contributing to Discord Message Analyzer

Thank you for your interest in contributing to the Discord Message Analyzer! This tool was created for and by the Autonomi community, and we welcome contributions from everyone.

## How You Can Help

There are many ways to contribute to this project, even if you're not a Python expert:

### 🐛 Report Bugs

If you find a bug, please create an issue on GitHub with:

- A clear description of what went wrong  
- Steps to reproduce the problem  
- What you expected to happen
- Your operating system and Python version
- If possible, a sample of the error message (but **never include your Discord token or private message content**)

### 💡 Suggest Features

Have an idea for a new feature? Open an issue describing:

- What problem the feature would solve
- How you envision it working
- Any examples from other tools that do something similar

### 📖 Improve Documentation

Documentation improvements are always welcome:

- Fix typos or clarify confusing sections
- Add examples of how you use the tool
- Translate documentation to other languages
- Create video tutorials or guides

### 🔧 Submit Code

Ready to contribute code? Great! Here's how:

## Development Setup

1. **Fork the repository** on GitHub (click the Fork button)

2. **Clone your fork** to your local machine:

   ```bash
   git clone https://github.com/YOUR_USERNAME/discord-message-analyzer.git
   cd discord-message-analyzer
   ```

3. **Create a virtual environment** and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Create a branch** for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

## Making Changes

### Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and not too long
- Add comments for complex logic

### Testing Your Changes

Before submitting:

1. Test your changes with actual Discord exports
2. Verify the tool still works with the example configuration
3. Check that error handling works properly
4. Make sure no sensitive data is accidentally included

### Security Considerations

**CRITICAL**: Never commit sensitive data!

- No Discord tokens
- No actual message exports
- No real server or channel IDs in examples
- No user-specific configuration files

Always use placeholder values in examples and documentation.

## Submitting Changes

1. **Commit your changes** with clear, descriptive messages:

   ```bash
   git add .
   git commit -m "Add feature: description of what you added"
   ```

2. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Write a clear description of your changes
   - Explain why the change is useful

### Pull Request Guidelines

A good pull request:

- Solves one specific problem or adds one clear feature
- Includes a clear description of what changed and why
- Updates documentation if needed
- Doesn't break existing functionality
- Follows the project's code style

## Feature Ideas

Here are some features we'd love to see implemented:

### High Priority

- [ ] Date range filtering within the analyzer (not just at export time)
- [ ] HTML output format for better readability
- [ ] CSV export for data analysis in spreadsheets
- [ ] Progress bars for processing large exports
- [ ] Better error messages with suggestions for fixes

### Medium Priority

- [ ] Analyze multiple users in a single run
- [ ] Thread reconstruction (show full conversation threads)
- [ ] Search functionality (find messages containing keywords)
- [ ] Statistics dashboard (message frequency, activity patterns)
- [ ] Configuration file validation

### Advanced Features

- [ ] Sentiment analysis of replies
- [ ] Visualization of activity over time (charts/graphs)
- [ ] Network analysis of user interactions
- [ ] Integration with Discord bots for real-time analysis
- [ ] Web interface for non-technical users

## Code Review Process

All contributions go through code review:

1. A maintainer will review your pull request
2. They may ask questions or request changes
3. Discussion happens in the pull request comments
4. Once approved, your code will be merged

Don't be discouraged if changes are requested - it's a normal part of the process and helps maintain code quality!

## Community Guidelines

### Be Respectful

- Treat everyone with respect and kindness
- Welcome newcomers and help them learn
- Accept constructive criticism gracefully
- Focus on ideas, not people

### Be Collaborative

- Share knowledge and help others
- Give credit where credit is due
- Be open to different approaches and perspectives

### Be Responsible

- Test your code before submitting
- Don't break existing functionality
- Keep security in mind
- Respect user privacy

## Questions?

If you have questions about contributing:

- Open an issue with the "question" label
- Ask in the Autonomi Discord community
- Check existing issues and pull requests for similar discussions

## Recognition

Contributors will be recognized in:

- The project README
- Release notes when features are shipped
- GitHub's contributor graph

Thank you for helping make this tool better for everyone in the community!

---

**Remember**: By contributing to this project, you agree that your contributions will be licensed under the MIT License.