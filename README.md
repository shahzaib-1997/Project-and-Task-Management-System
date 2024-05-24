# Project and Task Management System

Welcome to the Project and Task Management System! This Django application allows users to create and manage projects, add other users to projects, and perform CRUD operations on tasks within those projects. The application also implements JWT authentication, custom permission handling, and soft delete functionality.

## Features

1. **User Authentication**: Utilizes JSON Web Token (JWT) for user authentication and authorization, with custom authentication classes.
2. **Project Management**: Users can create projects, add multiple users to their projects, and manage project details.
3. **Task Management**: Within each project, users can create, read, update, and delete tasks. Each task includes a title, description, status, and due date.
4. **Soft Delete**: Implements soft delete functionality for both projects and tasks, allowing records to be marked as deleted instead of being permanently removed from the database.
5. **Permission-Based Authorization**: Project owners can assign different permissions (create, update, delete, add members) to project members.

## Technologies Used

- Django
- Django Rest Framework (DRF)
- JWT (JSON Web Token)

## Installation

### Prerequisites

- Python 3.x
- Django 5.x
- Django Rest Framework
- PyJWT

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/shahzaib-1997/Project-and-Task-Management-System.git
   cd Project-and-Task-Management-System
   ```

2. **Create a virtual environment and activate it**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On MacOS/Linux
   ```

3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply the migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

## Permissions

Project owners can assign different permissions to project members:

- **can_create**: Allows creating tasks within the project.
- **can_update**: Allows updating tasks within the project.
- **can_delete**: Allows deleting tasks within the project.
- **add_members**: Allows adding other users to the project.

## API Endpoints

### Authentication

- **Register**: `POST /api/users/register/`
- **Login**: `POST /api/users/login/`

### Projects

- **Create Project**: `POST /api/projects/`
- **Read Projects**: `GET /api/projects/`
- **Update Project**: `PUT /api/projects/{id}/`
- **Delete Project (Soft Delete)**: `DELETE /api/projects/{id}/`

### Tasks

- **Create Task**: `POST /api/projects/{project_id}/tasks/`
- **Read Tasks**: `GET /api/projects/{project_id}/tasks/`
- **Update Task**: `PUT /api/projects/{project_id}/tasks/{task_id}/`
- **Delete Task (Soft Delete)**: `DELETE /api/projects/{project_id}/tasks/{task_id}/`

### Project Members

- **Add Project Member**: `POST /api/projects/{project_id}/members/`
- **Read Project Member**: `GET /api/projects/{project_id}/members/`
- **Update Project Member Permissions**: `PUT /api/projects/{project_id}/members/{user_id}/`
- **Delete Project Member (Soft Delete)**: `DELETE /api/projects/{project_id}/members/{user_id}/`

## Soft Delete Implementation

Soft delete is implemented by adding a `deleted` field to both the Project and Task models. Instead of deleting records from the database, the `deleted` field is set to `True`. Queries are then filtered to exclude records where `deleted` is `True`.

---

Thank you for using the Project and Task Management System! If you encounter any issues or have any questions, please feel free to open an issue on the GitHub repository.
