import os

import logging
from queue import Queue
from threading import Thread
from typing import final
from constants import FAILED_URLS

from download_helper import (
    get_download_links,
    get_download_dir,
    download_repo_through_pydriller,
    get_downloaded_repos,
)

logger = logging.getLogger(__name__)

failed_links = []


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            try:
                download_repo_through_pydriller(directory, link)
            except Exception as e:
                failed_links.append(link)
            finally:
                self.queue.task_done()


def main():
    download_dir = get_download_dir()
    links = get_download_links()

    # Create a queue to communicate with the worker threads
    queue = Queue()

    # Create 16 worker threads
    for _ in range(16):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put the tasks into the queue as a tuple
    repos = get_downloaded_repos()
    final = []

    for link in links:
        print("Queueing {}".format(link))
        if os.path.basename(link) not in repos:
            queue.put((download_dir, link))
            final.append(link)

    print("downloading ", len(final))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()

    print(failed_links)


# main()
