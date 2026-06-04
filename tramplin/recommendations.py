"""
Recommendation Engine for Tramplin.
Matches seekers to opportunities (and vice versa) based on skill/tag overlap,
freshness boost, and work-format preference.
"""
from django.utils import timezone
from django.db.models import Q


def _normalize(tag: str) -> str:
    return tag.strip().lower()


def score_opportunity(user_skills: list[str], user_format: str | None, opp) -> int:
    """
    Return an integer match score (0–100) for a single Opportunity.

    Scoring:
      - Base: intersection(user_skills, opp.skills_list) / max(len(opp.skills_list), 1) * 80
        (capped at 80 so boosts can push to 100)
      - Freshness boost: +10 if created within last 7 days, +5 if within 14 days
      - Format match: +10 if user preferred format matches opp.format
    """
    opp_skills = [_normalize(s) for s in opp.skills_list]
    user_skills_norm = [_normalize(s) for s in user_skills]

    if not opp_skills:
        base = 0
    else:
        matched = sum(1 for s in user_skills_norm if s in opp_skills)
        base = int(matched / len(opp_skills) * 80)

    # Freshness boost
    freshness = 0
    if opp.created_at:
        age_days = (timezone.now() - opp.created_at).days
        if age_days <= 7:
            freshness = 10
        elif age_days <= 14:
            freshness = 5

    # Format match boost
    format_boost = 0
    if user_format and opp.format == user_format:
        format_boost = 10

    return min(base + freshness + format_boost, 100)


def get_recommended_opportunities(user, limit: int = 20) -> list[dict]:
    """
    Return a list of dicts: {"opportunity": <Opportunity>, "score": int}
    for the given seeker user, ordered by score descending.
    Only approved, active opportunities are considered.
    Only results with score > 0 are returned.
    """
    from .models import Opportunity

    user_skills = user.skills_list  # list of strings
    # Infer preferred format from profile (stored in skills or a dedicated field if added later)
    # For now we derive it from the user's `about` text as a heuristic, or default to None.
    user_format = getattr(user, "preferred_format", None)

    opps = (
        Opportunity.objects
        .filter(
            status=Opportunity.STATUS_ACTIVE,
            moderation_status=Opportunity.MODERATION_APPROVED,
            type__in=[Opportunity.TYPE_VACANCY, Opportunity.TYPE_INTERNSHIP],
        )
        .select_related("employer")
    )

    results = []
    for opp in opps:
        s = score_opportunity(user_skills, user_format, opp)
        if s > 0:
            results.append({"opportunity": opp, "score": s})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def get_matched_seekers(employer_user, limit: int = 50) -> list[dict]:
    """
    For an employer, return seekers ranked by how well their skills match
    the employer's active approved vacancies.

    Returns list of dicts: {"seeker": <User>, "score": int}
    """
    from .models import Opportunity, User, Application

    # Collect all skills required across employer's active opportunities
    employer_opps = Opportunity.objects.filter(
        employer=employer_user,
        status=Opportunity.STATUS_ACTIVE,
        moderation_status=Opportunity.MODERATION_APPROVED,
    )

    if not employer_opps.exists():
        return []

    # Build a unified required-skills set (union across all active opps)
    required_skills = set()
    for opp in employer_opps:
        required_skills.update(_normalize(s) for s in opp.skills_list)

    if not required_skills:
        return []

    # Fetch seekers who have already applied (to show them first) or are public
    seekers = User.objects.filter(
        role=User.ROLE_SEEKER,
        is_blocked=False,
    ).exclude(skills="")

    results = []
    for seeker in seekers:
        seeker_skills = [_normalize(s) for s in seeker.skills_list]
        if not seeker_skills:
            continue
        matched = sum(1 for s in seeker_skills if s in required_skills)
        score = int(matched / len(required_skills) * 100)
        if score > 0:
            results.append({"seeker": seeker, "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]
