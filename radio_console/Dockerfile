FROM python:3.11 AS builder


RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /server
COPY requirements.txt .
RUN pip3 install -r requirements.txt


# Final stage:
FROM python:3.11

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /radio_console
COPY . .

EXPOSE 8080
CMD ["python3", "main.py"]
