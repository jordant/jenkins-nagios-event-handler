import ast
import optparse
import sys

from jenkinsapi.jenkins import Jenkins


def parse_options():
    parser = optparse.OptionParser()
    parser.add_option(
        "-j", "--job_name", metavar="jobname", action="store",
        type="string", dest="job_name", default=False,
        help="name of jenkins job"
    )

    parser.add_option(
        "-b", "--buildarams", metavar="BUILDPARAMS", action="store",
        default=False, dest="build_params",
        help="job build params in json"
    )

    parser.add_option(
        "--url", metavar="URL", action="store",
        default="http://localhost:8080", dest="jenkins_url",
        help="Jenkins server URL"
    )

    parser.add_option(
        "--username", metavar="USERNAME", action="store",
        default="jenkins", dest="username",
        help="Jenkins server username"
    )

    parser.add_option(
        "--password", metavar="PASSWORD", action="store",
        default="jenkins", dest="password",
        help="Jenkins server password"
    )

    options = parser.parse_args(sys.argv)[0]
    if not options.job_name:
        parser.error('job_name not defined')

    return options


def build_param_dict():
    options = parse_options()
    return ast.literal_eval(options.build_params)


def get_jenkins():
    options = parse_options()
    return Jenkins(options.jenkins_url,
                   username=options.username,
                   password=options.password)


def invoke_jenkins(job_name, params):
    leeroy = get_jenkins()
    if (leeroy.has_job(job_name)):
        job = leeroy.get_job(job_name)
        return job.invoke(build_params=params)
    else:
        raise("Cannot find job %s" % job_name)
        return


def main():
    options = parse_options()
    invoke_jenkins(options.job_name, build_param_dict())

if __name__ == "__main__":
    main()
