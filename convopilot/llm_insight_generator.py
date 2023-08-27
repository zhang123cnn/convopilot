
from convopilot.interface import PipelineModule
from convopilot.llm_models import get_llm_model


class LLMInsightGenerator(PipelineModule):
    def __init__(self, llm_metadata, gdoc_writer):
        super().__init__()
        self.model = get_llm_model(llm_metadata['model'])
        self.context = llm_metadata['context']
        self.llm_prompt = llm_metadata['prompt']
        self.gdoc_writer = gdoc_writer

    def run(self):
        previous_response = ""
        transcription_data = ""
        while True:
            latest = self.input_queue.get()
            if latest is None:
                break

            transcription_data += latest

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

            self.output_data(response)

        if self.gdoc_writer is not None:
            self.gdoc_writer.insert_paragraph_front(previous_response + "\n")
            self.gdoc_writer.insert_paragraph_front(self.llm_prompt, 'HEADING_2')
            self.gdoc_writer.insert_paragraph_front(f"{self.context} \n")
            self.gdoc_writer.insert_paragraph_front("Context:", 'HEADING_2')

        print("Stopped llm generation.")
