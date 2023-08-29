
from convopilot.interface import PipelineModule
from convopilot.llm_models import get_llm_model


class LLMInsightGenerator(PipelineModule):
    def __init__(self, name, llm_metadata, gdoc_writer):
        super().__init__(name)
        self.model = get_llm_model(llm_metadata['model'])
        self.context = llm_metadata['context']
        self.llm_prompt = llm_metadata['prompt']
        self.gdoc_writer = gdoc_writer
        self.previous_response = ""
        self.transcription_data = ""

    def process(self, data, source):
        self.transcription_data += data

        prompt = f"""
        You are the best AI conversation facilitator. You are helping a group of people have a conversation about a topic. 
        This is the context for the conversation:
        {self.context}
        This is what the group want you to help answer:
        {self.llm_prompt}
        This is your answer up until 30 seconds ago:
        {self.previous_response}
        This is the latest 2000 words of the conversation:
        {self.transcription_data[-2000:]}

        Given the information above, could you generate a new answer considering your previous answer and latest conversation?
        """

        response = self.model.generate_text(prompt)
        self.previous_response = response
        print(response)

        self.output_data(response)

    
    def onFinish(self):
        if self.gdoc_writer is not None:
            self.gdoc_writer.insert_paragraph_front(self.previous_response + "\n")
            self.gdoc_writer.insert_paragraph_front(self.llm_prompt, 'HEADING_2')
            self.gdoc_writer.insert_paragraph_front(f"{self.context} \n")
            self.gdoc_writer.insert_paragraph_front("Context:", 'HEADING_2')

        self.transcription_data = ""
        self.previous_response = ""

        print("Stopped llm generation.")

