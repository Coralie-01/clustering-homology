# Start by pulling the HH-suite image
FROM soedinglab/hh-suite as hh-suite

# Now, set up your Python environment
FROM python:3.8.18-bookworm

# Set the working directory in the container
WORKDIR /app

# Set non-interactive installation mode and timezone
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

# Copy Python requirements and setup files
COPY ./requirements.txt /app/requirements.txt
COPY ./setup.py /app/setup.py

# Install Python dependencies
RUN pip install -r /app/requirements.txt && pip install ipykernel

# Install additional system dependencies
RUN apt-get update && apt-get install -y python3-tk && rm -rf /var/lib/apt/lists/*

# Generate Jupyter Notebook config and set token
RUN jupyter notebook --generate-config
RUN echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py

# Copy HH-suite binaries and libraries from the hh-suite stage
COPY --from=hh-suite /usr/local/hh-suite/bin/ /usr/local/bin/
COPY --from=hh-suite /usr/local/lib/ /usr/local/lib/
ENV PATH="/usr/local/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# Set the default command for the container
CMD ["bash"]
