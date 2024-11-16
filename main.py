from services import OpenAIAssistantService, FileUploader, SafeOpenAI

if __name__ == "__main__":
    assistant_service = OpenAIAssistantService()
    file_uploader = FileUploader()
    # completion = client.client.chat.completions.create(
    #     model="ft:gpt-4o-mini-2024-07-18:personal::ATsaRXHQ",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {
    #             "role": "user",
    #             "content": "Кожа ладоней в сыпи, зуд отсуствует",
    #         },
    #     ],
    # )
    # print(completion.choices[0].message)
    # training_file = client.client.files.create(
    #     file=open("test.jsonl", "rb"), purpose="fine-tune"
    # )

    # fine_tuning = client.client.fine_tuning.jobs.create(
    #     training_file=training_file.id, model="gpt-4o-mini-2024-07-18"
    # )

    # status = client.client.fine_tuning.jobs.retrieve(fine_tuning.id)
    # print(training_file, fine_tuning, status)
    # print(client.client.fine_tuning.jobs.retrieve("ftjob-33kLY1SjDk2PHCoPGiZVxXfr"))
    # file-E59FbenEz2BOPaaivqMpSSKx
    # ftjob-OWQE1JhZskdnUq13LC8FomaO
    # FileObject(id='file-cJZyfYLEWxM5VPqdplKfBIHb', bytes=5268, created_at=1731684069, filename='test.jsonl', object='file', purpose='fine-tune', status='processed', status_details=None) FineTuningJob(id='ftjob-33kLY1SjDk2PHCoPGiZVxXfr', created_at=1731684070, error=Error(code=None, message=None, param=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-4o-mini-2024-07-18', object='fine_tuning.job', organization_id='org-j88KpbjZZmmbhDscTi1fPETK', result_files=[], seed=635102575, status='validating_files', trained_tokens=None, training_file='file-cJZyfYLEWxM5VPqdplKfBIHb', validation_file=None, estimated_finish=None, integrations=[], user_provided_suffix=None) FineTuningJob(id='ftjob-33kLY1SjDk2PHCoPGiZVxXfr', created_at=1731684070, error=Error(code=None, message=None, param=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-4o-mini-2024-07-18', object='fine_tuning.job', organization_id='org-j88KpbjZZmmbhDscTi1fPETK', result_files=[], seed=635102575, status='validating_files', trained_tokens=None, training_file='file-cJZyfYLEWxM5VPqdplKfBIHb', validation_file=None, estimated_finish=None, integrations=[], user_provided_suffix=None)
