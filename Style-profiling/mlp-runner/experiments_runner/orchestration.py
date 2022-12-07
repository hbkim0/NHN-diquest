from __future__ import annotations

import sys
import os.path
import multiprocessing

from .pipeline import Pipeline

import logging
from typing import Callable, Optional


class _LoggerWriter:
    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self, msg: str):
        if msg.endswith('\n'):
            self.buf.append(msg.rstrip('\n'))
            self.logfct(''.join(self.buf))
            self.buf = []
        else:
            self.buf.append(msg)

    def flush(self):
        pass

    @staticmethod
    def get_logger(pipeline: Pipeline) -> logging.Logger:

        #
        logger = logging.getLogger(pipeline.pipeline_name)
        logger.setLevel(logging.DEBUG)

        #
        formatter = logging.Formatter(
            fmt='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        #
        handler = logging.FileHandler(os.path.join(pipeline.pipeline_root, f'{pipeline.pipeline_name}.log'), 'w')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        #
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger


class LocalRunner:

    def __init__(
        self,
        pipeline: Pipeline,
        exception_handler:
        Optional[Callable] = None,
        done_handler: Optional[Callable] = None
    ) -> None:

        self._process = None
        self._pipeline = pipeline
        self._exception_handler = exception_handler
        self._done_handler = done_handler
        self._start()

    def _run(self):
        logger = _LoggerWriter.get_logger(self._pipeline)
        sys.stdout = _LoggerWriter(logger.info)
        sys.stderr = _LoggerWriter(logger.error)

        try:
            while len(self._pipeline) > 0:
                func = self._pipeline.pop()
                func()
        except Exception as e:
            logger.error(e)
            if callable(self._exception_handler):
                self._exception_handler()
        else:
            if callable(self._done_handler):
                self._done_handler()

    def _start(self):
        if len(self._pipeline) > 0:
            self._process = multiprocessing.Process(target=self._run, daemon=True)
            self._process.start()

    def is_alive(self):
        return self._process.is_alive() if self._process is not None else False

    @staticmethod
    def run(
        pipeline: Pipeline,
        exception_handler: Optional[Callable] = None,
        done_handler: Optional[Callable] = None
    ) -> LocalRunner:
        return LocalRunner(pipeline, exception_handler, done_handler)


if __name__ == '__main__':
    def example_local_runner():
        import time

        def print_and_sleep(secs=1.0):
            print(f'{multiprocessing.current_process()}')
            time.sleep(secs)
            print(f'{multiprocessing.current_process()}')

        def print_and_busy_wait(cnt=1000):
            print(f'{multiprocessing.current_process()}')
            for a in range(cnt * 10000):
                a = 1 ** 10
                a = a // 0.1
            print(f'{multiprocessing.current_process()}')

        print(f'{multiprocessing.current_process()}: before')
        runner = LocalRunner.run(Pipeline('name', './', [
            lambda: print_and_sleep(),
            lambda: print_and_sleep(2.0),
            lambda: print_and_busy_wait()
        ]))
        print(f'{multiprocessing.current_process()}: after')

        for cnt in range(50):
            print(f'runner.is_alive({cnt}): {runner.is_alive()}')
            time.sleep(0.1)

    example_local_runner()
