import subprocess


def export_env(filename='.env'):
    data = ['heroku', 'config:set']
    unset = ['heroku', 'config:unset']
    with open(filename, 'r') as config:
        data, unset = herokuOjbCreate(config, data, unset)
    # run heroku configuration
    subprocess.check_call(data)
    subprocess.check_call(unset)
    # check_call fires an exception on failure.
    # if we're here, both calls succeeded.
    return 0


def travisCI_env(filename='.env'):
    with open(filename, 'r') as config:
        travisCalls(config)

def travisCalls(config):
    unset = ['travis', 'env', 'unset']
    for line in config.readlines():
        line.strip()
        tmp = line.split('=')
        # further ignore whitespace padding that was around the =
        tmp = list(map(str.strip, tmp))
        # subprocess.check_call(data)
        if len(tmp[0]) and tmp[0][0] == '#':
            unset.append(tmp[0][1:])
        # check for nonempty variable and content
        elif len(tmp[0]) and len(tmp[1]):
            tmp[1] = tmp[1].replace("'", "")
            print('{1}'.format(*tmp))
            subprocess.check_call(
                ["travis", "env", "set", '{0}'.format(*tmp), '{1}'.format(*tmp), '-p'])
    subprocess.check_call(unset)


def herokuOjbCreate(config, data, unset):

    for line in config.readlines():
        # ignore whitespace padding
        line.strip()
        tmp = line.split('=')
        # further ignore whitespace padding that was around the =
        tmp = list(map(str.strip, tmp))
        if len(tmp[0]) and tmp[0][0] == '#':
            # the heroku CLI cannot return if a variable is not yet set
            # or if it has been set to the empty string.
            # delete commented-out variables to be safe.
            unset.append(tmp[0][1:])
        # check for nonempty variable and content
        elif len(tmp[0]) and len(tmp[1]):

            data.append('{0}={1}'.format(*tmp))
    return data, unset


if __name__ == '__main__':
    import sys
    # export_env('.env')
    travisCI_env('.env')
    sys.exit()


# travis encrypt SOMEVAR="secretvalue" --add env.SOMEVAR
