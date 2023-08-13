
from convopilot import google_doc
from convopilot.interface import InsightGenerator
from convopilot.llm_models import get_llm_model


class LLMInsightGenerator(InsightGenerator):
    def __init__(self, input_queue, llm_model, context, llm_prompt, gdoc_writer):
        self.model = get_llm_model(llm_model)
        self.context = context
        self.llm_prompt = llm_prompt
        self.gdoc_writer = gdoc_writer
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

        if self.gdoc_writer is not None:
            self.gdoc_writer.insert_paragraph_front(previous_response + "\n")
            self.gdoc_writer.insert_paragraph_front(self.llm_prompt, 'HEADING_2')
            self.gdoc_writer.insert_paragraph_front(f"{self.context} \n")
            self.gdoc_writer.insert_paragraph_front("Context:", 'HEADING_2')

        print("Stopped llm generation.")
