# 📔 Personal Diary App

A beautiful, feature-rich personal diary web application built with Flask and SQLite. Keep your thoughts, memories, and reflections organized with mood tracking, categories, and powerful analytics.

## ✨ Features

- **User Authentication** - Secure login and registration with password hashing
- **Mood Tracking** - Log your emotional state with each entry (Happy, Sad, Neutral, Excited, Anxious, Calm)
- **Categories** - Organize entries by categories (Work, Personal, Travel, Health, Relationships, Dreams, Goals)
- **Search & Filter** - Easily find entries by keywords or category
- **Edit & Delete** - Modify or remove entries anytime
- **Favorites** - Mark your favorite entries for quick access
- **Statistics Dashboard** - View analytics with:
  - Total entries, words, and character count
  - Entry breakdown by category
  - Mood distribution charts
  - Favorite entry count
- **Monthly View** - Browse all entries organized by month
- **Entry Details** - View full entries with word and character statistics
- **Responsive Design** - Beautiful UI with pink gradient theme
- **Word Count** - See writing statistics for each entry

## 🛠️ Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite
- **Frontend**: HTML, CSS, Jinja2 templates
- **Security**: Werkzeug (password hashing)

## 📋 Requirements

- Python 3.7+
- Flask
- Werkzeug

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-diary-app.git
   cd personal-diary-app
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask werkzeug
   ```

4. **Run the application**
   ```bash
   python "jahnavi.personal diary.py"
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 📚 Usage

1. **Register** - Create a new account with a username and password
2. **Login** - Sign in with your credentials
3. **Add Entries** - Write diary entries and select mood & category
4. **View Dashboard** - See all your entries with filtering options
5. **Edit/Delete** - Modify or remove entries as needed
6. **Mark Favorites** - Click the star icon to mark important entries
7. **View Stats** - Check your writing statistics and mood trends
8. **Monthly View** - Browse entries organized by month

## 📁 Project Structure

```
personal-diary-app/
├── jahnavi.personal diary.py   # Main Flask application
├── templates/
│   ├── login.html              # Login page
│   ├── register.html            # Registration page
│   ├── dashboard.html           # Main dashboard
│   ├── add_entry.html           # Add/edit entry
│   ├── view_entry.html          # View full entry
│   ├── stats.html               # Statistics page
│   └── monthly.html             # Monthly view
├── diary.db                     # SQLite database (auto-created)
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🎨 Features Highlight

### Mood Tracking
Track your emotions with 6 different mood options:
- 😊 Happy
- 😢 Sad
- 😐 Neutral
- 🤩 Excited
- 😰 Anxious
- 😌 Calm

### Writing Statistics
- Word count per entry
- Total characters
- Average entry length (in stats)
- Total writing volume

### Organization
- 8 predefined categories
- Custom category creation
- Search by keywords
- Filter by category
- Monthly organization

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- User-specific data (each user only sees their entries)
- SQL injection prevention with parameterized queries

## 🌟 Color Theme

Beautiful pink gradient theme:
- Hot pink (#ff69b4) - Main accent
- Deep pink (#ff1493) - Buttons and hover states
- Pink gradient background

## 📝 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `password` - Hashed password

### Entries Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `content` - Entry text
- `category` - Entry category
- `mood` - Emotional state
- `is_favorite` - Bookmark status
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## 🐛 Known Limitations

- Single-server deployment (not production-ready)
- In-memory session management
- SQLite (suitable for small deployments)
- No backup/export features

## 🚀 Future Enhancements

- [ ] Export entries to PDF/CSV
- [ ] Rich text editor
- [ ] Image attachments
- [ ] Sharing entries (private/public)
- [ ] Dark mode
- [ ] Mobile app
- [ ] Cloud backup
- [ ] Recurring reminders
- [ ] Location tagging

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 💬 Support

If you encounter any issues or have suggestions, please open an issue on GitHub.

## 👨‍💻 Author

Created with ❤️ for personal journaling

---

**Enjoy keeping your personal diary! 📝✨**
