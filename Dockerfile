FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12

# Copy requirements file
COPY lambda/requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy function code
COPY lambda/ ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD ["chat_handler.lambda_handler"]
