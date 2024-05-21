# Project and Task Management System

Welcome to the Project and Task Management System! This Django application allows users to create and manage projects, add other users in projects, and perform CRUD operations on tasks within those projects. The application also implements JWT authentication and soft delete functionality.

## Features

1. **User Authentication**: Utilizes JSON Web Token (JWT) for user authentication and authorization.
2. **Project Management**: Users can create projects, add multiple users to their projects, and manage project details.
3. **Task Management**: Within each project, users can create, read, update, and delete tasks. Each task includes a title, description, status, and due date.
4. **Soft Delete**: Implements soft delete functionality for both projects and tasks, allowing records to be marked as deleted instead of being permanently removed from the database.

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

   git clone https://github.com/shahzaib-1997/Project-and-Task-Management-System.git
   cd Project-and-Task-Management-System

2. **Create a virtual environment and activate it**

   python -m venv venv
   .\venv\Scripts\activate

3. **Install the required packages**

   pip install -r requirements.txt

4. **Apply the migrations**

   python manage.py makemigrations
   python manage.py migrate

5. **Create a superuser**

   python manage.py createsuperuser

6. **Run the server**

   python manage.py runserver


## API Endpoints

### Authentication

- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`

### Projects

- **Create Project**: `POST /api/project/`
- **Read Projects**: `GET /api/project/`
- **Update Project**: `PUT /api/project/{id}/`
- **Delete Project (Soft Delete)**: `DELETE /api/project/{id}/`

### Tasks

- **Create Task**: `POST /api/task/?project_id={project_id}`
- **Read Tasks**: `GET /api/task/?project_id={project_id}`
- **Update Task**: `PUT /api/task/{task_id}/`
- **Delete Task (Soft Delete)**: `DELETE /api/task/{task_id}/`

## Soft Delete Implementation

Soft delete is implemented by adding a `deleted` field to both the Project and Task models. Instead of deleting records from the database, the `deleted` field is set to `True`. Queries are then filtered to exclude records where `deleted` is `True`.


Thank you for using the Project and Task Management System! If you encounter any issues or have any questions, please feel free to open an issue on the GitHub repository.