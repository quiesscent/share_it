# ✝️ Religion Blog Web App

A simple web application built with **Flask** and **SQLite3**, where users can share, view, and comment on religious topics. This blog-style platform encourages open, respectful discussions on faith, spirituality, and religious teachings.

---

## 🔧 Tech Stack

* **Framework**: Flask
* **Database**: SQLite3
* **Templating**: Jinja2
* **Frontend**: HTML5, CSS3, Bootstrap
* **Authentication**: Flask-Login 

---

## 🚀 Features

* 🖍️ Create, edit, and delete blog posts
* 💬 Comment on religious discussions
* 🔐 User authentication and session management
* 🗂️ Optional post categories/tags (e.g., Bible Study, Quranic Teachings, Reflections)
* 🔹 Simple, user-friendly interface with spiritual aesthetics

---

## 📂 Project Structure

```
share_it/
├── share_it/
│   ├── forms.py
│   ├── share.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── account.html
│   │   ├── email.html
│   │   ├── feed.html
│   │   ├── login.html
│   │   ├── post.html
│   │   ├── register.html
│   │   ├── reset.html
│   │   ├── reset_code.html
│   │   ├── reset_pass.html
│   └── static/
```

---

## 🛠️ Installation

```bash
git clone https://github.com/quiesscent/share_it.git
cd share_it

# Create a virtual environment
python -m venv env
source env/bin/activate  # For Unix/Linux
# env\Scripts\activate  # For Windows

# Run the app
python run.py

```

App will be live at:

```
http://127.0.0.1:5000
```

---

## 📈 Database Setup

Make sure to create the SQLite3 DB if not present:

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

---

## 📘 Sample Features To Expand

* User registration
* Reset Password
* Confirm Password Reset
* Post like/reaction system
* Topic subscriptions or notifications

---

## 💪 Contributing

Contributions are welcome! If you'd like to add features, improve UI, or fix bugs, feel free to fork the repo and submit a PR.

---

## 📝 License

MIT License.

---

## 👤 Author

* **Ephesians Lewis**
* [Ephesians Lewis](https://github.com/quiesscent)

