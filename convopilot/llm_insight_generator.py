
from convopilot import google_doc
from convopilot.interface import InsightGenerator
from convopilot.llm_models import get_llm_model


class LLMInsightGenerator(InsightGenerator):
    def __init__(self, input_queue, llm_model, context, llm_prompt, gdocument):
        self.model = get_llm_model(llm_model)
        self.context = context
        self.llm_prompt = llm_prompt
        self.gdocument = gdocument
        self.input_queue = input_queue

    def generate(self):
        previous_response = ""
        while True:
            transcription_data = self.input_queue.get()
            if transcription_data is None:
                break

            prompt = f"""
            You are the best AI conversation facilitator. You are helping a group of people have a conversation about a topic. 
            This is the context for the conversation:
            {self.context}
            This is what the group want you to help answer:
            {self.llm_prompt}
            This is your answer up until 30 seconds ago:
            {previous_response}
            This is the latest 2000 words of the conversation:
            {transcription_data[-2000:]}

            Given the information above, could you generate a new answer considering your previous answer and latest conversation?
            """

            response = self.model.generate_text(prompt)
            previous_response = response
            print(response)

        if self.gdocument is not None:
            google_doc.insert_paragraph(
                self.gdocument['documentId'], previous_response + "\n")
            google_doc.insert_paragraph(
                self.gdocument['documentId'], self.llm_prompt, 'HEADING_2')
            google_doc.insert_paragraph(self.gdocument['documentId'], f"{self.context} \n")
            google_doc.insert_paragraph(
                self.gdocument['documentId'], "Context:", 'HEADING_2')

        print("Stopped llm generation.")
