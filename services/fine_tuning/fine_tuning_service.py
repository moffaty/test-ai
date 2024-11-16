from openai import OpenAI, OpenAIError
from openai.types import FileObject
from concurrent.futures import ThreadPoolExecutor


class FineTuningService:
    def __init__(self) -> None:
        self.client = OpenAI()

    def safe_api_call(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OpenAIError as e:
            print(f"API error: {e}")
            raise

    def upload_file(self, file_path: str) -> FileObject:
        return self.client.files.create(file=open(file_path, "rb"), purpose="fine-tune")

    def start_training(self, file: FileObject, model: str) -> str:
        return self.client.fine_tuning.jobs.create(training_file=file.id, model=model)

    def retrieve_job(self, job_id: str) -> None:
        return self.client.fine_tuning.jobs.retrieve(job_id)

    def wait_for_multiple_jobs(
        self, job_ids: list[str], polling_interval: int = 10
    ) -> dict:
        """Ожидание завершения нескольких задач."""
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    self.wait_for_completion, job_id, polling_interval
                ): job_id
                for job_id in job_ids
            }
            for future in futures:
                job_id = futures[future]
                try:
                    results[job_id] = future.result()
                except Exception as e:
                    results[job_id] = f"Failed: {e}"
        return results
