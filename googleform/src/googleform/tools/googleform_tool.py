from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
from google.oauth2 import service_account
import os 
from googleapiclient.discovery import build

class GoogleFormsInput(BaseModel):
    """Input schema for GoogleFormsTool."""
    form_title: str = Field(..., description="Title of the Google Form.")
    document_title: str = Field(..., description="Document title of the Google Form.")
    questions: List[str] = Field(..., description="List of questions to add to the form.")

class GoogleFormsTool(BaseTool):
    name: str = "Google Forms Creator"
    description: str = "A tool to create Google Forms and add questions to them."

    args_schema: Type[BaseModel] = GoogleFormsInput

    def _run(self, form_title: str, document_title: str, questions: List[str]) -> str:
        # Define the scope for Forms API
        SCOPES = ['https://www.googleapis.com/auth/forms.body']

        # Authenticate and build the service
        credentials = service_account.Credentials.from_service_account_file(
           os.getenv("SERVICEJSON") , scopes=SCOPES
        )

        service = build('forms', 'v1', credentials=credentials)

        # Define the form structure
        new_form = {
            "info": {
                "title": form_title,
                "documentTitle": document_title
            }
        }

        # Create the form
        form = service.forms().create(body=new_form).execute()
        form_id = form["formId"]
        print(form_id)
        form_url = form["responderUri"]

        # Prepare the questions in the required format
        questions_requests = {
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": question,
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "textQuestion": {}
                                }
                            }
                        },
                        "location": {"index": idx}
                    }
                } for idx, question in enumerate(questions)
            ]
        }

        # Batch update the form to add questions
        service.forms().batchUpdate(formId=form_id, body=questions_requests).execute()

        return f"Form created successfully: {form_url}"
