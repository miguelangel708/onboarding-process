# Project Name

A brief description of what your application does. Include the general purpose and main benefits or features.

## Technologies Used

- **Frontend**:
  - HTML
  - CSS
  - JavaScript

- **Backend**:
  - Flask (Python)

## Installation

### Prerequisites

Make sure you have [Python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/) installed on your machine.

### Backend Setup

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

### Frontend Setup

1. Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```

2. Open the `index.html` file in your web browser to view the application.

## Usage

Inside the web application, in the frontend, you can visualize a form, it is necessary to fill all the data, once you have them, a preview of the uploaded images will be visualized on the right side, after pressing the button, these images will be uploaded to the api that is in charge of doing the validations and consult the truora api with which the validations are done, the result of the validation can be shown on the screen.


### Usage Examples

- **API Calls**: the api in the backend receives a formdata with the parameters: 

1. fileFront: image of the front display of the document.
2. fileBack: image of the reverse display of the document
3. country: a string of 2 uppercase letters indicating the country
4. docType: a string indicating the document type
5. acceptTerms: a boolean indicating the user's authorization

## License

This project is owned by Truoura.

## Contact

If you have questions or need further assistance, you can contact me at:

- **Email**: miguelmunoz.aristizabal@gmail.com
- **GitHub**: [miguelangel708](https://github.com/miguelangel708)
