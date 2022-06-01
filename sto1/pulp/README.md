# Pulp

Pulp is a platform for managing repositories of content, such as software packages, and pushing that content out to large numbers of consumers. (taken from <https://pypi.org/project/pulpcore/>)

We use pulp as a mirror for all packages osism requires. We do not use the pull-trough cache feature as it only caches the versions that where once ordered
from this pulp installation and not other ones. Therefore we mirror all.

## Setup the mirrors

In case of a loss setup the mirrors like this.
Syncing needs to happen regularly - we still need to find a solution to this.
**WARNING** please do not use your local machine to execute the commands below.
Rather use a VM with a screen session so the client does not disconnect.

- Ansible
  
  Pull-through cache is not possible yet, so we need to mirror only special namespaces. No auto-publication.

  ```sh
  pulp ansible repository create --name "ansible-mirror"

  pulp ansible remote -t "role" create --name "ansible-roles" --url "https://galaxy.ansible.com/api/v1/roles/?namespace__name=elastic"
  pulp ansible remote -t "collection" create --name "ansible-collections" --url "https://galaxy.ansible.com/" --requirements "collections:\n  - osism.commons"

  pulp ansible repository sync --name "ansible-mirror" --remote "role:ansible-roles"
  pulp ansible repository sync --name "ansible-mirror" --remote "collection:ansible-collections"

  pulp ansible distribution create --name "ansible-mirror-latest" --base-path "ansible-mirror" --repository "ansible-mirror"
  ```

- Containers
  
  Pull-through cache is not possible yet, so we need to mirror only special namespaces. No auto-publication.

  ```sh
  pulp container repository create --name "container-mirror"
  pulp container remote create --name "container-mirror" --url "https://registry-1.docker.io" --upstream-name "library/hello-world"
  pulp container repository sync --name "container-mirror" --remote "container-mirror"
  pulp container distribution create --name "container-mirror-latest" --base-path "container-mirror" --repository "container-mirror"
  ```

- Debian Packages

  Pull-through cache is available. No auto-publication.

  ```sh
  pulp deb repository create --name "deb-mirror"
  pulp deb remote create --name "deb-mirror" --url http://ftp2.de.debian.org/debian/ --distribution bullseye --architecture amd64 --architecture arm64
  pulp deb repository sync --name "deb-mirror" --mirror --remote "deb-mirror"
  pulp deb distribution create --name "deb-mirror-latest" --base-path "deb-mirror" --repository "deb-mirror"
  pulp deb publication create --repository "deb-mirror" --structured True
  ```

- PyPI

  Pull-through cache is available. Auto-publication active.

  ```sh
  pulp python repository create --name "pypi-mirror" --autopublish
  pulp python remote create --name "pypi-mirror" --url https://pypi.org/ --includes '["shelf-reader", "pip-tools>=1.12,<=2.0"]' --excludes '["django~=1.0", "scipy"]'
  pulp python repository sync --name "pypi-mirror" --remote "pypi-mirror"
  pulp python distribution create --name "pypi-mirror-latest" --base-path "pypi-mirror" --repository "pypi-mirror" --remote "pypi-mirror"
  ```

## Keep mirrors updated

If a mirror has no auto-publish feature, you have to do the following things periodically (maybe via cron job?):

- (...) repository sync (...)
- (...) distribution sync (...)
- (...) publication sync (...) # if required

For a simple mirror of Debian repos it might be better to use verbatim publication instead of default APT publisher. This will mirror the upstream mirror exactly including signatures and it is much more efficient than APT publisher. Though, there is (currently) a bug with download policy streamed. Download policy immediate works fine.

If you have auto-publish active, you just have to run the sync periodically.

## Current mirror-sizes

Date: 2022-06-17

- Ansible (?GB)
- Containers (?GB)
- Debian (1091GB)
  - amd64 (612GB)
  - arm64 (479GB)
- PyPI (11700GB)
