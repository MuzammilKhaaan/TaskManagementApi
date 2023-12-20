# TaskManagementApi
Api for managing tasks

## Database
This application uses a MySQL database to store and manage data.

## Features
- **Basic Authentication and Authorization:**
- **Create Tasks:** Add new tasks.
- **Update Tasks:** Modify existing tasks.
- **Delete Tasks:** Remove tasks that are no longer necessary.
- **Retrieve Tasks:** Get a complete list of all tasks of a user.

## Getting Started

### Prerequisites
- Docker
- Git (for cloning the repository)

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/MuzammilKhaaan/TaskManagementApi.git
   
2. **Build the Application using Docker**
Navigate to the cloned directory and execute:
    ```bash
    docker-compose build

3. **Run the Application**
    ```bash
    docker-compose up

## Usage
Once the TestManagementApi is up and running, you can interact with the API via its endpoints to perform various task operations.

## Documentation
After starting the application, the Swagger documentation for the API is available at `http://localhost:5000/`. This documentation provides detailed information about each endpoint, including the expected request formats and the structure of the responses.
