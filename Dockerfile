FROM python:3.7
WORKDIR /code
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV SQLALCHEMY_DATABASE_URI=postgresql://bniqdzsfpaqncm:8f33f4beff931c2fac537c45b7ff4180b461185fa57a0b85fe3db144799ae424@ec2-3-230-219-251.compute-1.amazonaws.com:5432/dc4l098iqhscv1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001
COPY . .
CMD ["python", "run.py"]

