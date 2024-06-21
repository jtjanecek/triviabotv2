import pandas as pd

class Question():
    def __init__(self):
        self._questions = pd.read_csv('unit_speech.csv')


    def get_question(self) -> (str, str):
        '''
        Return a question and answer
        '''
        r = self._questions.sample(n=1)

        speech = r.iloc[0, 0]  # Value from the first column
        speech_type = r.iloc[0, 1]  # Value from the second column
        unit = r.iloc[0, 2]  # Value from the second column

        q = f"[Unit Speech][{speech_type}] {speech}"

        return q, unit