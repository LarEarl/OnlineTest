from celery import shared_task
from subprocess import Popen, PIPE, TimeoutExpired
from django.utils.timezone import now
import ast

from .models import CodeAttempt


def parse_by_type(value: str, data_type: str):
    value = value.strip()

    if data_type in ('int', 'float', 'bool'):
        return ast.literal_eval(value)

    if data_type in ('list', 'tuple', 'dict'):
        return ast.literal_eval(value)

    if data_type == 'str':
        return value

    return value


@shared_task(bind=True, time_limit=10)
def run_code_task(self, code_attempt_id):
    attempt = CodeAttempt.objects.get(id=code_attempt_id)
    attempt.status = 'running'
    attempt.save(update_fields=['status'])

    try:
        for case in attempt.question.code_cases.all():

            stdin = attempt.code
            if case.input_data:
                stdin += "\n###INPUT###\n" + case.input_data

            docker_timeout = case.time_limit + 3.0

            process = Popen(
                [
                    "docker", "run", "--rm", "-i",
                    "--network=none",
                    "--memory=128m",
                    "--cpus=0.5",
                    "python-runner"
                ],
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE,
                text=True
            )

            try:
                stdout, stderr = process.communicate(stdin, timeout=docker_timeout)
            except TimeoutExpired:
                process.kill()
                attempt.status = 'failed'
                attempt.stderr = 'Time limit exceeded'
                attempt.is_correct = False
                break

            if stderr:
                attempt.status = 'failed'
                attempt.stderr = stderr
                attempt.is_correct = False
                break

            try:
                user_output = parse_by_type(stdout, case.expected_output_type)
                expected_output = parse_by_type(
                    case.expected_output,
                    case.expected_output_type
                )
            except Exception as e:
                attempt.status = 'failed'
                attempt.stderr = f'Output parse error: {e}'
                attempt.is_correct = False
                break

            if user_output != expected_output:
                attempt.status = 'failed'
                attempt.stdout = stdout
                attempt.is_correct = False
                break

        else:
            attempt.status = 'success'
            attempt.is_correct = True
            attempt.stdout = stdout

    except Exception as e:
        attempt.status = 'failed'
        attempt.stderr = str(e)
        attempt.is_correct = False

    finally:
        attempt.finished_at = now()
        attempt.save()
