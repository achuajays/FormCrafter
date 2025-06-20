#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from googleform.crew import Googleform

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': """
            Create a simple 3-field form using the Aeroplane Class Usage Tool. The form should collect:

            Attendee's full name

            Feedback on the aeroplane class held on 20th June

            Interest level on a scale from 1 to 10

        """,
    }
    
    try:
        Googleform().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


