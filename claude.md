# Expense Tracker - Claude Code Project

## 📋 Project Overview

A terminal-based expense tracking application built with Python and Rich library for beautiful CLI formatting.

**Repository:** https://github.com/marbaji/expense-tracker

**Developer:** marbaji

**Created:** March 2026

---

## 🎯 Features

### Current Features

- ✅ **Add Expenses** - Simple prompts for amount, category, and description
- ✅ **View Expenses** - Beautiful table with category-based color coding
- ✅ **Summary View** - Total spending with breakdown by category
- ✅ **Budget Tracking** - Set monthly budgets with color-coded warnings
- ✅ **Search** - Find expenses by category or description keywords
- ✅ **CSV Export** - Export current month's expenses to CSV
- ✅ **Delete** - Remove expenses by ID
- ✅ **Flexible Input** - Accepts amounts with $, commas, and spaces

### Color Coding by Category

- Food: Bright Yellow
- Transport: Bright Blue
- Coffee: Cyan
- Entertainment: Magenta
- Shopping: Bright Magenta
- Utilities: Blue
- Health: Green
- Education: Bright Green
- Rent: Red
- Groceries: Yellow
- Other: White

---

## 🏗️ Architecture

### Files

- **`tracker.py`** - Main application (simple command-line interface)
- **`expense_tracker.py`** - Full-featured version with interactive menu
- **`expenses.json`** - User expense data (not tracked in git)
- **`budgets.json`** - User budget data (not tracked in git)
- **`.gitignore`** - Excludes personal data files

### Data Structure

**Expenses:**
```json
{
  "id": 1,
  "date": "2026-03-10",
  "amount": 45.50,
  "category": "Food",
  "description": "Lunch with team"
}
```

**Budgets:**
```json
{
  "Food": 200.00,
  "Transport": 100.00
}
```

---

## 🚀 Usage Commands

```bash
# Add expense (default)
python3 tracker.py

# View all expenses
python3 tracker.py view

# View summary with budgets
python3 tracker.py summary

# Set category budget
python3 tracker.py budget

# Search expenses
python3 tracker.py search <keyword>

# Export to CSV
python3 tracker.py export

# Delete expense
python3 tracker.py delete <ID>

# Show help
python3 tracker.py help
```

---

## 🔧 Development Notes

### Dependencies

- Python 3.x
- Rich library (`pip install rich`)

### Git Workflow

- **Main branch:** Production-ready code
- **Feature branches:** New features (e.g., `feature/budget-tracking`)
- **Pull Requests:** Used for code review and merging features

### Commit Convention

```
<type>: <short description>

<detailed description>

Features:
- Feature 1
- Feature 2

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 💡 Future Feature Ideas

### Potential Enhancements

- [ ] **Recurring Expenses** - Auto-add monthly bills
- [ ] **Income Tracking** - Track income vs expenses
- [ ] **Charts/Graphs** - Visual spending trends with Rich
- [ ] **Date Range Filters** - View expenses for specific periods
- [ ] **Multiple Currencies** - Support for different currencies
- [ ] **Categories Management** - Edit/rename/delete categories
- [ ] **Backup/Restore** - Export/import all data
- [ ] **Mobile Sync** - Cloud sync for mobile access
- [ ] **Receipt Scanning** - OCR for receipt data entry
- [ ] **Spending Insights** - AI-powered spending analysis

### Technical Improvements

- [ ] Add unit tests
- [ ] Create requirements.txt
- [ ] Add configuration file for user preferences
- [ ] Implement data validation
- [ ] Add logging for debugging
- [ ] Create Docker container
- [ ] Add GitHub Actions for CI/CD

---

## 📝 Development Guidelines

### Before Making Changes

1. Create a feature branch: `git checkout -b feature/feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive message
5. Push and create pull request

### Code Style

- Use Rich library for all terminal output
- Follow Python PEP 8 style guide
- Add docstrings to all functions
- Keep functions focused and single-purpose
- Use descriptive variable names

### Testing Checklist

- [ ] Feature works as expected
- [ ] No errors with edge cases (empty input, large numbers, etc.)
- [ ] Data persists correctly to JSON files
- [ ] Git ignores personal data files
- [ ] All commands in help menu work

---

## 🐛 Known Issues

None currently! 🎉

---

## 📚 Resources

- **Rich Library Docs:** https://rich.readthedocs.io/
- **Git Branching:** https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
- **GitHub Pull Requests:** https://docs.github.com/en/pull-requests

---

## 🎓 Learning Notes

### Git Commands Used

- `git init` - Initialize repository
- `git add` - Stage changes
- `git commit` - Save changes locally
- `git push` - Upload to GitHub
- `git pull` - Download from GitHub
- `git checkout -b` - Create new branch
- `git merge` - Merge branches
- `git branch -d` - Delete branch

### Key Learnings

1. **Feature branches** keep main stable
2. **Pull requests** enable code review
3. **Category-based colors** improve UX significantly
4. **Rich library** makes CLI apps beautiful
5. **Git workflow** is essential for collaboration

---

**Last Updated:** March 10, 2026

**Status:** ✅ Active Development
