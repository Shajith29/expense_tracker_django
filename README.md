Project Goals:
1) Learn Django fundamentals properly
2) Build a complete, deployable application
3) Use function-based views (FBVs)
4) Focus on clarity, correctness, and real-world patterns
5) Avoid over-engineering

Tech Stack:
Backend: Django (Python)
Frontend: HTML, Tailwind CSS
Database: SQLite
Authentication: Django Auth

Features:

Authentication:
  User registration
  Login & logout
  User-specific data isolation

Expense Management
  Add, edit, delete expenses
  Assign categories to expenses
  Protected deletes
  
Category Management
  Create & delete categories
  Category expense count
  Safe deletion using database constraints
  
Filtering & Search
  Filter by category
  Filter by month & year
  Date range filter (from → to)
  Search by description text

Reports & Analytics
  Monthly summary (total + category-wise)
  Yearly summary (month-wise totals)
  Export filtered expenses to CSV

Pagination
  Paginated expense list
  Preserves filters & search across pages
