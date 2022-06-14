from app.parameters import selectors
from app.utils import get_item

class Opinion():
    def __init__(self, author="", recommendation=None, stars=0, content="", useful=0, useless=0, publish_date=None, purchase_date=None, pros=[], cons=[], opinion_id=""):
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.publish_date = publish_date
        self.purchase_date = purchase_date
        self.pros = pros
        self.cons = cons
        self.opinion_id = opinion_id
    
    def extract_opinion(self, opinion):
        for key, value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id = opinion["data-entry-id"]
        return self

    def __str__(self) -> str:
        return f"opinion_id: {self.opinion_id}<br>" + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in selectors.keys())

    def __repr__(self) -> str:
        return f"Opinion(opinion_id={self.opinion_id}, " + ", ".join(f"{key}={str(getattr(self, key))}" for key in selectors.keys()) + ")"

    def to_dict(self) -> dict:
        return {"opinion_id": self.opinion_id} | {key: getattr(self, key) for key in selectors.keys()}


    