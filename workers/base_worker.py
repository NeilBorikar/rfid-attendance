import time
import logging


class BaseWorker:
    MAX_RETRIES = 5
    BACKOFF_SECONDS = 2

    def run_with_retry(self, task_fn, *args, **kwargs):
        attempt = 0

        while attempt < self.MAX_RETRIES:
            try:
                return task_fn(*args, **kwargs)

            except Exception as e:
                attempt += 1
                logging.error(
                    f"[Worker Retry {attempt}] {str(e)}"
                )
                time.sleep(self.BACKOFF_SECONDS ** attempt)

        raise RuntimeError("Max retries exceeded")
