##********************** MAIN BUILD **********************##
FROM python:3.12-alpine


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install the service
COPY --from=anchore/syft:latest /syft /usr/local/bin/syft


# Set the working directory in the container
WORKDIR /usr/src/app


# Copy the current directory contents into the container
COPY . .


# Install dependencies and the package
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt && \
    python setup.py install && \
    rm -rf /root/.cache/pip


# Run software-bill-of-materials when the container launches
ENTRYPOINT ["software_bill_of_materials"]