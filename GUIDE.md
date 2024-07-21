# Guide for Software Bill of Materials (SBOM) Tool

This guide provides detailed instructions on how to build, run, and use the Software Bill of Materials (SBOM) tool. The tool is designed to generate SBOMs for container images and filesystems using Syft.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Building the Docker Image](#building-the-docker-image)
4. [Running the Docker Container](#running-the-docker-container)
5. [Tool Usage](#tool-usage)
6. [Troubleshooting](#troubleshooting)
7. [Additional Information](#additional-information)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Git (optional, for cloning the repository)

## Project Structure

```
software-bill-of-materials/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── GUIDE.md
├── README.md
├── requirements.txt
├── setup.py
└── software-bill-of-materials/
    ├── __init__.py
    ├── __version__.py
    ├── main.py
    ├── core/
    |   ├── __init__.py
    |   ├── input.py
    |   ├── logger.py
    |   └── models.py
    |
    ├── service/
    |   ├── __init__.py
    |   └── syft.py
    |
    └── support/
        ├── __init__.py
        └── enums.py
```

## Building the Docker Image

1. Open a terminal and navigate to the project directory:

   ```bash
   cd path/to/software-bill-of-materials
   ```

2. Build the Docker image using the following command:

   ```bash
   sudo docker build --no-cache . -f Dockerfile -t software-bill-of-materials:latest
   ```

   This command builds a Docker image named `software-bill-of-materials` based on the instructions in the Dockerfile.

## Running the Docker Container

To run the SBOM tool inside a Docker container, use the following command structure:

```bash
sudo docker run --rm -it -v $(pwd)/output:/output software-bill-of-materials [arguments]
```

Replace `[arguments]` with the actual arguments for the tool.

### Explanation of Docker run options:

- `--rm`: Automatically remove the container when it exits.
- `-it`: Run container in interactive mode.
- `software-bill-of-materials`: The name of the Docker image to run.

## Tool Usage

The SBOM tool accepts several command-line arguments:

- `-t, --target`: (Required) Target as path/image to scan.
- `-ov, --output-via`: (Required) Specify output method: "file" or "webhook".
- `-w, --webhook`: Webhook URL (required if output_via is "webhook").
- `-o, --output`: File path for output (required if output_via is "file").
- `-l, --log`: Log level (DEBUG or ERROR, default is DEBUG).

### Example Commands:

1. Scan a Docker image and output to a file:
   ```bash
   sudo docker run --rm -it -v $(pwd)/output:/output software-bill-of-materials -ov file -o /output/results.json
   ```

2. Scan a local directory and send results to a webhook:
   ```bash
   sudo docker run --rm -it -v $(pwd)/output:/output -v /path/to/scan:/scan software-bill-of-materials -t /scan -ov webhook -w https://webhook.site/your-unique-url
   ```

3. Few ways to Run scan:
    - For image from registry
    ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output software-bill-of-materials 
    -t alpine:latest -ov file -o /output/alpine.json
    ```

    - For local docker image
    ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output -v /var/run/docker.sock:/var/run/docker.sock software-bill-of-materials 
    -t docker:attack-surface-discovery:latest -ov file -o /output/asm.json
    ```

    - For local repo path
    ```bash
    sudo docker run --rm -it -v $(pwd)/output:/output -v /home/tri/trishiras/attack-surface-discovery:/scan software-bill-of-materials 
    -t dir:/scan  -ov file -o /output/local.json
    ```


Note: When using file output or scanning local directories, you need to mount volumes to access the results or scan targets from your host machine.

## Troubleshooting

1. **Permission Issues**: If you encounter permission problems when writing to mounted volumes, you may need to adjust the permissions or use a named volume.

2. **Network Issues**: Ensure your Docker network settings allow the container to access the target network or webhook URL.

3. **Missing Requirements**: If the build fails due to missing requirements, check that your `requirements.txt` file is up to date and includes all necessary dependencies.

## Additional Information

- The tool uses Python 3.12 as specified in the Dockerfile.
- The tool integrates Syft for generating SBOMs. For detailed information about Syft's capabilities, refer to its documentation or use the `syft --help` command inside the container.
- The SBOM tool supports various output formats through Syft, including CycloneDX JSON/XML, SPDX JSON/Tag-Value, and custom templates.


###  syft --help output

```
Generate a packaged-based Software Bill Of Materials (SBOM) from container images and filesystems

Usage:
  syft [SOURCE] [flags]
  syft [command]

Examples:
  syft scan alpine:latest                                a summary of discovered packages
  syft scan alpine:latest -o json                        show all possible cataloging details
  syft scan alpine:latest -o cyclonedx                   show a CycloneDX formatted SBOM
  syft scan alpine:latest -o cyclonedx-json              show a CycloneDX JSON formatted SBOM
  syft scan alpine:latest -o spdx                        show a SPDX 2.3 Tag-Value formatted SBOM
  syft scan alpine:latest -o spdx@2.2                    show a SPDX 2.2 Tag-Value formatted SBOM
  syft scan alpine:latest -o spdx-json                   show a SPDX 2.3 JSON formatted SBOM
  syft scan alpine:latest -o spdx-json@2.2               show a SPDX 2.2 JSON formatted SBOM
  syft scan alpine:latest -vv                            show verbose debug information
  syft scan alpine:latest -o template -t my_format.tmpl  show a SBOM formatted according to given template file

  Supports the following image sources:
    syft scan yourrepo/yourimage:tag     defaults to using images from a Docker daemon. If Docker is not present, the image is pulled directly from the registry.
    syft scan path/to/a/file/or/dir      a Docker tar, OCI tar, OCI directory, SIF container, or generic filesystem directory

  You can also explicitly specify the scheme to use:
    syft scan docker:yourrepo/yourimage:tag            explicitly use the Docker daemon
    syft scan podman:yourrepo/yourimage:tag            explicitly use the Podman daemon
    syft scan registry:yourrepo/yourimage:tag          pull image directly from a registry (no container runtime required)
    syft scan docker-archive:path/to/yourimage.tar     use a tarball from disk for archives created from "docker save"
    syft scan oci-archive:path/to/yourimage.tar        use a tarball from disk for OCI archives (from Skopeo or otherwise)
    syft scan oci-dir:path/to/yourimage                read directly from a path on disk for OCI layout directories (from Skopeo or otherwise)
    syft scan singularity:path/to/yourimage.sif        read directly from a Singularity Image Format (SIF) container on disk
    syft scan dir:path/to/yourproject                  read directly from a path on disk (any directory)
    syft scan file:path/to/yourproject/file            read directly from a path on disk (any single file)


Available Commands:
  attest      Generate an SBOM as an attestation for the given [SOURCE] container image
  cataloger   Show available catalogers and configuration
  completion  Generate the autocompletion script for the specified shell
  config      show the syft configuration
  convert     Convert between SBOM formats
  help        Help about any command
  login       Log in to a registry
  scan        Generate an SBOM
  version     show version information

Flags:
      --base-path string                          base directory for scanning, no links will be followed above this directory, and all paths will be reported relative to this directory
  -c, --config string                             syft configuration file
      --enrich stringArray                        enable package data enrichment from local and online sources (options: all, golang, java, javascript)
      --exclude stringArray                       exclude paths from being scanned using a glob expression
      --file string                               file to write the default report output to (default is STDOUT) (DEPRECATED: use: output)
      --from stringArray                          specify the source behavior to use (e.g. docker, registry, oci-dir, ...)
  -h, --help                                      help for syft
  -o, --output stringArray                        report output format (<format>=<file> to output to a file), formats=[cyclonedx-json cyclonedx-xml github-json spdx-json spdx-tag-value syft-json syft-table syft-text template] (default [syft-table])
      --override-default-catalogers stringArray   set the base set of catalogers to use (defaults to 'image' or 'directory' depending on the scan source)
      --platform string                           an optional platform specifier for container image sources (e.g. 'linux/arm64', 'linux/arm64/v8', 'arm64', 'linux')
  -q, --quiet                                     suppress all logging output
  -s, --scope string                              selection of layers to catalog, options=[squashed all-layers] (default "squashed")
      --select-catalogers stringArray             add, remove, and filter the catalogers to be used
      --source-name string                        set the name of the target being analyzed
      --source-version string                     set the version of the target being analyzed
  -t, --template string                           specify the path to a Go template file
  -v, --verbose count                             increase verbosity (-v = info, -vv = debug)
      --version                                   version for syft

Use "syft [command] --help" for more information about a command.
```

For more information or to report issues, please refer to the project's documentation or repository.