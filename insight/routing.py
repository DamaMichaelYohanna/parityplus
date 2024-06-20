import datetime


from fastapi import Depends, FastAPI, status, HTTPException
from sqlmodel import Session, select

from insight.schema import InsightUpdate
from user.models import User
from user.deps import get_current_user
from insight.models import Insight
from database import get_session

insight = FastAPI()


@insight.get('/')
async def insight_list(session: Session = Depends(get_session),
                       current_user: User = Depends(get_current_user)):
    """List out all the insight by a user."""
    insights = session.exec(select(Insight).where(Insight.user_id == current_user.id)).all()
    return insights


@insight.get("/{insight_id}")
async def insight_detail(insight_id: int,
                         session: Session = Depends(get_session),
                         current_user: User = Depends(get_current_user)
                         ):
    """display details of a particular insight"""
    return session.get(Insight, insight_id)


@insight.post('/compose', status_code=status.HTTP_201_CREATED)
async def compose_insight(new_insight: Insight,
                          session: Session = Depends(get_session),
                          current_user: User = Depends(get_current_user)):
    """endpoint to add new insight"""
    new_insight.id = None
    new_insight.date = str(datetime.datetime.now().date())
    new_insight.user_id = current_user.id
    new_insight.user = current_user
    session.add(new_insight)
    session.commit()
    return {"message": "insight created successfully"}


@insight.put("/update/{insight_id}/")
async def update_insight(insight_id: int,
                         update_insight: InsightUpdate,
                         session: Session = Depends(get_session),
                         current_user: User = Depends(get_current_user)):
    """endpoint for updating notes of insight by the creator"""
    old_insight = session.get(Insight, insight_id)

    if not old_insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    if old_insight.user != current_user:
        raise HTTPException(status_code=403, detail="Request forbidden")

    old_insight.note = update_insight.note
    session.commit()
    return {"message": "Insight updated successfully"}


@insight.delete("/delete/{insight_id}/")
async def update_insight(insight_id: int,
                         session: Session = Depends(get_session),
                         current_user: User = Depends(get_current_user)):
    """endpoint for deleting insight by user who created them"""
    old_insight = session.get(Insight, insight_id)
    if not old_insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    if not old_insight in current_user.insight:
        raise HTTPException(status_code=403, detail="Request forbidden")
    session.delete(old_insight)
    session.commit()
    return {"message": "Insight deleted successfully"}


@insight.put("/like/{insight_id}/")
async def like_insight(insight_id: int,
                       session: Session = Depends(get_session),
                       current_user: User = Depends(get_current_user)):
    """endpoint for deleting insight by user who created them"""
    insight_to_like = session.get(Insight, insight_id)
    if not insight_to_like:
        raise HTTPException(status_code=404, detail="Insight not found")
    insight_to_like.likes += 1
    session.commit()
    return {"message": "You liked this insight"}


@insight.post('/comment', status_code=status.HTTP_201_CREATED)
async def compose_insight(new_insight: Insight,
                          session: Session = Depends(get_session),
                          current_user: User = Depends(get_current_user)):
    """endpoint to comment on insights"""
    new_insight.id = None
    new_insight.date = str(datetime.datetime.now().date())
    new_insight.user_id = current_user.id
    new_insight.user = current_user
    session.add(new_insight)
    session.commit()
    return {"message": "insight created successfully"}