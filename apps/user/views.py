import logging

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view

from apps.auth.decorators import user_login_required
from apps.base.views import SuccessJsonResponse, ErrorJsonResponse
from apps.user.models import Friends, FriendRequest

User = get_user_model()


logger = logging.getLogger(__name__)


@api_view(["GET"])
@user_login_required
def search_user(request):
    query = request.GET.get('query')
    if not query:
        logger.warning("search_user empty query")
        # success response, empty query should not be an error
        return SuccessJsonResponse({"message": "Empty 'query'"})
    search_result = User.objects.filter(
        Q(email=query) | Q(first_name__contains=query)
    ).only('first_name', 'email')

    logger.info(f"search_user query: {query}")

    # need to paginate with, but ignoring for now
    return SuccessJsonResponse({
        'result': [{'email': user.email, 'first_name': user.first_name} for user in search_result]
    })


@api_view(["GET"])
@user_login_required
def get_friends_list(request):
    """
    return list of friends for current loggeed in user
    """
    friend_list_qs = Friends.objects.select_related('my_friend').filter(my_user=request.user)
    return SuccessJsonResponse({
        'result': [{'email': user.my_friend.email, 'first_name': user.my_friend.first_name} for user in friend_list_qs]
    })


@api_view(["GET"])
@user_login_required
def get_friends_request_list(request):
    """
    return list of friends for current loggeed in user
    """
    friend_request_qs = FriendRequest.objects.select_related('sent_by').filter(
        sent_to=request.user, status__isnull=True
    )
    return SuccessJsonResponse({
        'result': [{'email': user.sent_by.email, 'first_name': user.sent_by.first_name} for user in friend_request_qs]
    })


@api_view(["POST"])
@user_login_required
def send_friend_request(request):
    """
    send friend request to another user based on their email
    """
    friend_email = request.data.get('email')
    # Check if the email is the same as the user's own email
    if friend_email and friend_email == request.user.email:
        logger.warning("send_friend_request, attempting to send friend request to themselves")
        return ErrorJsonResponse({"message": "Invalid Operation"})
    # Try to find the user with the given email
    try:
        other_user = User.objects.get(email=friend_email)
    except User.DoesNotExist as e:
        logger.error("send_friend_request, user not found with given email")
        return ErrorJsonResponse({"message": "No user found with given email"})

    # since it is a friend request, it can be sent from either party only once. If user A sends a request to user B
    # then user B will accept the request, B cannot send the request w/o rejecting the request.
    if FriendRequest.objects.filter(
            Q(sent_by=request.user, sent_to=other_user) |
            Q(sent_by=other_user, sent_to__email=request.user.email)
    ).exists():
        # either current user or other user already created a friend request
        logger.info("send_friend_request, Friend Request object already exists")
        return ErrorJsonResponse({"message": "Friend Request already exists"})
    # Create a new friend request
    FriendRequest.objects.create(
        sent_by=request.user, sent_to=other_user
    )
    return SuccessJsonResponse({
        "message": "Friend Request Sent"
    }, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@user_login_required
def accept_friend_request(request):
    """
    send friend request to another user based on their email
    """
    friend_email = request.data.get('email')

    if friend_email and friend_email == request.user.email:
        logger.warning("accept_friend_request, attempting to send friend request to themselves")
        return ErrorJsonResponse({"message": "Invalid Operation"})

    try:
        friend_request_obj = FriendRequest.objects.get(
            sent_to=request.user, sent_by__email=friend_email
        )

    except FriendRequest.DoesNotExist as _:
        return ErrorJsonResponse({"message": "Friend Request does not exists"})

    if friend_request_obj.status is not None:
        return ErrorJsonResponse({"message": "Friend Request already accepted"})

    friend_request_obj.status = FriendRequest.STATUS_ACCEPTED
    friend_request_obj.save(update_fields=['status'])
    return SuccessJsonResponse({"message": "Friend Request accepted"})


@api_view(["POST"])
@user_login_required
def reject_friend_request(request):
    """
    send friend request to another user based on their email
    """
    friend_email = request.data.get('email')

    if friend_email and friend_email == request.user.email:
        logger.warning("accept_friend_request, attempting to send friend request to themselves")
        return ErrorJsonResponse({"message": "Invalid Operation"})

    try:
        friend_request_obj = FriendRequest.objects.get(
            sent_to=request.user, sent_by__email=friend_email
        )
    except FriendRequest.DoesNotExist as _:
        return ErrorJsonResponse({"message": "Friend Request does not exists"})

    if friend_request_obj.status is not None:
        return ErrorJsonResponse({"message": "Friend Request already rejected"})

    friend_request_obj.status = FriendRequest.STATUS_REJECTED
    friend_request_obj.save(update_fields=['status'])
    return SuccessJsonResponse({"message": "Friend Request rejected"})
