#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCwebDjango.settings')
    is_testing = 'test' in sys.argv
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # these 6 lines are for coverage testing

    if is_testing:
        import coverage
        cov = coverage.coverage(source=['mcwebapp'])
        cov.set_option('report:show_missing', True)
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    # and these 5 for the report
    
    if is_testing:
        cov.stop()
        cov.save()
        cov.html_report(directory='covhtml') # put html report in the directory 'covhtml'
        cov.report()
    