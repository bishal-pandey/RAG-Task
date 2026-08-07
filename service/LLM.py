from db.booking_sql import BookingDb, BookingInfo
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class LLM:
    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.chat = self.client.chats.create(model="gemini-2.5-flash")
        self.db = BookingDb()


    def booking_tool(self, message):
        prompt = prompt = f"""
        You are an interview booking assistant.

        Extract the following fields:

        - name
        - email
        - date
        - time

        Return ONLY valid JSON It should be able to execute Json.load(response).

        If the message is NOT an interview booking request,
        return null.

        {message}

        """
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"))
        # response = self.chat.send_message(prompt)
        if response.text.strip().lower()=='null':
            return None

        data = json.loads(response.text)
        booking_info = BookingInfo(
            Name=data.get("name"),
            Email=data.get("email"),
            Date=data.get("date"),
            Time=data.get("time")
        )
        db_session = self.db.get_session()
        try:
            db_session.add(booking_info)
            db_session.commit()
            print(f"Booking information for '{data.get('name')}' saved to the database.")
        except Exception as e:
            print(f"Error saving booking information: {e}")
        finally:
                db_session.close()
        return f"""Book interview 
            Details: 
            {data}"""
        
    def generate_prompt(self, history,message, document):
        context = "\n\n".join(document)
        prompt = f"""
        You are helpful assistant
        This isnot Interview Booking
        Conversational History:
        {history}

        context:
        {context}

        User Message:
        {message}
        
        Response:
        """
        return prompt

    def conversation(self,message, history, document):
        booking = self.booking_tool(message)
        if booking == None:
            prompt = self.generate_prompt(history, message, document)
            response = self.chat.send_message(prompt)
            print(prompt)
            print(response)
            return response.text
        else:
             return booking


