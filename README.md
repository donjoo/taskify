# Task Management Application with Task Completion Report

## Project Status
**Currently in Development:** API endpoints and Admin Panel are under development. Features are being implemented to allow users to submit completion reports and worked hours for tasks.

---

## Overview
This Task Management Application aims to enhance task tracking and accountability by allowing users to submit a **Completion Report** and **Worked Hours** when marking a task as completed. Admins and SuperAdmins can review these reports to monitor progress and performance.  

Key goals:  
- Transparent task tracking.  
- Improved accountability for users.  
- Admin and SuperAdmin oversight through a web Admin Panel.  

---

## Features

### 1. API Endpoints
**User Authentication:**  
- JWT Authentication: Users can authenticate via username and password to receive a JWT token for secure API requests.

**Tasks API:**  
- `GET /tasks`: Fetch all tasks assigned to the logged-in user.  
  - Returns tasks only for the requesting user.  
- `PUT /tasks/{id}`: Update the status of a task to "Completed".  
  - Requires **Completion Report** and **Worked Hours** when marking as completed.  
- `GET /tasks/{id}/report`: Admins and SuperAdmins can view **Completion Report** and **Worked Hours** for a specific task.  
  - Available only for completed tasks.

---

### 2. Admin Panel (Web Application)
**SuperAdmin Features:**  
- Manage all users (create, delete, assign roles).  
- Manage all admins (create, delete, assign roles).  
- Assign users to admins.  
- View and manage all tasks.  
- View all task reports submitted by users.

**Admin Features:**  
- Assign tasks to users.  
- View and manage tasks assigned to their users.  
- View completion reports submitted by users.  
- Cannot manage user roles.

---

### 3. Task Workflow

**Roles and Permissions:**  
- **SuperAdmin:** Full access to manage users, admins, and tasks.  
- **Admin:** Manage tasks and view completion reports for assigned users. Cannot manage users.  
- **User:** Can view assigned tasks, update status, and submit completion reports with worked hours.

**Task Model Fields:**  
- `Title`: Name of the task.  
- `Description`: Detailed description of the task.  
- `Assigned To`: User assigned to the task.  
- `Due Date`: Deadline for the task.  
- `Status`: Task status (`Pending`, `In Progress`, `Completed`).  
- `Completion Report`: Text field for report when task is completed.  
- `Worked Hours`: Numeric field for hours worked on the task.

**Completion Report & Worked Hours:**  
- Required when marking a task as completed.  
- Admins and SuperAdmins can view these reports via API or Admin Panel.

---

## Technology Stack
- Backend: **Python, Django**  
- Database: **SQLite**  
- Authentication: **JWT**  
- Admin Panel: **HTML Templates (custom)**  

---

