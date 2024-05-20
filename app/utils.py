selectors = {
    "opinion_id": (None, "data-entry-id"),
    "author": ("span.user-post__author-name",),
    "recommendation": ("span.user-post__author-recomendation > em",),
    "rating": ("span.user-post__score-count",),
    "content": ("div.user-post__text",),
    "pros": ("div.review-feature__title--positives ~ div.review-feature__item", None, True),
    "cons": ("div.review-feature__title--negatives ~ div.review-feature__item", None, True),
    "useful": ("span[id^='votes-yes']",),
    "useless": ("span[id^='votes-no']",),
    "post_date": ("span.user-post__published > time:nth-child(1)","datetime"),
    "purchase_date": ("span.user-post__published > time:nth-child(2)","datetime")
}

def extract(ancestor, selector=None, attribute=None, returns_list=False):
    if selector:
        if returns_list:
            if attribute:
                return [tag[attribute].strip() for tag in ancestor.select(selector)]
            return [tag.get_text().strip() for tag in ancestor.select(selector)]
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute].strip()
            except TypeError:
                return None
        try:
            return ancestor.select_one(selector).get_text().strip()
        except AttributeError:
            return None
    if attribute:
        return ancestor[attribute].strip()
    return ancestor.get_text().strip()