FROM python:3.12.2-slim as base

# Set the working directory
ADD . .

# Install dependencies
RUN pip install -r requirements.txt
# Expose the port
EXPOSE 5000
# Run the application
CMD ["python", "-m", "drafter"]
