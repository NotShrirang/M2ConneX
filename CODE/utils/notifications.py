from notification.models import Notification
from .emails import (
    send_opportunity_application_email,
    send_opportunity_application_accepted_email,
    send_opportunity_application_rejected_email
)


def create_notification(user, notification_type, object):
    """
    Create a notification for a user

    Parameters:
    user (User): User object for which the notification is to be created
    notification_type (str): Type of notification to be created
    object (object): Object for which the notification is to be created

    """
    if notification_type == 'EVENT':
        link = '/event/' + str(object.id) + '/'
        message = 'Event ' + object.name + ' is scheduled on ' + \
            object.date.strftime('%d %b %Y') + ' at ' + \
            object.time.strftime('%H:%M') + ' in ' + object.venue + \
            '.' + ' Click here to view the event.'
    elif notification_type == 'CONNECTION_REQUEST':
        link = '/users/' + str(object.id) + '/'
        message = 'You have a new connection request from ' + \
            object.firstName + ' ' + object.lastName + '.'
    elif notification_type == 'CONNECTION_ACCEPTED':
        link = '/users/' + str(object.id) + '/'
        message = object.firstName + ' ' + object.lastName + \
            ' has accepted your connection request.'
    elif notification_type == 'OPPORTUNITY_APPLICATION':
        link = '/opportunity/' + str(object.id) + '/'
        Notification.objects.create(
            user=object.opportunity.user,
            notificationType='OPPORTUNITY_APPLICATION',
            link='/profile/' + str(object.applicant.id) + '/',
            message='You have a new application for ' +
            object.opportunity.name + ' opportunity from ' +
            object.applicant.firstName + ' ' +
            object.applicant.lastName + '.'
        )
        message = 'You have successfully applied for ' + \
            object.opportunity.name + ' opportunity.'
        send_opportunity_application_email(name=str(object.applicant.firstName) + ' ' + str(object.applicant.lastName),
                                           opportunityName=str(object.opportunity.name), companyName=str(object.opportunity.companyName), receiver=str(object.applicant.email))
    elif notification_type == 'OPPORTUNITY_APPLICATION_ACCEPTED':
        link = '/opportunity/' + str(object.id) + '/'
        message = 'Congratulations! Your application for ' + \
            object.opportunity.name + ' opportunity has been accepted.'
        send_opportunity_application_accepted_email(name=object.applicant.firstName + ' ' + object.applicant.lastName,
                                                    opportunityName=object.opportunity.name, companyName=object.opportunity.companyName, receiver=object.applicant.email)
    elif notification_type == 'OPPORTUNITY_APPLICATION_REJECTED':
        link = '/opportunity/' + str(object.id) + '/'
        message = f"""Thank you for your application to the
            '{object.opportunity.name}' opportunity at
            '{object.opportunity.companyName}'.
            Unfortunately, they've chosen to not move
            forward with your candidacy at this time.
            Your dream job is still waiting for you.
            Keep it up! Click here to view the more
            opportunities."""
        send_opportunity_application_rejected_email(name=object.applicant.firstName + ' ' + object.applicant.lastName,
                                                    opportunityName=object.opportunity.name, companyName=object.opportunity.companyName, receiver=object.applicant.email)
    elif notification_type == 'LIKE':
        link = '/feed/' + str(object.feed.id) + '/'
        message = object.user.firstName + ' ' + object.user.lastName + \
            ' liked your post.'
    elif notification_type == 'COMMENT':
        link = '/feed/' + str(object.feed.id) + '/'
        message = object.user.firstName + ' ' + object.user.lastName + \
            ' commented on your post.'
    else:
        link = '/'
        message = 'You have a new notification.'

    notification = Notification.objects.create(
        user=user,
        notificationType=notification_type,
        link=link,
        message=message
    )
    notification.save()
    return notification
