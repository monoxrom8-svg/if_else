from django.urls import path
from . import views

app_name = "tramplin"

urlpatterns = [
    path("", views.home, name="home"),
    path("internships/", views.internships, name="internships"),
    path("events/", views.events, name="events"),
    path("vacancies/", views.vacancies, name="vacancies"),
    path("opportunity/<int:pk>/", views.opportunity_detail, name="opportunity_detail"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/employer/", views.employer_dashboard, name="employer_dashboard"),
    path("dashboard/seeker/", views.seeker_dashboard, name="seeker_dashboard"),
    path("dashboard/opportunity/<int:pk>/edit/", views.edit_opportunity, name="edit_opportunity"),
    path("dashboard/application/<int:pk>/status/", views.update_application_status, name="update_application_status"),
    # Seeker social features
    path("dashboard/favorite/toggle/", views.toggle_favorite, name="toggle_favorite"),
    path("dashboard/contact/add/<int:user_id>/", views.add_contact, name="add_contact"),
    path("dashboard/contact/remove/<int:user_id>/", views.remove_contact, name="remove_contact"),
    path("dashboard/recommend/send/", views.send_recommendation, name="send_recommendation"),
    path("dashboard/recommend/read/", views.mark_recommendations_read, name="mark_recommendations_read"),
    # Contact request flow
    path("profile/<int:user_id>/contact/request/", views.send_contact_request, name="send_contact_request"),
    path("profile/<int:user_id>/contact/accept/", views.accept_contact_request, name="accept_contact_request"),
    # Chat API
    path("chat/send/", views.chat_send, name="chat_send"),
    path("chat/messages/<int:user_id>/", views.chat_messages, name="chat_messages"),
    path("chat/unread/", views.chat_unread_count, name="chat_unread_count"),
    path("chat/inbox/", views.chat_inbox, name="chat_inbox"),
    path("chat/mini-profile/<int:user_id>/", views.chat_mini_profile, name="chat_mini_profile"),
    path("chat/typing/<int:user_id>/", views.chat_typing_signal, name="chat_typing_signal"),
    path("chat/presence/<int:user_id>/", views.chat_presence, name="chat_presence"),
    path("networking/", views.public_profiles, name="public_profiles"),
    path("profile/<int:user_id>/", views.public_profile, name="public_profile"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("companies/", views.companies, name="companies"),
    path("company/<int:employer_id>/", views.company_profile, name="company_profile"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    # Admin panel
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("admin-panel/user/<int:user_id>/role/", views.admin_set_role, name="admin_set_role"),
    path("admin-panel/user/<int:user_id>/block/", views.admin_toggle_block, name="admin_toggle_block"),
    path("admin-panel/user/<int:user_id>/delete/", views.admin_delete_user, name="admin_delete_user"),
    path("account/delete/", views.delete_my_account, name="delete_my_account"),
    path("admin-panel/user/<int:user_id>/block-detail/", views.admin_block_detail, name="admin_block_detail"),
    path("admin-panel/user/<int:user_id>/verify/", views.admin_verify_employer, name="admin_verify_employer"),
    path("admin-panel/review/<int:review_id>/moderate/", views.admin_moderate_review, name="admin_moderate_review"),
    path("admin-panel/opportunity/<int:opp_id>/moderate/", views.admin_moderate_opportunity, name="admin_moderate_opportunity"),
    path("admin-panel/submission/<int:pk>/moderate/", views.admin_moderate_submission, name="admin_moderate_submission"),
    path("admin-panel/mentor/<int:application_id>/moderate/", views.admin_moderate_mentor, name="admin_moderate_mentor"),
    path("geocode/", views.geocode_search, name="geocode_search"),
    path("apply/<int:opp_id>/", views.apply_for_opportunity, name="apply_for_opportunity"),
    path("submit-opportunity/", views.submit_opportunity, name="submit_opportunity"),
    # Mentor programme
    path("mentor/apply/", views.apply_mentor, name="apply_mentor"),
    path("mentor/set-available/", views.mentor_set_available, name="mentor_set_available"),
    # Curator
    path("dashboard/curator/", views.curator_dashboard, name="curator_dashboard"),
    path("curator/<int:user_id>/", views.curator_public_profile, name="curator_public_profile"),
]
