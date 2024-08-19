# onboarding/KYC process for users

This project enables the end user to:
1. Upload a photo of their document's front side.
2. Upload a photo of the back side of their document.
3. Visualize the final result of their validation.

## Technologies Used

- **Frontend**:
  - HTML
  - CSS
  - JavaScript

- **Backend**:
  - Flask (Python)

## Installation

### Prerequisites

Make sure you have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/) installed on your machine. If you prefer using Docker, ensure you have [Docker](https://www.docker.com/get-started) installed.

### Backend Setup

#### Option 1: Running Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/your_repository.git
    cd your_repository
    ```

2. Navigate to the backend directory:
    ```bash
    cd backend
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the backend directory with the following structure:
    ```env
    truoraDocumentValidationURL=
    truoraApiKey=
    ```
   This file is used to keep sensitive information such as API URLs and keys confidential. The decision to make the repository public is based on the fact that sensitive information is not exposed in the code, but rather loaded from this `.env` file to ensure security.

5. Run the Flask server:
    ```bash
    python -m flask run --host=0.0.0.0
    ```

   The server will be available at `http://localhost:5000`.

#### Option 2: Using Docker

1. Make sure Docker is installed on your machine.

2. Build the Docker image:
    ```bash
    docker build -t backend-onboarding .
    ```

3. Create a `.env` file in the root of your project directory (where your Dockerfile is located) with the following structure:
    ```env
    truoraDocumentValidationURL=
    truoraApiKey=
    ```
   This file is required for the Docker container to access the necessary environment variables for proper functioning of the backend.

4. Run the Docker container:
    ```bash
    docker run -p 5000:5000 --env-file .env backend-onboarding
    ```

   The backend server will be available at `http://localhost:5000` inside the Docker container.

### Frontend Setup

1. Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```

2. Open the `index.html` file in your web browser to view the application.

## Usage

Inside the web application, you will find a form in the frontend. It is necessary to fill out all the required fields. Once the data is filled, a preview of the uploaded images will be displayed on the right side. After pressing the submit button, these images will be uploaded to the API, which handles the validations and consults the Truora API for processing. The result of the validation will be shown on the screen.

### Usage Examples

- **API Calls**: The API in the backend receives a `FormData` object with the following parameters:
    1. `fileFront`: Image of the front side of the document.
    2. `fileBack`: Image of the back side of the document.
    3. `country`: A string of 2 uppercase letters indicating the country.
    4. `docType`: A string indicating the document type.
    5. `acceptTerms`: A boolean indicating the user's authorization.

## License

This project is owned by Truora.

## Contact

If you have questions or need further assistance, you can contact me at:

- **Email**: your_email@gmail.com
- **GitHub**: [your_username](https://github.com/your_username)
