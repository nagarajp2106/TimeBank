# TimeBank - Skill Exchange Platform

TimeBank is a modern, premium web platform designed for peer-to-peer skill exchange. It operates on a "Time Coin" economy where users trade their expertise for time, fostering a community of continuous learning and teaching.

## 🚀 Concept
In TimeBank, time is the primary currency. Every user starts with a balance of Time Coins, which they can use to enroll in courses. By teaching others, users earn more coins, which they can then reinvest in their own learning.

## ✨ Key Features
- **Dual-Role System**: Users can participate as both **Learners** (acquiring new skills) and **Instructors** (sharing expertise).
- **Time Coin Wallet**: Integrated wallet system that tracks your learning credits. Every new user starts with **50 coins**.
- **Course Marketplace**: Browse courses across various categories like Programming, Design, Music, Cooking, and more.
- **Interactive Learning**: Courses support YouTube video integration and additional notes/resources.
- **Smart Enrollment**: A streamlined process for requesting and approving course access.
- **Transaction History**: Transparent tracking of all coin exchanges between users.
- **Premium UI/UX**: A sleek, responsive, and learner-centric interface designed for an optimal user experience.

## 🛠 Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS, JavaScript
- **Database**: SQLite (Development)
- **Media**: Support for Profile Pictures and YouTube Embeds

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Git

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/nagarajp2106/TimeBank.git
   cd TimeBank
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If requirements.txt is missing, ensure `django` and `pillow` are installed.*

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```
   Access the app at `http://127.0.0.1:8000`.

## 📖 Documentation
Detailed instructions for users can be found in the [User Guide](USER_GUIDE.md).

---
*Built with ❤️ by **Nagaraj Patil** for the community of lifelong learners.*
