import datetime

from fastapi import FastAPI, Depends, status, Form
from sqlmodel import Session, select

from database import get_session
from job.models import Job
from user.deps import get_current_user
from user.models import User

job = FastAPI()


@job.get('/')
async def job_list(session: Session = Depends(get_session)):
    statement = select(Job)
    all_jobs = session.exec(statement)
    return all_jobs.all()


@job.post('/')
async def job_post(session: Session = Depends(get_session),
                   title: str = Form(...),
                   details: str = Form(...),
                   current_user: User = Depends(get_current_user)
                   ):
    new_job = Job(title=title, details=details,
                  author_id=current_user.id, filter="remote",
                  date=str(datetime.datetime.now().date()))
    print(new_job)
    session.add(new_job)
    session.commit()
    return {"message": "Job posted successfully."}
